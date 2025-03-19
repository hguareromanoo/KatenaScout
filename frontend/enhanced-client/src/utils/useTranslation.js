/**
 * Translation hook for easy access to translations
 */
import { useContext } from 'react';
import LanguageContext from '../contexts/LanguageContext';
import translations, { DEFAULT_LANGUAGE } from '../locales';
import { getFromStorage } from './storage';

/**
 * Custom hook for accessing translations
 * 
 * @returns {Object} translation utilities
 */
export const useTranslation = () => {
  // Use language context if available
  try {
    const context = useContext(LanguageContext);
    if (context) {
      return {
        t: context.t,
        currentLanguage: context.currentLanguage,
        setLanguage: context.setLanguage
      };
    }
  } catch (e) {
    // Fallback if used outside context (should be rare)
    console.warn('useTranslation used outside LanguageContext', e);
  }

  // Fallback implementation if used outside of context
  const currentLanguage = getFromStorage('language', DEFAULT_LANGUAGE);
  
  const t = (keyPath) => {
    try {
      const langData = translations[currentLanguage] || translations[DEFAULT_LANGUAGE];
      const keys = keyPath.split('.');
      let result = langData;
      
      for (const key of keys) {
        if (result && result[key] !== undefined) {
          result = result[key];
        } else {
          // Fallback to default language
          if (currentLanguage !== DEFAULT_LANGUAGE) {
            let fallback = translations[DEFAULT_LANGUAGE];
            for (const fbKey of keys) {
              if (fallback && fallback[fbKey] !== undefined) {
                fallback = fallback[fbKey];
              } else {
                return keyPath;
              }
            }
            return fallback;
          }
          return keyPath;
        }
      }
      
      return result;
    } catch (error) {
      console.error('Translation error:', error);
      return keyPath;
    }
  };

  // Warning: this hook doesn't provide setLanguage when used outside context
  return { t, currentLanguage, setLanguage: () => console.warn('setLanguage not available outside LanguageContext') };
};

export default useTranslation;