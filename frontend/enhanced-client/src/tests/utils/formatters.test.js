/**
 * Tests for formatter utility functions
 */
import { formatMetricName, formatPlayerName } from '../../utils/formatters';

describe('formatMetricName', () => {
  test('should replace underscores with spaces', () => {
    expect(formatMetricName('passing_accuracy')).toBe('Passing Accuracy');
  });

  test('should capitalize each word', () => {
    expect(formatMetricName('shots_on_target')).toBe('Shots On Target');
  });

  test('should handle single word', () => {
    expect(formatMetricName('speed')).toBe('Speed');
  });

  test('should return empty string for empty input', () => {
    expect(formatMetricName('')).toBe('');
  });

  test('should handle undefined input', () => {
    expect(formatMetricName(undefined)).toBe('');
  });
});

describe('formatPlayerName', () => {
  test('should add spaces between capital letters', () => {
    expect(formatPlayerName('JohnDoe')).toBe('John Doe');
  });

  test('should capitalize first letter of each word', () => {
    expect(formatPlayerName('john doe')).toBe('John Doe');
  });

  test('should handle mixed case', () => {
    expect(formatPlayerName('johnDoe')).toBe('John Doe');
  });

  test('should replace multiple spaces with a single space', () => {
    expect(formatPlayerName('John   Doe')).toBe('John Doe');
  });

  test('should return empty string for empty input', () => {
    expect(formatPlayerName('')).toBe('');
  });

  test('should handle undefined input', () => {
    expect(formatPlayerName(undefined)).toBe('');
  });
});