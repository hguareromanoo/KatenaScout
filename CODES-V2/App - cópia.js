import React, { useState, useEffect } from 'react';
import { 
  Send, X, UserCircle, Trophy, TrendingUp, BarChart3, Clock, Package, Calendar, 
  Search, Menu, Home, Heart, LogIn, LogOut, User, Shield, Upload, Star,
  Settings, Sparkles, PlayIcon, Layers, MessageSquare, Pin, ChevronRight,
  LayoutDashboard, Users, Eye
} from 'lucide-react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, Tooltip, Legend 
} from 'recharts';

// Import the logo
import logo from './mylogo.svg';

// Import supabase client
import supabase, { 
  signIn, signUp, signOut, getUserProfile, getUserPreferences,
  createChatSession, getChatSessions, getChatMessages, addChatMessage,
  saveSearchParameters, saveSearchResults
} from './lib/supabase';

// Import the new components
import PlayerCompletePage from './components/PlayerCompletePage';
import PlayerRecommendationsPage from './components/PlayerRecommendationsPage';

// Main App Component
function App() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userType, setUserType] = useState(null); // 'player' or 'club'
  const [userData, setUserData] = useState(null);
  
  // App state
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [currentView, setCurrentView] = useState('dashboard'); // 'login', 'dashboard', 'scout', 'playground', etc.
  const [playgroundTab, setPlaygroundTab] = useState('dashboard'); // 'dashboard', 'talent', 'insight'
  const [favorites, setFavorites] = useState([]);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    return localStorage.getItem('language') || 'english';
  });
  
  // Featured players data
  const [featuredPlayers] = useState([
    {
      id: 'player-1',
      name: 'Lionel Messi',
      positions: ['rw', 'cf', 'amf'],
      age: 36,
      club: 'Inter Miami CF',
      country: 'Argentina',
      stats: {
        goals: 8.9,
        assists: 7.8,
        pass_accuracy: 92,
        successful_dribbles: 6.3,
        key_passes: 4.2,
        shots_on_target: 3.9,
        chances_created: 4.5,
        rating: 9.4
      },
      score: 98,
      photoUrl: 'https://i.imgur.com/2Sfm6uf.jpg'
    },
    {
      id: 'player-2',
      name: 'Cristiano Ronaldo',
      positions: ['cf', 'lw'],
      age: 39,
      club: 'Al-Nassr FC',
      country: 'Portugal',
      stats: {
        goals: 9.1,
        assists: 3.5,
        pass_accuracy: 87,
        successful_dribbles: 2.8,
        key_passes: 2.1,
        shots_on_target: 4.7,
        aerial_duels_won: 6.8,
        rating: 9.2
      },
      score: 96,
      photoUrl: 'https://i.imgur.com/AGM6gQq.jpg'
    },
    {
      id: 'player-3',
      name: 'Neymar Jr',
      positions: ['lw', 'amf'],
      age: 32,
      club: 'Al-Hilal SFC',
      country: 'Brazil',
      stats: {
        goals: 7.2,
        assists: 6.9,
        pass_accuracy: 89,
        successful_dribbles: 7.4,
        key_passes: 3.9,
        shots_on_target: 3.2,
        progressive_runs: 6.7,
        rating: 8.9
      },
      score: 94,
      photoUrl: 'https://i.imgur.com/YXS4AXj.jpg'
    },
    {
      id: 'player-4',
      name: 'Kylian Mbappé',
      positions: ['cf', 'lw'],
      age: 25,
      club: 'Real Madrid',
      country: 'France',
      stats: {
        goals: 8.5,
        assists: 5.2,
        pass_accuracy: 84,
        successful_dribbles: 5.9,
        key_passes: 2.8,
        shots_on_target: 4.2,
        sprint_speed: 9.8,
        rating: 9.1
      },
      score: 95,
      photoUrl: 'https://i.imgur.com/eFQQ5y2.jpg'
    },
    {
      id: 'player-5',
      name: 'Erling Haaland',
      positions: ['cf'],
      age: 23,
      club: 'Manchester City',
      country: 'Norway',
      stats: {
        goals: 9.3,
        assists: 2.3,
        pass_accuracy: 79,
        successful_dribbles: 1.8,
        shots_on_target: 5.2,
        aerial_duels_won: 7.2,
        finishing: 9.6,
        rating: 9.0
      },
      score: 93,
      photoUrl: 'https://i.imgur.com/Ja0TYho.jpg'
    }
  ]);
  
  // AI Highlighted gems
  const [hiddenGems] = useState([
    {
      id: 'gem-1',
      name: 'Endrick Felipe',
      positions: ['cf'],
      age: 17,
      club: 'Real Madrid',
      country: 'Brazil',
      stats: {
        goals: 6.4,
        assists: 2.2,
        pass_accuracy: 76,
        successful_dribbles: 4.3,
        shots_on_target: 3.1,
        finishing: 7.9,
        rating: 7.8
      },
      score: 87,
      highlight: 'Potencial de craque mundial',
      photoUrl: 'https://i.imgur.com/5YhStUP.jpg'
    },
    {
      id: 'gem-2',
      name: 'Lamine Yamal',
      positions: ['rw', 'amf'],
      age: 16,
      club: 'Barcelona',
      country: 'Spain',
      stats: {
        goals: 4.2,
        assists: 5.8,
        pass_accuracy: 85,
        successful_dribbles: 6.9,
        key_passes: 3.7,
        progressive_runs: 5.8,
        rating: 7.9
      },
      score: 86,
      highlight: 'Promessa do futebol espanhol',
      photoUrl: 'https://i.imgur.com/3mXD7dj.jpg'
    },
    {
      id: 'gem-3',
      name: 'João Pedro',
      positions: ['cf'],
      age: 22,
      club: 'Brighton & Hove Albion',
      country: 'Brazil',
      stats: {
        goals: 5.9,
        assists: 3.1,
        pass_accuracy: 81,
        successful_dribbles: 4.7,
        key_passes: 2.2,
        shots_on_target: 3.8,
        rating: 7.6
      },
      score: 84,
      highlight: 'Atacante completo e versátil',
      photoUrl: 'https://i.imgur.com/qiGDPE0.jpg'
    }
  ]);
  
  // Upcoming matches
  const [upcomingMatches] = useState([
    {
      id: 'match-1',
      home: 'Real Madrid',
      away: 'Barcelona',
      competition: 'La Liga',
      date: '2025-03-15T20:00:00',
      stadium: 'Santiago Bernabéu',
      relevantPlayers: ['player-4'],
      important: true
    },
    {
      id: 'match-2',
      home: 'Manchester City',
      away: 'Liverpool',
      competition: 'Premier League',
      date: '2025-03-16T16:30:00',
      stadium: 'Etihad Stadium',
      relevantPlayers: ['player-5'],
      important: true
    },
    {
      id: 'match-3',
      home: 'Inter Miami CF',
      away: 'LA Galaxy',
      competition: 'MLS',
      date: '2025-03-17T19:00:00',
      stadium: 'Chase Stadium',
      relevantPlayers: ['player-1'],
      important: false
    },
    {
      id: 'match-4',
      home: 'Al-Nassr FC',
      away: 'Al-Hilal SFC',
      competition: 'Saudi Pro League',
      date: '2025-03-20T18:00:00',
      stadium: 'Al-Awwal Park',
      relevantPlayers: ['player-2', 'player-3'],
      important: false
    }
  ]);
  
  // User usage stats
  const [usageStats] = useState({
    searches: 27,
    favoritedPlayers: 8,
    lastActivity: new Date(Date.now() - 3600000 * 24).toISOString(),
    recommendedActions: [
      { text: 'Completar perfil', done: false },
      { text: 'Analisar talentos por posição', done: false },
      { text: 'Salvar preferências de busca', done: true }
    ]
  });
  
  // Chat history
  const [chatHistory, setChatHistory] = useState(() => {
    const savedHistory = localStorage.getItem('chatHistory');
    return savedHistory ? JSON.parse(savedHistory) : [];
  });
  
  // Check if user is logged in from Supabase session and load user data
  useEffect(() => {
    const checkSession = async () => {
      try {
        // Get session from Supabase
        const { session } = await supabase.auth.getSession();
        const storedLanguage = localStorage.getItem('language');
        const storedFavorites = localStorage.getItem('favorites');
        
        if (storedLanguage) {
          setCurrentLanguage(storedLanguage);
        }
        
        if (session?.user) {
          setIsAuthenticated(true);
          
          // Get user profile from Supabase
          try {
            const { data: profile, error } = await supabase
              .from('profiles')
              .select('*')
              .eq('id', session.user.id)
              .single();
              
            if (error) throw error;
            
            // Set user data from profile
            setUserData(profile);
            setUserType(profile.user_type || 'club');
            
            // Set language preference from profile if available
            if (profile.language) {
              setCurrentLanguage(profile.language);
              localStorage.setItem('language', profile.language);
            }
            
            // Always go directly to scout/chat view for logged in users
            setCurrentView('scout');
          } catch (profileError) {
            console.error("Error loading user profile:", profileError);
            // If we can't load the profile but have a valid session,
            // still authenticate the user but with minimal data
            setUserData({
              id: session.user.id,
              email: session.user.email,
              name: session.user.user_metadata?.name || session.user.email.split('@')[0],
              user_type: 'club',
              language: 'english'
            });
            setUserType('club');
            setCurrentView('scout');
          }
        } else {
          setCurrentView('login');
        }
        
        if (storedFavorites) {
          setFavorites(JSON.parse(storedFavorites));
        }
      } catch (error) {
        console.error("Session check error:", error);
        setCurrentView('login');
      }
    };
    
    checkSession();
    
    // Set up auth state listener
    const { data: authListener } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        if (event === 'SIGNED_IN' && session) {
          // User signed in, get their profile
          try {
            const { data: profile, error } = await supabase
              .from('profiles')
              .select('*')
              .eq('id', session.user.id)
              .single();
              
            if (error) throw error;
            
            setIsAuthenticated(true);
            setUserData(profile);
            setUserType(profile.user_type || 'club');
            
            if (profile.language) {
              setCurrentLanguage(profile.language);
              localStorage.setItem('language', profile.language);
            }
            
            // Always go directly to scout/chat view for authenticated users
            setCurrentView('scout');
          } catch (error) {
            console.error("Error loading user profile after sign in:", error);
          }
        } else if (event === 'SIGNED_OUT') {
          // User signed out
          setIsAuthenticated(false);
          setUserData(null);
          setUserType(null);
          setCurrentView('login');
        }
      }
    );
    
    // Clean up subscription on unmount
    return () => {
      if (authListener && authListener.subscription) {
        authListener.subscription.unsubscribe();
      }
    };
  }, []);
  
  // Function to handle language change
  const handleLanguageChange = (language) => {
    setCurrentLanguage(language);
    localStorage.setItem('language', language);
    
    // Update userData with the new language
    if (userData) {
      const updatedUserData = { ...userData, language };
      setUserData(updatedUserData);
      localStorage.setItem('user', JSON.stringify(updatedUserData));
    }
  };
  
  // Save favorites to localStorage when they change
  useEffect(() => {
    if (favorites.length > 0) {
      localStorage.setItem('favorites', JSON.stringify(favorites));
    }
  }, [favorites]);
  
  // Save chat history to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);
  
  // Function to add a new chat to history
  const addChatToHistory = async (chatId, query) => {
    try {
      // Create a new chat object
      const newChat = {
        id: chatId,
        title: query.length > 30 ? query.substring(0, 30) + '...' : query,
        date: new Date().toISOString(),
        snippet: query
      };
      
      // Add the new chat to the beginning of the history in state
      setChatHistory(prevHistory => [newChat, ...prevHistory]);
      
      // If user is authenticated, save the chat session to Supabase
      if (isAuthenticated && userData?.id) {
        try {
          // Check if we should create a new chat session in Supabase
          const { data: existingSession, error: sessionError } = await supabase
            .from('chat_sessions')
            .select('id')
            .eq('external_id', chatId)
            .single();
            
          if (sessionError && sessionError.code !== 'PGRST116') {
            // Error other than "not found"
            console.error("Error checking for chat session:", sessionError);
          }
          
          if (!existingSession) {
            // Create new chat session in Supabase
            const sessionData = await createChatSession(
              query, // Use the first query as the name 
              currentLanguage || 'english',
              chatId // Pass the external ID to link with local storage
            );
            
            console.log("Created new chat session in Supabase:", sessionData);
            
            // Update the local chat with the Supabase ID
            if (sessionData && sessionData.id) {
              newChat.supabaseId = sessionData.id;
              setChatHistory(prevHistory => {
                const updatedHistory = [...prevHistory];
                const index = updatedHistory.findIndex(chat => chat.id === chatId);
                if (index !== -1) {
                  updatedHistory[index] = {...updatedHistory[index], supabaseId: sessionData.id};
                }
                return updatedHistory;
              });
            }
          }
        } catch (supabaseError) {
          console.error("Error with Supabase chat session:", supabaseError);
          // Continue with local storage only if Supabase fails
        }
      }
    } catch (error) {
      console.error("Error adding chat to history:", error);
      // Still add to local history even if Supabase fails
      const newChat = {
        id: chatId,
        title: query.length > 30 ? query.substring(0, 30) + '...' : query,
        date: new Date().toISOString(),
        snippet: query
      };
      setChatHistory(prevHistory => [newChat, ...prevHistory]);
    }
  };
  
  // Load chat history from Supabase when user logs in
  useEffect(() => {
    const loadChatHistory = async () => {
      if (isAuthenticated && userData?.id) {
        try {
          // Get chat sessions from Supabase
          const { data: sessions, error } = await getChatSessions();
          
          if (error) throw error;
          
          if (sessions && sessions.length > 0) {
            // Format the sessions for our chat history
            const formattedSessions = sessions.map(session => ({
              id: session.external_id || session.id,
              title: session.name || 'Untitled Chat',
              date: session.created_at,
              snippet: session.name || 'Chat session',
              supabsaseId: session.id // Keep track of the Supabase ID
            }));
            
            // Update chat history state, preserving any local history
            setChatHistory(prevHistory => {
              // Get IDs of sessions from Supabase
              const supabaseIds = formattedSessions.map(s => s.id);
              
              // Filter out local sessions that are now in Supabase
              const filteredLocalHistory = prevHistory.filter(
                local => !supabaseIds.includes(local.id)
              );
              
              // Combine Supabase sessions with remaining local sessions
              return [...formattedSessions, ...filteredLocalHistory];
            });
          }
        } catch (error) {
          console.error("Error loading chat history from Supabase:", error);
        }
      }
    };
    
    loadChatHistory();
  }, [isAuthenticated, userData]);

  // Function to handle when a player is selected from the chat
  const handlePlayerSelected = (player, metrics) => {
    setSelectedPlayer(player);
    setMetrics(metrics);
  };
  
  // Function to handle user login
  const handleLogin = async (user, type) => {
    try {
      setIsAuthenticated(true);
      setUserType(type);
      setUserData(user);
      
      // Check if this is a demo account or if onboarding is already completed
      const isDemoAccount = user.id?.includes('demo') || user.email?.includes('demo');
      
      if (isDemoAccount || user.onboarding_completed) {
        // Skip onboarding for demo accounts or users who already completed it
        setCurrentView('scout');
      } else {
        // Check if this is the first login or if onboarding is needed
        try {
          const { data: profiles } = await supabase
            .from('profiles')
            .select('onboarding_completed')
            .eq('id', user.id)
            .single();
          
          const hasCompletedOnboarding = profiles?.onboarding_completed || false;
          
          if (!hasCompletedOnboarding) {
            setShowOnboarding(true);
            setCurrentView('onboarding');
          } else {
            // Direct to scout/chat view after login if onboarding is completed
            setCurrentView('scout');
          }
        } catch (profileError) {
          console.error("Error checking onboarding status:", profileError);
          // Handle profile error gracefully - just go to scout view
          setCurrentView('scout');
        }
      }
      
      // Save language preference
      if (user.language) {
        localStorage.setItem('language', user.language);
      }
    } catch (error) {
      console.error("Error during login:", error);
      // Handle errors gracefully - for now just proceed to scout view
      setCurrentView('scout');
    }
  };
  
  // Function to complete onboarding
  const completeOnboarding = async (updatedUserData) => {
    try {
      // Update local state
      const newUserData = {...userData, ...updatedUserData, onboarding_completed: true};
      setUserData(newUserData);
      
      // Update profile in Supabase
      const { error } = await supabase
        .from('profiles')
        .update({
          name: updatedUserData.name || userData.name,
          language: updatedUserData.language || userData.language,
          team: updatedUserData.team || userData.team,
          position: updatedUserData.position || userData.position,
          onboarding_completed: true
        })
        .eq('id', userData.id);
      
      if (error) throw error;
      
      // Set language preference
      if (updatedUserData.language) {
        setCurrentLanguage(updatedUserData.language);
        localStorage.setItem('language', updatedUserData.language);
      }
      
      setShowOnboarding(false);
      setCurrentView('scout');
    } catch (error) {
      console.error("Error completing onboarding:", error);
      // Continue anyway to avoid blocking the user
      setShowOnboarding(false);
      setCurrentView('scout');
    }
  };
  
  // Function to handle user logout
  const handleLogout = async () => {
    try {
      // Sign out from Supabase
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
      
      // Clear app state
      setIsAuthenticated(false);
      setUserType(null);
      setUserData(null);
      setCurrentView('login');
      
      // Clear any sensitive data from localStorage 
      // but keep language preference
      const language = localStorage.getItem('language');
      localStorage.clear();
      if (language) localStorage.setItem('language', language);
      
    } catch (error) {
      console.error("Error during logout:", error);
      // Force logout anyway for safety
      setIsAuthenticated(false);
      setUserType(null);
      setUserData(null);
      setCurrentView('login');
    }
  };
  
  // Function to toggle favorite status for a player
  const toggleFavorite = async (player) => {
    const playerExists = favorites.some(fav => fav.id === player.id);
    
    // Update local state first for immediate feedback
    if (playerExists) {
      setFavorites(favorites.filter(fav => fav.id !== player.id));
    } else {
      setFavorites([...favorites, player]);
    }
    
    // Save to localStorage
    const updatedFavorites = playerExists 
      ? favorites.filter(fav => fav.id !== player.id)
      : [...favorites, player];
    localStorage.setItem('favorites', JSON.stringify(updatedFavorites));
    
    // If user is authenticated, save to Supabase
    if (isAuthenticated && userData?.id) {
      try {
        // Get the current user preferences from Supabase
        const { data: userPrefs, error: prefsError } = await supabase
          .from('user_preferences')
          .select('*')
          .eq('user_id', userData.id)
          .single();
          
        if (prefsError && prefsError.code !== 'PGRST116') {
          // Error other than "not found"
          console.error("Error fetching user preferences:", prefsError);
          // Try direct API call to backend to handle preferences
          tryBackendPreferencesUpdate(player, playerExists);
          return;
        }
        
        if (!userPrefs) {
          console.log("No user preferences found, creating new preferences");
          // Create preferences if they don't exist
          const { data: insertData, error: insertError } = await supabase
            .from('user_preferences')
            .insert({
              user_id: userData.id,
              language: userData.language || currentLanguage || 'english',
              theme: 'dark',
              notifications_enabled: true,
              favorite_players: playerExists ? [] : [player]
            })
            .select();
            
          if (insertError) {
            console.error("Error creating user preferences:", insertError);
            // Try direct API call to backend to handle preferences
            tryBackendPreferencesUpdate(player, playerExists);
          } else {
            console.log("Created new user preferences:", insertData);
          }
        } else {
          console.log("Updating existing user preferences");
          // Update existing preferences
          let updatedFavs = [...(userPrefs.favorite_players || [])];
          
          if (playerExists) {
            // Remove player from favorites
            updatedFavs = updatedFavs.filter(fav => {
              // Check by ID or name if ID is not available
              return fav.id !== player.id && 
                   (fav.name !== player.name || fav.positions?.join() !== player.positions?.join());
            });
          } else {
            // Add player to favorites
            updatedFavs.push(player);
          }
          
          const { data: updateData, error: updateError } = await supabase
            .from('user_preferences')
            .update({
              favorite_players: updatedFavs
            })
            .eq('user_id', userData.id)
            .select();
            
          if (updateError) {
            console.error("Error updating user preferences:", updateError);
            // Try direct API call to backend to handle preferences
            tryBackendPreferencesUpdate(player, playerExists);
          } else {
            console.log("Updated user preferences:", updateData);
          }
        }
      } catch (error) {
        console.error("Error updating favorites in Supabase:", error);
        // Try direct API call to backend to handle preferences
        tryBackendPreferencesUpdate(player, playerExists);
      }
    }
  };
  
  // Helper function to try updating preferences via backend API if Supabase direct update fails
  const tryBackendPreferencesUpdate = async (player, isRemoving) => {
    try {
      // Get auth token for the API call
      const { data: authData } = await supabase.auth.getSession();
      const authToken = authData?.session?.access_token;
      
      if (!authToken) {
        console.error("No auth token available for API call");
        return;
      }
      
      // Prepare headers with auth token
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      };
      
      // Prepare request body
      const requestBody = {
        action: isRemoving ? 'remove_favorite' : 'add_favorite',
        player: player
      };
      
      // Make API call to update preferences
      const response = await fetch('http://localhost:5001/user/preferences', {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody)
      });
      
      const data = await response.json();
      
      if (!data.success) {
        console.error("Error updating preferences via API:", data.error);
      } else {
        console.log("Successfully updated preferences via API:", data.message);
      }
    } catch (error) {
      console.error("Error in API call to update preferences:", error);
    }
  };
  
  // Check if a player is in favorites
  const isPlayerFavorite = (player) => {
    return player && favorites.some(fav => fav.id === player.id);
  };
  
  // Load favorites from Supabase when user logs in
  useEffect(() => {
    const loadFavorites = async () => {
      if (isAuthenticated && userData?.id) {
        try {
          const { data: userPrefs, error } = await getUserPreferences();
          
          if (error) {
            console.error("Error loading user preferences:", error);
            return;
          }
          
          if (userPrefs?.favorite_players?.length > 0) {
            // Update favorites state, preserving any local favorites
            setFavorites(prev => {
              // Get IDs of Supabase favorites
              const supabaseIds = userPrefs.favorite_players.map(p => p.id);
              
              // Filter out local favorites that match Supabase favorites by ID
              const uniqueLocalFavs = prev.filter(
                local => !supabaseIds.includes(local.id)
              );
              
              // Combine Supabase favorites with unique local favorites
              return [...userPrefs.favorite_players, ...uniqueLocalFavs];
            });
            
            // Update localStorage too
            localStorage.setItem('favorites', JSON.stringify([
              ...userPrefs.favorite_players,
              ...favorites.filter(fav => !userPrefs.favorite_players.some(p => p.id === fav.id))
            ]));
          }
        } catch (error) {
          console.error("Error loading favorites from Supabase:", error);
        }
      }
    };
    
    loadFavorites();
  }, [isAuthenticated, userData]);

  // Components are now imported at the top of the file
  
  // Render different views based on authentication state and current view
  // Define translations for UI components
  const getTranslations = () => {
    const translations = {
      english: {
        // Navigation
        chat: "Chat",
        playground: "Playground",
        configuration: "Configuration",
        profile: "Profile",
        logout: "Log out",
        newChat: "New chat",
        recentChats: "RECENT CHATS",
        noHistory: "No chat history",
        
        // Playground
        dashboard: "Dashboard",
        talentAnalysis: "Talent Analysis",
        inSight: "In Sight",
        playersInSight: "Players In Sight",
        noPlayers: "No players in sight yet",
        useScoutAI: "Use the Scout AI to find and favorite players",
        advancedTools: "Advanced scouting tools and player analysis",
        
        // Configuration
        configTitle: "Configuration",
        languageSettings: "Language Settings",
        languageChangesImmediately: "Language will change immediately",
        searchPreferences: "Search Preferences",
        includeRetired: "Include retired players",
        transferMarket: "Only show players in transfer market",
        saveSearchPreferences: "Save Search Preferences",
        
        // Positions
        defenders: "Defenders",
        midfielders: "Midfielders",
        forwards: "Forwards",
        goalkeepers: "Goalkeepers",
        viewTopPlayers: "View top players",
        
        // Profile
        profileTitle: "Profile",
        name: "Name",
        email: "Email",
        club: "Club/Organization",
        position: "Position",
        currentTeam: "Current Team",
        saveProfile: "Save Profile",
        player: "Player Account",
        
        // Player Info
        age: "Age",
        height: "Height",
        weight: "Weight"
      },
      portuguese: {
        // Navigation
        chat: "Chat",
        playground: "Ambiente",
        configuration: "Configurações",
        profile: "Perfil",
        logout: "Sair",
        newChat: "Novo chat",
        recentChats: "CHATS RECENTES",
        noHistory: "Nenhum histórico de chat",
        
        // Playground
        dashboard: "Painel",
        talentAnalysis: "Análise de Talentos",
        inSight: "Em Vista",
        playersInSight: "Jogadores Em Vista",
        noPlayers: "Nenhum jogador em vista ainda",
        useScoutAI: "Use o Scout AI para encontrar e favoritar jogadores",
        advancedTools: "Ferramentas avançadas de scout e análise de jogadores",
        
        // Configuration
        configTitle: "Configurações",
        languageSettings: "Configurações de Idioma",
        languageChangesImmediately: "O idioma mudará imediatamente",
        searchPreferences: "Preferências de Busca",
        includeRetired: "Incluir jogadores aposentados",
        transferMarket: "Mostrar apenas jogadores no mercado de transferências",
        saveSearchPreferences: "Salvar Preferências de Busca",
        
        // Positions
        defenders: "Defensores",
        midfielders: "Meio-campistas",
        forwards: "Atacantes",
        goalkeepers: "Goleiros",
        viewTopPlayers: "Ver melhores jogadores",
        
        // Profile
        profileTitle: "Perfil",
        name: "Nome",
        email: "Email",
        club: "Clube/Organização",
        position: "Posição",
        currentTeam: "Time Atual",
        saveProfile: "Salvar Perfil",
        player: "Conta de Jogador",
        
        // Player Info
        age: "Idade",
        height: "Altura",
        weight: "Peso"
      },
      spanish: {
        // Navigation
        chat: "Chat",
        playground: "Entorno",
        configuration: "Configuración",
        profile: "Perfil",
        logout: "Cerrar sesión",
        newChat: "Nuevo chat",
        recentChats: "CHATS RECIENTES",
        noHistory: "Sin historial de chat",
        
        // Playground
        dashboard: "Panel",
        talentAnalysis: "Análisis de Talentos",
        inSight: "En Vista",
        playersInSight: "Jugadores En Vista",
        noPlayers: "Aún no hay jugadores en vista",
        useScoutAI: "Use Scout AI para encontrar y favoritar jugadores",
        advancedTools: "Herramientas avanzadas de scout y análisis de jugadores",
        
        // Configuration
        configTitle: "Configuración",
        languageSettings: "Configuración de Idioma",
        languageChangesImmediately: "El idioma cambiará inmediatamente",
        searchPreferences: "Preferencias de Búsqueda",
        includeRetired: "Incluir jugadores retirados",
        transferMarket: "Mostrar solo jugadores en el mercado de fichajes",
        saveSearchPreferences: "Guardar Preferencias de Búsqueda",
        
        // Positions
        defenders: "Defensores",
        midfielders: "Centrocampistas",
        forwards: "Delanteros",
        goalkeepers: "Porteros",
        viewTopPlayers: "Ver mejores jugadores",
        
        // Profile
        profileTitle: "Perfil",
        name: "Nombre",
        email: "Email",
        club: "Club/Organización",
        position: "Posición",
        currentTeam: "Equipo Actual",
        saveProfile: "Guardar Perfil",
        player: "Cuenta de Jugador",
        
        // Player Info
        age: "Edad",
        height: "Altura",
        weight: "Peso"
      },
      bulgarian: {
        // Navigation
        chat: "Чат",
        playground: "Платформа",
        configuration: "Настройки",
        profile: "Профил",
        logout: "Изход",
        newChat: "Нов чат",
        recentChats: "СКОРОШНИ ЧАТОВЕ",
        noHistory: "Няма история на чата",
        
        // Playground
        dashboard: "Табло",
        talentAnalysis: "Анализ на Таланти",
        inSight: "На фокус",
        playersInSight: "Играчи на фокус",
        noPlayers: "Все още няма играчи на фокус",
        useScoutAI: "Използвайте Scout AI, за да намерите и маркирате играчи",
        advancedTools: "Напреднали инструменти за скаутинг и анализ на играчи",
        
        // Configuration
        configTitle: "Настройки",
        languageSettings: "Настройки на Езика",
        languageChangesImmediately: "Езикът ще се промени веднага",
        searchPreferences: "Предпочитания за Търсене",
        includeRetired: "Включи пенсионирани играчи",
        transferMarket: "Показвай само играчи на трансферния пазар",
        saveSearchPreferences: "Запази Предпочитанията за Търсене",
        
        // Positions
        defenders: "Защитници",
        midfielders: "Полузащитници",
        forwards: "Нападатели",
        goalkeepers: "Вратари",
        viewTopPlayers: "Виж най-добрите играчи",
        
        // Profile
        profileTitle: "Профил",
        name: "Име",
        email: "Имейл",
        club: "Клуб/Организация",
        position: "Позиция",
        currentTeam: "Настоящ Отбор",
        saveProfile: "Запази Профил",
        player: "Акаунт на Играч",
        
        // Player Info
        age: "Възраст",
        height: "Височина",
        weight: "Тегло"
      }
    };
    
    return translations[currentLanguage] || translations.english;
  };
  
  const renderContent = () => {
    if (!isAuthenticated || currentView === 'login') {
      return <LoginView onLogin={handleLogin} currentLanguage={currentLanguage} />;
    }
    
    // Get translations for current language
    const t = getTranslations();
    
    return (
      <div className="flex h-screen bg-gray-900 overflow-hidden">
        {/* ChatGPT-style Sidebar */}
        <div className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col overflow-hidden">
          {/* Logo area */}
          <div className="p-4 border-b border-gray-800 flex items-center">
            <img src={logo} alt="KatenaScout Logo" className="w-8 h-8 mr-2" />
            <h1 className="text-white font-bold text-lg">KatenaScout</h1>
          </div>
          
          {/* New chat button */}
          <button 
            onClick={() => {
              setCurrentView('scout');
              // Generate a new session ID for a new chat
              const newSessionId = `session-${Date.now()}`;
              localStorage.setItem('chatSessionId', newSessionId);
              // Force a reload of the chat interface
              const event = new CustomEvent('new-chat');
              document.dispatchEvent(event);
            }}
            className="mx-3 mt-3 flex items-center gap-3 rounded-md border border-white/20 px-3 py-3 text-white transition-colors hover:bg-gray-800"
          >
            <Sparkles size={16} /> {t.newChat}
          </button>
          
          {/* Chat History */}
          <div className="mt-4 px-3 flex flex-col flex-shrink-0">
            <h3 className="text-xs font-medium text-gray-400 mb-2 px-2">{t.recentChats}</h3>
            <div className="overflow-y-auto max-h-[30vh] pr-1 custom-scrollbar">
              {chatHistory.length === 0 ? (
                <div className="text-center py-3 text-gray-500 text-sm">
                  {t.noHistory}
                </div>
              ) : (
                chatHistory.map((chat, index) => (
                  <button 
                    key={chat.id || index}
                    onClick={() => {
                      setCurrentView('scout');
                      // Set session ID to existing chat ID to continue the conversation
                      localStorage.setItem('chatSessionId', chat.id);
                      // Force a reload of the chat interface
                      const event = new CustomEvent('load-chat', { detail: { chatId: chat.id, title: chat.title } });
                      document.dispatchEvent(event);
                    }}
                    className="flex flex-col items-start text-left text-sm mb-1 p-2 rounded-md hover:bg-gray-800 text-gray-300 w-full"
                  >
                    <div className="flex items-center w-full">
                      <MessageSquare size={14} className="mr-2 flex-shrink-0" />
                      <div className="flex-1 truncate">{chat.title}</div>
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(chat.date).toLocaleDateString()}
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
          
          {/* Navigation menu */}
          <div className="mt-5 flex flex-col flex-grow overflow-hidden">
            <nav className="space-y-1 px-3 overflow-y-auto custom-scrollbar">
              {/* Chat */}
              <button
                onClick={() => setCurrentView('scout')}
                className={`flex items-center gap-3 w-full rounded-md px-3 py-3 text-sm transition-colors ${
                  currentView === 'scout' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <MessageSquare size={16} /> {t.chat}
              </button>
              
              {/* Playground */}
              <button
                onClick={() => setCurrentView('playground')}
                className={`flex items-center gap-3 w-full rounded-md px-3 py-3 text-sm transition-colors ${
                  currentView === 'playground' || currentView === 'playground-talent' || currentView === 'playground-insight' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <PlayIcon size={16} /> {t.playground}
              </button>
              
              {/* Configuration */}
              <button
                onClick={() => setCurrentView('configuration')}
                className={`flex items-center gap-3 w-full rounded-md px-3 py-3 text-sm transition-colors ${
                  currentView === 'configuration' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <Settings size={16} /> {t.configuration}
              </button>
              
              {/* Profile */}
              <button
                onClick={() => setCurrentView('profile')}
                className={`flex items-center gap-3 w-full rounded-md px-3 py-3 text-sm transition-colors ${
                  currentView === 'profile' ? 'bg-gray-800 text-white' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <User size={16} /> {t.profile}
              </button>
            </nav>
            
            <div className="mt-auto">
              <div className="border-t border-gray-800 pt-2 px-3 mt-4">
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-3 w-full rounded-md px-3 py-3 text-sm text-gray-400 hover:bg-gray-800 hover:text-white"
                >
                  <LogOut size={16} /> {t.logout}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Main Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Onboarding View */}
          {currentView === 'onboarding' && (
            <div className="flex-1 bg-gray-900 text-white p-8 flex items-center justify-center">
              <div className="bg-gray-800 p-8 rounded-xl max-w-2xl w-full">
                <div className="flex items-center mb-6">
                  <div className="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center mr-4">
                    <span className="text-white text-2xl">⚽</span>
                  </div>
                  <h1 className="text-2xl font-bold text-white">Welcome to KatenaScout</h1>
                </div>
                
                <p className="text-gray-300 mb-8">Let's set up your profile to get the best experience.</p>
                
                <form onSubmit={(e) => {
                  e.preventDefault();
                  const formData = new FormData(e.target);
                  const language = formData.get('language');
                  
                  // Set language immediately
                  handleLanguageChange(language);
                  
                  const data = {
                    name: formData.get('name'),
                    language: language,
                    theme: formData.get('theme')
                  };
                  
                  if (userType === 'club') {
                    data.team = formData.get('team');
                  } else if (userType === 'player') {
                    data.position = formData.get('position');
                  }
                  
                  completeOnboarding(data);
                }}>
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm text-gray-400 mb-1">Name</label>
                      <input 
                        name="name"
                        type="text" 
                        defaultValue={userData?.name} 
                        className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                        required
                      />
                    </div>
                    
                    {userType === 'club' && (
                      <div>
                        <label className="block text-sm text-gray-400 mb-1">Club/Organization</label>
                        <input 
                          name="team"
                          type="text" 
                          defaultValue={userData?.team} 
                          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                        />
                      </div>
                    )}
                    
                    {userType === 'player' && (
                      <div>
                        <label className="block text-sm text-gray-400 mb-1">Position</label>
                        <select 
                          name="position"
                          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                          defaultValue={userData?.position || 'cmf'}
                        >
                          <option value="gk">Goalkeeper</option>
                          <option value="cb">Center Back</option>
                          <option value="lb">Left Back</option>
                          <option value="rb">Right Back</option>
                          <option value="dmf">Defensive Midfielder</option>
                          <option value="cmf">Central Midfielder</option>
                          <option value="amf">Attacking Midfielder</option>
                          <option value="lw">Left Winger</option>
                          <option value="rw">Right Winger</option>
                          <option value="cf">Center Forward</option>
                        </select>
                      </div>
                    )}
                    
                    <div>
                      <label className="block text-sm text-gray-400 mb-1">Language</label>
                      <select 
                        name="language"
                        className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                        value={currentLanguage}
                        onChange={(e) => handleLanguageChange(e.target.value)}
                      >
                        <option value="english">English</option>
                        <option value="portuguese">Portuguese</option>
                        <option value="spanish">Spanish</option>
                        <option value="bulgarian">Bulgarian</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm text-gray-400 mb-1">Theme</label>
                      <div className="flex space-x-4">
                        <label className="flex items-center">
                          <input 
                            type="radio" 
                            name="theme" 
                            value="dark" 
                            defaultChecked={true}
                            className="mr-2" 
                          />
                          Dark
                        </label>
                        <label className="flex items-center">
                          <input 
                            type="radio" 
                            name="theme" 
                            value="light" 
                            className="mr-2" 
                          />
                          Light
                        </label>
                      </div>
                    </div>
                    
                    <div className="pt-4 space-y-3">
                      <button 
                        type="submit" 
                        className="w-full py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg"
                        onClick={() => {
                          // Additional click handler to ensure button works properly
                          const formElement = document.querySelector('form');
                          const nameInput = formElement.querySelector('input[name="name"]');
                          const languageSelect = formElement.querySelector('select[name="language"]');
                          const themeInput = formElement.querySelector('input[name="theme"]:checked');
                          
                          // Create data object manually as backup
                          const data = {
                            name: nameInput?.value || userData?.name || 'User',
                            language: languageSelect?.value || currentLanguage || 'english',
                            theme: themeInput?.value || 'dark'
                          };
                          
                          if (userType === 'club') {
                            const teamInput = formElement.querySelector('input[name="team"]');
                            data.team = teamInput?.value || userData?.team || '';
                          } else if (userType === 'player') {
                            const positionSelect = formElement.querySelector('select[name="position"]');
                            data.position = positionSelect?.value || userData?.position || 'cmf';
                          }
                          
                          // Complete onboarding directly if form submission fails
                          setTimeout(() => {
                            if (currentView === 'onboarding') {
                              completeOnboarding(data);
                            }
                          }, 500);
                        }}
                      >
                        Start Using KatenaScout
                      </button>
                      
                      <div className="text-center">
                        <button 
                          type="button"
                          className="text-gray-400 hover:text-white"
                          onClick={() => {
                            // Skip onboarding with default values
                            const data = {
                              name: userData?.name || 'User',
                              language: currentLanguage || 'english',
                              theme: 'dark',
                              team: userData?.team || '',
                              position: userData?.position || 'cmf'
                            };
                            completeOnboarding(data);
                          }}
                        >
                          Skip for now
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          )}
          
          {/* Chat Interface */}
          {currentView === 'scout' && (
            <div className="flex flex-col h-full overflow-hidden">
              {/* Chat Interface (Full Screen) */}
              <div className="flex-1 relative overflow-hidden">
                <ChatInterface 
                  onPlayerSelected={handlePlayerSelected} 
                  expanded={!selectedPlayer}
                  chatHistory={chatHistory}
                  addChatToHistory={addChatToHistory}
                  userData={{ ...userData, language: currentLanguage }}
                  isAuthenticated={isAuthenticated}
                />
                
                {/* Player Dashboard - Slide in from the side when a player is selected */}
                {/* Player Dashboard - Displayed as a popup modal when a player is selected */}
                {selectedPlayer && (
                  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70 z-50 p-4">
                    <div className="bg-gray-900 border border-gray-800 rounded-xl shadow-2xl overflow-hidden w-full max-w-4xl max-h-[90vh]">
                      <div className="relative h-full max-h-[90vh] flex flex-col">
                        <div className="absolute top-4 right-4 flex space-x-2 z-10">
                          {/* Favorite button */}
                          <button 
                            onClick={() => toggleFavorite(selectedPlayer)}
                            className={`p-2 rounded-full transition-colors ${
                              isPlayerFavorite(selectedPlayer) 
                                ? 'bg-red-600 text-white hover:bg-red-700' 
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                            }`}
                          >
                            <Heart size={20} fill={isPlayerFavorite(selectedPlayer) ? "white" : "none"} />
                          </button>
                          
                          {/* Close button */}
                          <button 
                            onClick={() => setSelectedPlayer(null)}
                            className="p-2 rounded-full bg-gray-700 text-gray-300 hover:bg-gray-600"
                          >
                            <X size={20} />
                          </button>
                        </div>
                        
                        <div className="overflow-y-auto flex-1">
                          <PlayerDashboard 
                            player={selectedPlayer} 
                            metrics={metrics}
                            onClose={() => setSelectedPlayer(null)}
                            isPlayerFavorite={isPlayerFavorite(selectedPlayer)}
                            toggleFavorite={() => toggleFavorite(selectedPlayer)}
                            userType={userType}
                            onViewComplete={() => {
                              setCurrentView('player-profile');
                              setSelectedPlayer(null);
                            }}
                          />
                        </div>
                        
                        <div className="p-4 border-t border-gray-700 flex justify-end bg-gray-800">
                          <button 
                            onClick={() => {
                              setCurrentView('player-profile');
                              setSelectedPlayer(null);
                            }}
                            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg flex items-center"
                          >
                            <UserCircle className="mr-2" size={18} />
                            View Full Profile
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
          
          {/* Playground View */}
          {currentView === 'playground' && (
            <div className="flex flex-col h-full bg-gray-900 text-white">
              {/* Playground Header */}
              <div className="border-b border-gray-800 p-4">
                <h1 className="text-xl font-bold flex items-center">
                  <PlayIcon className="mr-2 text-green-500" size={20} />
                  {t.playground}
                </h1>
                <p className="text-sm text-gray-400 mt-1">
                  {t.advancedTools}
                </p>
              </div>
              
              {/* Playground Navigation */}
              <div className="flex border-b border-gray-800">
                <button
                  onClick={() => setPlaygroundTab('dashboard')}
                  className={`px-4 py-3 font-medium flex items-center ${
                    playgroundTab === 'dashboard' 
                      ? 'text-white border-b-2 border-green-500' 
                      : 'text-gray-400 hover:text-gray-200'
                  }`}
                >
                  <LayoutDashboard size={16} className="mr-2" />
                  {t.dashboard}
                </button>
                
                <button
                  onClick={() => setPlaygroundTab('talent')}
                  className={`px-4 py-3 font-medium flex items-center ${
                    playgroundTab === 'talent' 
                      ? 'text-white border-b-2 border-green-500' 
                      : 'text-gray-400 hover:text-gray-200'
                  }`}
                >
                  <Users size={16} className="mr-2" />
                  {t.talentAnalysis}
                </button>
                
                <button
                  onClick={() => setPlaygroundTab('insight')}
                  className={`px-4 py-3 font-medium flex items-center ${
                    playgroundTab === 'insight' 
                      ? 'text-white border-b-2 border-green-500' 
                      : 'text-gray-400 hover:text-gray-200'
                  }`}
                >
                  <Pin size={16} className="mr-2" />
                  {t.inSight}
                </button>
              </div>
              
              {/* Playground Content */}
              <div className="flex-1 overflow-y-auto p-6">
                {/* Dashboard Tab */}
                {playgroundTab === 'dashboard' && (
                  <DashboardView 
                    featuredPlayers={featuredPlayers}
                    hiddenGems={hiddenGems}
                    upcomingMatches={upcomingMatches}
                    usageStats={usageStats}
                    onSelectPlayer={handlePlayerSelected}
                    setCurrentView={setCurrentView}
                    favorites={favorites}
                    isPlayerFavorite={isPlayerFavorite}
                    toggleFavorite={toggleFavorite}
                  />
                )}
                
                {/* Talent Analysis Tab */}
                {playgroundTab === 'talent' && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-4 gap-4">
                      {[t.defenders, t.midfielders, t.forwards, t.goalkeepers].map((position, idx) => (
                        <button key={idx} className="bg-gray-800 hover:bg-gray-750 transition-colors p-6 rounded-xl border border-gray-700 text-center">
                          <div className="w-12 h-12 mx-auto mb-3 bg-gray-700 rounded-full flex items-center justify-center">
                            {idx === 0 && <Shield size={20} className="text-blue-400" />}
                            {idx === 1 && <BarChart3 size={20} className="text-green-400" />}
                            {idx === 2 && <Trophy size={20} className="text-purple-400" />}
                            {idx === 3 && <Star size={20} className="text-yellow-400" />}
                          </div>
                          <h3 className="text-lg font-medium">{position}</h3>
                          <div className="mt-2 text-sm text-gray-400">{t.viewTopPlayers}</div>
                          <div className="mt-3 flex justify-center">
                            <ChevronRight size={18} className="text-gray-500" />
                          </div>
                        </button>
                      ))}
                    </div>
                    
                    <TalentAnalysisView 
                      featuredPlayers={featuredPlayers}
                      hiddenGems={hiddenGems}
                      onSelectPlayer={(player, metrics) => {
                        handlePlayerSelected(player, metrics);
                        setCurrentView('player-profile');
                      }}
                      isPlayerFavorite={isPlayerFavorite}
                      toggleFavorite={toggleFavorite}
                    />
                  </div>
                )}
                
                {/* In Sight Tab */}
                {playgroundTab === 'insight' && (
                  <div className="space-y-6">
                    <div className="bg-gray-800 rounded-xl p-6">
                      <h2 className="text-xl font-bold mb-6 flex items-center">
                        <Eye className="mr-2 text-green-500" size={20} />
                        {t.playersInSight}
                      </h2>
                      
                      {favorites.length > 0 ? (
                        <div className="overflow-x-auto">
                          <table className="w-full text-left">
                            <thead>
                              <tr className="border-b border-gray-700">
                                <th className="pb-3 font-medium text-gray-400">{t.name}</th>
                                <th className="pb-3 font-medium text-gray-400">{t.position}</th>
                                <th className="pb-3 font-medium text-gray-400">{t.age || "Age"}</th>
                                <th className="pb-3 font-medium text-gray-400">{t.height || "Height"}</th>
                                <th className="pb-3 font-medium text-gray-400">{t.weight || "Weight"}</th>
                                <th className="pb-3 font-medium text-gray-400">{t.club}</th>
                              </tr>
                            </thead>
                            <tbody>
                              {favorites.map((player) => (
                                <tr 
                                  key={player.id} 
                                  className="border-b border-gray-700 hover:bg-gray-750 cursor-pointer"
                                  onClick={() => {
                                    // Extract metrics from the player object to display in the dashboard
                                    const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => ({
                                      name: key.replace(/_/g, ' ')
                                            .split(' ')
                                            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                                            .join(' '),
                                      value: value,
                                      key: key
                                    }));
                                    
                                    handlePlayerSelected(player, playerMetrics);
                                    setCurrentView('player-profile');
                                  }}
                                >
                                  <td className="py-4">
                                    <div className="flex items-center">
                                      <div className="w-10 h-10 rounded-full bg-gray-700 overflow-hidden mr-3">
                                        <img 
                                          src={player.photoUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=128`}
                                          alt={player.name}
                                          className="w-full h-full object-cover"
                                          onError={(e) => {
                                            e.target.onerror = null; 
                                            e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=128`;
                                          }}
                                        />
                                      </div>
                                      <div className="font-medium">{player.name}</div>
                                    </div>
                                  </td>
                                  <td className="py-4">
                                    {player.positions?.map(pos => {
                                      const posMap = {
                                        'cb': 'Center Back',
                                        'lb': 'Left Back',
                                        'rb': 'Right Back',
                                        'dmf': 'Defensive Mid',
                                        'cmf': 'Central Mid',
                                        'amf': 'Attacking Mid',
                                        'lw': 'Left Wing',
                                        'rw': 'Right Wing',
                                        'cf': 'Center Forward',
                                        'gk': 'Goalkeeper',
                                      };
                                      return posMap[pos] || pos;
                                    }).join(', ')}
                                  </td>
                                  <td className="py-4">{player.age}</td>
                                  <td className="py-4">{player.height || '-'} cm</td>
                                  <td className="py-4">{player.weight || '-'} kg</td>
                                  <td className="py-4">{player.club}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      ) : (
                        <div className="text-center py-8 text-gray-400">
                          <Pin size={48} className="mx-auto mb-4 text-gray-600" />
                          <p className="text-lg">{t.noPlayers}</p>
                          <p className="mt-2">{t.useScoutAI}</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
          
          {/* Configuration view */}
          {currentView === 'configuration' && (
            <div className="flex-1 p-6 bg-gray-900 text-white overflow-auto">
              <h1 className="text-2xl font-bold mb-6">{t.configTitle}</h1>
              <div className="space-y-6">
                <div className="bg-gray-800 rounded-lg p-6">
                  <h2 className="text-xl font-semibold mb-4">{t.languageSettings}</h2>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="flex items-center space-x-2">
                      <input 
                        type="radio" 
                        id="lang-en" 
                        name="language" 
                        value="english"
                        checked={currentLanguage === 'english'} 
                        onChange={() => handleLanguageChange('english')}
                        className="h-4 w-4" 
                      />
                      <label htmlFor="lang-en">English</label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input 
                        type="radio" 
                        id="lang-pt" 
                        name="language" 
                        value="portuguese"
                        checked={currentLanguage === 'portuguese'} 
                        onChange={() => handleLanguageChange('portuguese')}
                        className="h-4 w-4" 
                      />
                      <label htmlFor="lang-pt">Portuguese</label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input 
                        type="radio" 
                        id="lang-es" 
                        name="language" 
                        value="spanish"
                        checked={currentLanguage === 'spanish'} 
                        onChange={() => handleLanguageChange('spanish')}
                        className="h-4 w-4" 
                      />
                      <label htmlFor="lang-es">Spanish</label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input 
                        type="radio" 
                        id="lang-bg" 
                        name="language" 
                        value="bulgarian"
                        checked={currentLanguage === 'bulgarian'} 
                        onChange={() => handleLanguageChange('bulgarian')}
                        className="h-4 w-4" 
                      />
                      <label htmlFor="lang-bg">Bulgarian</label>
                    </div>
                  </div>
                  <div className="mt-4 text-sm text-green-400">
                    {t.languageChangesImmediately}
                  </div>
                </div>
                
                <div className="bg-gray-800 rounded-lg p-6">
                  <h2 className="text-xl font-semibold mb-4">{t.searchPreferences}</h2>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>{t.includeRetired}</span>
                      <div className="relative inline-block w-10 mr-2 align-middle">
                        <input type="checkbox" id="include-retired" className="sr-only" />
                        <label 
                          htmlFor="include-retired" 
                          className="block h-6 w-10 bg-gray-600 rounded-full cursor-pointer transition-colors duration-200 ease-in-out"
                        ></label>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>{t.transferMarket}</span>
                      <div className="relative inline-block w-10 mr-2 align-middle">
                        <input type="checkbox" id="transfer-market" className="sr-only" />
                        <label 
                          htmlFor="transfer-market" 
                          className="block h-6 w-10 bg-gray-600 rounded-full cursor-pointer transition-colors duration-200 ease-in-out"
                        ></label>
                      </div>
                    </div>
                  </div>
                  <button className="mt-4 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-md text-white">
                    Save Search Preferences
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {/* Profile view */}
          {currentView === 'profile' && (
            <div className="flex-1 p-6 bg-gray-900 text-white overflow-auto">
              <h1 className="text-2xl font-bold mb-6">{t.profileTitle}</h1>
              <div className="space-y-6">
                <div className="bg-gray-800 rounded-lg p-6">
                  <div className="flex items-center mb-6">
                    <div className="w-20 h-20 bg-green-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mr-4">
                      {userData?.name?.charAt(0) || 'U'}
                    </div>
                    <div>
                      <h2 className="text-xl font-bold">{userData?.name || 'User'}</h2>
                      <p className="text-gray-400">{userData?.email || 'user@example.com'}</p>
                      <p className="text-gray-500 text-sm mt-1">
                        {userType === 'club' ? t.club : t.player}
                      </p>
                    </div>
                  </div>
                  
                  <div className="space-y-4 mt-6 pt-6 border-t border-gray-700">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm text-gray-400 mb-1">{t.name}</label>
                        <input 
                          type="text" 
                          defaultValue={userData?.name} 
                          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                        />
                      </div>
                      <div>
                        <label className="block text-sm text-gray-400 mb-1">{t.email}</label>
                        <input 
                          type="email" 
                          defaultValue={userData?.email} 
                          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                        />
                      </div>
                    </div>
                    
                    {userType === 'club' && (
                      <div>
                        <label className="block text-sm text-gray-400 mb-1">{t.club}</label>
                        <input 
                          type="text" 
                          defaultValue={userData?.team} 
                          className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                        />
                      </div>
                    )}
                    
                    {userType === 'player' && (
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm text-gray-400 mb-1">{t.currentTeam}</label>
                          <input 
                            type="text" 
                            defaultValue={userData?.team} 
                            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md"
                          />
                        </div>
                        <div>
                          <label className="block text-sm text-gray-400 mb-1">{t.position}</label>
                          <select className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md">
                            <option value="gk" selected={userData?.position === 'gk'}>Goalkeeper</option>
                            <option value="cb" selected={userData?.position === 'cb'}>Center Back</option>
                            <option value="lb" selected={userData?.position === 'lb'}>Left Back</option>
                            <option value="rb" selected={userData?.position === 'rb'}>Right Back</option>
                            <option value="dmf" selected={userData?.position === 'dmf'}>Defensive Midfielder</option>
                            <option value="cmf" selected={userData?.position === 'cmf'}>Central Midfielder</option>
                            <option value="amf" selected={userData?.position === 'amf'}>Attacking Midfielder</option>
                            <option value="lw" selected={userData?.position === 'lw'}>Left Winger</option>
                            <option value="rw" selected={userData?.position === 'rw'}>Right Winger</option>
                            <option value="cf" selected={userData?.position === 'cf'}>Center Forward</option>
                          </select>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="mt-6 flex justify-end">
                    <button className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-md text-white">
                      {t.saveProfile}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Player Complete Profile Page */}
          {currentView === 'player-profile' && selectedPlayer && (
            <div className="flex-1 flex overflow-hidden">
              <PlayerCompletePage 
                player={selectedPlayer}
                onClose={() => setCurrentView('scout')}
                isPlayerFavorite={isPlayerFavorite(selectedPlayer)}
                toggleFavorite={() => toggleFavorite(selectedPlayer)}
              />
            </div>
          )}
        </div>
      </div>
    );
  };

  return renderContent();
}

// Chat Interface Component with history and language support
const ChatInterface = ({ onPlayerSelected, expanded, chatHistory = [], addChatToHistory, userData = {}, isAuthenticated = false }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showNewChatButton, setShowNewChatButton] = useState(true);
  const [currentChatTitle, setCurrentChatTitle] = useState('');
  const [showHistory, setShowHistory] = useState(false);

  // State to keep track of the session
  const [sessionId, setSessionId] = useState(() => {
    const savedSessionId = localStorage.getItem('chatSessionId');
    return savedSessionId || `session-${Date.now()}`;
  });
  const [lastMessageWasSatisfactionQuestion, setLastMessageWasSatisfactionQuestion] = useState(false);
  
  // Listen for the load-chat and new-chat events
  useEffect(() => {
    const handleLoadChat = (event) => {
      setSessionId(event.detail.chatId);
      setCurrentChatTitle(event.detail.title);
      // We would load previous messages here if we had them stored
      setMessages([]);
    };
    
    const handleNewChat = () => {
      const newSessionId = localStorage.getItem('chatSessionId');
      setSessionId(newSessionId);
      setCurrentChatTitle('');
      setMessages([]);
    };
    
    document.addEventListener('load-chat', handleLoadChat);
    document.addEventListener('new-chat', handleNewChat);
    
    return () => {
      document.removeEventListener('load-chat', handleLoadChat);
      document.removeEventListener('new-chat', handleNewChat);
    };
  }, []);
  
  // Get user's language preference from app state
  const userLanguage = localStorage.getItem('language') || userData?.language || 'english';
  
  // Language-specific text
  const translations = {
    english: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Your intelligent scouting assistant",
      chatHistoryButton: "Chat History",
      closeHistoryButton: "Close History",
      historyTitle: "Chat History", 
      noHistoryFound: "No previous conversations found",
      previousConversations: "previous conversations",
      viewAll: "View all",
      clearHistory: "Clear",
      confirmClearHistory: "Are you sure you want to clear all chat history?",
      exportNotAvailable: "Full chat history export is coming soon!",
      welcomeTitle: "Hello, Coach!",
      welcomeMessage: "Describe the type of player you're looking for, and I'll find the best options for your team.",
      examplesTitle: "Search examples:",
      example1: "I need an offensive full-back with good crossing ability",
      example2: "Looking for center backs strong in aerial duels with good ball distribution",
      example3: "I want a young striker with good finishing and under 23 years old",
      playersFoundText: "Players found - Select to see details:",
      analyzing: "Analyzing players...",
      showingDetails: "Showing details of ",
      inputPlaceholder: "Describe the type of player you're looking for...",
      newChat: "New Chat"
    },
    portuguese: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Seu assistente de scouting inteligente",
      chatHistoryButton: "Histórico de Chats",
      closeHistoryButton: "Fechar Histórico",
      historyTitle: "Histórico de Conversas",
      noHistoryFound: "Nenhuma conversa anterior encontrada",
      previousConversations: "conversas anteriores",
      viewAll: "Ver todas",
      clearHistory: "Limpar",
      confirmClearHistory: "Tem certeza que deseja limpar todo o histórico de conversas?",
      exportNotAvailable: "Exportação completa do histórico estará disponível em breve!",
      welcomeTitle: "Olá, Técnico!",
      welcomeMessage: "Descreva o tipo de jogador que você está buscando, e eu encontrarei as melhores opções para sua equipe.",
      examplesTitle: "Exemplos de busca:",
      example1: "Preciso de um lateral ofensivo com boa capacidade de cruzamento",
      example2: "Busco zagueiros fortes no jogo aéreo e com boa saída de bola",
      example3: "Quero um atacante jovem com boa finalização e menos de 23 anos",
      playersFoundText: "Jogadores encontrados - Selecione para ver detalhes:",
      analyzing: "Analisando jogadores...",
      showingDetails: "Mostrando detalhes de ",
      inputPlaceholder: "Descreva o tipo de jogador que você procura...",
      newChat: "Nova Conversa"
    },
    spanish: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Tu asistente de scouting inteligente",
      chatHistoryButton: "Historial de Chats",
      closeHistoryButton: "Cerrar Historial",
      historyTitle: "Historial de Conversaciones",
      noHistoryFound: "No se encontraron conversaciones previas",
      previousConversations: "conversaciones anteriores",
      viewAll: "Ver todas",
      clearHistory: "Borrar",
      confirmClearHistory: "¿Estás seguro de que deseas borrar todo el historial de conversaciones?",
      exportNotAvailable: "¡La exportación completa del historial estará disponible pronto!",
      welcomeTitle: "¡Hola, Entrenador!",
      welcomeMessage: "Describe el tipo de jugador que estás buscando, y encontraré las mejores opciones para tu equipo.",
      examplesTitle: "Ejemplos de búsqueda:",
      example1: "Necesito un lateral ofensivo con buena capacidad de centro",
      example2: "Busco defensores centrales fuertes en duelos aéreos y con buena salida de balón",
      example3: "Quiero un delantero joven con buen definición y menos de 23 años",
      playersFoundText: "Jugadores encontrados - Selecciona para ver detalles:",
      analyzing: "Analizando jugadores...",
      showingDetails: "Mostrando detalles de ",
      inputPlaceholder: "Describe el tipo de jugador que estás buscando...",
      newChat: "Nueva Conversación"
    },
    bulgarian: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Вашият интелигентен скаутинг асистент",
      chatHistoryButton: "История на чатовете",
      closeHistoryButton: "Затвори историята",
      historyTitle: "История на разговорите",
      noHistoryFound: "Няма намерени предишни разговори",
      previousConversations: "предишни разговори",
      viewAll: "Вижте всички",
      clearHistory: "Изчисти",
      confirmClearHistory: "Сигурни ли сте, че искате да изчистите цялата история на разговорите?",
      exportNotAvailable: "Пълният експорт на историята ще бъде наличен скоро!",
      welcomeTitle: "Здравейте, Треньор!",
      welcomeMessage: "Опишете типа играч, който търсите, и ще намеря най-добрите опции за вашия отбор.",
      examplesTitle: "Примери за търсене:",
      example1: "Нужен ми е офанзивен бек с добра способност за центриране",
      example2: "Търся централни защитници, силни във въздушните дуели и с добро разпределяне на топката",
      example3: "Искам млад нападател с добро завършване и под 23 години",
      playersFoundText: "Намерени играчи - Изберете, за да видите детайли:",
      analyzing: "Анализиране на играчи...",
      showingDetails: "Показване на детайли за ",
      inputPlaceholder: "Опишете типа играч, който търсите...",
      newChat: "Нов разговор"
    }
  };
  
  // Get translations for the current language with fallback to English
  const t = translations[userLanguage] || translations.english;

  // Store session ID in localStorage when it changes
  React.useEffect(() => {
    localStorage.setItem('chatSessionId', sessionId);
  }, [sessionId]);
  
  // Function to start a new chat
  const startNewChat = async () => {
    setMessages([]);
    setInput('');
    const newSessionId = `session-${Date.now()}`;
    setSessionId(newSessionId);
    setLastMessageWasSatisfactionQuestion(false);
    
    // If user is authenticated, create a new chat session in Supabase
    if (userData?.id && isAuthenticated) {
      try {
        // Create new chat session in Supabase
        const sessionData = await createChatSession(
          "New chat", 
          userLanguage, 
          newSessionId // Pass external ID to link with local storage
        );
        
        console.log("Created new Supabase chat session:", sessionData);
      } catch (error) {
        console.error("Error creating new chat session in Supabase:", error);
        // Continue anyway with local session
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    setIsLoading(true);
      
    // If this is the first message in a new chat, add it to the chat history
    if (messages.length === 0) {
      addChatToHistory(sessionId, input);
    }
    
    // Check if we're responding to a satisfaction question
    const isSatisfactionResponse = lastMessageWasSatisfactionQuestion && 
      (input.toLowerCase().includes('não') || 
       input.toLowerCase().includes('refinar') || 
       input.toLowerCase().includes('outros') ||
       input.toLowerCase().includes('no') || 
       input.toLowerCase().includes('more') ||
       input.toLowerCase().includes('other') ||
       input.toLowerCase().includes('different') ||
       input.toLowerCase().includes('не') ||
       input.toLowerCase().includes('други'));
       
    // Add user's message to chat
    setMessages(prev => [...prev, { text: input, sender: 'user' }]);
    
    // Variables for tracking Supabase integration
    let supabaseSessionId = null;
    let authToken = null;
    
    // Get the Supabase session if user is authenticated
    if (isAuthenticated && userData?.id) {
      try {
        // Get the current Supabase auth session
        const { data: authData } = await supabase.auth.getSession();
        if (authData?.session?.access_token) {
          authToken = authData.session.access_token;
        }
        
        // Check if chat session exists in Supabase
        const { data: sessionData, error: sessionError } = await supabase
          .from('chat_sessions')
          .select('id')
          .eq('external_id', sessionId)
          .single();
          
        // Get Supabase session ID (needed for adding messages)
        if (sessionData?.id) {
          supabaseSessionId = sessionData.id;
        } else if (sessionError && sessionError.code === 'PGRST116') {
          // Session not found, create new one
          const newSession = await createChatSession(
            messages.length === 0 ? input : "Chat session", 
            userLanguage,
            sessionId
          );
          if (newSession?.id) {
            supabaseSessionId = newSession.id;
          }
        } else if (sessionError) {
          console.error("Error checking for chat session:", sessionError);
        }
        
        // Add message to Supabase chat messages
        if (supabaseSessionId) {
          await addChatMessage(supabaseSessionId, 'user', input);
        }
      } catch (error) {
        console.error("Error with Supabase before API call:", error);
        // Continue with the API call even if Supabase fails
      }
    }

    // Prepare the request body
    const requestBody = {
      session_id: sessionId,
      query: input,
      is_follow_up: messages.length > 0,
      satisfaction: isSatisfactionResponse ? false : null,
      language: localStorage.getItem('language') || userLanguage,  // Send the current language preference
      user_id: userData?.id || null, // Send user ID if available
      supabase_session_id: supabaseSessionId // Send Supabase session ID if available
    };

    // Prepare headers
    const headers = {
      'Content-Type': 'application/json',
    };
    
    // Add authorization if we have a token
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    try {
      // Use the correct backend API URL
      const apiUrl = 'http://localhost:5001/enhanced_search';
      console.log("Sending search request to:", apiUrl, requestBody);
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      console.log("Search response:", data); // Add logging to debug
      
      // If we get a Supabase session ID back, store it
      if (data.supabase_session_id) {
        supabaseSessionId = data.supabase_session_id;
      }
      
      if (data.success) {
        // Use the players data directly from the response if available
        let playersData = data.players || [];
        
        // Format player data if needed
        if (playersData.length > 0) {
          // Ensure each player has the required fields
          playersData = playersData.map(player => ({
            id: player.wyId || player.id || player.name,
            name: player.name || "Unknown Player",
            age: player.age || "?",
            club: player.club || "Unknown Club",
            positions: player.positions || ["cf"],
            stats: player.stats || {},
            score: player.score || 0
          }));
        }

        // Check if the response contains a satisfaction question (in multiple languages)
        const hasSatisfactionQuestion = 
          data.response.toLowerCase().includes('satisfeito') || 
          data.response.toLowerCase().includes('satisfied') ||
          data.response.toLowerCase().includes('refinar sua busca') ||
          data.response.toLowerCase().includes('refine your search') ||
          data.response.toLowerCase().includes('satisfecho') ||
          data.response.toLowerCase().includes('доволни');
        
        setLastMessageWasSatisfactionQuestion(hasSatisfactionQuestion);

        // Add the response to the chat
        setMessages(prev => [...prev, {
          text: data.response,
          sender: 'bot',
          showPlayerSelection: playersData.length > 0,
          players: playersData
        }]);
        
        // If the backend didn't handle Supabase integration, try to handle it here
        if (!data.supabase_session_id && isAuthenticated && userData?.id && supabaseSessionId) {
          try {
            // Add assistant message to Supabase
            await addChatMessage(supabaseSessionId, 'assistant', data.response);
            
            // If we have search results, save them to Supabase
            if (playersData.length > 0 && data.parameters) {
              try {
                // First save search parameters
                const searchParams = {
                  key_description_word: data.parameters?.key_description_word || input,
                  position_codes: data.parameters?.position_codes || [],
                  ...data.parameters
                };
                
                const savedParams = await saveSearchParameters(supabaseSessionId, searchParams);
                
                // Then save search results
                if (savedParams) {
                  await saveSearchResults(supabaseSessionId, savedParams.id, playersData);
                }
              } catch (resultError) {
                console.error("Error saving search results to Supabase:", resultError);
              }
            }
          } catch (error) {
            console.error("Error saving assistant response to Supabase:", error);
          }
        }
      } else {
        // Show error message
        const errorMsg = data.message || data.error || 'An error occurred while processing your search.';
        setMessages(prev => [...prev, { 
          text: errorMsg,
          sender: 'bot' 
        }]);
        
        // Save error message to Supabase if authenticated
        if (isAuthenticated && userData?.id && supabaseSessionId) {
          try {
            await addChatMessage(supabaseSessionId, 'assistant', errorMsg);
          } catch (error) {
            console.error("Error saving error message to Supabase:", error);
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMsg = 'Sorry, an error occurred while processing your search. Please try again.';
      
      setMessages(prev => [...prev, {
        text: errorMsg,
        sender: 'bot'
      }]);
      
      // Save error message to Supabase if authenticated
      if (isAuthenticated && userData?.id && supabaseSessionId) {
        try {
          await addChatMessage(supabaseSessionId, 'assistant', errorMsg);
        } catch (supabaseError) {
          console.error("Error saving error message to Supabase:", supabaseError);
        }
      }
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };

  const handlePlayerSelect = (player) => {
    // Ensure player has all required fields
    const enhancedPlayer = {
      ...player,
      id: player.id || player.wyId || player.name || "unknown",
      name: player.name || "Unknown Player",
      age: player.age || "?",
      club: player.club || "Unknown Club",
      positions: Array.isArray(player.positions) ? player.positions : ["cf"],
      stats: player.stats || {},
      score: player.score || 80
    };

    // Extract metrics from the player object to display in the dashboard
    const playerMetrics = Object.entries(enhancedPlayer.stats || {}).map(([key, value]) => ({
      name: formatMetricName(key),
      value: value,
      key: key
    }));

    setMessages(prev => [...prev, {
      text: `${t.showingDetails}${enhancedPlayer.name}...`,
      sender: 'bot'
    }]);
    
    // Call the parent component's callback to show the player dashboard
    onPlayerSelected(enhancedPlayer, playerMetrics);
  };

  // Helper function to format metric names for display
  const formatMetricName = (key) => {
    return key
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };
  
  // Helper function to format player names with proper spacing
  const formatPlayerName = (name) => {
    if (!name) return '';
    // Add spaces between capital letters if they're not already spaced
    return name.replace(/([A-Z])/g, ' $1').trim()
      // Replace multiple spaces with a single space
      .replace(/\s+/g, ' ')
      // Make sure first letter of each word is capitalized
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 border-r border-gray-700 overflow-hidden">
      {/* Header with soccer theme */}
      <div className="bg-gradient-to-r from-green-900 to-blue-900 p-4 flex items-center justify-between border-b border-gray-700 relative overflow-hidden">
        {/* Soccer field pattern in the background */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[30%] h-[120%] border-2 border-white rounded-full"></div>
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-0.5 h-full bg-white"></div>
        </div>
        
        <div className="flex items-center">
          <div className="w-10 h-10 mr-3 flex items-center justify-center bg-white rounded-full shadow-lg">
            <span className="text-green-700 text-2xl">⚽</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">{t.headerTitle}</h1>
            <p className="text-xs text-green-200 opacity-80">{t.headerSubtitle}</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {/* New chat button */}
          {showNewChatButton && (
            <button
              onClick={startNewChat}
              className="p-2 rounded-lg bg-green-600 bg-opacity-60 hover:bg-opacity-80 text-white flex items-center space-x-1"
              title={t.newChat}
            >
              <span className="text-sm whitespace-nowrap">{t.newChat}</span>
            </button>
          )}
          
          {/* Toggle chat history button */}
          <button 
            onClick={() => setShowHistory(!showHistory)}
            className="p-2 rounded-lg bg-green-800 bg-opacity-60 hover:bg-opacity-80 text-white flex items-center space-x-1"
            title={showHistory ? t.closeHistoryButton : t.chatHistoryButton}
          >
            {showHistory ? (
              <>
                <X size={16} />
                <span className="text-sm hidden md:inline-block">{t.closeHistoryButton}</span>
              </>
            ) : (
              <>
                <Clock size={16} />
                <span className="text-sm hidden md:inline-block">{t.chatHistoryButton}</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Chat History Drawer - Only visible when showHistory is true */}
      {showHistory && (
        <div className="border-b border-gray-700 bg-gray-800 overflow-hidden">
          <div className="px-4 py-3 bg-gray-800 border-b border-gray-700">
            <h3 className="text-lg font-medium text-white flex items-center">
              <Clock className="mr-2 text-green-400" size={18} />
              {t.historyTitle}
            </h3>
          </div>
          
          <div className="overflow-y-auto max-h-[300px] p-2 space-y-2 custom-scrollbar">
            {chatHistory.length === 0 ? (
              <div className="text-center p-6 text-gray-400">
                {t.noHistoryFound}
              </div>
            ) : (
              chatHistory.map((chat, index) => (
                <button 
                  key={chat.id || index}
                  onClick={() => {
                    // Force a reload of the chat interface
                    const event = new CustomEvent('load-chat', { 
                      detail: { chatId: chat.id, title: chat.title } 
                    });
                    document.dispatchEvent(event);
                    // Close the history panel
                    setShowHistory(false);
                  }}
                  className="w-full text-left p-3 rounded-lg bg-gray-750 hover:bg-gray-700 transition-colors border border-gray-700 hover:border-green-600 flex flex-col"
                >
                  <div className="flex justify-between items-center">
                    <h4 className="font-medium text-white flex items-center">
                      <MessageSquare size={14} className="mr-2 text-green-400" />
                      {chat.title}
                    </h4>
                    <span className="text-xs text-gray-400 bg-gray-700 px-2 py-1 rounded">
                      {new Date(chat.date).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-300 mt-2 truncate border-t border-gray-700 pt-2">{chat.snippet}</p>
                </button>
              ))
            )}
          </div>
          
          <div className="p-3 border-t border-gray-700 flex justify-between items-center">
            <span className="text-sm text-gray-400">{chatHistory.length} {t.previousConversations}</span>
            <div className="flex space-x-2">
              <button 
                onClick={() => {
                  if (window.confirm(t.confirmClearHistory || "Are you sure you want to clear all chat history?")) {
                    addChatToHistory("empty", ""); // Just a placeholder
                    setMessages([]);
                    localStorage.removeItem('chatHistory');
                    // Force reload of chat history by creating a temporary event
                    const event = new CustomEvent('history-cleared');
                    document.dispatchEvent(event);
                  }
                }}
                className="text-sm text-red-400 hover:text-red-300 bg-gray-750 px-2 py-1 rounded"
              >
                {t.clearHistory || "Clear"}
              </button>
              <button 
                onClick={() => {
                  // Future functionality could export all chats or show in a larger dialog
                  alert(t.exportNotAvailable || "Full chat history export is coming soon!");
                }}
                className="text-sm text-green-400 hover:text-green-300 bg-gray-750 px-2 py-1 rounded"
              >
                {t.viewAll}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900 bg-opacity-90 relative custom-scrollbar">
        {/* Soccer field background pattern */}
        <div className="absolute inset-0 opacity-5 pointer-events-none">
          <div className="w-full h-full border-2 border-white"></div>
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-white"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 border-2 border-white rounded-full"></div>
        </div>
        
        {messages.length === 0 && (
          <div className="text-center py-10 relative z-10">
            <div className="w-20 h-20 mx-auto mb-4 flex items-center justify-center bg-gradient-to-r from-green-600 to-green-700 rounded-full shadow-lg">
              <span className="text-white text-4xl">⚽</span>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">{t.welcomeTitle}</h2>
            <p className="text-gray-300 mb-6 max-w-md mx-auto">{t.welcomeMessage}</p>
            
            <div className="bg-gray-800 rounded-lg p-5 mx-auto max-w-md text-left border-l-4 border-green-500">
              <p className="text-white mb-3 font-medium">{t.examplesTitle}</p>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">1</span>
                  <span>"{t.example1}"</span>
                </li>
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">2</span>
                  <span>"{t.example2}"</span>
                </li>
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">3</span>
                  <span>"{t.example3}"</span>
                </li>
              </ul>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} 
               className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {/* User Avatar (only shown for bot messages) */}
            {message.sender === 'bot' && (
              <div className="w-8 h-8 rounded-full bg-green-700 flex items-center justify-center text-white mr-2 flex-shrink-0 self-start mt-1">
                ⚽
              </div>
            )}
            
            {/* Message bubble */}
            <div className={`rounded-lg p-4 max-w-[80%] shadow-md ${
              message.sender === 'user' 
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-tr-none' 
                : 'bg-gradient-to-r from-gray-800 to-gray-900 text-gray-100 rounded-tl-none'
            }`}>
              <div className="whitespace-pre-wrap">{message.text}</div>
              
              {/* Player Selection Cards */}
              {message.showPlayerSelection && message.players && message.players.length > 0 && (
                <div className="mt-4 space-y-3">
                  <div className="text-sm text-gray-200 font-medium border-b border-gray-700 pb-2 mb-3">
                    {t.playersFoundText}
                  </div>
                  <div className="grid grid-cols-1 gap-3">
                    {message.players.map((player, idx) => (
                      <button
                        key={idx}
                        onClick={() => handlePlayerSelect(player)}
                        className="text-left p-3 rounded bg-gray-700 bg-opacity-50 hover:bg-gray-600 transition-colors flex items-center border border-gray-600 hover:border-green-500"
                      >
                        {/* Player simple avatar */}
                        <div className="w-10 h-10 bg-blue-900 rounded-full flex items-center justify-center text-white text-xs font-bold mr-3">
                          {player.positions && Array.isArray(player.positions) && player.positions.length > 0 
                            ? player.positions[0].toUpperCase() 
                            : 'ST'}
                        </div>
                        
                        <div className="flex-1">
                          <div className="font-medium text-white">{formatPlayerName(player.name || "Unknown Player")}</div>
                          <div className="text-xs text-gray-300 flex items-center">
                            <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-1"></span>
                            {player.positions && Array.isArray(player.positions) 
                              ? player.positions.join(', ') 
                              : 'N/A'} • {player.age || '?'} anos • {player.club || 'Clube desconhecido'}
                          </div>
                        </div>
                        
                        {/* Score indicator */}
                        <div className="ml-2 w-9 h-9 flex-shrink-0 rounded-full bg-gradient-to-b from-blue-500 to-blue-700 flex items-center justify-center text-white font-bold text-sm">
                          {player.score ? Math.round(player.score) : '??'}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            {/* User Avatar (only shown for user messages) */}
            {message.sender === 'user' && (
              <div className="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center text-white ml-2 flex-shrink-0 self-start mt-1">
                👤
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="w-8 h-8 rounded-full bg-green-700 flex items-center justify-center text-white mr-2 flex-shrink-0 self-start mt-1">
              ⚽
            </div>
            <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-gray-100 rounded-lg rounded-tl-none p-4 shadow-md">
              <div className="flex items-center space-x-3">
                {/* Simple rotating soccer ball */}
                <div className="w-8 h-8 flex items-center justify-center animate-spin" 
                     style={{animationDuration: '1.5s'}}>
                  <span className="text-xl">⚽</span>
                </div>
                
                <div className="text-green-300 font-medium">{t.analyzing}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t border-gray-700 p-4 bg-gray-900">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t.inputPlaceholder}
            disabled={isLoading}
            className="flex-1 rounded-lg bg-gray-800 text-white p-3 border border-gray-700 focus:outline-none focus:border-green-500 shadow-inner"
          />
          <button 
            type="submit"
            disabled={isLoading}
            className={`text-white rounded-lg px-4 py-3 focus:outline-none flex items-center justify-center shadow-md ${
              isLoading ? 'bg-gray-600' : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'
            }`}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};

// Player Dashboard Component with improved design, player photo, radar chart, and favorites
const PlayerDashboard = ({ player, metrics, onClose, isPlayerFavorite, toggleFavorite, userType, onViewComplete }) => {
  // Helper function to get a color based on metric value
  const getMetricColor = (metric) => {
    // Placeholder logic - in a real app this would be based on comparison with league averages
    const value = parseFloat(metric.value);
    if (isNaN(value)) return 'text-gray-400';
    
    // Different metrics have different scales
    if (metric.key.includes('percent')) {
      if (value > 80) return 'text-green-500';
      if (value > 60) return 'text-yellow-500';
      return 'text-red-500';
    }
    
    // Default scale for other metrics
    if (value > 7) return 'text-green-500';
    if (value > 4) return 'text-yellow-500';
    return 'text-red-500';
  };

  // Helper function to format player names with proper spacing
  const formatPlayerName = (name) => {
    if (!name) return '';
    // Add spaces between capital letters if they're not already spaced
    return name.replace(/([A-Z])/g, ' $1').trim()
      // Replace multiple spaces with a single space
      .replace(/\s+/g, ' ')
      // Make sure first letter of each word is capitalized
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // Get player position in a more readable format
  const positionDisplay = player.positions?.map(pos => {
    const posMap = {
      'cb': 'Zagueiro',
      'lb': 'Lateral Esquerdo',
      'rb': 'Lateral Direito',
      'dmf': 'Volante',
      'cmf': 'Meio-Campo',
      'amf': 'Meia Atacante',
      'lw': 'Ponta Esquerda',
      'rw': 'Ponta Direita',
      'cf': 'Centroavante',
      'gk': 'Goleiro',
      // Add other positions as needed
    };
    return posMap[pos] || pos;
  }).join(', ');

  // Prepare ALL metrics for a single comprehensive radar chart
  const prepareAllRadarData = (allMetrics, maxMetrics = 15) => {
    if (!allMetrics || allMetrics.length === 0) return [];
    
    // Filter out metrics with no values or invalid values
    const validMetrics = allMetrics.filter(m => m.value !== undefined && m.value !== null);
    
    // Sort by importance (could implement more sophisticated sorting)
    // For now, prioritize key metrics like goals, assists, passes, etc.
    const keyMetricOrder = [
      'goals', 'assists', 'shots_on_target', 'pass_accuracy', 'key_passes',
      'interceptions', 'defensive_duels_won', 'successful_dribbles',
      'progressive_runs', 'aerial_duels_won'
    ];
    
    // Sort metrics by putting key metrics first, then alphabetically
    const sortedMetrics = [...validMetrics].sort((a, b) => {
      const aIndex = keyMetricOrder.indexOf(a.key);
      const bIndex = keyMetricOrder.indexOf(b.key);
      
      if (aIndex !== -1 && bIndex !== -1) return aIndex - bIndex;
      if (aIndex !== -1) return -1;
      if (bIndex !== -1) return 1;
      
      return a.name.localeCompare(b.name);
    });
    
    // Take top N metrics for the radar chart
    const selectedMetrics = sortedMetrics.slice(0, maxMetrics);
    
    // Normalize the values for the radar chart
    const normalizedMetrics = selectedMetrics.map(metric => {
      const value = parseFloat(metric.value);
      
      // If value is NaN, return a placeholder
      if (isNaN(value)) {
        return {
          name: metric.name,
          value: 0,
          fullMark: 100,
          originalValue: 'N/A',
          metricKey: metric.key
        };
      }
      
      // Scale value between 0-100 based on metric type
      let scaledValue = value;
      let fullMark = 100;
      
      // Percentage metrics are already 0-100
      if (metric.key.includes('percent')) {
        scaledValue = value;
      } 
      // For metrics that are typically small numbers (0-10)
      else if (value < 20) {
        scaledValue = value * 10;
      }
      // For metrics that are typically larger numbers
      else {
        scaledValue = Math.min(value, 100);
      }
      
      return {
        name: metric.name.length > 10 ? metric.name.substring(0, 10) + '...' : metric.name,
        value: scaledValue,
        fullMark: fullMark,
        originalValue: value.toFixed(2),
        metricKey: metric.key
      };
    });
    
    return normalizedMetrics;
  };

  // Custom function to render a comprehensive radar chart with all metrics
  const renderComprehensiveRadarChart = () => {
    const data = prepareAllRadarData(metrics);
    
    if (data.length === 0) {
      return (
        <div className="flex items-center justify-center h-96 bg-gray-800 rounded-xl">
          <p className="text-gray-400 text-center p-8">
            {t.noMetrics}
          </p>
        </div>
      );
    }
    
    // Fixed height container instead of aspect ratio to prevent layout bugs
    return (
      <div className="w-full h-[450px]">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart 
            cx="50%" 
            cy="50%" 
            outerRadius="65%" 
            data={data}
          >
            <PolarGrid strokeDasharray="3 3" stroke="#4B5563" />
            <PolarAngleAxis 
              dataKey="name" 
              tick={{ fill: '#E5E7EB', fontSize: 12 }}
              stroke="#6B7280"
            />
            <PolarRadiusAxis 
              angle={30} 
              domain={[0, 100]} 
              tick={{ fill: '#9CA3AF' }}
              stroke="#4B5563"
              axisLine={false}
            />
            <Radar
              name={formatPlayerName(player.name)}
              dataKey="value"
              stroke="#10B981"
              fill="#10B981"
              fillOpacity={0.6}
            />
            <Tooltip 
              formatter={(value, name, props) => {
                try {
                  // Safe access to originalValue
                  const originalValue = props?.payload?.originalValue || value;
                  return [originalValue, name];
                } catch (e) {
                  return [value, name];
                }
              }}
              contentStyle={{ 
                backgroundColor: '#1F2937', 
                borderColor: '#374151', 
                color: '#F9FAFB',
                borderRadius: '0.375rem',
                padding: '8px 12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
              }} 
              labelStyle={{ fontWeight: 'bold', marginBottom: '6px' }}
            />
            <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px' }} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  // Player photo URL - use a placeholder if not available
  const getPlayerImageUrl = (player) => {
    // First try photoUrl if it exists
    if (player.photoUrl) {
      return player.photoUrl;
    }
    
    // Try to use player ID for the image
    const playerId = player.wyId || player.id;
    if (playerId) {
      // Always use the player ID for the image request to match backend expectations
      return `http://localhost:5001/player-image/${playerId}`;
    }
    
    // Fallback to UI Avatars API
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
  };
  
  const playerPhotoUrl = getPlayerImageUrl(player);

  // Translation for player dashboard
  const getDashboardTranslation = () => {
    const lang = localStorage.getItem('language') || 'english';
    const translations = {
      english: {
        title: "Player Dashboard",
        currentClub: "Current club",
        contractUntil: "Contract until",
        rating: "Rating",
        noMetrics: "No metrics available for this player. Try selecting another player with more statistical data.",
        viewFullProfile: "View Full Profile",
        addToFavorites: "Add to favorites",
        removeFromFavorites: "Remove from favorites",
        close: "Close"
      },
      portuguese: {
        title: "Dashboard do Jogador",
        currentClub: "Clube atual",
        contractUntil: "Contrato até",
        rating: "Pontuação",
        noMetrics: "Sem métricas disponíveis para este jogador. Tente selecionar outro jogador com mais dados estatísticos.",
        viewFullProfile: "Ver Perfil Completo",
        addToFavorites: "Adicionar aos favoritos",
        removeFromFavorites: "Remover dos favoritos",
        close: "Fechar"
      },
      spanish: {
        title: "Panel del Jugador",
        currentClub: "Club actual",
        contractUntil: "Contrato hasta",
        rating: "Puntuación",
        noMetrics: "No hay métricas disponibles para este jugador. Intenta seleccionar otro jugador con más datos estadísticos.",
        viewFullProfile: "Ver Perfil Completo",
        addToFavorites: "Añadir a favoritos",
        removeFromFavorites: "Quitar de favoritos",
        close: "Cerrar"
      },
      bulgarian: {
        title: "Табло на играча",
        currentClub: "Настоящ клуб",
        contractUntil: "Договор до",
        rating: "Рейтинг",
        noMetrics: "Няма налични показатели за този играч. Опитайте да изберете друг играч с повече статистически данни.",
        viewFullProfile: "Вижте пълния профил",
        addToFavorites: "Добави в любими",
        removeFromFavorites: "Премахни от любими",
        close: "Затвори"
      }
    };
    return translations[lang] || translations.english;
  };

  // Get translations
  const t = getDashboardTranslation();

  return (
    <div className="w-full bg-gray-950 flex flex-col overflow-hidden">
      {/* Header with actions */}
      <div className="bg-gray-800 p-4 flex justify-between items-center border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <div className="w-8 h-8 mr-3 text-green-500 font-bold">⚽</div>
          {t.title}
        </h2>
      </div>

      {/* Player Overview Card */}
      <div className="p-6 overflow-y-auto custom-scrollbar">
        <div className="bg-gradient-to-r from-green-900 to-blue-900 rounded-xl mb-6 text-white shadow-lg overflow-hidden relative">
          {/* Soccer field background pattern - lower z-index */}
          <div className="absolute inset-0 opacity-10" style={{ zIndex: 0 }}>
            <div className="w-full h-full border border-white"></div>
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[60%] h-[70%] border border-white rounded-full"></div>
            <div className="absolute left-1/2 -translate-x-1/2 w-0.5 h-full bg-white opacity-50"></div>
            <div className="absolute top-[85%] left-[50%] -translate-x-1/2 w-[15%] h-[30%] border border-white rounded-t-full"></div>
            <div className="absolute top-0 left-[50%] -translate-x-1/2 w-[15%] h-[30%] border border-white rounded-b-full"></div>
          </div>
          
          {/* Player card */}
          <div className="relative h-full">
            {/* Photo background area (left side) */}
            <div className="absolute left-0 top-0 bottom-0 w-1/3 bg-gradient-to-r from-black to-transparent opacity-50"></div>
            
            {/* Content wrapper */}
            <div className="relative flex p-6">
              {/* Player Photo - Larger and more prominent */}
              <div className="mr-6">
                <div className="w-36 h-44 overflow-hidden rounded-lg border-4 border-white bg-gray-800 shadow-xl relative">
                  <img 
                    src={playerPhotoUrl} 
                    alt={player.name} 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.onerror = null; 
                      e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                    }}
                  />
                  
                  {/* Position badge */}
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-2 text-center">
                    <div className="text-xs font-bold">{positionDisplay}</div>
                  </div>
                  
                  {/* Position badge at bottom right */}
                  <div className="absolute -bottom-4 -right-4">
                    <div className="w-16 h-16 flex items-center justify-center bg-gradient-to-b from-blue-500 to-blue-700 rounded-full shadow-lg border-2 border-white">
                      <span className="text-2xl font-bold text-white">{player.positions?.[0]?.toUpperCase() || 'ST'}</span>
                    </div>
                  </div>
                  
                  {/* Favorite indicator */}
                  {isPlayerFavorite && (
                    <div className="absolute top-2 right-2">
                      <div className="w-8 h-8 rounded-full bg-red-600 flex items-center justify-center shadow-lg">
                        <Heart size={16} fill="white" />
                      </div>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Player info */}
              <div className="flex-1">
                <div className="flex items-center">
                  <div className="mr-3 p-1 bg-white bg-opacity-20 rounded">
                    <img 
                      src={`https://ui-avatars.com/api/?name=${encodeURIComponent(player.club?.substring(0,2) || 'FC')}&background=111827&color=fff&size=20&font-size=0.5&bold=true`}
                      alt="Club"
                      className="w-6 h-6 rounded-full"
                    />
                  </div>
                  <h1 className="text-3xl font-bold">{formatPlayerName(player.name)}</h1>
                </div>
                
                <div className="flex items-center mt-2 mb-4">
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.age} anos</span>
                  </div>
                  <div className="h-4 border-r border-white border-opacity-30 mx-3"></div>
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.height || '--'} cm</span>
                  </div>
                  <div className="h-4 border-r border-white border-opacity-30 mx-3"></div>
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.weight || '--'} kg</span>
                  </div>
                </div>
                
                {/* Contract info in a modern card */}
                <div className="bg-black bg-opacity-30 backdrop-blur-sm rounded-lg p-4 mt-2 border border-white border-opacity-20">
                  <h3 className="text-sm uppercase text-green-300 mb-3 flex items-center">
                    <Trophy className="mr-2" size={14} />
                    {t.title}
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="flex items-center">
                        <Package className="mr-2 text-blue-300" size={14} />
                        <span className="text-sm text-gray-300">{t.currentClub}</span>
                      </div>
                      <div className="font-medium">{player.club || "Unknown"}</div>
                    </div>
                    <div>
                      <div className="flex items-center">
                        <Calendar className="mr-2 text-blue-300" size={14} />
                        <span className="text-sm text-gray-300">{t.contractUntil}</span>
                      </div>
                      <div className="font-medium">{player.contractUntil || "Unknown"}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Comprehensive Radar Chart Section */}
        <div className="bg-gray-800 rounded-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-white mb-5 flex items-center border-b border-gray-700 pb-3">
            <BarChart3 className="mr-3 text-green-500" size={24} />
            Radar de Performance
          </h2>
          
          {/* Main radar chart with all metrics */}
          {renderComprehensiveRadarChart()}
          
          <div className="mt-5 text-gray-400 text-sm border-t border-gray-700 pt-3">
            <p>O radar mostra os valores normalizados das métricas do jogador. Passe o mouse sobre as métricas para ver os valores originais.</p>
          </div>
        </div>
        
        {/* Metrics Table with scrolling */}
        <div className="bg-gray-800 rounded-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center border-b border-gray-700 pb-3">
            <TrendingUp className="mr-3 text-green-500" size={24} />
            Métricas Detalhadas
          </h2>
          
          {/* Added max-height and overflow for scrolling if too many metrics */}
          <div className="max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
            <div className="grid grid-cols-2 gap-x-10 gap-y-2">
              {metrics.map((metric, idx) => (
                <div key={idx} className="flex justify-between items-center py-2 border-b border-gray-700">
                  <span className="text-gray-300 pr-4">{metric.name}</span>
                  <span className={`font-bold ${getMetricColor(metric)}`}>
                    {typeof metric.value === 'number' ? metric.value.toFixed(2) : metric.value || 'N/A'}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Note about metrics */}
          <div className="mt-4 text-gray-500 text-xs italic">
            Total de {metrics.length} métricas disponíveis para este jogador.
          </div>
        </div>
        
        {/* Player actions section - conditionally shown based on user type */}
        {userType === 'club' && (
          <div className="bg-gray-800 rounded-xl p-6 mb-6">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center border-b border-gray-700 pb-3">
              <UserCircle className="mr-3 text-green-500" size={24} />
              Ações de Scout
            </h2>
            
            <div className="space-y-3">
              <button 
                onClick={onViewComplete}
                className="w-full py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-medium rounded-lg flex items-center justify-center"
              >
                <UserCircle className="mr-2" size={18} />
                Ver Perfil Completo
              </button>
              
              <button className="w-full py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium rounded-lg flex items-center justify-center">
                <Star className="mr-2" size={18} />
                Solicitar Informações Completas
              </button>
              
              <button className="w-full py-3 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg flex items-center justify-center">
                <Search className="mr-2" size={18} />
                Buscar Jogadores Similares
              </button>
              
              <button className="w-full py-3 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg flex items-center justify-center">
                <Shield className="mr-2" size={18} />
                Solicitar Contato com Agente
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// LoginView Component
const LoginView = ({ onLogin }) => {
  const [loginType, setLoginType] = useState('club'); // Default to club login
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    team: '',
    position: '',
    language: 'english' // Default language
  });
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isOnboardingStep, setIsOnboardingStep] = useState(false);
  const [verificationNeeded, setVerificationNeeded] = useState(false);
  const [verificationCode, setVerificationCode] = useState('');
  const [availableLanguages, setAvailableLanguages] = useState([]);
  
  // Fetch available languages on component mount
  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        // In a real app, this would fetch from the API
        // For now, hard-code the response
        const languages = {
          "english": {
            "code": "en",
            "name": "English",
            "native_name": "English"
          },
          "portuguese": {
            "code": "pt",
            "name": "Portuguese",
            "native_name": "Português"
          },
          "spanish": {
            "code": "es",
            "name": "Spanish", 
            "native_name": "Español"
          },
          "bulgarian": {
            "code": "bg",
            "name": "Bulgarian",
            "native_name": "Български"
          }
        };
        
        setAvailableLanguages(Object.entries(languages).map(([key, value]) => ({
          id: key,
          ...value
        })));
      } catch (err) {
        console.error("Error fetching languages:", err);
      }
    };
    
    fetchLanguages();
  }, []);
  
  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  // Handle login/register form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    
    console.log("Form submission:", formData); // Debug
    
    // Check if this is a demo account login
    if (!isRegistering && 
        (formData.email === "club@demo.com" || formData.email === "player@demo.com") && 
        formData.password === "password123") {
      
      console.log("Using demo account login");
      
      // Create a mock user for demo accounts
      const isDemoClub = formData.email === "club@demo.com";
      const mockUser = {
        id: isDemoClub ? "demo-club-id" : "demo-player-id",
        email: formData.email,
        name: isDemoClub ? "Demo Club" : "Demo Player",
        user_type: isDemoClub ? "club" : "player",
        language: "english",
        team: isDemoClub ? "FC Demo" : null,
        position: isDemoClub ? null : "cf",
        created_at: new Date().toISOString(),
        onboarding_completed: true
      };
      
      // Call the login handler directly with the mock user
      onLogin(mockUser, mockUser.user_type);
      setLoading(false);
      return;
    }
    
    // Basic validation
    if (!formData.email || !formData.password) {
      setError('Please fill in all required fields.');
      setLoading(false);
      return;
    }
    
    try {
      if (isRegistering) {
        // Registration logic
        if (!formData.name) {
          setError('Name is required for registration.');
          setLoading(false);
          return;
        }
        
        if (loginType === 'player' && !formData.position) {
          setError('Position is required for player accounts.');
          setLoading(false);
          return;
        }
        
        // Create metadata for Supabase user
        const metadata = {
          name: formData.name,
          user_type: loginType,
          language: formData.language,
          team: formData.team || null,
          position: formData.position || null
        };
        
        console.log("Registration metadata:", metadata); // Debug
        
        // Register user with Supabase
        const { data, error } = await signUp(
          formData.email,
          formData.password,
          metadata
        );
        
        console.log("Registration response:", data); // Debug
        
        if (error) {
          console.error("Registration error:", error);
          throw error;
        }
        
        if (data && data.user) {
          console.log("User registered successfully:", data.user);
          
          // Check if we have a session - in that case we can skip verification
          if (data.session && data.session.access_token) {
            console.log("Session available - skipping verification");
            setIsOnboardingStep(true);
          } else {
            // Otherwise show verification screen
            setVerificationNeeded(true);
          }
        } else {
          setError('Registration failed. Please try again.');
        }
      } else {
        // Login logic        
        console.log("Attempting login with:", formData.email);
        
        // Sign in user with Supabase
        const { data, error } = await signIn(
          formData.email,
          formData.password
        );
        
        console.log("Login response:", data); // Debug
        
        if (error) {
          console.error("Login error:", error);
          throw error;
        }
        
        if (data && data.user) {
          console.log("User logged in successfully:", data.user);
          
          // Get user profile
          const { data: profile, error: profileError } = await supabase
            .from('profiles')
            .select('*')
            .eq('id', data.user.id)
            .single();
            
          console.log("Profile data:", profile); // Debug
            
          if (profileError) {
            console.error("Profile error:", profileError);
            
            // If profile not found, create one on the fly
            if (profileError.code === 'PGRST116') {
              console.log("Profile not found - creating new profile");
              
              try {
                // Create a new profile
                const newProfile = {
                  id: data.user.id,
                  email: data.user.email,
                  name: data.user.user_metadata?.name || data.user.email.split('@')[0],
                  user_type: data.user.user_metadata?.user_type || loginType,
                  language: data.user.user_metadata?.language || formData.language,
                  team: data.user.user_metadata?.team,
                  position: data.user.user_metadata?.position,
                  organization_id: 'default',
                  onboarding_completed: true,
                  created_at: new Date().toISOString()
                };
                
                const { data: createdProfile, error: createError } = await supabase
                  .from('profiles')
                  .insert(newProfile)
                  .select()
                  .single();
                  
                if (createError) {
                  console.error("Profile creation error:", createError);
                } else {
                  console.log("Profile created:", createdProfile);
                  // Call the login handler with the new profile
                  onLogin(createdProfile, createdProfile.user_type);
                  return;
                }
              } catch (profileCreateError) {
                console.error("Error creating profile:", profileCreateError);
              }
            }
          }
          
          // Create or use profile information
          const user = profile || {
            id: data.user.id,
            email: data.user.email,
            name: data.user.user_metadata?.name || data.user.email.split('@')[0],
            user_type: data.user.user_metadata?.user_type || loginType,
            language: data.user.user_metadata?.language || formData.language,
            team: data.user.user_metadata?.team,
            position: data.user.user_metadata?.position,
            created_at: new Date().toISOString()
          };
          
          console.log("Final user data:", user); // Debug
          
          // Call the parent component's login handler
          onLogin(user, user.user_type);
        } else {
          setError('Login failed. Please check your credentials.');
        }
      }
    } catch (err) {
      console.error("Error during authentication:", err);
      setError(err.message || "An unexpected error occurred. Please try again.");
      
      // TEMPORARY - FOR TESTING ONLY
      // If we're in a local environment, create a mock user to bypass auth issues
      if (window.location.hostname === 'localhost') {
        console.log("BYPASSING AUTH FOR LOCAL TESTING");
        const mockUser = {
          id: `mock-${Date.now()}`,
          email: formData.email,
          name: formData.name || formData.email.split('@')[0],
          user_type: loginType,
          language: formData.language || 'english',
          team: formData.team,
          position: formData.position,
          created_at: new Date().toISOString(),
          onboarding_completed: true
        };
        onLogin(mockUser, loginType);
      }
    } finally {
      setLoading(false);
    }
  };
  
  // Handle verification code submission
  const handleVerificationSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    
    try {
      console.log("Bypassing verification for testing");
      
      // Skip verification and move directly to onboarding for testing
      setVerificationNeeded(false);
      setIsOnboardingStep(true);
      
      // Alternatively, try to sign in directly for testing purposes
      /*
      const { data, error } = await signIn(
        formData.email,
        formData.password
      );
      
      if (error) {
        throw error;
      }
      
      if (data?.user) {
        // Move to onboarding
        setVerificationNeeded(false);
        setIsOnboardingStep(true);
      } else {
        setError('Login failed. Please try again.');
      }
      */
    } catch (err) {
      console.error("Error during verification:", err);
      setError(err.message || "An unexpected error occurred. Please try again.");
      
      // Even if there was an error, for testing purposes, let's continue to onboarding
      setVerificationNeeded(false);
      setIsOnboardingStep(true);
    } finally {
      setLoading(false);
    }
  };
  
  // Handle onboarding completion
  const handleOnboardingComplete = async () => {
    try {
      // Get current session
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session || !session.user) {
        throw new Error("No active session found. Please sign in again.");
      }
      
      // Get or create the user profile
      const { data: profile, error: profileError } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', session.user.id)
        .single();
        
      let user;
      
      if (profileError && profileError.code === 'PGRST116') {
        // Profile not found, create one
        const { data: newProfile, error: createError } = await supabase
          .from('profiles')
          .insert({
            id: session.user.id,
            email: formData.email,
            name: formData.name,
            user_type: loginType,
            language: formData.language,
            team: formData.team,
            position: formData.position,
            onboarding_completed: true
          })
          .select()
          .single();
          
        if (createError) throw createError;
        user = newProfile;
      } else if (profileError) {
        throw profileError;
      } else {
        // Update existing profile
        const { data: updatedProfile, error: updateError } = await supabase
          .from('profiles')
          .update({
            name: formData.name,
            language: formData.language,
            team: formData.team,
            position: formData.position,
            onboarding_completed: true
          })
          .eq('id', profile.id)
          .select()
          .single();
          
        if (updateError) throw updateError;
        user = updatedProfile;
      }
      
      // Call the parent component's login handler with the user data
      onLogin(user, user.user_type);
    } catch (error) {
      console.error("Error completing onboarding:", error);
      setError(error.message || "Failed to complete onboarding. Please try again.");
      
      // Fall back to creating a local user object
      const user = {
        id: `user-${Date.now()}`,
        email: formData.email,
        name: formData.name || formData.email.split('@')[0],
        team: formData.team || null,
        position: formData.position || null,
        language: formData.language,
        user_type: loginType,
        created_at: new Date().toISOString(),
        onboarding_completed: true
      };
      
      onLogin(user, loginType);
    }
  };
  
  // Render the verification step
  if (verificationNeeded) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        <div className="absolute inset-0 overflow-hidden z-0">
          {/* Soccer field background */}
          <div className="absolute inset-0 opacity-5">
            <div className="w-full h-full border-2 border-white"></div>
            <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-white"></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-60 h-60 border-2 border-white rounded-full"></div>
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[40%] h-[40%] border-2 border-white rounded-t-full"></div>
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[40%] h-[40%] border-2 border-white rounded-b-full"></div>
          </div>
        </div>
        
        <div className="max-w-md w-full relative z-10">
          {/* Logo/Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-r from-green-600 to-green-700 shadow-lg mb-4">
              <img src={logo} alt="KatenaScout Logo" className="w-16 h-16" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">KatenaScout</h1>
            <p className="text-gray-300">Verify Your Email</p>
          </div>
          
          {/* Verification Card */}
          <div className="bg-gray-800 rounded-xl shadow-xl overflow-hidden p-6">
            <h2 className="text-xl font-bold text-white mb-4">Email Verification</h2>
            
            <p className="text-gray-300 mb-6">
              We've sent a verification code to <span className="text-green-400">{formData.email}</span>. 
              Please check your inbox and enter the code below to continue.
            </p>
            
            {error && (
              <div className="bg-red-900 bg-opacity-20 border border-red-700 text-red-300 px-4 py-3 rounded-lg mb-4">
                {error}
              </div>
            )}
            
            <form onSubmit={handleVerificationSubmit} className="space-y-4">
              <div>
                <label htmlFor="verificationCode" className="block text-gray-300 mb-1">Verification Code</label>
                <input 
                  type="text" 
                  id="verificationCode"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value)}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                  placeholder="Enter code"
                />
              </div>
              
              <div className="pt-2">
                <button 
                  type="submit"
                  disabled={loading}
                  className={`w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium py-3 rounded-lg shadow-md flex items-center justify-center ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                >
                  {loading ? 'Verifying...' : 'Verify Email'}
                </button>
              </div>
            </form>
            
            <div className="mt-6 text-center">
              <button 
                onClick={() => setVerificationNeeded(false)}
                className="text-green-400 hover:text-green-300"
              >
                Back to Login
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  // Render the onboarding step
  if (isOnboardingStep) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        <div className="absolute inset-0 overflow-hidden z-0">
          {/* Soccer field background */}
          <div className="absolute inset-0 opacity-5">
            <div className="w-full h-full border-2 border-white"></div>
            <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-white"></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-60 h-60 border-2 border-white rounded-full"></div>
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[40%] h-[40%] border-2 border-white rounded-t-full"></div>
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[40%] h-[40%] border-2 border-white rounded-b-full"></div>
          </div>
        </div>
        
        <div className="max-w-md w-full relative z-10">
          {/* Logo/Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-r from-green-600 to-green-700 shadow-lg mb-4">
              <img src={logo} alt="KatenaScout Logo" className="w-16 h-16" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">KatenaScout</h1>
            <p className="text-gray-300">Welcome to KatenaScout!</p>
          </div>
          
          {/* Onboarding Card */}
          <div className="bg-gray-800 rounded-xl shadow-xl overflow-hidden p-6">
            <h2 className="text-xl font-bold text-white mb-4">Select Your Language</h2>
            
            <p className="text-gray-300 mb-6">
              Choose your preferred language for the platform. This will be used for all interactions with our AI scout.
            </p>
            
            <div className="space-y-4">
              {availableLanguages.map(lang => (
                <button
                  key={lang.id}
                  onClick={() => setFormData(prev => ({ ...prev, language: lang.id }))}
                  className={`w-full flex items-center justify-between p-3 rounded-lg border ${
                    formData.language === lang.id 
                      ? 'bg-green-800 bg-opacity-30 border-green-500 text-white' 
                      : 'bg-gray-700 border-gray-600 text-gray-300 hover:bg-gray-650'
                  }`}
                >
                  <div className="flex items-center">
                    <span className="text-lg mr-2">{lang.code === 'en' ? '🇬🇧' : lang.code === 'pt' ? '🇧🇷' : lang.code === 'es' ? '🇪🇸' : '🇧🇬'}</span>
                    <span>{lang.native_name}</span>
                  </div>
                  
                  {formData.language === lang.id && (
                    <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 0 1 0 1.414l-8 8a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 1.414-1.414L8 12.586l7.293-7.293a1 1 0 0 1 1.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}
                </button>
              ))}
              
              <div className="pt-6">
                <button 
                  onClick={handleOnboardingComplete}
                  className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium py-3 rounded-lg shadow-md flex items-center justify-center"
                >
                  Continue to Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  // Render the main login/registration form
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
      <div className="absolute inset-0 overflow-hidden z-0">
        {/* Soccer field background */}
        <div className="absolute inset-0 opacity-5">
          <div className="w-full h-full border-2 border-white"></div>
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-white"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-60 h-60 border-2 border-white rounded-full"></div>
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[40%] h-[40%] border-2 border-white rounded-t-full"></div>
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[40%] h-[40%] border-2 border-white rounded-b-full"></div>
        </div>
      </div>
      
      <div className="max-w-md w-full relative z-10">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-r from-green-600 to-green-700 shadow-lg mb-4">
            <img src={logo} alt="KatenaScout Logo" className="w-16 h-16" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">KatenaScout</h1>
          <p className="text-gray-300">Intelligent Scouting Platform</p>
        </div>
        
        {/* Login/Register Card */}
        <div className="bg-gray-800 rounded-xl shadow-xl overflow-hidden">
          {/* Tab Selector */}
          <div className="flex border-b border-gray-700">
            <button 
              className={`flex-1 py-4 text-center font-medium ${loginType === 'club' ? 'bg-green-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
              onClick={() => setLoginType('club')}
            >
              <Shield className="inline-block mr-2" size={18} />
              Club/Scout
            </button>
            <button 
              className={`flex-1 py-4 text-center font-medium ${loginType === 'player' ? 'bg-green-800 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
              onClick={() => setLoginType('player')}
            >
              <UserCircle className="inline-block mr-2" size={18} />
              Player
            </button>
          </div>
          
          {/* Form */}
          <div className="p-6">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <LogIn className="mr-3 text-green-500" size={24} />
              {isRegistering ? 'Create New Account' : 'Login to Your Account'}
            </h2>
            
            {error && (
              <div className="bg-red-900 bg-opacity-20 border border-red-700 text-red-300 px-4 py-3 rounded-lg mb-4">
                {error}
              </div>
            )}
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-gray-300 mb-1">Email</label>
                <input 
                  type="email" 
                  id="email" 
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                  placeholder="example@email.com"
                />
              </div>
              
              <div>
                <label htmlFor="password" className="block text-gray-300 mb-1">Password</label>
                <input 
                  type="password" 
                  id="password" 
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                  placeholder="******"
                />
              </div>
              
              {isRegistering && (
                <>
                  <div>
                    <label htmlFor="name" className="block text-gray-300 mb-1">Full Name</label>
                    <input 
                      type="text" 
                      id="name" 
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                      placeholder={loginType === 'club' ? "Club or Professional Name" : "Player Name"}
                    />
                  </div>
                  
                  {loginType === 'club' && (
                    <div>
                      <label htmlFor="team" className="block text-gray-300 mb-1">Club/Organization</label>
                      <input 
                        type="text" 
                        id="team" 
                        name="team"
                        value={formData.team}
                        onChange={handleChange}
                        className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                        placeholder="Club or Organization Name"
                      />
                    </div>
                  )}
                  
                  {loginType === 'player' && (
                    <div>
                      <label htmlFor="position" className="block text-gray-300 mb-1">Position</label>
                      <select 
                        id="position" 
                        name="position"
                        value={formData.position}
                        onChange={handleChange}
                        className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-green-500"
                      >
                        <option value="">Select your position</option>
                        <option value="gk">Goalkeeper</option>
                        <option value="cb">Center Back</option>
                        <option value="lb">Left Back</option>
                        <option value="rb">Right Back</option>
                        <option value="dmf">Defensive Midfielder</option>
                        <option value="cmf">Central Midfielder</option>
                        <option value="amf">Attacking Midfielder</option>
                        <option value="lw">Left Winger</option>
                        <option value="rw">Right Winger</option>
                        <option value="cf">Center Forward</option>
                      </select>
                    </div>
                  )}
                </>
              )}
              
              <div className="pt-2">
                <button 
                  type="submit"
                  disabled={loading}
                  className={`w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium py-3 rounded-lg shadow-md flex items-center justify-center ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                >
                  {loading ? (
                    <span>Loading...</span>
                  ) : (
                    <>
                      {isRegistering ? 'Create Account' : 'Login'}
                      <LogIn className="ml-2" size={18} />
                    </>
                  )}
                </button>
              </div>
            </form>
            
            <div className="mt-6 text-center">
              <button 
                onClick={() => setIsRegistering(!isRegistering)} 
                className="text-green-400 hover:text-green-300"
              >
                {isRegistering 
                  ? 'Already have an account? Log in' 
                  : 'Don\'t have an account? Sign up'}
              </button>
            </div>
            
            {/* Demo accounts section */}
            <div className="mt-8 border-t border-gray-700 pt-6">
              <h3 className="text-gray-400 text-sm mb-3">Quick Demo Access:</h3>
              <div className="grid grid-cols-2 gap-3">
                <button 
                  onClick={() => {
                    setLoginType('club');
                    setFormData({
                      email: 'club@demo.com',
                      password: 'password123',
                      name: 'Demo Club',
                      team: 'FC Demo',
                      position: '',
                      language: 'english'
                    });
                    
                    // Auto-login for demo accounts
                    const mockUser = {
                      id: "demo-club-id",
                      email: 'club@demo.com',
                      name: 'Demo Club',
                      user_type: 'club',
                      language: 'english',
                      team: 'FC Demo',
                      position: null,
                      created_at: new Date().toISOString(),
                      onboarding_completed: true
                    };
                    
                    // Use a timeout to ensure form updates first
                    setTimeout(() => onLogin(mockUser, 'club'), 100);
                  }}
                  className="p-2 text-sm bg-blue-700 hover:bg-blue-600 rounded text-white"
                >
                  <Shield className="inline-block mr-1" size={14} />
                  Try Club Demo
                </button>
                <button 
                  onClick={() => {
                    setLoginType('player');
                    setFormData({
                      email: 'player@demo.com',
                      password: 'password123',
                      name: 'Demo Player',
                      team: '',
                      position: 'cf',
                      language: 'english'
                    });
                    
                    // Auto-login for demo accounts
                    const mockUser = {
                      id: "demo-player-id",
                      email: 'player@demo.com',
                      name: 'Demo Player',
                      user_type: 'player',
                      language: 'english',
                      team: null,
                      position: 'cf',
                      created_at: new Date().toISOString(),
                      onboarding_completed: true
                    };
                    
                    // Use a timeout to ensure form updates first
                    setTimeout(() => onLogin(mockUser, 'player'), 100);
                  }}
                  className="p-2 text-sm bg-green-700 hover:bg-green-600 rounded text-white"
                >
                  <UserCircle className="inline-block mr-1" size={14} />
                  Try Player Demo
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div className="text-center mt-8 text-gray-500 text-sm">
          KatenaScout &copy; {new Date().getFullYear()} • All rights reserved
        </div>
      </div>
    </div>
  );
};

// TopNavBar Component
const TopNavBar = ({ userType, userData, onLogout, currentView, setCurrentView }) => {
  return (
    <div className="bg-gray-800 border-b border-gray-700 px-4 py-2 flex items-center justify-between">
      {/* Logo and Brand */}
      <div className="flex items-center">
        <div className="w-10 h-10 mr-3 flex items-center justify-center bg-white rounded-full shadow-lg">
          <span className="text-green-700 text-2xl">⚽</span>
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">KatenaScout</h1>
          <p className="text-xs text-green-200 opacity-80">Scouting Inteligente</p>
        </div>
      </div>
      
      {/* Search Bar */}
      <div className="flex-1 mx-8 hidden md:block">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="search"
            className="block w-full bg-gray-700 border border-gray-600 rounded-lg py-2 pl-10 pr-3 text-gray-300 placeholder-gray-400 focus:outline-none focus:border-green-500"
            placeholder="Buscar jogadores, posições ou habilidades..."
          />
        </div>
      </div>
      
      {/* User Info and Menu */}
      <div className="flex items-center space-x-4">
        <div className="hidden md:block text-right">
          <p className="text-white font-medium">{userData?.name || 'Usuário'}</p>
          <p className="text-xs text-gray-400">{userType === 'club' ? 'Clube/Scout' : 'Jogador'}</p>
        </div>
        
        <div className="relative">
          <button className="h-10 w-10 rounded-full bg-gray-700 flex items-center justify-center text-white border border-gray-600 hover:border-green-500">
            <UserCircle size={24} />
          </button>
          
          {/* Dropdown Menu - Would be implemented with a state in real app */}
          {/* {showMenu && (
            <div className="absolute right-0 top-12 w-56 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-50">
              <ul className="py-2">
                <li>
                  <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-gray-700">
                    <User className="inline-block mr-2" size={16} />
                    Meu Perfil
                  </button>
                </li>
                <li>
                  <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-gray-700">
                    <LogOut className="inline-block mr-2" size={16} />
                    Sair
                  </button>
                </li>
              </ul>
            </div>
          )} */}
        </div>
        
        <button 
          onClick={onLogout}
          className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 text-gray-300"
          title="Sair"
        >
          <LogOut size={20} />
        </button>
      </div>
    </div>
  );
};

// SideNavBar Component
const SideNavBar = ({ currentView, setCurrentView, userType }) => {
  return (
    <div className="w-16 md:w-56 bg-gray-900 border-r border-gray-700 flex flex-col">
      <nav className="flex-1 p-2">
        <ul className="space-y-2">
          {/* Dashboard */}
          <li>
            <button
              onClick={() => setCurrentView('dashboard')}
              className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                currentView === 'dashboard' 
                  ? 'bg-green-800 text-white' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100'
              }`}
            >
              <Home className="flex-shrink-0" size={20} />
              <span className="ml-3 hidden md:block">Dashboard</span>
            </button>
          </li>
          
          {/* Scout AI */}
          <li>
            <button
              onClick={() => setCurrentView('scout')}
              className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                currentView === 'scout' 
                  ? 'bg-green-800 text-white' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100'
              }`}
            >
              <Search className="flex-shrink-0" size={20} />
              <span className="ml-3 hidden md:block">Scout AI</span>
            </button>
          </li>
          
          {/* Talent Analysis */}
          <li>
            <button
              onClick={() => setCurrentView('talent-analysis')}
              className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                currentView === 'talent-analysis' 
                  ? 'bg-green-800 text-white' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100'
              }`}
            >
              <BarChart3 className="flex-shrink-0" size={20} />
              <span className="ml-3 hidden md:block">Análise de Talentos</span>
            </button>
          </li>
          
          {/* Favorites */}
          <li>
            <button
              onClick={() => setCurrentView('favorites')}
              className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                currentView === 'favorites' 
                  ? 'bg-green-800 text-white' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100'
              }`}
            >
              <Heart className="flex-shrink-0" size={20} />
              <span className="ml-3 hidden md:block">Favoritos</span>
            </button>
          </li>
          
          {/* Profile */}
          <li>
            <button
              onClick={() => setCurrentView('profile')}
              className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                currentView === 'profile' 
                  ? 'bg-green-800 text-white' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100'
              }`}
            >
              <UserCircle className="flex-shrink-0" size={20} />
              <span className="ml-3 hidden md:block">Meu Perfil</span>
            </button>
          </li>
          
          {/* Show video upload option only for player accounts */}
          {userType === 'player' && (
            <li>
              <button
                onClick={() => setCurrentView('videos')}
                className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                  currentView === 'videos' 
                    ? 'bg-green-800 text-white' 
                    : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100'
                }`}
              >
                <Upload className="flex-shrink-0" size={20} />
                <span className="ml-3 hidden md:block">Meus Vídeos</span>
              </button>
            </li>
          )}
        </ul>
      </nav>
      
      <div className="p-3 mt-auto border-t border-gray-800">
        <div className="w-full p-2 rounded-lg bg-green-900 bg-opacity-30 flex items-center justify-center">
          <span className="text-green-500 text-xl">⚽</span>
          <span className="ml-2 text-xs text-green-300 hidden md:block">KatenaScout v1.0</span>
        </div>
      </div>
    </div>
  );
};

// FavoritesView Component
const FavoritesView = ({ favorites, onSelectPlayer, setCurrentView }) => {
  const [searchQuery, setSearchQuery] = useState('');
  
  // Filter favorites based on search query
  const filteredFavorites = favorites.filter(player => {
    if (searchQuery.trim() === '') return true;
    
    const query = searchQuery.toLowerCase();
    return (
      player.name?.toLowerCase().includes(query) ||
      player.club?.toLowerCase().includes(query) ||
      player.positions?.some(pos => pos.toLowerCase().includes(query))
    );
  });
  
  // Helper function to format player names
  const formatPlayerName = (name) => {
    if (!name) return '';
    return name.replace(/([A-Z])/g, ' $1').trim()
      .replace(/\s+/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };
  
  // Helper function to get position in a readable format
  const getPositionName = (pos) => {
    const posMap = {
      'cb': 'Zagueiro',
      'lb': 'Lateral Esquerdo',
      'rb': 'Lateral Direito',
      'dmf': 'Volante',
      'cmf': 'Meio-Campo',
      'amf': 'Meia Atacante',
      'lw': 'Ponta Esquerda',
      'rw': 'Ponta Direita',
      'cf': 'Centroavante',
      'gk': 'Goleiro',
    };
    return posMap[pos] || pos;
  };
  
  // Set up the metrics for a player when selected
  const handlePlayerSelect = (player) => {
    // Extract metrics from the player object to display in the dashboard
    const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => ({
      name: key.replace(/_/g, ' ')
              .split(' ')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' '),
      value: value,
      key: key
    }));
    
    // Call the parent component's callback to show the player dashboard
    onSelectPlayer(player, playerMetrics);
  };
  
  return (
    <div className="flex-1 bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <Heart className="mr-3 text-red-500" size={24} />
          Jogadores Favoritos
        </h2>
      </div>
      
      {/* Search & Filters */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="search"
            className="block w-full bg-gray-700 border border-gray-600 rounded-lg py-2 pl-10 pr-3 text-gray-300 placeholder-gray-400 focus:outline-none focus:border-green-500"
            placeholder="Procurar nos favoritos..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>
      
      {/* Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        {favorites.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-20 h-20 rounded-full bg-gray-800 flex items-center justify-center mb-4">
              <Heart className="text-gray-600" size={40} />
            </div>
            <h3 className="text-xl font-medium text-gray-300 mb-2">Nenhum favorito ainda</h3>
            <p className="text-gray-500 max-w-md">
              Você ainda não adicionou nenhum jogador aos favoritos. Use o Scout AI para encontrar e favoritar jogadores.
            </p>
            <button 
              onClick={() => setCurrentView('scout')}
              className="mt-6 px-6 py-2 bg-green-700 hover:bg-green-600 text-white rounded-lg flex items-center"
            >
              <Search className="mr-2" size={18} />
              Ir para o Scout AI
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredFavorites.map((player, index) => (
              <div 
                key={index} 
                className="bg-gray-800 rounded-xl overflow-hidden border border-gray-700 hover:border-green-500 transition-colors shadow-md"
              >
                <div className="p-4 flex items-center">
                  {/* Player Avatar */}
                  <div className="w-16 h-16 bg-blue-900 rounded-full flex items-center justify-center text-white font-bold mr-4 relative">
                    <span>{player.positions?.[0]?.toUpperCase() || 'ST'}</span>
                    <div className="absolute -top-1 -right-1">
                      <div className="w-6 h-6 rounded-full bg-red-600 flex items-center justify-center shadow-lg">
                        <Heart size={12} fill="white" />
                      </div>
                    </div>
                  </div>
                  
                  {/* Player Info */}
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-white">{formatPlayerName(player.name)}</h3>
                    <div className="text-sm text-gray-400 flex items-center">
                      <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-1"></span>
                      {player.positions?.map(pos => getPositionName(pos)).join(', ') || 'N/A'}
                    </div>
                    <div className="text-sm text-gray-400 mt-1">
                      {player.age ? `${player.age} anos` : ''} • {player.club || 'Clube desconhecido'}
                    </div>
                  </div>
                </div>
                
                {/* Action Button */}
                <button 
                  onClick={() => handlePlayerSelect(player)}
                  className="w-full py-3 bg-gradient-to-r from-green-700 to-green-800 hover:from-green-800 hover:to-green-900 text-white font-medium"
                >
                  Ver Perfil Completo
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// ProfileView Component
const ProfileView = ({ userData, userType }) => {
  return (
    <div className="flex-1 bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <UserCircle className="mr-3 text-green-500" size={24} />
          Meu Perfil
        </h2>
      </div>
      
      {/* Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-2xl mx-auto">
          {/* Profile Card */}
          <div className="bg-gray-800 rounded-xl overflow-hidden shadow-lg mb-6">
            {/* Cover Photo */}
            <div className="h-32 bg-gradient-to-r from-green-900 to-blue-900 relative">
              <div className="absolute inset-0 opacity-10">
                <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[60%] h-[120%] border-2 border-white rounded-full"></div>
                <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-0.5 h-full bg-white"></div>
              </div>
            </div>
            
            {/* Profile Info */}
            <div className="px-6 pb-6 relative">
              {/* Avatar */}
              <div className="absolute -top-12 left-6 w-24 h-24">
                <div className="w-full h-full rounded-full bg-gray-700 border-4 border-gray-800 flex items-center justify-center text-white text-3xl">
                  {userType === 'club' ? (
                    <Shield size={40} />
                  ) : (
                    <UserCircle size={40} />
                  )}
                </div>
              </div>
              
              {/* User Type Badge */}
              <div className="absolute right-6 -top-6">
                <div className="px-4 py-2 bg-green-700 rounded-full text-white text-sm font-medium">
                  {userType === 'club' ? 'Clube/Scout' : 'Jogador'}
                </div>
              </div>
              
              {/* User Info */}
              <div className="mt-16">
                <h3 className="text-2xl font-bold text-white mb-1">{userData?.name}</h3>
                <p className="text-gray-400">{userData?.email}</p>
                
                {/* Additional Info Based on User Type */}
                <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                  {userType === 'club' && (
                    <>
                      <div className="bg-gray-700 rounded-lg p-4">
                        <h4 className="text-gray-300 text-sm mb-2">Clube/Organização</h4>
                        <p className="text-white font-medium">{userData?.team || 'Não informado'}</p>
                      </div>
                      <div className="bg-gray-700 rounded-lg p-4">
                        <h4 className="text-gray-300 text-sm mb-2">Membro desde</h4>
                        <p className="text-white font-medium">
                          {userData?.createdAt 
                            ? new Date(userData.createdAt).toLocaleDateString() 
                            : 'Não informado'}
                        </p>
                      </div>
                    </>
                  )}
                  
                  {userType === 'player' && (
                    <>
                      <div className="bg-gray-700 rounded-lg p-4">
                        <h4 className="text-gray-300 text-sm mb-2">Posição</h4>
                        <p className="text-white font-medium">
                          {userData?.position 
                            ? (() => {
                                const posMap = {
                                  'cb': 'Zagueiro',
                                  'lb': 'Lateral Esquerdo',
                                  'rb': 'Lateral Direito',
                                  'dmf': 'Volante',
                                  'cmf': 'Meio-Campo',
                                  'amf': 'Meia Atacante',
                                  'lw': 'Ponta Esquerda',
                                  'rw': 'Ponta Direita',
                                  'cf': 'Centroavante',
                                  'gk': 'Goleiro',
                                };
                                return posMap[userData.position] || userData.position;
                              })() 
                            : 'Não informado'}
                        </p>
                      </div>
                      <div className="bg-gray-700 rounded-lg p-4">
                        <h4 className="text-gray-300 text-sm mb-2">Membro desde</h4>
                        <p className="text-white font-medium">
                          {userData?.createdAt 
                            ? new Date(userData.createdAt).toLocaleDateString() 
                            : 'Não informado'}
                        </p>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
          
          {/* Edit Profile Button */}
          <div className="text-center mb-6">
            <button className="px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium rounded-lg shadow-md">
              Editar Perfil
            </button>
          </div>
          
          {/* Account Settings Section */}
          <div className="bg-gray-800 rounded-xl overflow-hidden shadow-lg mb-6">
            <div className="p-6">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <UserCircle className="mr-3 text-green-500" size={20} />
                Configurações da Conta
              </h3>
              
              <div className="space-y-4">
                <div className="flex justify-between items-center py-3 border-b border-gray-700">
                  <div>
                    <h4 className="text-white font-medium">Alterar Senha</h4>
                    <p className="text-gray-400 text-sm">Atualize sua senha periodicamente para maior segurança</p>
                  </div>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg">
                    Alterar
                  </button>
                </div>
                
                <div className="flex justify-between items-center py-3 border-b border-gray-700">
                  <div>
                    <h4 className="text-white font-medium">Notificações</h4>
                    <p className="text-gray-400 text-sm">Gerencie suas preferências de notificações</p>
                  </div>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg">
                    Configurar
                  </button>
                </div>
                
                <div className="flex justify-between items-center py-3 border-b border-gray-700">
                  <div>
                    <h4 className="text-white font-medium">Privacidade</h4>
                    <p className="text-gray-400 text-sm">Controle quem pode ver suas informações</p>
                  </div>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg">
                    Ajustar
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          {/* Danger Zone */}
          <div className="bg-red-900 bg-opacity-20 border border-red-800 rounded-xl p-6">
            <h3 className="text-xl font-bold text-red-300 mb-4">Zona de Perigo</h3>
            <p className="text-red-200 mb-4">Ações que não podem ser desfeitas:</p>
            
            <div className="flex justify-between items-center">
              <div>
                <h4 className="text-white font-medium">Excluir Conta</h4>
                <p className="text-red-200 text-sm">Esta ação não pode ser desfeita</p>
              </div>
              <button className="px-4 py-2 bg-red-800 hover:bg-red-700 text-white rounded-lg">
                Excluir
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// VideosUploadView Component for Players
const VideosUploadView = ({ userData }) => {
  const [videos, setVideos] = useState([
    // Sample videos for demo
    {
      id: 1,
      title: 'Melhores momentos - Temporada 2023',
      thumbnail: 'https://via.placeholder.com/300x200/1F2937/FFFFFF?text=Video+Thumbnail',
      date: '2023-05-15',
      duration: '02:45',
      views: 124
    },
    {
      id: 2,
      title: 'Gols e assistências - Janeiro 2024',
      thumbnail: 'https://via.placeholder.com/300x200/1F2937/FFFFFF?text=Video+Thumbnail',
      date: '2024-01-20',
      duration: '01:58',
      views: 87
    }
  ]);
  
  return (
    <div className="flex-1 bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <Upload className="mr-3 text-green-500" size={24} />
          Meus Vídeos
        </h2>
      </div>
      
      {/* Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        {/* Upload Section */}
        <div className="bg-gray-800 rounded-xl p-6 mb-6">
          <h3 className="text-xl font-bold text-white mb-4">Enviar Novo Vídeo</h3>
          
          <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center">
            <Upload className="mx-auto mb-4 text-gray-500" size={48} />
            <p className="text-gray-300 mb-4">Arraste e solte seu vídeo aqui, ou clique para selecionar</p>
            <button className="px-6 py-2 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium rounded-lg">
              Selecionar Vídeo
            </button>
            <p className="text-gray-500 text-sm mt-4">Formatos aceitos: MP4, MOV, AVI • Tamanho máximo: 500MB</p>
          </div>
        </div>
        
        {/* Videos Gallery */}
        <div className="bg-gray-800 rounded-xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-white">Meus Vídeos</h3>
            <div className="text-gray-400">
              {videos.length} vídeos
            </div>
          </div>
          
          {videos.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-400">Você ainda não enviou nenhum vídeo.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {videos.map(video => (
                <div key={video.id} className="bg-gray-700 rounded-lg overflow-hidden shadow-md">
                  <div className="relative">
                    <img 
                      src={video.thumbnail} 
                      alt={video.title}
                      className="w-full h-48 object-cover"
                    />
                    <div className="absolute bottom-2 right-2 bg-black bg-opacity-70 px-2 py-1 rounded text-white text-xs">
                      {video.duration}
                    </div>
                  </div>
                  
                  <div className="p-4">
                    <h4 className="text-white font-medium mb-1">{video.title}</h4>
                    <div className="flex justify-between text-gray-400 text-sm">
                      <span>{new Date(video.date).toLocaleDateString()}</span>
                      <span>{video.views} visualizações</span>
                    </div>
                    
                    <div className="flex space-x-2 mt-4">
                      <button className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded">
                        Editar
                      </button>
                      <button className="py-2 px-3 bg-gray-600 hover:bg-gray-500 text-white rounded">
                        Compartilhar
                      </button>
                      <button className="py-2 px-3 bg-red-600 hover:bg-red-700 text-white rounded">
                        Excluir
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Dashboard Component
const DashboardView = ({ 
  featuredPlayers, 
  hiddenGems, 
  upcomingMatches, 
  usageStats, 
  onSelectPlayer, 
  setCurrentView,
  favorites,
  isPlayerFavorite,
  toggleFavorite
}) => {
  // Format date for matches
  const formatMatchDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };
  
  // Format player data for display
  const formatPlayerName = (name) => {
    if (!name) return '';
    return name.replace(/([A-Z])/g, ' $1').trim()
      .replace(/\s+/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };
  
  // Set up metrics for a player when selected
  const handlePlayerSelect = (player) => {
    // Extract metrics from the player object to display in the dashboard
    const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => ({
      name: key.replace(/_/g, ' ')
              .split(' ')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' '),
      value: value,
      key: key
    }));
    
    // Call the parent component's callback to show the player dashboard
    onSelectPlayer(player, playerMetrics);
  };
  
  return (
    <div className="flex-1 bg-gray-900 overflow-y-auto">
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-gray-400">Bem-vindo ao KatenaScout, sua plataforma inteligente de scouting esportivo.</p>
        </div>
        
        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content - 2 columns wide */}
          <div className="lg:col-span-2 space-y-6">
            {/* Featured Players Section */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 bg-gradient-to-r from-green-900 to-blue-900">
                <h2 className="text-xl font-bold text-white flex items-center">
                  <Star className="mr-2 text-yellow-300" size={20} />
                  Jogadores em Destaque
                </h2>
              </div>
              
              <div className="p-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {featuredPlayers.map((player) => (
                    <div 
                      key={player.id}
                      className="bg-gray-750 rounded-lg overflow-hidden border border-gray-700 hover:border-green-500 transition-colors"
                    >
                      {/* Player Photo */}
                      <div className="relative h-40 overflow-hidden bg-gray-700">
                        <img 
                          src={player.photoUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`}
                          alt={player.name}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.onerror = null; 
                            e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                          }}
                        />
                        
                        {/* Rating badge */}
                        <div className="absolute top-0 right-0 m-2">
                          <div className="w-12 h-12 flex items-center justify-center bg-gradient-to-b from-green-500 to-green-700 rounded-full shadow-lg border-2 border-white">
                            <span className="text-lg font-bold text-white">{player.score}</span>
                          </div>
                        </div>
                        
                        {/* Favorite button */}
                        <button 
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleFavorite(player);
                          }}
                          className="absolute top-0 left-0 m-2 p-2 rounded-full bg-gray-800 bg-opacity-60 hover:bg-opacity-80 text-white"
                        >
                          <Heart 
                            size={16} 
                            fill={isPlayerFavorite(player) ? 'white' : 'none'} 
                            className={isPlayerFavorite(player) ? 'text-red-500' : 'text-white'}
                          />
                        </button>
                      </div>
                      
                      {/* Player Info */}
                      <div className="p-3">
                        <h3 className="font-bold text-white text-lg">{formatPlayerName(player.name)}</h3>
                        <div className="flex justify-between items-center text-sm text-gray-400 mb-2">
                          <div>{player.positions?.join(', ')}</div>
                          <div className="flex items-center">
                            <span>{player.age} anos</span>
                          </div>
                        </div>
                        <div className="text-sm text-gray-400 mb-3">
                          {player.club} • {player.country}
                        </div>
                        <button 
                          onClick={() => handlePlayerSelect(player)}
                          className="w-full py-2 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-medium rounded-lg text-sm flex items-center justify-center"
                        >
                          <Search className="mr-1" size={14} />
                          Ver Detalhes
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            {/* AI Highlighted Gems Section */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 bg-gradient-to-r from-purple-900 to-indigo-900">
                <h2 className="text-xl font-bold text-white flex items-center">
                  <TrendingUp className="mr-2 text-purple-300" size={20} />
                  Destaques da IA
                </h2>
              </div>
              
              <div className="p-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {hiddenGems.map((player) => (
                    <div 
                      key={player.id}
                      className="bg-gradient-to-r from-gray-800 to-gray-750 rounded-lg overflow-hidden border border-gray-700 hover:border-purple-500 transition-colors"
                    >
                      <div className="flex p-3">
                        {/* Player Photo */}
                        <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-700 flex-shrink-0 border-2 border-purple-500">
                          <img 
                            src={player.photoUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`}
                            alt={player.name}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              e.target.onerror = null; 
                              e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                            }}
                          />
                        </div>
                        
                        {/* Player Info */}
                        <div className="ml-3 flex-1">
                          <h3 className="font-bold text-white">{formatPlayerName(player.name)}</h3>
                          <div className="text-xs text-gray-400 mb-1">{player.positions?.join(', ')} • {player.age} anos</div>
                          <div className="text-xs text-gray-400">{player.club} • {player.country}</div>
                        </div>
                      </div>
                      
                      {/* AI Highlight */}
                      <div className="px-3 py-2 bg-purple-900 bg-opacity-30 border-t border-purple-800">
                        <div className="text-xs text-purple-300 mb-1">Destaque IA:</div>
                        <p className="text-sm text-white">{player.highlight}</p>
                      </div>
                      
                      <div className="p-3 flex items-center justify-between">
                        <div className="flex items-center text-gray-300">
                          <Star className="text-yellow-400 mr-1" size={14} />
                          <span className="text-sm font-medium">{player.score}</span>
                        </div>
                        
                        <div className="flex space-x-2">
                          <button 
                            onClick={() => handlePlayerSelect(player)}
                            className="px-3 py-1 bg-purple-700 hover:bg-purple-600 text-white rounded-lg text-sm"
                          >
                            Detalhes
                          </button>
                          
                          <button 
                            onClick={() => toggleFavorite(player)}
                            className={`p-1 rounded-lg ${isPlayerFavorite(player) ? 'bg-red-600 text-white' : 'bg-gray-700 text-gray-300'}`}
                          >
                            <Heart size={16} fill={isPlayerFavorite(player) ? 'white' : 'none'} />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Matches Section */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 bg-gradient-to-r from-blue-900 to-blue-800">
                <h2 className="text-xl font-bold text-white flex items-center">
                  <Calendar className="mr-2 text-blue-300" size={20} />
                  Jogos
                </h2>
              </div>
              
              <div className="p-4">
                <div className="space-y-3">
                  {upcomingMatches.map((match) => (
                    <div 
                      key={match.id}
                      className={`rounded-lg overflow-hidden ${match.important ? 'border-l-4 border-blue-600' : 'border border-gray-700'}`}
                    >
                      <div className="bg-gray-750 p-4">
                        <div className="flex justify-between items-center mb-2">
                          <div className="text-xs text-gray-400">{match.competition}</div>
                          <div className="text-xs bg-blue-900 text-blue-200 px-2 py-1 rounded">
                            {formatMatchDate(match.date)}
                          </div>
                        </div>
                        
                        <div className="flex items-center justify-center">
                          <div className="text-right flex-1">
                            <div className="font-bold text-white">{match.home}</div>
                          </div>
                          
                          <div className="px-4 text-gray-400 font-bold">VS</div>
                          
                          <div className="text-left flex-1">
                            <div className="font-bold text-white">{match.away}</div>
                          </div>
                        </div>
                        
                        <div className="text-center mt-2 text-sm text-gray-400">
                          {match.stadium}
                        </div>
                        
                        {/* If the match contains relevant players we're tracking */}
                        {match.relevantPlayers && match.relevantPlayers.length > 0 && (
                          <div className="mt-3 border-t border-gray-700 pt-2">
                            <div className="text-xs text-blue-400 mb-1">Jogadores relevantes:</div>
                            <div className="flex flex-wrap gap-2">
                              {match.relevantPlayers.map(playerId => {
                                // Find the player in featured players
                                const player = featuredPlayers.find(p => p.id === playerId);
                                if (!player) return null;
                                
                                return (
                                  <button 
                                    key={player.id}
                                    onClick={() => handlePlayerSelect(player)}
                                    className="px-2 py-1 bg-blue-900 bg-opacity-40 hover:bg-opacity-60 text-white rounded-full text-xs flex items-center"
                                  >
                                    <div className="w-4 h-4 bg-blue-700 rounded-full flex items-center justify-center mr-1 text-[8px]">
                                      {player.positions[0]?.toUpperCase() || ''}
                                    </div>
                                    {formatPlayerName(player.name)}
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          {/* Sidebar - 1 column wide */}
          <div className="space-y-6">
            {/* User Stats */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 bg-gradient-to-r from-gray-800 to-gray-700">
                <h2 className="text-xl font-bold text-white flex items-center">
                  <UserCircle className="mr-2 text-gray-300" size={20} />
                  Atividade do Usuário
                </h2>
              </div>
              
              <div className="p-4">
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-gray-750 p-3 rounded-lg">
                      <div className="text-gray-400 text-sm mb-1">Buscas</div>
                      <div className="text-2xl text-white font-bold">{usageStats.searches}</div>
                    </div>
                    
                    <div className="bg-gray-750 p-3 rounded-lg">
                      <div className="text-gray-400 text-sm mb-1">Favoritos</div>
                      <div className="text-2xl text-white font-bold">{usageStats.favoritedPlayers}</div>
                    </div>
                  </div>
                  
                  <div className="bg-gray-750 p-3 rounded-lg">
                    <div className="text-gray-400 text-sm mb-1">Última atividade</div>
                    <div className="text-white">
                      {new Date(usageStats.lastActivity).toLocaleDateString('pt-BR', {
                        day: 'numeric',
                        month: 'long',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </div>
                  
                  <div className="bg-gray-750 p-3 rounded-lg">
                    <div className="text-gray-400 text-sm mb-2">Ações recomendadas</div>
                    <div className="space-y-2">
                      {usageStats.recommendedActions.map((action, index) => (
                        <div key={index} className="flex items-center">
                          <div className={`w-5 h-5 mr-2 rounded-full flex items-center justify-center ${
                            action.done ? 'bg-green-600' : 'bg-gray-600'
                          }`}>
                            {action.done ? (
                              <span className="text-white text-xs">✓</span>
                            ) : (
                              <span className="text-white text-xs">!</span>
                            )}
                          </div>
                          <span className={`text-sm ${action.done ? 'text-gray-400 line-through' : 'text-white'}`}>
                            {action.text}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Quick Actions */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 bg-gradient-to-r from-gray-800 to-gray-700">
                <h2 className="text-xl font-bold text-white">Ações Rápidas</h2>
              </div>
              
              <div className="p-4 space-y-3">
                <button 
                  onClick={() => setCurrentView('scout')}
                  className="w-full p-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-lg flex items-center"
                >
                  <Search className="mr-3" size={18} />
                  <span className="font-medium">Iniciar Nova Busca</span>
                </button>
                
                <button 
                  onClick={() => setCurrentView('talent-analysis')}
                  className="w-full p-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg flex items-center"
                >
                  <BarChart3 className="mr-3" size={18} />
                  <span className="font-medium">Análise de Talentos</span>
                </button>
                
                <button 
                  onClick={() => setCurrentView('favorites')}
                  className="w-full p-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white rounded-lg flex items-center"
                >
                  <Heart className="mr-3" size={18} />
                  <span className="font-medium">Meus Favoritos</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// TalentAnalysisView Component
const TalentAnalysisView = ({ featuredPlayers, hiddenGems, onSelectPlayer, isPlayerFavorite, toggleFavorite }) => {
  const [selectedPosition, setSelectedPosition] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Combine featured players and hidden gems
  const allPlayers = [...featuredPlayers, ...hiddenGems];
  
  // Filter players by position and search query
  const filteredPlayers = allPlayers.filter(player => {
    // Position filter
    const positionMatches = selectedPosition === 'all' || 
      (player.positions && player.positions.includes(selectedPosition));
    
    // Search filter
    const query = searchQuery.toLowerCase();
    const searchMatches = searchQuery === '' || 
      player.name.toLowerCase().includes(query) || 
      player.club?.toLowerCase().includes(query) || 
      player.country?.toLowerCase().includes(query);
    
    return positionMatches && searchMatches;
  });
  
  // Get all unique positions from our players
  const allPositions = Array.from(new Set(
    allPlayers.flatMap(player => player.positions || [])
  )).sort();
  
  // Position groups for the tabs
  const positionGroups = [
    { id: 'all', name: 'Todos', positions: [] },
    { id: 'gk', name: 'Goleiros', positions: ['gk'] },
    { id: 'def', name: 'Defensores', positions: ['cb', 'lb', 'rb'] },
    { id: 'mid', name: 'Meio-Campistas', positions: ['dmf', 'cmf', 'amf'] },
    { id: 'att', name: 'Atacantes', positions: ['lw', 'rw', 'cf'] }
  ];
  
  // Format player name
  const formatPlayerName = (name) => {
    if (!name) return '';
    return name.replace(/([A-Z])/g, ' $1').trim()
      .replace(/\s+/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };
  
  // Format position name
  const getPositionName = (pos) => {
    const posMap = {
      'cb': 'Zagueiro',
      'lb': 'Lateral Esquerdo',
      'rb': 'Lateral Direito',
      'dmf': 'Volante',
      'cmf': 'Meio-Campo',
      'amf': 'Meia Atacante',
      'lw': 'Ponta Esquerda',
      'rw': 'Ponta Direita',
      'cf': 'Centroavante',
      'gk': 'Goleiro',
    };
    return posMap[pos] || pos;
  };
  
  // Handle player selection
  const handlePlayerSelect = (player) => {
    // Extract metrics from the player object
    const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => ({
      name: key.replace(/_/g, ' ')
              .split(' ')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' '),
      value: value,
      key: key
    }));
    
    // Call the parent component's callback
    onSelectPlayer(player, playerMetrics);
  };
  
  return (
    <div className="flex-1 bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <BarChart3 className="mr-3 text-green-500" size={24} />
          Análise de Talentos
        </h2>
      </div>
      
      {/* Position Filter Tabs */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="flex overflow-x-auto custom-scrollbar">
          {positionGroups.map(group => (
            <button
              key={group.id}
              onClick={() => setSelectedPosition(group.id)}
              className={`px-6 py-3 font-medium text-sm whitespace-nowrap ${
                selectedPosition === group.id
                  ? 'text-white border-b-2 border-green-500'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              {group.name}
            </button>
          ))}
        </div>
      </div>
      
      {/* Search & Filters */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="search"
            className="block w-full bg-gray-700 border border-gray-600 rounded-lg py-2 pl-10 pr-3 text-gray-300 placeholder-gray-400 focus:outline-none focus:border-green-500"
            placeholder="Procurar por nome, clube ou país..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>
      
      {/* Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        {filteredPlayers.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-center">
            <div className="w-16 h-16 rounded-full bg-gray-800 flex items-center justify-center mb-4">
              <Search className="text-gray-600" size={32} />
            </div>
            <h3 className="text-xl font-medium text-gray-300 mb-2">Nenhum jogador encontrado</h3>
            <p className="text-gray-500 max-w-md">
              Não encontramos jogadores com os filtros selecionados. Tente alterar a posição ou critérios de busca.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Display players by position if a specific position group is selected */}
            {selectedPosition !== 'all' ? (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {filteredPlayers.map(player => (
                    <div 
                      key={player.id}
                      className="bg-gray-800 rounded-lg overflow-hidden border border-gray-700 hover:border-green-500 transition-colors shadow-md"
                    >
                      <div className="p-4 flex items-start">
                        {/* Player Photo */}
                        <div className="w-20 h-20 bg-gray-700 rounded-lg overflow-hidden flex-shrink-0 mr-3">
                          <img 
                            src={player.photoUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`}
                            alt={player.name}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              e.target.onerror = null; 
                              e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                            }}
                          />
                        </div>
                        
                        {/* Player Info */}
                        <div className="flex-1">
                          <div className="flex justify-between">
                            <h3 className="font-bold text-white">{formatPlayerName(player.name)}</h3>
                            <div className="flex items-center ml-2">
                              <button 
                                onClick={(e) => {
                                  e.stopPropagation();
                                  toggleFavorite(player);
                                }}
                                className={`p-1 rounded-full ${isPlayerFavorite(player) ? 'text-red-500' : 'text-gray-400 hover:text-gray-300'}`}
                              >
                                <Heart size={14} fill={isPlayerFavorite(player) ? 'currentColor' : 'none'} />
                              </button>
                            </div>
                          </div>
                          
                          <div className="text-sm text-gray-400">
                            {player.positions?.map(pos => getPositionName(pos)).join(', ')}
                          </div>
                          
                          <div className="text-sm text-gray-400 mt-1 mb-2">
                            {player.age} anos • {player.club}
                          </div>
                          
                          {/* Key Stats */}
                          <div className="grid grid-cols-3 gap-2 mt-2">
                            {Object.entries(player.stats || {}).slice(0, 3).map(([key, value], idx) => (
                              <div key={idx} className="bg-gray-750 p-1 rounded text-center">
                                <div className="text-xs text-gray-400">{key.split('_')[0]}</div>
                                <div className="text-sm font-medium text-white">{value}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                      
                      {/* Player Rating */}
                      <div className="bg-gray-750 px-4 py-2 flex justify-between items-center border-t border-gray-700">
                        <div className="flex items-center">
                          <Star className="text-yellow-400 mr-1" size={16} />
                          <span className="text-white font-medium">{player.score}</span>
                        </div>
                        
                        <button 
                          onClick={() => handlePlayerSelect(player)}
                          className="px-3 py-1 bg-green-700 hover:bg-green-600 text-white text-sm rounded"
                        >
                          Ver Perfil
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              // Group by position when showing all
              positionGroups.slice(1).map(group => {
                const positionPlayers = filteredPlayers.filter(player => 
                  player.positions && player.positions.some(pos => group.positions.includes(pos))
                );
                
                if (positionPlayers.length === 0) return null;
                
                return (
                  <div key={group.id} className="space-y-3">
                    <h3 className="text-xl font-bold text-white border-b border-gray-700 pb-2">
                      {group.name}
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                      {positionPlayers.slice(0, 4).map(player => (
                        <div 
                          key={player.id}
                          className="bg-gray-800 rounded-lg overflow-hidden border border-gray-700 hover:border-green-500 transition-colors shadow-md"
                        >
                          <div className="p-4 flex items-start">
                            {/* Player Photo */}
                            <div className="w-16 h-16 bg-gray-700 rounded-lg overflow-hidden flex-shrink-0 mr-3">
                              <img 
                                src={player.photoUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`}
                                alt={player.name}
                                className="w-full h-full object-cover"
                                onError={(e) => {
                                  e.target.onerror = null; 
                                  e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                                }}
                              />
                            </div>
                            
                            {/* Player Info */}
                            <div className="flex-1">
                              <div className="flex justify-between">
                                <h3 className="font-bold text-white">{formatPlayerName(player.name)}</h3>
                                <div className="flex items-center ml-2">
                                  <button 
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      toggleFavorite(player);
                                    }}
                                    className={`p-1 rounded-full ${isPlayerFavorite(player) ? 'text-red-500' : 'text-gray-400 hover:text-gray-300'}`}
                                  >
                                    <Heart size={14} fill={isPlayerFavorite(player) ? 'currentColor' : 'none'} />
                                  </button>
                                </div>
                              </div>
                              
                              <div className="text-sm text-gray-400">
                                {player.positions?.map(pos => getPositionName(pos)).join(', ')}
                              </div>
                              
                              <div className="text-sm text-gray-400 mt-1">
                                {player.age} anos • {player.club}
                              </div>
                              
                              <button 
                                onClick={() => handlePlayerSelect(player)}
                                className="mt-2 px-3 py-1 bg-green-700 hover:bg-green-600 text-white text-sm rounded-lg flex items-center"
                              >
                                <Search className="mr-1" size={12} />
                                Ver Perfil
                              </button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    {positionPlayers.length > 4 && (
                      <div className="text-right">
                        <button 
                          onClick={() => {
                            setSelectedPosition(group.id);
                          }}
                          className="text-green-400 hover:text-green-300 text-sm"
                        >
                          Ver todos os {positionPlayers.length} {group.name.toLowerCase()} →
                        </button>
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;