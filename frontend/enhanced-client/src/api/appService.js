/**
 * Application services for KatenaScout frontend
 */
import { fetchAPI } from '../utils/apiUtils';
/**
 * Application services for KatenaScout frontend
 */

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
      const response = await fetchAPI('/languages', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        return data.languages || [];
      }
      
      return [];
    } catch (error) {
      console.error('Error fetching languages:', error);
      return [];
    }
  },
  
  /**
   * Check API health
   * 
   * @returns {Promise} - API health status
   */
  checkHealth: async () => {
    try {
      const response = await fetchAPI('/health', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        return data;
      }
      
      return { status: 'error', message: 'API is not responding properly' };
    } catch (error) {
      console.error('Error checking health:', error);
      return { status: 'error', message: 'Could not connect to API' };
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
   * Generate a scout report for a player
   * 
   * @param {Object} params - Report parameters
   * @param {string} params.session_id - The chat session ID
   * @param {string} params.player_id - The player ID
   * @param {string} params.language - Language for the report (pt, en, es, bg)
   * @param {string} params.format - Format of the report (html, pdf)
   * @returns {Promise} - Scout report content or URL
   */
  generateScoutReport: async (params) => {
    try {
      const response = await fetchAPI('/scout_report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/html, application/pdf',
        },
        body: JSON.stringify(params)
      });
      
      if (!response.ok) {
        throw new Error(`Failed to generate report: ${response.status} ${response.statusText}`);
      }
      
      // Return content based on format requested
      if (params.format === 'pdf') {
        return await response.blob();
      } else {
        return await response.text();
      }
    } catch (error) {
      console.error('Error generating scout report:', error);
      throw error;
    }
  },
  
  /**
   * Get a scout report for a player via GET request
   * 
   * @param {string} player_id - The player ID
   * @param {Object} params - Additional parameters
   * @param {string} params.session_id - The chat session ID
   * @param {string} params.language - Language for the report (pt, en, es, bg)
   * @param {string} params.format - Format of the report (html, pdf)
   * @returns {Promise} - Scout report content or URL
   */
  getScoutReport: async (player_id, params = {}) => {
    try {
      const queryParams = new URLSearchParams({
        session_id: params.session_id || '',
        language: params.language || 'en',
        format: params.format || 'html'
      }).toString();
      
      const response = await fetchAPI(`/scout_report/${player_id}?${queryParams}`, {
        method: 'GET',
        headers: {
          'Accept': params.format === 'pdf' ? 'application/pdf' : 'text/html',
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to get report: ${response.status} ${response.statusText}`);
      }
      
      // Return content based on format requested
      if (params.format === 'pdf') {
        return await response.blob();
      } else {
        return await response.text();
      }
    } catch (error) {
      console.error(`Error getting scout report for player ${player_id}:`, error);
      throw error;
    }
  },
  
  /**
   * Search for players by name directly (without LLM processing)
   * 
   * @param {string} query - Player name to search for
   * @param {Object} options - Search options
   * @param {number} options.limit - Maximum number of results to return
   * @returns {Promise} - Search results
   */
  // Update the searchPlayersByName function
// Inside appService.js, update searchPlayersByName
searchPlayersByName: async (query, options = {}) => {
  try {
    const { limit = 15 } = options;
    
    // Use the direct search endpoint
    const queryParams = new URLSearchParams({
      query,
      limit
    }).toString();
    
    const response = await fetchAPI(`/players/search?${queryParams}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      }
    });
    
    try {
      const data = await response.json();
      
      if (data.success && Array.isArray(data.players)) {
        return data.players;
      }
      
      // If the API returns data in a different format
      if (Array.isArray(data)) {
        return data;
      }
      
      return [];
    } catch (jsonError) {
      console.error('Error parsing JSON response:', jsonError);
      return [];
    }
  } catch (error) {
    console.error('Error searching players by name:', error);
    return [];
  }
},
  
  /**
   * Search for players with advanced query processing (with LLM)
   * 
   * @param {string} query - The search query
   * @param {Object} options - Search options
   * @param {string} options.session_id - Session ID for conversation memory
   * @param {boolean} options.is_follow_up - Whether this is a follow-up to previous query
   * @param {boolean} options.satisfaction - User satisfaction with previous results
   * @param {string} options.language - Language for response
   * @returns {Promise} - Search results with AI-powered recommendations
   */
  searchPlayers: async (query, options = {}) => {
    try {
      const response = await fetchAPI('/enhanced_search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          session_id: options.session_id || '',
          query: query,
          is_follow_up: options.is_follow_up || false,
          satisfaction: options.satisfaction || null,
          language: options.language || 'english'
        })
      });
      
      const data = await response.json();
      
      if (data.success && data.players) {
        return data.players;
      }
      
      return [];
    } catch (error) {
      console.error('Error searching players:', error);
      return [];
    }
  },
  
  /**
   * Handle common API errors with user-friendly messages
   * 
   * @param {Error} error - The error object
   * @param {string} defaultMessage - Default message if none can be determined
   * @param {string} language - Language for message
   * @returns {string} - User-friendly error message
   */
  handleError: (error, defaultMessage = 'An error occurred', language = 'english') => {
    // Network errors
    if (!navigator.onLine) {
      return {
        english: 'Network connection lost. Please check your internet connection and try again.',
        portuguese: 'Conexão de internet perdida. Por favor, verifique sua conexão e tente novamente.',
        spanish: 'Conexión de red perdida. Por favor, compruebe su conexión a internet e inténtelo de nuevo.',
        bulgarian: 'Загубена мрежова връзка. Моля, проверете вашата интернет връзка и опитайте отново.'
      }[language] || defaultMessage;
    }
    
    // API errors
    if (error.message && error.message.includes('429')) {
      return {
        english: 'Too many requests. Please try again in a few moments.',
        portuguese: 'Muitas requisições. Por favor, tente novamente em alguns instantes.',
        spanish: 'Demasiadas solicitudes. Por favor, inténtelo de nuevo en unos momentos.',
        bulgarian: 'Твърде много заявки. Моля, опитайте отново след малко.'
      }[language] || defaultMessage;
    }
    
    // Return default message when no specific case matches
    return defaultMessage;
  }
};

export default appService;