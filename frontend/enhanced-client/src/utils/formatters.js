/**
 * Utility functions for formatting text and data
 */

/**
 * Formats metric names for display by replacing underscores with spaces 
 * and capitalizing each word
 * 
 * @param {string} key - The metric key/name to format
 * @returns {string} - The formatted metric name
 */
export const formatMetricName = (key) => {
  if (!key) return '';
  
  return key
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

/**
 * Formats player names with proper spacing between capital letters
 * 
 * @param {string} name - The player name to format
 * @returns {string} - The formatted player name
 */
export const formatPlayerName = (name) => {
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