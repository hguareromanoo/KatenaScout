/**
 * Player-specific utility functions
 */
import { formatMetricName } from './formatters';
import { playerService } from '../api';

/**
 * List of stats where lower values are better
 * Used for stat coloration and comparison
 */
export const NEGATIVE_STATS = [
  'ballLosses', 'miscontrols', 'dispossessed', 'challengeLost', 
  'foulsCommitted', 'yellowCards', 'redCards', 'errorLeadToShot',
  'errorLeadToGoal', 'penaltyConceded', 'ownGoals', 'dribbledPast',
  'dangerousOwnHalfLosses', 'possessionLost'
];

/**
 * Normalize metrics for radar chart display
 * 
 * This transforms the metrics for visual display while keeping original values
 * for tooltips and data display. This is essential for making the radar chart
 * polygon visible and proportional.
 * 
 * @param {Array} metrics - Array of player metrics 
 * @returns {Array} - Normalized metrics with displayValue for the chart
 */
export const normalizeMetricsForRadar = (metrics) => {
  if (!metrics || !metrics.length) return [];
  
  return metrics.map(metric => {
    const { key, value, positionAverage } = metric;
    let normalizedValue;
    
    // If we have a position average, use it for normalization
    if (positionAverage && positionAverage > 0) {
      // For negative stats, invert the ratio (lower is better)
      if (NEGATIVE_STATS.includes(key)) {
        // If player has value = 0, give them full score
        normalizedValue = value === 0 ? 100 : Math.min(100, (positionAverage / value) * 50);
      } else {
        // For regular stats, normalize as % of position average * 2 (so avg = 50)
        normalizedValue = Math.min(100, (value / positionAverage) * 50);
      }
    } else {
      // If no average, use a simple normalization approach
      // Scale values to 0-100 based on reasonable assumptions
      
      // For percentage stats (those containing "percent" or ending in "Won")
      if (key.includes("percent") || key.endsWith("Won")) {
        normalizedValue = Math.min(100, value);
      } else if (key.includes("xg") || key.includes("goals") || key.includes("assists")) {
        // For goal/xG related stats, scale appropriately
        normalizedValue = Math.min(100, value * 10); // Assuming avg ~5-10 is good
      } else {
        // General scaling for other stats
        normalizedValue = Math.min(100, value * 5); // Conservative scaling
      }
    }
    
    // Return the metric with both original and normalized values
    return {
      ...metric,
      displayValue: Math.max(0, normalizedValue || 0) // Ensure non-negative
    };
  });
};

/**
 * Convert player stats to metrics array for visualization
 * 
 * @param {Object} player - Player object with stats property
 * @returns {Array} - Array of metrics objects
 */
export const playerStatsToMetrics = (player) => {
  if (!player || !player.stats) return [];
  
  return Object.entries(player.stats).map(([key, value]) => ({
    name: formatMetricName(key),
    value: value !== undefined && value !== null ? value : 0,
    key: key,
    originalValue: value // Keep original for debugging
  }));
};

/**
 * Get primary position of a player
 * 
 * @param {Object} player - Player object with positions array
 * @returns {string} - Primary position or empty string
 */
export const getPrimaryPosition = (player) => {
  if (!player || !player.positions || !player.positions.length) return '';
  
  return player.positions[0];
};

/**
 * Format player position list as string
 * 
 * @param {Object} player - Player object
 * @returns {string} - Formatted positions string
 */
export const formatPositions = (player) => {
  if (!player || !player.positions) return '';
  
  return player.positions.join(', ');
};

/**
 * Format player age with proper suffix
 * 
 * @param {Object} player - Player object with age property
 * @param {string} language - Language code
 * @returns {string} - Formatted age string
 */
export const formatPlayerAge = (player, language = 'english') => {
  if (!player || !player.age) return '';
  
  const age = parseInt(player.age);
  if (isNaN(age)) return '';
  
  // Different formats based on language
  switch(language) {
    case 'english':
      return `${age} years`;
    case 'portuguese':
      return `${age} anos`;
    case 'spanish':
      return `${age} años`;
    case 'bulgarian':
      return `${age} години`;
    default:
      return `${age}`;
  }
};

/**
 * Get player image URL
 * 
 * @param {Object} player - Player object
 * @returns {string} - Image URL or null
 */
export const getPlayerImageUrl = (player) => {
  if (!player) return null;
  
  // Use image_url if available
  if (player.image_url) return player.image_url;
  
  // Otherwise use player service to get image by ID
  if (player.id) {
    return playerService.getPlayerImageUrl(player.id);
  }
  
  return null;
};

/**
 * Create a player comparison object between two players
 * 
 * @param {Object} player1 - First player
 * @param {Object} player2 - Second player
 * @returns {Object} - Comparison data
 */
/**
 * Determine color class for stat based on comparison with position average
 * 
 * @param {string} statName - Name of the stat
 * @param {number} value - Player's stat value
 * @param {number} positionAverage - Average value for this stat in the player's position
 * @returns {string} - Tailwind color class
 */
export const getStatColorClass = (statName, value, positionAverage) => {
  // If no value or no average, return neutral color
  if (value === undefined || value === null || !positionAverage) {
    return 'text-gray-400';
  }
  
  // Calculate performance ratio
  const ratio = value / positionAverage;
  
  // Determine if it's a negative stat (where lower is better)
  const isNegativeStat = NEGATIVE_STATS.includes(statName);
  
  // Thresholds for color categorization
  const GOOD_THRESHOLD = 1.2;  // 20% better than average
  const POOR_THRESHOLD = 0.8;  // 20% worse than average
  
  // For regular stats (higher is better)
  if (!isNegativeStat) {
    if (ratio >= GOOD_THRESHOLD) return 'text-green-500';
    if (ratio <= POOR_THRESHOLD) return 'text-red-500';
    return 'text-yellow-500'; // Around average
  } 
  // For negative stats (lower is better)
  else {
    if (ratio <= POOR_THRESHOLD) return 'text-green-500'; // Low value is good
    if (ratio >= GOOD_THRESHOLD) return 'text-red-500';   // High value is bad
    return 'text-yellow-500'; // Around average
  }
};

/**
 * Enhanced version of playerStatsToMetrics that includes position averages
 * 
 * @param {Object} player - Player object with stats and position_averages
 * @returns {Array} - Array of metrics with color classes
 */
export const playerStatsToMetricsWithColors = (player) => {
  if (!player || !player.stats) return [];
  
  const metrics = Object.entries(player.stats).map(([key, value]) => {
    const metricObj = {
      name: formatMetricName(key),
      value: value !== undefined && value !== null ? value : 0,
      key: key,
      originalValue: value,
      colorClass: 'text-white' // Default color
    };
    
    // If position averages available, calculate color
    if (player.position_averages && player.position_averages[key]) {
      const posAvg = player.position_averages[key];
      metricObj.positionAverage = posAvg;
      metricObj.colorClass = getStatColorClass(key, value, posAvg);
    }
    
    return metricObj;
  });
  
  return metrics;
};

export const comparePlayersData = (player1, player2) => {
  if (!player1 || !player2) return null;
  
  // Get all stats keys from both players
  const allKeys = new Set();
  if (player1.stats) Object.keys(player1.stats).forEach(key => allKeys.add(key));
  if (player2.stats) Object.keys(player2.stats).forEach(key => allKeys.add(key));
  
  // Create comparison metrics
  const metrics = Array.from(allKeys).map(key => {
    const value1 = player1.stats?.[key] || 0;
    const value2 = player2.stats?.[key] || 0;
    const diff = value1 - value2;
    
    // Check if this is a negative stat where lower is better
    const isNegativeStat = NEGATIVE_STATS.includes(key);
    
    // For negative stats, invert the winner logic
    let winner;
    if (isNegativeStat) {
      winner = diff < 0 ? 'player1' : diff > 0 ? 'player2' : 'tie';
    } else {
      winner = diff > 0 ? 'player1' : diff < 0 ? 'player2' : 'tie';
    }
    
    return {
      key,
      name: formatMetricName(key),
      player1Value: value1,
      player2Value: value2,
      difference: diff,
      isNegativeStat,
      winner
    };
  });
  
  return {
    player1: {
      name: player1.name,
      position: getPrimaryPosition(player1),
      imageUrl: getPlayerImageUrl(player1)
    },
    player2: {
      name: player2.name,
      position: getPrimaryPosition(player2),
      imageUrl: getPlayerImageUrl(player2)
    },
    metrics
  };
};