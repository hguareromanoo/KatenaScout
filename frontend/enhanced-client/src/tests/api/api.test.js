/**
 * Tests for API service layer
 */
import { fetchAPI } from '../../api/api';
import { API_URL } from '../../config';

describe('fetchAPI', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('should call fetch with correct URL and default options', async () => {
    const mockResponse = { data: 'test' };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce(mockResponse)
    });

    const endpoint = '/test-endpoint';
    const result = await fetchAPI(endpoint);

    expect(fetch).toHaveBeenCalledWith(`${API_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    expect(result).toEqual(mockResponse);
  });

  test('should merge custom options with defaults', async () => {
    const mockResponse = { data: 'test' };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce(mockResponse)
    });

    const endpoint = '/test-endpoint';
    const options = {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer token'
      }
    };
    
    const result = await fetchAPI(endpoint, options);

    expect(fetch).toHaveBeenCalledWith(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token'
      },
    });
    expect(result).toEqual(mockResponse);
  });

  test('should stringify body if provided as object', async () => {
    const mockResponse = { data: 'test' };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce(mockResponse)
    });

    const endpoint = '/test-endpoint';
    const body = { key: 'value' };
    const options = {
      method: 'POST',
      body
    };
    
    await fetchAPI(endpoint, options);

    expect(fetch).toHaveBeenCalledWith(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    });
  });

  test('should not stringify body if already a string', async () => {
    const mockResponse = { data: 'test' };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValueOnce(mockResponse)
    });

    const endpoint = '/test-endpoint';
    const body = JSON.stringify({ key: 'value' });
    const options = {
      method: 'POST',
      body
    };
    
    await fetchAPI(endpoint, options);

    expect(fetch).toHaveBeenCalledWith(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body
    });
  });

  test('should throw error if response is not ok', async () => {
    const errorData = { error: 'test error' };
    fetch.mockResolvedValueOnce({
      ok: false,
      json: jest.fn().mockResolvedValueOnce(errorData)
    });

    const endpoint = '/test-endpoint';
    
    await expect(fetchAPI(endpoint)).rejects.toThrow('test error');
  });

  test('should handle network errors', async () => {
    const networkError = new Error('Network error');
    fetch.mockRejectedValueOnce(networkError);

    const endpoint = '/test-endpoint';
    
    await expect(fetchAPI(endpoint)).rejects.toThrow('Network error');
  });

  test('should handle JSON parsing errors in error response', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      statusText: 'Not Found',
      json: jest.fn().mockRejectedValueOnce(new Error('Invalid JSON'))
    });

    const endpoint = '/test-endpoint';
    
    await expect(fetchAPI(endpoint)).rejects.toThrow('Not Found');
  });
});