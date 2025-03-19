/**
 * Main application provider component that combines all contexts
 */
import React, { createContext, useState, useEffect, useContext } from 'react';
import { LanguageProvider } from './LanguageContext';
import { SessionProvider } from './SessionContext';
import { UIProvider } from './UIContext';
import { ComparisonProvider } from './ComparisonContext';
import { getFromStorage, setToStorage } from '../utils/storage';

// Create a favorites context
const FavoritesContext = createContext();

/**
 * Provider for favorites management
 */
export const FavoritesProvider = ({ children }) => {
  // Initialize favorites from localStorage
  const [favorites, setFavorites] = useState(() => {
    return getFromStorage('favorites', [], true);
  });

  // Save favorites to localStorage when they change
  useEffect(() => {
    setToStorage('favorites', favorites, true);
  }, [favorites]);

  // Check if a player is in favorites
  const isPlayerFavorite = (player) => {
    if (!player) return false;
    return favorites.some(f => 
      (f.id && player.id && f.id === player.id) || 
      (f.name && player.name && f.name === player.name)
    );
  };

  // Toggle favorite status
  const toggleFavorite = (player) => {
    if (!player) return;
    
    if (isPlayerFavorite(player)) {
      setFavorites(favorites.filter(f => 
        (f.id && player.id && f.id !== player.id) || 
        (f.name && player.name && f.name !== player.name)
      ));
    } else {
      setFavorites([...favorites, player]);
    }
  };

  // Value provided by the context
  const value = {
    favorites,
    isPlayerFavorite,
    toggleFavorite
  };

  return (
    <FavoritesContext.Provider value={value}>
      {children}
    </FavoritesContext.Provider>
  );
};

/**
 * Custom hook to use the favorites context
 */
export const useFavorites = () => {
  const context = useContext(FavoritesContext);
  if (!context) {
    throw new Error('useFavorites must be used within a FavoritesProvider');
  }
  return context;
};

/**
 * Main app provider that combines all contexts
 */
const AppProvider = ({ children }) => {
  return (
    <UIProvider>
      <LanguageProvider>
        <FavoritesProvider>
          <SessionProvider>
            <ComparisonProvider>
              {children}
            </ComparisonProvider>
          </SessionProvider>
        </FavoritesProvider>
      </LanguageProvider>
    </UIProvider>
  );
};

export default AppProvider;