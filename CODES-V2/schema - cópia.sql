-- KatenaScout Supabase Migration Script
-- Creates the necessary tables and security policies for multi-tenant platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable Row Level Security (RLS)
-- Note: This assumes the profiles table already exists from Supabase Auth setup
ALTER TABLE IF EXISTS profiles ENABLE ROW LEVEL SECURITY;

-- Organizations/Tenants table for multi-tenant structure
CREATE TABLE IF NOT EXISTS organizations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  logo_url TEXT,
  subscription_tier TEXT DEFAULT 'free',
  subscription_status TEXT DEFAULT 'active',
  max_users INTEGER DEFAULT 5,
  settings JSONB DEFAULT '{}'
);

-- Enable RLS on organizations
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;

-- Organization members table
CREATE TABLE IF NOT EXISTS organization_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(organization_id, user_id)
);

-- Enable RLS on organization_members
ALTER TABLE organization_members ENABLE ROW LEVEL SECURITY;

-- Add organization_id to profiles table if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'organization_id'
  ) THEN
    ALTER TABLE profiles ADD COLUMN organization_id UUID REFERENCES organizations(id);
  END IF;
  
  -- Add onboarding_completed to profiles table if it doesn't exist
  IF NOT EXISTS (
    SELECT FROM information_schema.columns 
    WHERE table_name = 'profiles' AND column_name = 'onboarding_completed'
  ) THEN
    ALTER TABLE profiles ADD COLUMN onboarding_completed BOOLEAN DEFAULT FALSE;
  END IF;
END $$;

-- Chat sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  language TEXT DEFAULT 'english',
  name TEXT,
  is_favorite BOOLEAN DEFAULT FALSE,
  external_id TEXT -- To link with frontend session IDs
);

-- Add external_id to chat_sessions table if it already exists
DO $$
BEGIN
  IF EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_name = 'chat_sessions'
  ) AND NOT EXISTS (
    SELECT FROM information_schema.columns 
    WHERE table_name = 'chat_sessions' AND column_name = 'external_id'
  ) THEN
    ALTER TABLE chat_sessions ADD COLUMN external_id TEXT;
  END IF;
END $$;

-- Enable RLS on chat_sessions
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;

-- Chat messages table
CREATE TABLE IF NOT EXISTS chat_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
  role TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on chat_messages
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- Search parameters table
CREATE TABLE IF NOT EXISTS search_parameters (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
  key_description_word TEXT[] NOT NULL,
  position_codes TEXT[] NOT NULL,
  other_parameters JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on search_parameters
ALTER TABLE search_parameters ENABLE ROW LEVEL SECURITY;

-- Search results table
CREATE TABLE IF NOT EXISTS search_results (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
  parameters_id UUID REFERENCES search_parameters(id) ON DELETE CASCADE,
  player_id TEXT NOT NULL,
  player_data JSONB,
  score NUMERIC,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on search_results
ALTER TABLE search_results ENABLE ROW LEVEL SECURITY;

-- Player videos table
CREATE TABLE IF NOT EXISTS player_videos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  storage_path TEXT NOT NULL,
  thumbnail_path TEXT,
  duration INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  views INTEGER DEFAULT 0,
  visibility TEXT DEFAULT 'private',
  tags TEXT[]
);

-- Enable RLS on player_videos
ALTER TABLE player_videos ENABLE ROW LEVEL SECURITY;

-- AI recommendations table for players
CREATE TABLE IF NOT EXISTS player_recommendations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  recommendation_type TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  viewed BOOLEAN DEFAULT FALSE
);

-- Enable RLS on player_recommendations
ALTER TABLE player_recommendations ENABLE ROW LEVEL SECURITY;

-- User preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  language TEXT DEFAULT 'english',
  theme TEXT DEFAULT 'dark',
  notifications_enabled BOOLEAN DEFAULT TRUE,
  preferred_positions TEXT[],
  favorite_players JSONB DEFAULT '[]',
  dashboard_layout JSONB DEFAULT '{}'
);

-- Enable RLS on user_preferences
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Heat maps table
CREATE TABLE IF NOT EXISTS heat_maps (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  position TEXT NOT NULL,
  data JSONB NOT NULL,
  title TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on heat_maps
ALTER TABLE heat_maps ENABLE ROW LEVEL SECURITY;

-- Create security policies

-- Profiles policy: Users can see their own profile
CREATE POLICY IF NOT EXISTS profiles_user_policy ON profiles 
  FOR ALL USING (auth.uid() = id);

-- Organizations policy: Members can see their own organizations
CREATE POLICY IF NOT EXISTS organizations_member_policy ON organizations 
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM organization_members 
      WHERE organization_id = organizations.id AND user_id = auth.uid()
    )
  );

-- Organizations policy: Only organization admins can modify their organization
CREATE POLICY IF NOT EXISTS organizations_admin_policy ON organizations 
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM organization_members 
      WHERE organization_id = organizations.id 
      AND user_id = auth.uid() 
      AND role = 'admin'
    )
  );

-- Organization members policy: Members can see their own membership and other members in their organization
CREATE POLICY IF NOT EXISTS org_members_view_policy ON organization_members 
  FOR SELECT USING (
    user_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM organization_members om 
      WHERE om.organization_id = organization_members.organization_id 
      AND om.user_id = auth.uid()
    )
  );

-- Organization members policy: Only admins can manage members
CREATE POLICY IF NOT EXISTS org_members_admin_policy ON organization_members 
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM organization_members 
      WHERE organization_id = organization_members.organization_id 
      AND user_id = auth.uid() 
      AND role = 'admin'
    )
  );

-- Chat sessions policy: Users can access their own sessions
CREATE POLICY IF NOT EXISTS chat_sessions_user_policy ON chat_sessions 
  FOR ALL USING (user_id = auth.uid());

-- Chat sessions policy: Organization members can access organization sessions
CREATE POLICY IF NOT EXISTS chat_sessions_org_policy ON chat_sessions 
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM organization_members 
      WHERE organization_id = chat_sessions.organization_id 
      AND user_id = auth.uid()
    )
  );

-- Chat messages policy: Access restricted to session owner or organization members
CREATE POLICY IF NOT EXISTS chat_messages_access_policy ON chat_messages 
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM chat_sessions 
      WHERE id = chat_messages.session_id 
      AND (
        user_id = auth.uid() OR 
        EXISTS (
          SELECT 1 FROM organization_members 
          WHERE organization_id = chat_sessions.organization_id 
          AND user_id = auth.uid()
        )
      )
    )
  );

-- Search parameters policy: Access restricted to session owner or organization members
CREATE POLICY IF NOT EXISTS search_params_access_policy ON search_parameters 
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM chat_sessions 
      WHERE id = search_parameters.session_id 
      AND (
        user_id = auth.uid() OR 
        EXISTS (
          SELECT 1 FROM organization_members 
          WHERE organization_id = chat_sessions.organization_id 
          AND user_id = auth.uid()
        )
      )
    )
  );

-- Search results policy: Access restricted to session owner or organization members
CREATE POLICY IF NOT EXISTS search_results_access_policy ON search_results 
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM chat_sessions 
      WHERE id = search_results.session_id 
      AND (
        user_id = auth.uid() OR 
        EXISTS (
          SELECT 1 FROM organization_members 
          WHERE organization_id = chat_sessions.organization_id 
          AND user_id = auth.uid()
        )
      )
    )
  );

-- Player videos policy: Players can manage their own videos
CREATE POLICY IF NOT EXISTS player_videos_owner_policy ON player_videos 
  FOR ALL USING (user_id = auth.uid());

-- Player videos policy: Public videos can be viewed by anyone
CREATE POLICY IF NOT EXISTS player_videos_public_policy ON player_videos 
  FOR SELECT USING (visibility = 'public');

-- Player recommendations policy: Players can view their own recommendations
CREATE POLICY IF NOT EXISTS player_recommendations_policy ON player_recommendations 
  FOR ALL USING (user_id = auth.uid());

-- User preferences policy: Users can manage their own preferences
CREATE POLICY IF NOT EXISTS user_preferences_policy ON user_preferences 
  FOR ALL USING (user_id = auth.uid());

-- Heat maps policy: Users can manage their own heat maps
CREATE POLICY IF NOT EXISTS heat_maps_owner_policy ON heat_maps 
  FOR ALL USING (user_id = auth.uid());

-- Heat maps policy: Organization members can view heat maps
CREATE POLICY IF NOT EXISTS heat_maps_org_policy ON heat_maps 
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM profiles 
      WHERE profiles.id = heat_maps.user_id 
      AND profiles.organization_id IN (
        SELECT organization_id FROM organization_members 
        WHERE user_id = auth.uid()
      )
    )
  );

-- Create an index for external_id to improve chat session lookup
CREATE INDEX IF NOT EXISTS idx_chat_sessions_external_id ON chat_sessions(external_id);

-- Insert some demo data (only if tables are empty)
INSERT INTO organizations (name, subscription_tier)
SELECT 'Demo Organization', 'professional'
WHERE NOT EXISTS (SELECT 1 FROM organizations LIMIT 1);

-- Add admin user to demo organization (will need to be updated with actual user ID in production)
DO $$
DECLARE
  org_id UUID;
  admin_user_id UUID;
BEGIN
  SELECT id INTO org_id FROM organizations WHERE name = 'Demo Organization' LIMIT 1;
  
  -- This is just placeholder logic - in production you'd need to use actual user IDs
  -- For now, we'll check if there's a user in auth.users table
  SELECT id INTO admin_user_id FROM auth.users LIMIT 1;
  
  IF org_id IS NOT NULL AND admin_user_id IS NOT NULL THEN
    INSERT INTO organization_members (organization_id, user_id, role)
    VALUES (org_id, admin_user_id, 'admin')
    ON CONFLICT (organization_id, user_id) DO NOTHING;
  END IF;
END $$;