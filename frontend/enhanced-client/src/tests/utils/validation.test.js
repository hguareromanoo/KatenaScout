/**
 * Tests for validation utility functions
 */
import { 
  isEmpty, isNumber, isValidUrl, isValidPlayer, validateSearchQuery 
} from '../../utils/validation';

describe('isEmpty', () => {
  test('should return true for null', () => {
    expect(isEmpty(null)).toBe(true);
  });

  test('should return true for undefined', () => {
    expect(isEmpty(undefined)).toBe(true);
  });

  test('should return true for empty string', () => {
    expect(isEmpty('')).toBe(true);
  });

  test('should return true for empty array', () => {
    expect(isEmpty([])).toBe(true);
  });

  test('should return true for empty object', () => {
    expect(isEmpty({})).toBe(true);
  });

  test('should return false for non-empty string', () => {
    expect(isEmpty('hello')).toBe(false);
  });

  test('should return false for non-empty array', () => {
    expect(isEmpty([1, 2, 3])).toBe(false);
  });

  test('should return false for non-empty object', () => {
    expect(isEmpty({ key: 'value' })).toBe(false);
  });
});

describe('isNumber', () => {
  test('should return true for number type', () => {
    expect(isNumber(42)).toBe(true);
  });

  test('should return true for valid number string', () => {
    expect(isNumber('42')).toBe(true);
  });

  test('should return true for decimal', () => {
    expect(isNumber(3.14)).toBe(true);
  });

  test('should return true for decimal string', () => {
    expect(isNumber('3.14')).toBe(true);
  });

  test('should return false for non-numeric string', () => {
    expect(isNumber('hello')).toBe(false);
  });

  test('should return false for array', () => {
    expect(isNumber([1, 2, 3])).toBe(false);
  });

  test('should return false for object', () => {
    expect(isNumber({ key: 'value' })).toBe(false);
  });

  test('should return false for NaN', () => {
    expect(isNumber(NaN)).toBe(false);
  });
});

describe('isValidUrl', () => {
  test('should return true for http URL', () => {
    expect(isValidUrl('http://example.com')).toBe(true);
  });

  test('should return true for https URL', () => {
    expect(isValidUrl('https://example.com')).toBe(true);
  });

  test('should return true for URL with path', () => {
    expect(isValidUrl('https://example.com/path')).toBe(true);
  });

  test('should return true for URL without protocol', () => {
    expect(isValidUrl('example.com')).toBe(true);
  });

  test('should return false for invalid URL', () => {
    expect(isValidUrl('not a url')).toBe(false);
  });

  test('should return false for empty string', () => {
    expect(isValidUrl('')).toBe(false);
  });

  test('should return false for null', () => {
    expect(isValidUrl(null)).toBe(false);
  });
});

describe('isValidPlayer', () => {
  test('should return true for valid player object with name', () => {
    expect(isValidPlayer({ name: 'John Doe' })).toBe(true);
  });

  test('should return false for player without name', () => {
    expect(isValidPlayer({ id: '123' })).toBe(false);
  });

  test('should return false for empty object', () => {
    expect(isValidPlayer({})).toBe(false);
  });

  test('should return false for null', () => {
    expect(isValidPlayer(null)).toBe(false);
  });

  test('should return false for non-object', () => {
    expect(isValidPlayer('not an object')).toBe(false);
  });
});

describe('validateSearchQuery', () => {
  test('should return valid for query with sufficient length', () => {
    const result = validateSearchQuery('midfielder with good passing');
    expect(result.isValid).toBe(true);
    expect(result.message).toBe('');
  });

  test('should return invalid for short query', () => {
    const result = validateSearchQuery('mi');
    expect(result.isValid).toBe(false);
    expect(result.message).toBe('Search query must be at least 3 characters');
  });

  test('should return invalid for empty query', () => {
    const result = validateSearchQuery('');
    expect(result.isValid).toBe(false);
    expect(result.message).toBe('Search query is required');
  });

  test('should return invalid for null query', () => {
    const result = validateSearchQuery(null);
    expect(result.isValid).toBe(false);
    expect(result.message).toBe('Search query is required');
  });
});