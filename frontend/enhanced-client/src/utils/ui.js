/**
 * UI utility functions
 */

/**
 * Get class names conditionally
 * Similar to the 'classnames' library but simpler
 * 
 * @param {Object} classMap - Object mapping class names to boolean conditions
 * @returns {string} - Combined class names where condition is true
 */
export const classNames = (classMap) => {
  if (!classMap || typeof classMap !== 'object') return '';
  
  return Object.entries(classMap)
    .filter(([_, condition]) => Boolean(condition))
    .map(([className]) => className)
    .join(' ');
};

/**
 * Truncate text to a maximum length with ellipsis
 * 
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length (default: 100)
 * @returns {string} - Truncated text
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text || typeof text !== 'string') return '';
  
  if (text.length <= maxLength) return text;
  
  return text.substring(0, maxLength) + '...';
};

/**
 * Create color style based on value compared to maximum
 * Used for stat bars and indicators
 * 
 * @param {number} value - Current value
 * @param {number} max - Maximum value (default: 100)
 * @returns {Object} - Object with color class and style properties
 */
export const getValueColor = (value, max = 100) => {
  if (!value || typeof value !== 'number') return { color: 'bg-gray-500', style: { width: '0%' } };
  
  // Normalize value to percentage
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  
  // Determine color based on percentage
  let color = 'bg-green-500';
  if (percentage < 30) color = 'bg-red-500';
  else if (percentage < 60) color = 'bg-yellow-500';
  
  return {
    color,
    style: { width: `${percentage}%` }
  };
};

/**
 * Format a number as a percentage
 * 
 * @param {number} value - Value to format
 * @param {number} total - Total value to calculate percentage from
 * @param {number} decimals - Number of decimal places (default: 0)
 * @returns {string} - Formatted percentage string
 */
export const formatPercentage = (value, total, decimals = 0) => {
  if (typeof value !== 'number' || typeof total !== 'number' || total === 0) {
    return '0%';
  }
  
  const percentage = (value / total) * 100;
  return `${percentage.toFixed(decimals)}%`;
};

/**
 * Detect if device is mobile based on screen width
 * 
 * @returns {boolean} - True if mobile device
 */
export const isMobile = () => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth < 768;
};

/**
 * Create a debounced function that delays invoking func
 * 
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} - Debounced function
 */
export const debounce = (func, wait = 300) => {
  let timeout;
  
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};