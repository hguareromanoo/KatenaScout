/**
 * Utility functions for formatting text and data
 */

/**
 * Formats metric names for display by replacing underscores with spaces 
 * and capitalizing each word, or translating them if translation function is provided
 * 
 * @param {string} key - The metric key/name to format
 * @param {function} t - Translation function (optional)
 * @param {object} options - Additional options like showUnit (optional)
 * @returns {string} - The formatted and/or translated metric name
 */
export const formatMetricName = (key, t, options = {}) => {
  if (!key) return '';
  
  // Check if translation is available
  if (t) {
    const translationKey = `metrics.${key}`;
    const translation = t(translationKey);
    
    // If we have a valid translation (not just the key itself)
    if (translation && translation !== translationKey) {
      // Add unit if specified and showUnit option is true
      if (options.showUnit) {
        const unit = t(`metrics.units.${getMetricUnit(key)}`);
        if (unit && unit !== `metrics.units.${getMetricUnit(key)}`) {
          return `${translation} (${unit})`;
        }
      }
      return translation;
    }
  }
  
  // Fallback to standard formatting
  return key
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

/**
 * Formats player names with proper spacing between capital letters
 * 
 * @param {string} name - The player name to format
 * @returns {string} - The formatted player name
 */
export const formatPlayerName = (name) => {
  if (!name) return '';
  
  // Add spaces between capital letters if they're not already spaced
  return name.replace(/([A-Z])/g, ' $1').trim()
    // Replace multiple spaces with a single space
    .replace(/\s+/g, ' ')
    // Make sure first letter of each word is capitalized
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

/**
 * Gets the category of a metric for grouping and visualization purposes
 * 
 * @param {string} key - The metric key
 * @returns {string} - The category identifier
 */
export const getMetricCategory = (key) => {
  if (!key) return 'general';

  const matchCategories = {
    'matches': 'participation',
    'matchesIn': 'participation', 
    'matchesComing': 'participation',
    'matchesSubstituted': 'participation',
    'minutes': 'participation',
  };

  const passingCategories = {
    'pass': 'passing',
    'assist': 'passing',
    'cross': 'passing',
    'smart': 'passing',
    'key': 'passing',
    'through': 'passing',
    'vertical': 'passing',
    'lateral': 'passing',
    'long': 'passing',
    'forward': 'passing',
    'back': 'passing',
  };

  const attackingCategories = {
    'goal': 'attacking',
    'shot': 'attacking',
    'head': 'attacking',
    'xg': 'attacking',
    'penalty': 'attacking',
    'offensiveDuel': 'attacking',
    'dribble': 'attacking',
    'attack': 'attacking',
    'freeKick': 'attacking',
    'corner': 'attacking',
    'touchInBox': 'attacking',
  };

  const defensiveCategories = {
    'defensiveDuel': 'defensive',
    'intercept': 'defensive',
    'slidingTackle': 'defensive',
    'clearance': 'defensive',
    'pressingDuel': 'defensive',
    'recovery': 'defensive',
    'defensive': 'defensive',
    'block': 'defensive',
  };

  const physicalCategories = {
    'aerial': 'physical',
    'acceleration': 'physical',
    'progressiveRun': 'physical',
    'distanceCovered': 'physical',
    'sprint': 'physical',
  };

  const miscCategories = {
    'card': 'discipline',
    'foul': 'discipline',
  };

  const goalkeeperCategories = {
    'gk': 'goalkeeper',
  };

  // Check each category map
  for (const [pattern, category] of Object.entries({
    ...matchCategories,
    ...passingCategories,
    ...attackingCategories,
    ...defensiveCategories, 
    ...physicalCategories,
    ...miscCategories,
    ...goalkeeperCategories
  })) {
    if (key.includes(pattern)) {
      return category;
    }
  }

  return 'general';
};

/**
 * Get the appropriate unit for a metric if applicable
 * 
 * @param {string} key - The metric key
 * @returns {string} - The unit identifier ('percent', 'minutes', etc) or empty
 */
export const getMetricUnit = (key) => {
  if (key.startsWith('xg') || key.includes('percent') || key.endsWith('Percent')) {
    return 'percent';
  }
  
  if (key.includes('minutes')) {
    return 'minutes';
  }
  
  if (key.includes('Length') || key.includes('Distance')) {
    return 'meters';
  }
  
  return 'count';
};

/**
 * Check if a metric is a ratio or percentage
 * 
 * @param {string} key - The metric key
 * @returns {boolean} - True if the metric is a percentage or ratio
 */
export const isPercentageMetric = (key) => {
  return key.startsWith('xg') || 
         key.includes('percent') || 
         key.endsWith('Percent') || 
         key.startsWith('successful') ||
         key.includes('Conversion') ||
         key.includes('Won');
};

/**
 * Returns the icon name for a specific metric category
 * 
 * @param {string} key - The metric key
 * @returns {string} - The icon name to use for this metric
 */
export const getMetricIcon = (key) => {
  const category = getMetricCategory(key);
  
  const categoryIcons = {
    'participation': 'clock',
    'passing': 'send',
    'attacking': 'target',
    'defensive': 'shield',
    'physical': 'activity',
    'discipline': 'alert-triangle',
    'goalkeeper': 'hand',
    'general': 'bar-chart-2',
  };
  
  // More specific icons for particular stats
  const specificIcons = {
    'goals': 'award',
    'assists': 'star',
    'shots': 'target',
    'shotsOnTarget': 'bullseye',
    'yellowCards': 'square',
    'redCards': 'square-fill',
    'duelsWon': 'swords',
    'fouls': 'alert-triangle',
    'forwardPasses': 'arrow-up-right',
    'backPasses': 'arrow-down-left',
    'keyPasses': 'key',
    'smartPasses': 'zap',
    'progressiveRun': 'trending-up',
    'slidingTackles': 'scissors',
    'aerialDuels': 'arrow-up',
    'interceptions': 'hand-stop',
    'xgShot': 'percent',
    'xgAssist': 'percent',
  };
  
  return specificIcons[key] || categoryIcons[category] || 'circle';
};

/**
 * Formats player position codes for display using translation keys.
 * 
 * @param {string} code - The position code (e.g., 'lcb', 'cmf').
 * @param {function} t - The translation function.
 * @returns {string} - The translated position name or the original code.
 */
export const formatPlayerPositionCode = (code, t) => {
  if (!code || !t) return code || '';
  
  const translationKey = `positions.${code.toLowerCase()}`; // Ensure lowercase key
  const translatedName = t(translationKey);
  
  // Return translated name if different from key, otherwise fallback to code
  return (translatedName && translatedName !== translationKey) ? translatedName : code.toUpperCase();
};

/**
 * Formats preferred foot for display using translation keys.
 * 
 * @param {string} foot - The preferred foot ('left', 'right', 'both').
 * @param {function} t - The translation function.
 * @returns {string} - The translated foot name or the original value.
 */
export const formatPreferredFoot = (foot, t) => {
  if (!foot || !t) return foot || '';
  
  const lowerFoot = foot.toLowerCase();
  let translationKey = '';

  if (lowerFoot === 'left') {
    translationKey = 'player.leftFoot';
  } else if (lowerFoot === 'right') {
    translationKey = 'player.rightFoot';
  } else if (lowerFoot === 'both') {
    translationKey = 'player.bothFeet';
  } else {
    return foot; // Return original if not recognized
  }

  const translatedName = t(translationKey);
  
  // Return translated name if different from key, otherwise fallback to original capitalized
  return (translatedName && translatedName !== translationKey) 
    ? translatedName 
    : foot.charAt(0).toUpperCase() + foot.slice(1);
};
