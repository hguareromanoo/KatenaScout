/**
 * Language context for managing app translations
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import translations, { DEFAULT_LANGUAGE } from '../locales';
import { getFromStorage, setToStorage } from '../utils/storage';

// Create the context
const LanguageContext = createContext();

/**
 * Provider component for language context
 */
export const LanguageProvider = ({ children }) => {
  // Initialize language from localStorage or default
  const [currentLanguage, setLanguage] = useState(() => {
    return getFromStorage('language', DEFAULT_LANGUAGE);
  });

  // Update localStorage when language changes
  useEffect(() => {
    setToStorage('language', currentLanguage);
  }, [currentLanguage]);

  /**
   * Get a translation by key path (e.g. 'chat.welcomeTitle')
   */
  const t = (keyPath) => {
    try {
      // Get the current language translations or fallback to default
      const langData = translations[currentLanguage] || translations[DEFAULT_LANGUAGE];
      
      // Split the key path and traverse the translations object
      const keys = keyPath.split('.');
      let result = langData;
      
      for (const key of keys) {
        if (result && result[key] !== undefined) {
          result = result[key];
        } else {
          // Key not found in current language, try fallback
          if (currentLanguage !== DEFAULT_LANGUAGE) {
            let fallback = translations[DEFAULT_LANGUAGE];
            for (const fbKey of keys) {
              if (fallback && fallback[fbKey] !== undefined) {
                fallback = fallback[fbKey];
              } else {
                // Return the key as fallback
                return keyPath;
              }
            }
            return fallback;
          }
          // Return the key as last resort
          return keyPath;
        }
      }
      
      return result;
    } catch (error) {
      console.error('Translation error:', error);
      return keyPath;
    }
  };

  // Value provided by the context
  const value = {
    currentLanguage,
    setLanguage,
    t
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

/**
 * Custom hook to use the language context
 */
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export default LanguageContext;