/**
 * Export all contexts and hooks for easy access
 */

// Export the main AppProvider
export { default as AppProvider } from './AppProvider';

// Export individual context providers
export { LanguageProvider, useLanguage } from './LanguageContext';
export { FavoritesProvider, useFavorites } from './AppProvider';
export { SessionProvider, useSession } from './SessionContext';
export { UIProvider, useUI } from './UIContext';
export { ComparisonProvider, useComparison } from './ComparisonContext';

// Export the useTranslation hook from utils for convenience
export { useTranslation } from '../utils/useTranslation';