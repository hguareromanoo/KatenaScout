/**
 * Common API utilities for KatenaScout
 */
import { API_URL } from '../config';

/**
 * Generic fetch wrapper with error handling
 * 
 * @param {string} endpoint - API endpoint to call
 * @param {Object} options - Fetch options
 * @returns {Promise} - Fetch response
 */
export const fetchAPI = async (endpoint, options = {}) => {
  try {
    const url = `${API_URL}${endpoint}`;
    
    // Default options for all API calls
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    
    // Merge options
    const fetchOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...(options.headers || {}),
      },
    };
    
    // Add request body if provided
    if (options.body) {
      fetchOptions.body = typeof options.body === 'string' ? options.body : JSON.stringify(options.body);
    }
    
    // Make the API call
    const response = await fetch(url, fetchOptions);
    
    return response;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};