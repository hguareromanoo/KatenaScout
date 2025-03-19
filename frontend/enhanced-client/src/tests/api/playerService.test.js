/**
 * Tests for player service
 */
import playerService from '../../api/playerService';
import * as api from '../../api/api';
import { API_URL } from '../../config';

// Mock the fetchAPI function
jest.mock('../../api/api', () => ({
  fetchAPI: jest.fn()
}));

describe('playerService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('comparePlayer', () => {
    test('should call fetchAPI with correct parameters', async () => {
      const mockResponse = { success: true, comparison: 'test comparison' };
      api.fetchAPI.mockResolvedValueOnce(mockResponse);

      const params = {
        players: ['player1', 'player2'],
        language: 'english'
      };

      const result = await playerService.comparePlayer(params);

      expect(api.fetchAPI).toHaveBeenCalledWith('/player_comparison', {
        method: 'POST',
        body: JSON.stringify(params)
      });
      expect(result).toEqual(mockResponse);
    });

    test('should handle errors', async () => {
      const error = new Error('API error');
      api.fetchAPI.mockRejectedValueOnce(error);

      const params = {
        players: ['player1', 'player2']
      };

      await expect(playerService.comparePlayer(params)).rejects.toThrow('API error');
    });
  });

  describe('getPlayerImageUrl', () => {
    test('should return correct URL for valid player ID', () => {
      const playerId = 'player123';
      const expected = `${API_URL}/player-image/${playerId}`;
      
      const result = playerService.getPlayerImageUrl(playerId);
      
      expect(result).toEqual(expected);
    });

    test('should return null for null playerId', () => {
      const result = playerService.getPlayerImageUrl(null);
      expect(result).toBeNull();
    });
  });

  describe('formatPosition', () => {
    test('should join array of positions with comma', () => {
      const positions = ['Midfielder', 'Forward'];
      const expected = 'Midfielder, Forward';
      
      const result = playerService.formatPosition(positions);
      
      expect(result).toEqual(expected);
    });

    test('should return string position as is', () => {
      const position = 'Midfielder';
      
      const result = playerService.formatPosition(position);
      
      expect(result).toEqual(position);
    });

    test('should return empty string for empty input', () => {
      expect(playerService.formatPosition(null)).toBe('');
      expect(playerService.formatPosition(undefined)).toBe('');
      expect(playerService.formatPosition([])).toBe('');
    });
  });

  describe('formatValue', () => {
    test('should return value with € symbol if numeric', () => {
      expect(playerService.formatValue(1000000)).toBe('€1,000,000');
    });

    test('should keep € symbol if already present', () => {
      expect(playerService.formatValue('€5M')).toBe('€5M');
    });

    test('should keep $ symbol if present', () => {
      expect(playerService.formatValue('$10M')).toBe('$10M');
    });

    test('should parse numeric string', () => {
      expect(playerService.formatValue('1000000')).toBe('€1,000,000');
    });

    test('should return "N/A" for null or undefined', () => {
      expect(playerService.formatValue(null)).toBe('N/A');
      expect(playerService.formatValue(undefined)).toBe('N/A');
      expect(playerService.formatValue('')).toBe('N/A');
    });

    test('should return original value if not parseable as number', () => {
      expect(playerService.formatValue('Unknown')).toBe('Unknown');
    });
  });
});