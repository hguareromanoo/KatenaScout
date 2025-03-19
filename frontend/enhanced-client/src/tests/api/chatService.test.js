/**
 * Tests for chat service
 */
import chatService from '../../api/chatService';
import * as api from '../../api/api';

// Mock the fetchAPI function
jest.mock('../../api/api', () => ({
  fetchAPI: jest.fn()
}));

describe('chatService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('enhancedSearch', () => {
    test('should call fetchAPI with correct parameters', async () => {
      const mockResponse = { success: true, data: 'test' };
      api.fetchAPI.mockResolvedValueOnce(mockResponse);

      const params = {
        session_id: 'test-session',
        query: 'find midfielders',
        is_follow_up: false,
        satisfaction: null,
        language: 'english'
      };

      const result = await chatService.enhancedSearch(params);

      expect(api.fetchAPI).toHaveBeenCalledWith('/enhanced_search', {
        method: 'POST',
        body: JSON.stringify(params)
      });
      expect(result).toEqual(mockResponse);
    });

    test('should handle errors', async () => {
      const error = new Error('API error');
      api.fetchAPI.mockRejectedValueOnce(error);

      const params = {
        session_id: 'test-session',
        query: 'find midfielders'
      };

      await expect(chatService.enhancedSearch(params)).rejects.toThrow('API error');
    });
  });

  describe('getFollowUpSuggestions', () => {
    test('should call fetchAPI with correct parameters', async () => {
      const mockResponse = { success: true, suggestions: ['suggestion1', 'suggestion2'] };
      api.fetchAPI.mockResolvedValueOnce(mockResponse);

      const sessionId = 'test-session';
      const result = await chatService.getFollowUpSuggestions(sessionId);

      expect(api.fetchAPI).toHaveBeenCalledWith(`/follow_up_suggestions/${sessionId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getChatHistory', () => {
    test('should call fetchAPI with correct parameters', async () => {
      const mockResponse = { success: true, messages: [] };
      api.fetchAPI.mockResolvedValueOnce(mockResponse);

      const sessionId = 'test-session';
      const result = await chatService.getChatHistory(sessionId);

      expect(api.fetchAPI).toHaveBeenCalledWith(`/chat_history/${sessionId}`);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('explainStats', () => {
    test('should call fetchAPI with correct parameters', async () => {
      const mockResponse = { success: true, explanations: {} };
      api.fetchAPI.mockResolvedValueOnce(mockResponse);

      const params = {
        stat: 'xG',
        language: 'english'
      };

      const result = await chatService.explainStats(params);

      expect(api.fetchAPI).toHaveBeenCalledWith('/explain_stats', {
        method: 'POST',
        body: JSON.stringify(params)
      });
      expect(result).toEqual(mockResponse);
    });
  });
});