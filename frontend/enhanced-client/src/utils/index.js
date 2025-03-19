/**
 * Export all utility functions
 */

// Export formatters
export { formatMetricName, formatPlayerName } from './formatters';

// Export storage utilities
export { getFromStorage, setToStorage, removeFromStorage } from './storage';

// Export date utilities
export { formatDate, calculateAge, formatDateRange } from './dates';

// Export validation utilities
export { isEmpty, isNumber, isValidUrl, isValidPlayer, validateSearchQuery } from './validation';

// Export UI utilities
export { 
  classNames, truncateText, getValueColor, formatPercentage, isMobile, debounce 
} from './ui';

// Export search utilities
export { 
  filterItems, sortItems, groupItems, extractUniqueValues 
} from './search';

// Export statistics utilities
export { 
  statsToMetrics, calculateScore, comparePlayerStats 
} from './statistics';

// Export player utilities
export {
  playerStatsToMetrics, getPrimaryPosition, formatPositions,
  formatPlayerAge, getPlayerImageUrl, comparePlayersData
} from './playerUtils';

// Re-export useTranslation hook for convenience
export { useTranslation } from './useTranslation';