/**
 * Application services for KatenaScout frontend
 */
import { fetchAPI } from './api';

/**
 * Service for application-related operations
 */
const appService = {
  /**
   * Get available languages
   * 
   * @returns {Promise} - Available languages
   */
  getLanguages: async () => {
    try {
      return await fetchAPI('/languages');
    } catch (error) {
      console.error('Error getting languages:', error);
      // Return default languages as fallback
      return {
        success: false,
        languages: {
          english: { code: 'en', name: 'English', native_name: 'English' },
          portuguese: { code: 'pt', name: 'Portuguese', native_name: 'Português' },
          spanish: { code: 'es', name: 'Spanish', native_name: 'Español' },
          bulgarian: { code: 'bg', name: 'Bulgarian', native_name: 'Български' }
        },
        default: 'english'
      };
    }
  },
  
  /**
   * Check API health
   * 
   * @returns {Promise} - API health status
   */
  checkHealth: async () => {
    try {
      const response = await fetchAPI('/health');
      return { 
        status: 'online', 
        version: response.message || 'Unknown version',
        data: response
      };
    } catch (error) {
      console.error('API health check failed:', error);
      return { 
        status: 'offline', 
        error: error.message,
        message: 'Unable to connect to KatenaScout backend'
      };
    }
  },
  
  /**
   * Get application version
   * 
   * @returns {string} - Application version
   */
  getVersion: () => {
    return '1.0.0'; // Hardcoded for now, could be retrieved from package.json or API
  },
  
  /**
   * Handle backend errors in a standard way
   * 
   * @param {Error} error - The error object
   * @param {string} defaultMessage - Default message to show if error doesn't have one
   * @param {string} language - Language for the error message
   * @returns {Object} - Standardized error response
   */
  handleError: (error, defaultMessage = 'An error occurred', language = 'english') => {
    console.error('API error:', error);
    
    // Try to extract error details if available
    let errorMessage = defaultMessage;
    let errorCode = 'unknown_error';
    
    if (error.response) {
      // The request was made and the server responded with an error status
      errorMessage = error.response.message || error.response.error || defaultMessage;
      errorCode = error.response.error || 'server_error';
    } else if (error.message) {
      // The request was made but no response was received
      errorMessage = error.message;
      errorCode = 'network_error';
    }
    
    return {
      success: false,
      error: errorCode,
      message: errorMessage,
      language
    };
  }
};

export default appService;