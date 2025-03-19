/**
 * Validation utility functions
 */

/**
 * Check if a value is empty (null, undefined, empty string, empty array, or empty object)
 * 
 * @param {*} value - Value to check
 * @returns {boolean} - True if empty, false otherwise
 */
export const isEmpty = (value) => {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string') return value.trim() === '';
  if (Array.isArray(value)) return value.length === 0;
  if (typeof value === 'object') return Object.keys(value).length === 0;
  return false;
};

/**
 * Check if a value is a number
 * 
 * @param {*} value - Value to check
 * @returns {boolean} - True if number, false otherwise
 */
export const isNumber = (value) => {
  if (typeof value === 'number') return !isNaN(value);
  if (typeof value === 'string') return !isNaN(parseFloat(value)) && isFinite(value);
  return false;
};

/**
 * Check if a string is a valid URL
 * 
 * @param {string} url - URL to check
 * @returns {boolean} - True if valid URL, false otherwise
 */
export const isValidUrl = (url) => {
  try {
    if (!url || typeof url !== 'string') return false;
    
    // Simple regex for URL validation
    const pattern = /^(https?:\/\/)?([\w.-]+)\.([a-z]{2,})(\/[^\s]*)?$/i;
    return pattern.test(url);
  } catch (error) {
    return false;
  }
};

/**
 * Check if a player object has valid required data
 * 
 * @param {Object} player - Player object to validate
 * @returns {boolean} - True if valid, false otherwise
 */
export const isValidPlayer = (player) => {
  // Basic validation
  if (!player || typeof player !== 'object') return false;
  
  // Check for mandatory property - name
  if (!player.name) return false;
  
  // Check for valid player ID (at least one of these should exist)
  const hasValidId = 
    (player.id !== undefined && player.id !== null) ||
    (player.wyId !== undefined && player.wyId !== null) ||
    (player.player_id !== undefined && player.player_id !== null);
  
  // Check for basic player information
  const hasBasicInfo = 
    player.positions || 
    player.age || 
    player.nationality || 
    player.height || 
    player.weight || 
    player.value || 
    player.foot;
  
  // Check for stats object (can be empty but should exist)
  const hasStats = player.stats && typeof player.stats === 'object';
  
  // Player is valid if it has a name and at least some additional data
  return hasValidId && (hasBasicInfo || hasStats);
};

/**
 * Validate a search query
 * 
 * @param {string} query - Search query to validate
 * @returns {Object} - Validation result with isValid and message properties
 */
export const validateSearchQuery = (query) => {
  if (!query || typeof query !== 'string') {
    return { isValid: false, message: 'Search query is required' };
  }
  
  if (query.trim().length < 3) {
    return { isValid: false, message: 'Search query must be at least 3 characters' };
  }
  
  return { isValid: true, message: '' };
};