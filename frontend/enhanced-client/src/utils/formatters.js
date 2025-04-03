import { 
  Swords, Shield, Pass, Ball, Running, Goalie, 
  Zap, Target, Crosshair, Activity, Heart, Star,
  Flag
} from 'lucide-react';

/**
 * Utility functions for formatting text and data
 */

/**
 * Maps metric categories to their respective icons and colors
 */
export const metricCategoryIcons = {
  attacking: { icon: Swords, color: 'text-red-400' },
  defending: { icon: Shield, color: 'text-blue-400' },
  passing: { icon: Pass, color: 'text-green-400' },
  possession: { icon: Ball, color: 'text-yellow-400' },
  physical: { icon: Running, color: 'text-purple-400' },
  goalkeeping: { icon: Goalie, color: 'text-cyan-400' },
  setPieces: { icon: Flag, color: 'text-orange-400' },
  general: { icon: Activity, color: 'text-gray-400' }
};

/**
 * Maps metric keys to their categories
 */
export const metricCategories = {
  // Attacking metrics
  goals: 'attacking',
  assists: 'attacking',
  shots: 'attacking',
  shotsOnTarget: 'attacking',
  headShots: 'attacking',
  xgShot: 'attacking',
  xgAssist: 'attacking',
  shotAssists: 'attacking',
  shotOnTargetAssists: 'attacking',
  secondAssists: 'attacking',
  thirdAssists: 'attacking',
  shotsBlocked: 'attacking',
  goalConversion: 'attacking',
  touchInBox: 'attacking',
  
  // Passing metrics
  passes: 'passing',
  successfulPasses: 'passing',
  smartPasses: 'passing',
  successfulSmartPasses: 'passing',
  passesToFinalThird: 'passing',
  successfulPassesToFinalThird: 'passing',
  crosses: 'passing',
  successfulCrosses: 'passing',
  forwardPasses: 'passing',
  successfulForwardPasses: 'passing',
  backPasses: 'passing',
  successfulBackPasses: 'passing',
  throughPasses: 'passing',
  successfulThroughPasses: 'passing',
  keyPasses: 'passing',
  successfulKeyPasses: 'passing',
  verticalPasses: 'passing',
  successfulVerticalPasses: 'passing',
  longPasses: 'passing',
  successfulLongPasses: 'passing',
  lateralPasses: 'passing',
  successfulLateralPasses: 'passing',
  progressivePasses: 'passing',
  successfulProgressivePasses: 'passing',
  linkupPlays: 'passing',
  successfulLinkupPlays: 'passing',
  
  // Defending metrics
  interceptions: 'defending',
  defensiveActions: 'defending',
  successfulDefensiveAction: 'defending',
  clearances: 'defending',
  slidingTackles: 'defending',
  successfulSlidingTackles: 'defending',
  defensiveDuels: 'defending',
  defensiveDuelsWon: 'defending',
  newDefensiveDuelsWon: 'defending',
  counterpressingRecoveries: 'defending',
  
  // Possession metrics
  duels: 'possession',
  duelsWon: 'possession',
  newDuelsWon: 'possession',
  offensiveDuels: 'possession',
  offensiveDuelsWon: 'possession',
  newOffensiveDuelsWon: 'possession',
  aerialDuels: 'possession',
  aerialDuelsWon: 'possession',
  fieldAerialDuels: 'possession',
  fieldAerialDuelsWon: 'possession',
  dribbles: 'possession',
  successfulDribbles: 'possession',
  newSuccessfulDribbles: 'possession',
  dribblesAgainst: 'possession',
  dribblesAgainstWon: 'possession',
  progressiveRun: 'possession',
  ballRecoveries: 'possession',
  opponentHalfRecoveries: 'possession',
  dangerousOpponentHalfRecoveries: 'possession',
  losses: 'possession',
  ownHalfLosses: 'possession',
  dangerousOwnHalfLosses: 'possession',
  
  // Physical metrics
  accelerations: 'physical',
  pressingDuels: 'physical',
  pressingDuelsWon: 'physical',
  looseBallDuels: 'physical',
  looseBallDuelsWon: 'physical',
  missedBalls: 'physical',
  fouls: 'physical',
  foulsSuffered: 'physical',
  yellowCards: 'physical',
  redCards: 'physical',
  directRedCards: 'physical',
  offsides: 'physical',
  
  // Goalkeeping metrics
  gkSaves: 'goalkeeping',
  gkConcededGoals: 'goalkeeping',
  gkShotsAgainst: 'goalkeeping',
  gkExits: 'goalkeeping',
  gkSuccessfulExits: 'goalkeeping',
  gkAerialDuels: 'goalkeeping',
  gkAerialDuelsWon: 'goalkeeping',
  gkCleanSheets: 'goalkeeping',
  xgSave: 'goalkeeping',
  goalKicks: 'goalkeeping',
  goalKicksShort: 'goalkeeping',
  goalKicksLong: 'goalkeeping',
  successfulGoalKicks: 'goalkeeping',
  
  // Set pieces
  freeKicks: 'setPieces',
  freeKicksOnTarget: 'setPieces',
  directFreeKicks: 'setPieces',
  directFreeKicksOnTarget: 'setPieces',
  corners: 'setPieces',
  penalties: 'setPieces',
  successfulPenalties: 'setPieces'
};

/**
 * Formats metric names for display using translations and icons
 * 
 * @param {string} key - The metric key/name to format
 * @param {function} t - The translation function
 * @returns {Object} - Object containing formatted name, icon component, and category info
 */
export const formatMetricName = (key, t) => {
  if (!key) return { name: '', icon: null, category: null, color: null };
  
  // Get the translation key
  const translationKey = `metrics.${key}`;
  
  // Try to get the translated name
  const translatedName = t ? t(translationKey) : null;
  
  // Get the category for this metric
  const category = metricCategories[key] || 'general';
  
  // Get the icon and color for this category
  const { icon: IconComponent, color } = metricCategoryIcons[category];
  
  return {
    name: translatedName && translatedName !== translationKey 
      ? translatedName 
      : key
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' '),
    icon: IconComponent,
    category,
    color
  };
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