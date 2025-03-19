/**
 * Tests for storage utility functions
 */
import { getFromStorage, setToStorage, removeFromStorage } from '../../utils/storage';

describe('storage utilities', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  describe('getFromStorage', () => {
    test('should get value from localStorage', () => {
      localStorage.getItem.mockReturnValueOnce('test-value');
      
      const value = getFromStorage('test-key');
      
      expect(localStorage.getItem).toHaveBeenCalledWith('test-key');
      expect(value).toBe('test-value');
    });

    test('should return default value when key not found', () => {
      localStorage.getItem.mockReturnValueOnce(null);
      
      const value = getFromStorage('missing-key', 'default-value');
      
      expect(localStorage.getItem).toHaveBeenCalledWith('missing-key');
      expect(value).toBe('default-value');
    });

    test('should parse JSON when parseJson is true', () => {
      localStorage.getItem.mockReturnValueOnce(JSON.stringify({ test: 'data' }));
      
      const value = getFromStorage('json-key', null, true);
      
      expect(localStorage.getItem).toHaveBeenCalledWith('json-key');
      expect(value).toEqual({ test: 'data' });
    });

    test('should return default value when JSON parsing fails', () => {
      localStorage.getItem.mockReturnValueOnce('invalid-json');
      console.error = jest.fn(); // Mock console.error
      
      const value = getFromStorage('invalid-json-key', 'default-value', true);
      
      expect(localStorage.getItem).toHaveBeenCalledWith('invalid-json-key');
      expect(value).toBe('default-value');
      expect(console.error).toHaveBeenCalled();
    });
  });

  describe('setToStorage', () => {
    test('should set value in localStorage', () => {
      setToStorage('test-key', 'test-value');
      
      expect(localStorage.setItem).toHaveBeenCalledWith('test-key', 'test-value');
    });

    test('should stringify value when stringify is true', () => {
      const testObject = { test: 'data' };
      
      setToStorage('json-key', testObject, true);
      
      expect(localStorage.setItem).toHaveBeenCalledWith('json-key', JSON.stringify(testObject));
    });

    test('should handle errors', () => {
      localStorage.setItem.mockImplementationOnce(() => {
        throw new Error('Test error');
      });
      
      console.error = jest.fn(); // Mock console.error
      
      setToStorage('error-key', 'test-value');
      
      expect(console.error).toHaveBeenCalled();
    });
  });

  describe('removeFromStorage', () => {
    test('should remove item from localStorage', () => {
      removeFromStorage('test-key');
      
      expect(localStorage.removeItem).toHaveBeenCalledWith('test-key');
    });

    test('should handle errors', () => {
      localStorage.removeItem.mockImplementationOnce(() => {
        throw new Error('Test error');
      });
      
      console.error = jest.fn(); // Mock console.error
      
      removeFromStorage('error-key');
      
      expect(console.error).toHaveBeenCalled();
    });
  });
});