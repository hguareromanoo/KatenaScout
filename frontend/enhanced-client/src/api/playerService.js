/**
 * Player API service for KatenaScout frontend
 */
import { fetchAPI } from './api';
import { API_URL } from '../config';

/**
 * Service for player-related API operations
 */
const playerService = {
  /**
   * Get player comparison data
   * 
   * @param {Object} params - Comparison parameters
   * @param {Array} params.player_ids - Array of player IDs to compare
   * @param {string} params.session_id - The chat session ID
   * @param {string} params.language - Language for the comparison
   * @returns {Promise} - Comparison results
   */
  /**
   * Compare two players with detailed metric-by-metric analysis
   * 
   * @param {Object} params - Comparison parameters
   * @param {Array} params.player_ids - Array of two player IDs to compare
   * @param {string} params.session_id - The chat session ID
   * @param {string} params.language - Language for the comparison
   * @param {Object} params.search_weights - Optional weights from search query
   * @param {boolean} params.include_ai_analysis - Whether to include AI-generated analysis text
   * @returns {Promise} - Detailed comparison results
   */
  comparePlayer: async (params) => {
    try {
      return await fetchAPI('/player_comparison', {
        method: 'POST',
        body: params,
      });
    } catch (error) {
      console.error('Player comparison error:', error);
      throw error;
    }
  },
  
  /**
   * Generate tactical analysis for two players in a specific style and formation
   * 
   * @param {Object} params - Analysis parameters
   * @param {Array} params.player_ids - Array of two player IDs to compare
   * @param {string} params.session_id - The chat session ID
   * @param {string} params.original_query - Original search query for context (not used with player_comparison)
   * @param {string} params.playing_style - Tactical style (e.g., "Tiki-Taka")
   * @param {string} params.formation - Formation (e.g., "4-3-3")
   * @param {string} params.language - Language for the analysis
   * @returns {Promise} - Tactical analysis results
   */
  generateTacticalAnalysis: async (params) => {
    try {
      console.log("Calling player_comparison endpoint with language:", params.language);
      // Use the player_comparison endpoint with include_ai_analysis flag
      const analysisParams = {
        player_ids: params.player_ids,
        session_id: params.session_id,
        language: params.language,
        include_ai_analysis: true,
        playing_style: params.playing_style,
        formation: params.formation
      };
      
      // If complete player objects are provided, include them
      if (params.players) {
        analysisParams.players = params.players;
      }
      
      const result = await fetchAPI('/player_comparison', {
        method: 'POST',
        body: analysisParams,
      });
      
      // Format the response to match the expected format from tactical_analysis
      if (result.success) {
        return {
          success: true,
          tactical_analysis: result.comparison || "",
          tactical_data: {
            player1_name: result.players[0]?.name,
            player2_name: result.players[1]?.name,
            style_display_name: params.playing_style.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
            formation: params.formation,
            style_description: ""
          },
          players: result.players || []
        };
      }
      return result;
    } catch (error) {
      console.error('Tactical analysis error:', error);
      throw error;
    }
  },
  
  /**
   * Get player image URL - uses imageDataURL if available
   * 
   * @param {Object|string} playerOrId - Player object or player ID
   * @returns {string} - Image URL or null
   */
  getPlayerImageUrl: (playerOrId) => {
    // If no player, return null
    if (!playerOrId) return null;
    
    // If player object is provided
    if (typeof playerOrId === 'object') {
      // Try multiple image fields in order of preference
      
      // 1. Check for data URLs (they contain the image data directly)
      if (playerOrId.imageDataURL && playerOrId.imageDataURL.startsWith('data:image')) {
        return playerOrId.imageDataURL;
      }
      
      // 2. Check if image_url is an absolute URL
      if (playerOrId.image_url) {
        // If it's already an absolute URL, use it directly
        if (playerOrId.image_url.startsWith('http')) {
          return playerOrId.image_url;
        }
        
        // If it's a relative URL, prepend the API_URL
        // Make sure to handle cases where image_url starts with /
        const imagePath = playerOrId.image_url.startsWith('/') 
          ? playerOrId.image_url 
          : `/${playerOrId.image_url}`;
        
        return `${API_URL}${imagePath}`;
      }
      
      // 3. Try alternative image fields
      if (playerOrId.photoUrl) {
        return playerOrId.photoUrl;
      }
      
      if (playerOrId.image) {
        return playerOrId.image;
      }
      
      // 4. Use player ID to construct URL to backend endpoint
      // Get ID for API endpoint - try multiple ID fields
      const playerId = playerOrId.wyId || playerOrId.id || playerOrId.player_id;
      if (!playerId) return null;
      
      // Add player's has_image flag in logging for debugging
      console.log(`Getting image for player ${playerId} (has_image: ${playerOrId.has_image})`);
      
      // Use API endpoint with cache-busting parameter to prevent browser caching issues
      return `${API_URL}/player-image/${playerId}?t=${Date.now()}`;
    }
    
    // If string ID is provided, use API endpoint
    if (typeof playerOrId === 'string' || typeof playerOrId === 'number') {
      return `${API_URL}/player-image/${playerOrId}?t=${Date.now()}`;
    }
    
    return null;
  },
  
  /**
   * Format player position
   * 
   * @param {Array|string} positions - Player position(s)
   * @returns {string} - Formatted position string
   */
  formatPosition: (positions) => {
    if (!positions) return '';
    
    if (Array.isArray(positions)) {
      return positions.join(', ');
    }
    
    return positions;
  },
  
  /**
   * Format player value with currency symbol
   * 
   * @param {string|number} value - Player market value
   * @returns {string} - Formatted value string
   */
  formatValue: (value) => {
    if (!value) return 'N/A';
    
    // If value contains "€" or "$", return as is
    if (typeof value === 'string' && (value.includes('€') || value.includes('$'))) {
      return value;
    }
    
    // Try to parse as number and format with € symbol
    const numValue = parseFloat(value);
    if (!isNaN(numValue)) {
      return `€${numValue.toLocaleString()}`;
    }
    
    // Return original value as fallback
    return value;
  },
  
  /**
   * Get complete player data by ID
   * 
   * @param {string} playerId - The player ID
   * @param {string} language - Language for the player data
   * @returns {Promise} - Player data
   */
  getPlayerById: async (playerId, language = 'english') => {
    try {
      // Use enhanced_search to get player by ID
      // This leverages the unified backend's player search capabilities
      const response = await fetchAPI('/enhanced_search', {
        method: 'POST',
        body: {
          session_id: `player-detail-${Date.now()}`,
          query: `Get details for player with ID ${playerId}`,
          is_follow_up: false,
          language
        }
      });
      
      // Check if we got player data back
      if (response.success && response.players && response.players.length > 0) {
        // Find the matching player
        const player = response.players.find(p => p.id === playerId || p.wyId === playerId);
        if (player) {
          return {
            success: true,
            player
          };
        }
      }
      
      // If we couldn't find the player, return an error
      return {
        success: false,
        error: 'Player not found',
        message: `No player found with ID ${playerId}`
      };
    } catch (error) {
      console.error('Error getting player by ID:', error);
      return {
        success: false,
        error: error.message || 'Failed to get player data',
        message: 'An error occurred while retrieving player data'
      };
    }
  },
  
  /**
   * Get complete player data with ALL available stats - DEPRECATED
   * This method is no longer needed as complete profile data is included in the player object
   * 
   * @deprecated Use the complete_profile data included in the player object instead
   * @param {string} playerId - The player ID
   * @param {string} sessionId - Session ID for context
   * @param {string} language - Language for the player data
   * @returns {Promise} - Complete player data
   */
  getCompletePlayer: async (playerId, sessionId = null, language = 'english') => {
    console.warn('getCompletePlayer is deprecated - complete profile data is now included in player objects');
    
    try {
      // Return success with null player to trigger fallback to existing player data
      return {
        success: false,
        error: 'API endpoint deprecated',
        message: 'Complete player data is now included in search results'
      };
    } catch (error) {
      console.error('Error in deprecated getCompletePlayer method:', error);
      return {
        success: false,
        error: error.message || 'Failed to get complete player data',
        message: 'An error occurred while retrieving complete player data'
      };
    }
  }
};

export default playerService;