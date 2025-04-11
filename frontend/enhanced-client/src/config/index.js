/**
 * Configuration constants for KatenaScout application
 */

// API URL Configuration - Change this to switch between local and production backends
// export const API_URL = 'http://localhost:5000'; // Local development
export const API_URL = 'https://katenascout-09ho.onrender.com'; // Production

// Default language if none is stored
export const DEFAULT_LANGUAGE = 'english';

// Available languages 
export const AVAILABLE_LANGUAGES = [
  { id: 'english', name: 'English', native_name: 'English', code: 'en', flag: '🇬🇧' },
  { id: 'portuguese', name: 'Portuguese', native_name: 'Português', code: 'pt', flag: '🇧🇷' },
  { id: 'spanish', name: 'Spanish', native_name: 'Español', code: 'es', flag: '🇪🇸' },
  { id: 'bulgarian', name: 'Bulgarian', native_name: 'Български', code: 'bg', flag: '🇧🇬' }
];