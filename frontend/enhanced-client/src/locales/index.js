/**
 * Exports all language translations
 */
import en from './en';
import pt from './pt';
import es from './es';
import bg from './bg';

// Export all available translations
export default {
  english: en,
  portuguese: pt,
  spanish: es,
  bulgarian: bg
};

// Fallback language
export const DEFAULT_LANGUAGE = 'english';

// Available language options
export const AVAILABLE_LANGUAGES = [
  { id: 'english', name: 'English', native_name: 'English', code: 'en', flag: '🇬🇧' },
  { id: 'portuguese', name: 'Portuguese', native_name: 'Português', code: 'pt', flag: '🇧🇷' },
  { id: 'spanish', name: 'Spanish', native_name: 'Español', code: 'es', flag: '🇪🇸' },
  { id: 'bulgarian', name: 'Bulgarian', native_name: 'Български', code: 'bg', flag: '🇧🇬' }
];