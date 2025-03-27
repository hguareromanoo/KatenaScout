/**
 * Chat API service for KatenaScout frontend
 */
import { fetchAPI } from './api';

/**
 * Service for chat-related API operations
 */
const chatService = {
  /**
   * Send a query to the enhanced search endpoint
   * 
   * This endpoint now handles multiple intents:
   * - player_search: Searching for players based on criteria
   * - player_comparison: Comparing players
   * - explain_stats: Explaining football statistics
   * - casual_conversation: General conversation
   * 
   * @param {Object} params - Search parameters
   * @param {string} params.session_id - The chat session ID
   * @param {string} params.query - The user's query
   * @param {boolean} params.is_follow_up - Whether this is a follow-up query
   * @param {boolean|null} params.satisfaction - User satisfaction (true, false, or null)
   * @param {string} params.language - The language for the response
   * @returns {Promise} - Search results with response appropriate to the detected intent
   */
  enhancedSearch: async (params) => {
    try {
      const response = await fetchAPI('/enhanced_search', {
        method: 'POST',
        body: params,
      });
      
      // Debug logging for comparison response
      if (response && response.comparison) {
        console.log("API RESPONSE - Comparison data received:", {
          in_chat_comparison: response.in_chat_comparison,
          comparison_text_length: response.comparison ? response.comparison.length : 0,
          players_count: response.players ? response.players.length : 0,
          full_response: response
        });
      }
      
      return response;
    } catch (error) {
      console.error('Enhanced search error:', error);
      throw error;
    }
  },
  
  /**
   * Get follow-up suggestions for a chat session
   * 
   * @param {string} sessionId - The chat session ID
   * @param {string} language - The language for suggestions
   * @returns {Promise} - Follow-up suggestions
   */
  getFollowUpSuggestions: async (sessionId, language = 'english') => {
    try {
      return await fetchAPI(`/follow_up_suggestions/${sessionId}?language=${language}`);
    } catch (error) {
      console.error('Error getting follow-up suggestions:', error);
      return { 
        success: false, 
        suggestions: [],
        error: error.message || 'Failed to get follow-up suggestions'
      };
    }
  },
  
  /**
   * Get chat history for a session
   * 
   * @param {string} sessionId - The chat session ID
   * @param {string} language - The language for the chat history
   * @returns {Promise} - Chat history
   */
  getChatHistory: async (sessionId, language = 'english') => {
    try {
      return await fetchAPI(`/chat_history/${sessionId}?language=${language}`);
    } catch (error) {
      console.error('Error getting chat history:', error);
      return { 
        success: false, 
        messages: [],
        error: error.message || 'Failed to get chat history'
      };
    }
  },
  
  /**
   * Get explanation for football statistics
   * 
   * @param {Object} params - Stats parameters
   * @param {Array} params.stats - Array of statistics to explain
   * @param {string} params.session_id - The chat session ID
   * @param {string} params.language - The language for the explanation
   * @returns {Promise} - Stats explanation
   */
  explainStats: async (params) => {
    try {
      return await fetchAPI('/explain_stats', {
        method: 'POST',
        body: params,
      });
    } catch (error) {
      console.error('Error explaining stats:', error);
      throw error;
    }
  },
  
  /**
   * Get available languages for the application
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
  }
};

export default chatService;