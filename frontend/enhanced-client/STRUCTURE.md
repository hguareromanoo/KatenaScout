# KatenaScout Frontend Structure

This document describes the architecture and organization of the KatenaScout frontend application.

## Directory Structure

```
/frontend/enhanced-client/
├── public/                 # Static assets
├── src/
│   ├── api/                # API service layer
│   │   ├── api.js          # Core API fetch utilities
│   │   ├── chatService.js  # Chat & search related services
│   │   ├── playerService.js # Player data services
│   │   ├── appService.js   # Application services
│   │   └── index.js        # Export convenience file
│   ├── components/         # React components
│   │   ├── ChatInterface.js # Chat UI component
│   │   ├── ErrorBoundary.js # Error handling component
│   │   ├── FavoritesView.js # Favorites management view
│   │   ├── OnboardingView.js # Initial language selector
│   │   ├── PlayerCompletePage.js # Detailed player view
│   │   ├── PlayerDashboard.js # Player stats modal
│   │   └── SettingsView.js  # Settings page
│   ├── config/             # Configuration constants
│   │   └── index.js        # API endpoints, defaults, etc.
│   ├── contexts/           # React context providers
│   │   ├── AppProvider.js  # Main provider wrapper
│   │   ├── LanguageContext.js # Translation context
│   │   ├── SessionContext.js # Chat session state
│   │   ├── UIContext.js    # UI state management
│   │   └── index.js        # Export convenience file
│   ├── locales/            # Translation files
│   │   ├── en.js           # English translations
│   │   ├── pt.js           # Portuguese translations
│   │   ├── es.js           # Spanish translations
│   │   ├── bg.js           # Bulgarian translations
│   │   └── index.js        # Export convenience file
│   ├── utils/              # Utility functions
│   │   ├── dates.js        # Date formatting utilities
│   │   ├── formatters.js   # Text formatting
│   │   ├── playerUtils.js  # Player data utilities
│   │   ├── search.js       # Search & filtering utilities
│   │   ├── statistics.js   # Statistical functions
│   │   ├── storage.js      # LocalStorage utilities
│   │   ├── ui.js           # UI helper functions
│   │   ├── validation.js   # Data validation
│   │   ├── useTranslation.js # Translation hook
│   │   └── index.js        # Export convenience file
│   ├── App.js              # Main App component
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
└── package.json            # Dependencies and scripts
```

## Architecture Overview

The application follows a clean, modular architecture focusing on separation of concerns:

### Core Concepts

1. **Component-Based UI**: Each UI element is a separate component with its own file
2. **Context-Based State Management**: Uses React Context for global state
3. **Service Layer**: API interactions abstracted through service modules
4. **Utility Functions**: Pure functions for data manipulation and formatting
5. **Internationalization (i18n)**: Translations organized by language
6. **Configuration**: Constants extracted for easy management

### Data Flow

1. User interacts with a component (e.g., ChatInterface)
2. Component calls context methods (e.g., addMessage from SessionContext)
3. Context makes API calls through service layer (e.g., chatService.enhancedSearch)
4. API response processed, updates context state
5. Components re-render with new state
6. Utility functions handle data formatting and transformation

## Key Features

### Multi-Language Support

- Uses LanguageContext for language state
- Translations in locales directory (en.js, pt.js, es.js, bg.js)
- Components access translations via useTranslation hook
- Persistently stored in localStorage

### Chat & Search Experience

- ChatInterface handles user interaction
- Chat history maintained in SessionContext
- Messages and responses formatted consistently
- Player search results displayed inline

### Player Data Visualization

- PlayerDashboard shows summary statistics
- PlayerCompletePage shows detailed player view
- Uses Recharts for data visualization (RadarChart)
- Player metrics standardized through utility functions

### Favorites Management

- User can favorite players for later reference
- FavoritesView provides search and filtering
- Favorites stored in localStorage via FavoritesContext

## State Management

### Context Structure

- **AppProvider**: Main wrapper combining all contexts
- **LanguageContext**: Language selection and translations
- **SessionContext**: Chat session state and player selection
- **UIContext**: UI state (current view, sidebar, onboarding)
- **FavoritesContext**: Favorites management

## Service Layer

### API Interface

- **api.js**: Core fetch wrapper with error handling
- **chatService.js**: Chat and search endpoints
- **playerService.js**: Player data endpoints and utilities
- **appService.js**: Application-level services

## Utility Functions

### Categories

- **dates.js**: Date formatting and calculations
- **formatters.js**: Text formatting utilities
- **playerUtils.js**: Player-specific data helpers
- **search.js**: Search and filtering
- **statistics.js**: Stats calculations
- **storage.js**: localStorage wrappers
- **ui.js**: UI helper functions
- **validation.js**: Data validation

## Getting Started

To understand the codebase when making changes:

1. Start with `src/App.js` to understand the top-level structure
2. Look at individual components in `src/components/`
3. Examine context providers in `src/contexts/` to understand state
4. Check utility functions in `src/utils/` for data processing
5. Review API services in `src/api/` for backend communication

## Development Guidelines

1. **Component Creation**:
   - Create new components in `src/components/`
   - Use existing contexts for state management
   - Keep components focused on a single responsibility

2. **State Management**:
   - Use contexts for global state
   - Use component state for UI-specific state
   - Add new context providers as needed for logical grouping

3. **API Integration**:
   - Add new endpoints to appropriate service file
   - Use the fetchAPI wrapper for consistent error handling
   - Return standardized response objects

4. **Utilities**:
   - Create pure functions (no side effects)
   - Group related functions in the appropriate utility file
   - Document with JSDoc comments

5. **Translations**:
   - Add new translation keys to all language files
   - Use nested objects for organization
   - Access via the useTranslation hook

## Common Patterns

### Component with Context

```jsx
import React from 'react';
import { useTranslation, useSession } from '../contexts';

const MyComponent = () => {
  const { t } = useTranslation();
  const { sessionId } = useSession();
  
  return <div>{t('some.translation.key')}</div>;
};
```

### API Service Call

```jsx
import { chatService } from '../api';

const handleSearch = async () => {
  try {
    const result = await chatService.enhancedSearch({
      query: searchTerm,
      session_id: sessionId
    });
    // Handle result
  } catch (error) {
    // Handle error
  }
};
```

### Using Utility Functions

```jsx
import { filterItems, formatPlayerName } from '../utils';

// Filter a list
const filteredPlayers = filterItems(players, searchTerm, ['name', 'position']);

// Format a value
const displayName = formatPlayerName(player.name);
```