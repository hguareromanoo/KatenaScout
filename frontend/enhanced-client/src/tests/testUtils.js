/**
 * Test utilities for KatenaScout frontend tests
 */
import React from 'react';
import { render } from '@testing-library/react';
import { AppProvider } from '../contexts/AppProvider';

/**
 * Render component wrapped in AppProvider for testing
 * 
 * @param {JSX.Element} ui - Component to render
 * @param {Object} options - Additional render options
 * @returns {Object} - Testing library render result
 */
export function renderWithProviders(ui, options = {}) {
  const Wrapper = ({ children }) => {
    return <AppProvider>{children}</AppProvider>;
  };

  return render(ui, { wrapper: Wrapper, ...options });
}

/**
 * Mock the fetch API to return the given response
 * 
 * @param {Object} response - Response to return
 * @returns {Function} - Mocked fetch function
 */
export function mockFetchResponse(response) {
  global.fetch.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve(response),
    })
  );
}

/**
 * Mock a fetch error
 * 
 * @param {Error} error - Error to throw
 * @returns {Function} - Mocked fetch function
 */
export function mockFetchError(error) {
  global.fetch.mockImplementationOnce(() =>
    Promise.reject(error)
  );
}

/**
 * Mock a fetch response with HTTP error
 * 
 * @param {number} status - HTTP status code
 * @param {Object} data - Error data
 * @returns {Function} - Mocked fetch function
 */
export function mockFetchErrorResponse(status, data) {
  global.fetch.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status,
      json: () => Promise.resolve(data),
    })
  );
}

/**
 * Create dummy player data for testing
 * 
 * @param {number} id - Player ID
 * @param {Object} overrides - Properties to override
 * @returns {Object} - Player object
 */
export function createMockPlayer(id, overrides = {}) {
  return {
    id: `player-${id}`,
    name: `Player ${id}`,
    positions: ['Midfielder'],
    age: 25,
    height: 180,
    weight: 75,
    foot: 'Right',
    nationality: 'England',
    value: '€15M',
    stats: {
      passing: 85,
      shooting: 78,
      pace: 82,
      dribbling: 80,
      defending: 75,
      physical: 79
    },
    ...overrides
  };
}

/**
 * Create mock API responses for testing
 */
export const mockResponses = {
  searchResults: {
    success: true,
    response: "Here are some players that match your criteria",
    players: [
      createMockPlayer(1),
      createMockPlayer(2),
      createMockPlayer(3)
    ],
    language: "english"
  },
  playerComparison: {
    success: true,
    comparison: "Player 1 has better passing but Player 2 has better shooting",
    comparison_aspects: ["Passing", "Shooting", "Defense", "Physical"],
    players: [
      createMockPlayer(1),
      createMockPlayer(2)
    ],
    language: "english"
  },
  error: {
    success: false,
    error: "server_error",
    message: "An unexpected error occurred. Please try again.",
    language: "english"
  }
};