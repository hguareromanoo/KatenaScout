/**
 * Statistics utility functions for player data
 */

/**
 * Convert player stats object to array of metrics
 * 
 * @param {Object} stats - Player statistics object
 * @param {Function} formatter - Function to format metric names (optional)
 * @returns {Array} - Array of metric objects
 */
export const statsToMetrics = (stats, formatter) => {
  if (!stats || typeof stats !== 'object') return [];
  
  return Object.entries(stats).map(([key, value]) => {
    const name = formatter ? formatter(key) : key.replace(/_/g, ' ');
    
    return {
      key,
      name,
      value: value !== undefined && value !== null ? value : 0,
      originalValue: value
    };
  });
};

/**
 * Calculate player score based on position and stats
 * 
 * @param {Object} player - Player object with stats
 * @param {string} position - Position to score for
 * @returns {number} - Score between 0-100
 */
export const calculateScore = (player, position) => {
  if (!player || !player.stats || !position) return 0;
  
  const stats = player.stats;
  let score = 0;
  let totalWeight = 0;
  
  // Position-specific stat weights
  const weights = getWeightsForPosition(position);
  
  // Calculate weighted score
  Object.entries(weights).forEach(([stat, weight]) => {
    if (stats[stat] !== undefined && stats[stat] !== null) {
      score += (stats[stat] * weight);
      totalWeight += weight;
    }
  });
  
  // Normalize score to 0-100
  return totalWeight > 0 ? Math.round((score / totalWeight) * 100) : 0;
};

/**
 * Get weights for different player positions
 * 
 * @param {string} position - Player position
 * @returns {Object} - Weights for each stat
 */
const getWeightsForPosition = (position) => {
  position = position.toLowerCase();
  
  // Default weights
  const defaultWeights = {
    pace: 1,
    shooting: 1,
    passing: 1,
    dribbling: 1,
    defending: 1,
    physical: 1
  };
  
  // Position-specific weights
  const positionWeights = {
    // Attackers
    'striker': { pace: 1.5, shooting: 2, dribbling: 1.5, physical: 1 },
    'forward': { pace: 1.5, shooting: 2, dribbling: 1.5 },
    'winger': { pace: 2, dribbling: 2, passing: 1.5 },
    
    // Midfielders
    'midfielder': { passing: 2, dribbling: 1.5, defending: 1 },
    'attacking midfielder': { passing: 2, dribbling: 1.5, shooting: 1.5 },
    'defensive midfielder': { defending: 2, physical: 1.5, passing: 1.5 },
    
    // Defenders
    'defender': { defending: 2, physical: 1.5, pace: 1 },
    'fullback': { pace: 1.5, defending: 1.5, passing: 1 },
    'center back': { defending: 2, physical: 2 },
    
    // Goalkeeper
    'goalkeeper': { reflexes: 2, positioning: 2, handling: 1.5 }
  };
  
  // Find matching position
  const matchingPosition = Object.keys(positionWeights).find(p => 
    position.includes(p)
  );
  
  return matchingPosition 
    ? { ...defaultWeights, ...positionWeights[matchingPosition] } 
    : defaultWeights;
};

/**
 * Compare two players across multiple metrics
 * 
 * @param {Object} player1 - First player object with stats
 * @param {Object} player2 - Second player object with stats
 * @returns {Object} - Comparison results
 */
export const comparePlayerStats = (player1, player2) => {
  if (!player1 || !player2 || !player1.stats || !player2.stats) {
    return { better: null, metrics: [] };
  }
  
  const stats1 = player1.stats;
  const stats2 = player2.stats;
  
  // Get all unique stat keys
  const allKeys = new Set([
    ...Object.keys(stats1),
    ...Object.keys(stats2)
  ]);
  
  // Compare each stat
  const metrics = Array.from(allKeys).map(key => {
    const value1 = stats1[key] !== undefined ? stats1[key] : 0;
    const value2 = stats2[key] !== undefined ? stats2[key] : 0;
    const diff = value1 - value2;
    
    return {
      key,
      name: key.replace(/_/g, ' '),
      player1Value: value1,
      player2Value: value2,
      difference: diff,
      better: diff > 0 ? 'player1' : diff < 0 ? 'player2' : 'tie'
    };
  });
  
  // Determine overall better player
  const player1Wins = metrics.filter(m => m.better === 'player1').length;
  const player2Wins = metrics.filter(m => m.better === 'player2').length;
  
  const better = player1Wins > player2Wins 
    ? 'player1' 
    : player2Wins > player1Wins 
      ? 'player2' 
      : 'tie';
  
  return { better, metrics };
};