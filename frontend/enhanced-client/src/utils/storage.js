/**
 * Storage utility functions for working with localStorage
 */

/**
 * Gets a value from localStorage with optional parsing
 * 
 * @param {string} key - The key to get from localStorage
 * @param {*} defaultValue - The default value to return if the key doesn't exist
 * @param {boolean} parseJson - Whether to parse the value as JSON
 * @returns {*} - The value from localStorage or the default value
 */
export const getFromStorage = (key, defaultValue = null, parseJson = false) => {
  try {
    const value = localStorage.getItem(key);
    if (value === null) return defaultValue;
    return parseJson ? JSON.parse(value) : value;
  } catch (error) {
    console.error(`Error reading ${key} from localStorage:`, error);
    return defaultValue;
  }
};

/**
 * Sets a value in localStorage with optional stringifying
 * 
 * @param {string} key - The key to set in localStorage
 * @param {*} value - The value to set
 * @param {boolean} stringify - Whether to stringify the value as JSON
 */
export const setToStorage = (key, value, stringify = false) => {
  try {
    const valueToStore = stringify ? JSON.stringify(value) : value;
    localStorage.setItem(key, valueToStore);
  } catch (error) {
    console.error(`Error writing ${key} to localStorage:`, error);
  }
};

/**
 * Removes a value from localStorage
 * 
 * @param {string} key - The key to remove from localStorage
 */
export const removeFromStorage = (key) => {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error(`Error removing ${key} from localStorage:`, error);
  }
};