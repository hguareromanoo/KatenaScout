import React, { useState, useEffect } from 'react';
import { 
  X, Heart, ArrowLeft, User, UserCircle, Trophy, TrendingUp, 
  BarChart3, Clock, Package, Calendar, Globe, Footprints,
  Loader
} from 'lucide-react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, Tooltip, Legend 
} from 'recharts';
import { useTranslation, useFavorites, useSession } from '../contexts';
import { playerService } from '../api/api';
import { 
  isValidPlayer, formatPositions, getValueColor
} from '../utils';
import { 
  playerStatsToMetricsWithColors, NEGATIVE_STATS, normalizeMetricsForRadar 
} from '../utils/playerUtils';

/**
 * PlayerCompletePage - Full detailed player profile
 */
const PlayerCompletePage = ({ player, onClose }) => {
  const { t } = useTranslation();
  const { isPlayerFavorite, toggleFavorite } = useFavorites();
  const { session } = useSession();
  const [activeTab, setActiveTab] = useState('overview');
  const [completePlayer, setCompletePlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const isFavorite = isPlayerFavorite(player);
  
  // Use the complete profile data that's already included with the player
  useEffect(() => {
    if (!player) {
      setError('Invalid player data');
      setLoading(false);
      return;
    }
    
    try {
      setLoading(true);
      
      // Check if player already has complete_profile data
      if (player.complete_profile) {
        console.log("Using complete_profile data already included with player");
        
        // Create an enhanced player object with the complete profile data
        const enhancedPlayer = {
          ...player,
          // Merge the complete profile stats with the existing stats
          stats: {
            ...player.stats,
            ...player.complete_profile.stats
          },
          // Add position averages
          position_averages: player.complete_profile.position_averages || {}
        };
        
        setCompletePlayer(enhancedPlayer);
      } else {
        // No complete_profile data, just use the player as is
        console.warn('No complete_profile data found, using regular player data');
        setCompletePlayer(player);
      }
    } catch (err) {
      console.error('Error processing player data:', err);
      setError(err.message || 'Failed to process player data');
      // Fall back to the passed-in player on error
      setCompletePlayer(player);
    } finally {
      setLoading(false);
    }
  }, [player]);

  // Show loading state while fetching data
  if (loading) {
    return (
      <div className="h-[95vh] flex flex-col items-center justify-center">
        <Loader className="animate-spin text-green-500 w-12 h-12 mb-4" />
        <p className="text-gray-300">{t('loading.fetchingPlayerData', 'Fetching player data...')}</p>
      </div>
    );
  }

  // Check if we have valid player data
  const activePlayer = completePlayer || player;
  if (!isValidPlayer(activePlayer)) {
    return (
      <div className="p-6">
        <h3 className="text-xl text-red-400 mb-4">{t('errors.playerNotFound')}</h3>
        <p className="text-gray-300 mb-4">{error || t('errors.loadingFailed')}</p>
        <button 
          onClick={onClose} 
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-white"
        >
          {t('playerDashboard.close')}
        </button>
      </div>
    );
  }
  
  // Prepare metrics from player stats using utility with color support
  const metrics = playerStatsToMetricsWithColors(activePlayer);
  
  // Prepare normalized metrics for radar chart
  const radarMetrics = normalizeMetricsForRadar(metrics);
  
  // Select key metrics for the radar chart - no more than 8 for readability
  const selectRadarMetrics = (allMetrics) => {
    const keyMetricNames = [
      // Attacking
      "goals", "assists", "xgShot", 
      // Passing
      "successfulPasses", "progressivePasses", "keyPasses",
      // Defending
      "defensiveDuelsWon", "interceptions",
      // Possession
      "successfulDribbles", "progressiveRun",
      // Physical
      "aerialDuelsWon", "duelsWon"
    ];
    
    // If goalkeeper, show different key metrics
    if (activePlayer.is_goalkeeper) {
      return allMetrics.filter(m => 
        ["gkSaves", "gkSuccessfulExits", "goalkeeperExitsPerformed", 
         "successfulPasses", "successfulLongPasses", "ballRecoveries"].some(term => m.key?.includes(term))
      ).slice(0, 8);
    }
    
    // Filter to key metrics that exist in the data
    return allMetrics.filter(m => 
      keyMetricNames.some(key => m.key?.includes(key))
    ).slice(0, 8); // Limit to 8 metrics for readability
  };
  
  // Get selected metrics for radar
  const selectedRadarMetrics = selectRadarMetrics(radarMetrics);
  
  // Group metrics by category for better organization
  const metricCategories = {
    attacking: metrics.filter(m => ["goals", "assists", "shots", "shotsOnTarget", "xgShot", "xgAssist", 
                                   "goalConversion", "shotsOnTarget"].some(term => m.key?.includes(term))),
    passing: metrics.filter(m => ["passes", "forwardPasses", "backPasses", "lateralPasses", "longPasses", 
                                 "progressivePasses", "passesToFinalThird", "smartPasses", "throughPasses",
                                 "keyPasses", "crosses"].some(term => m.key?.includes(term))),
    defending: metrics.filter(m => ["defensiveDuels", "interceptions", "slidingTackles", "clearances", 
                                   "ballRecoveries", "opponentHalfRecoveries", "counterpressingRecoveries"]
                                   .some(term => m.key?.includes(term))),
    possession: metrics.filter(m => ["successfulDribbles", "progressiveRun", "offensiveDuels", 
                                    "ballLosses", "dangerousOwnHalfLosses", "accelerations"]
                                    .some(term => m.key?.includes(term))),
    physical: metrics.filter(m => ["aerialDuels", "duels"].some(term => m.key?.includes(term))),
    goalkeeping: metrics.filter(m => ["gkSaves", "gkSuccessfulExits", "goalkeeperExitsPerformed", 
                                     "successfulGoalKicks"].some(term => m.key?.includes(term))),
  };
  
  // Filter out empty categories
  const activeCategories = Object.entries(metricCategories)
    .filter(([_, metrics]) => metrics.length > 0)
    .reduce((obj, [key, value]) => ({...obj, [key]: value}), {});
  
  return (
    <div className="h-[95vh] flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-750 p-6 flex items-center relative">
        {/* Back/Close button */}
        <button 
          onClick={onClose}
          className="absolute top-3 left-3 text-gray-400 hover:text-white p-1 rounded-full hover:bg-gray-700 z-10"
        >
          <ArrowLeft size={24} />
        </button>
        
        {/* Player image */}
        <div className="w-24 h-24 bg-gray-700 rounded-full mr-5 flex items-center justify-center overflow-hidden relative mt-5">
          {player.image_url || player.imageDataURL ? (
            <img 
              src={playerService.getPlayerImageUrl(player)} 
              alt={player.name} 
              className="w-full h-full object-cover"
              onError={(e) => {
                // Log error for debugging
                console.warn(`CompletePage: Image load failed for player ${player.name} (ID: ${player.wyId || player.id})`);
                
                e.target.onerror = null; 
                e.target.style.display = 'none';
                // Only add fallback icon if it doesn't exist yet
                if (!e.target.parentNode.querySelector('.player-fallback-icon')) {
                  const fallbackDiv = document.createElement('div');
                  fallbackDiv.className = 'flex items-center justify-center w-full h-full player-fallback-icon';
                  fallbackDiv.innerHTML = '<span class="text-3xl">⚽</span>';
                  e.target.parentNode.appendChild(fallbackDiv);
                }
              }} 
            />
          ) : (
            <UserCircle className="text-gray-500 w-full h-full" />
          )}
        </div>
        
        {/* Player info */}
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-white">{player.name}</h2>
          <div className="text-gray-300 flex flex-wrap gap-x-4 mt-1">
            {player.positions && (
              <span className="flex items-center">
                <UserCircle className="mr-1" size={16} />
                {player.positions.join(', ')}
              </span>
            )}
            {player.age && (
              <span className="flex items-center">
                <Calendar className="mr-1" size={16} />
                {player.age} {t('playerDashboard.age')}
              </span>
            )}
            {player.nationality && (
              <span className="flex items-center">
                <Globe className="mr-1" size={16} />
                {player.nationality}
              </span>
            )}
            {player.foot && (
              <span className="flex items-center">
                <Footprints className="mr-1" size={16} />
                {player.foot}
              </span>
            )}
          </div>
        </div>
        
        {/* Favorite button */}
        <button
          onClick={() => toggleFavorite(player)}
          className={`p-2 rounded-full ${
            isFavorite 
              ? 'bg-red-500 bg-opacity-20 text-red-400 hover:bg-opacity-30' 
              : 'bg-gray-700 text-gray-400 hover:text-white hover:bg-gray-650'
          }`}
          title={isFavorite ? t('playerDashboard.removeFromFavorites') : t('playerDashboard.addToFavorites')}
        >
          <Heart size={20} fill={isFavorite ? '#f56565' : 'none'} />
        </button>
      </div>
      
      {/* Tabs Navigation */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="flex">
          <button
            className={`px-6 py-3 text-sm font-medium ${
              activeTab === 'overview' 
                ? 'text-white border-b-2 border-green-500' 
                : 'text-gray-400 hover:text-gray-300'
            }`}
            onClick={() => setActiveTab('overview')}
          >
            {t('playerDashboard.overview', 'Overview')}
          </button>
          <button
            className={`px-6 py-3 text-sm font-medium ${
              activeTab === 'stats' 
                ? 'text-white border-b-2 border-green-500' 
                : 'text-gray-400 hover:text-gray-300'
            }`}
            onClick={() => setActiveTab('stats')}
          >
            {t('playerDashboard.statistics', 'Statistics')}
          </button>
          <button
            className={`px-6 py-3 text-sm font-medium ${
              activeTab === 'details' 
                ? 'text-white border-b-2 border-green-500' 
                : 'text-gray-400 hover:text-gray-300'
            }`}
            onClick={() => setActiveTab('details')}
          >
            {t('playerDashboard.details', 'Details')}
          </button>
        </div>
      </div>
      
      {/* Tab Content - Scrollable */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-900">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-7 gap-6">
            {/* Radar Chart */}
            <div className="lg:col-span-4 bg-gray-800 rounded-lg p-5">
              <h3 className="text-lg font-semibold text-white mb-4">{t('playerCompletePage.performanceOverview', 'Performance Overview')}</h3>
              <div style={{ height: '400px' }}>
                {selectedRadarMetrics.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart outerRadius="70%" data={selectedRadarMetrics}>
                      <PolarGrid stroke="#4a5568" />
                      <PolarAngleAxis 
                        dataKey="name" 
                        tick={{ fill: '#a0aec0', fontSize: '11px' }} 
                      />
                      <PolarRadiusAxis 
                        angle={30} 
                        domain={[0, 100]} 
                        tick={{ fill: '#718096', fontSize: '10px' }} 
                      />
                      <Radar
                        name={activePlayer.name}
                        dataKey="displayValue"  
                        stroke="#48bb78"
                        fill="#48bb78"
                        fillOpacity={0.5}
                      />
                      <Tooltip content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const metric = payload[0].payload;
                          const isNegative = metric.key && NEGATIVE_STATS.includes(metric.key);
                          
                          return (
                            <div className="bg-gray-800 border border-gray-700 p-2 rounded shadow-lg">
                              <p className="text-gray-300 text-xs">{metric.name}</p>
                              <p className={`${metric.colorClass || 'text-white'} font-bold text-sm`}>
                                {metric.value} {isNegative && <span className="text-xs italic">({t('playerCompletePage.lowerIsBetter', 'lower is better')})</span>}
                              </p>
                              {metric.positionAverage && (
                                <div className="flex justify-between text-xs mt-1">
                                  <span className="text-gray-400">{t('playerCompletePage.positionAvg', 'Position avg')}:</span>
                                  <span className="text-gray-300">{metric.positionAverage.toFixed(1)}</span>
                                </div>
                              )}
                            </div>
                          );
                        }
                        return null;
                      }} />
                      <Legend />
                    </RadarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-full flex items-center justify-center text-gray-400">
                    {t('playerDashboard.noMetrics', 'No metrics available for this player.')}
                  </div>
                )}
              </div>
            </div>
            
            {/* Player Details */}
            <div className="lg:col-span-3 space-y-6">
              {/* Basic Info */}
              <div className="bg-gray-800 rounded-lg p-5">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <User className="mr-2" size={18} />
                  {t('playerCompletePage.playerInformation', 'Player Information')}
                </h3>
                
                <div className="space-y-3">
                  {player.positions && (
                    <div className="flex">
                      <div className="w-1/3 text-gray-400">{t('playerDashboard.position')}</div>
                      <div className="w-2/3 text-white">{player.positions.join(', ')}</div>
                    </div>
                  )}
                  
                  {player.nationality && (
                    <div className="flex">
                      <div className="w-1/3 text-gray-400">{t('playerCompletePage.nationality', 'Nationality')}</div>
                      <div className="w-2/3 text-white">{player.nationality}</div>
                    </div>
                  )}
                  
                  {player.age && (
                    <div className="flex">
                      <div className="w-1/3 text-gray-400">{t('playerDashboard.age')}</div>
                      <div className="w-2/3 text-white">{player.age}</div>
                    </div>
                  )}
                  
                  {player.foot && (
                    <div className="flex">
                      <div className="w-1/3 text-gray-400">{t('playerDashboard.foot')}</div>
                      <div className="w-2/3 text-white">{player.foot}</div>
                    </div>
                  )}
                  
                  {player.height && (
                    <div className="flex">
                      <div className="w-1/3 text-gray-400">{t('playerDashboard.height')}</div>
                      <div className="w-2/3 text-white">{player.height} cm</div>
                    </div>
                  )}
                  
                  {player.weight && (
                    <div className="flex">
                      <div className="w-1/3 text-gray-400">{t('playerDashboard.weight')}</div>
                      <div className="w-2/3 text-white">{player.weight} kg</div>
                    </div>
                  )}
                  
                  {player.value && (
                    <div className="flex">
                      <div className="w-1/3 text-gray-400">{t('playerDashboard.value')}</div>
                      <div className="w-2/3 text-white">{player.value}</div>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Key Stats */}
              <div className="bg-gray-800 rounded-lg p-5">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <TrendingUp className="mr-2" size={18} />
                  {t('playerCompletePage.keyAttributes', 'Key Attributes')}
                </h3>
                
                <div className="grid grid-cols-2 gap-3">
                  {metrics.slice(0, 6).map((metric, index) => (
                    <div key={index} className="bg-gray-750 rounded-lg p-3">
                      <div className="text-xs text-gray-400 mb-1">{metric.name}</div>
                      <div className={`${metric.colorClass || 'text-white'} font-medium flex items-center justify-between`}>
                        <span>{metric.value}</span>
                        {metric.positionAverage && (
                          <span className="text-xs text-gray-400">
                            avg: {metric.positionAverage.toFixed(1)}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Statistics Tab */}
        {activeTab === 'stats' && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold text-white mb-6">{t('playerCompletePage.completeStatistics', 'Complete Statistics')}</h3>
            
            {/* Display stats by category with collapsible sections */}
            <div className="space-y-8">
              {Object.entries(activeCategories).map(([category, categoryMetrics]) => (
                <div key={category} className="mb-6">
                  <h4 className="text-lg font-medium text-white mb-4 capitalize border-b border-gray-700 pb-2">
                    {t(`playerCompletePage.categoryStats.${category}`, `${category.charAt(0).toUpperCase() + category.slice(1)} Statistics`)}
                  </h4>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {categoryMetrics.map((metric, index) => {
                      const isNegativeStat = NEGATIVE_STATS.includes(metric.key);
                      
                      return (
                        <div key={index} className="bg-gray-750 rounded-lg p-4">
                          <div className="flex justify-between items-center">
                            <div className="text-sm text-gray-400 mb-1">{metric.name}</div>
                            {isNegativeStat && (
                              <div className="text-xs text-gray-500 italic">{t('playerCompletePage.lowerIsBetter', 'Lower is better')}</div>
                            )}
                          </div>
                          
                          <div className="flex justify-between items-center">
                            <div className={`${metric.colorClass || 'text-white'} text-xl font-medium`}>
                              {metric.value}
                            </div>
                            {metric.positionAverage && (
                              <div className="text-sm text-gray-400">
                                {t('playerCompletePage.average', 'Avg')}: {metric.positionAverage.toFixed(1)}
                              </div>
                            )}
                          </div>
                          
                          <div className="mt-2 w-full bg-gray-700 rounded-full h-2">
                            <div 
                              className={`${metric.colorClass ? metric.colorClass.replace('text-', 'bg-') : "bg-green-500"} h-2 rounded-full`}
                              style={{ 
                                width: `${Math.min(100, Math.max(0, isNegativeStat 
                                  ? (metric.positionAverage && metric.value > 0 
                                    ? Math.min(100, (metric.positionAverage / metric.value * 100)) 
                                    : 100)
                                  : metric.value))}%` 
                              }}
                            ></div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
              
              {/* No stats message if no categories are available */}
              {Object.keys(activeCategories).length === 0 && (
                <div className="text-center py-8 text-gray-400">
                  {t('playerCompletePage.noStatsAvailable', 'No statistics available for this player.')}
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Details Tab */}
        {activeTab === 'details' && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-semibold text-white mb-6">{t('playerCompletePage.playerDetails', 'Player Details')}</h3>
            
            <div className="space-y-6">
              {/* Personal Information */}
              <div>
                <h4 className="text-lg text-white mb-3 border-b border-gray-700 pb-2">{t('playerCompletePage.personalInformation', 'Personal Information')}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex flex-col">
                    <span className="text-gray-400 text-sm">{t('playerCompletePage.fullName', 'Full Name')}</span>
                    <span className="text-white">{player.name}</span>
                  </div>
                  
                  {player.nationality && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerCompletePage.nationality', 'Nationality')}</span>
                      <span className="text-white">{player.nationality}</span>
                    </div>
                  )}
                  
                  {player.age && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerDashboard.age', 'Age')}</span>
                      <span className="text-white">{player.age} {t('playerCompletePage.years', 'years')}</span>
                    </div>
                  )}
                  
                  {player.foot && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerDashboard.foot', 'Preferred Foot')}</span>
                      <span className="text-white">{player.foot}</span>
                    </div>
                  )}
                  
                  {player.height && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerDashboard.height', 'Height')}</span>
                      <span className="text-white">{player.height} {t('playerCompletePage.cm', 'cm')}</span>
                    </div>
                  )}
                  
                  {player.weight && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerDashboard.weight', 'Weight')}</span>
                      <span className="text-white">{player.weight} {t('playerCompletePage.kg', 'kg')}</span>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Professional Information */}
              <div>
                <h4 className="text-lg text-white mb-3 border-b border-gray-700 pb-2">{t('playerCompletePage.professionalInformation', 'Professional Information')}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {player.positions && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerDashboard.position', 'Position')}</span>
                      <span className="text-white">{player.positions.join(', ')}</span>
                    </div>
                  )}
                  
                  {player.value && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerDashboard.value', 'Market Value')}</span>
                      <span className="text-white">{player.value}</span>
                    </div>
                  )}
                  
                  {player.current_club && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerCompletePage.currentClub', 'Current Club')}</span>
                      <span className="text-white">{player.current_club}</span>
                    </div>
                  )}
                  
                  {player.contract_until && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerCompletePage.contractUntil', 'Contract Until')}</span>
                      <span className="text-white">{player.contract_until}</span>
                    </div>
                  )}
                  
                  {player.contract && player.contract.contractExpiration && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerCompletePage.contractExpiration', 'Contract Expiration')}</span>
                      <span className="text-white">{player.contract.contractExpiration}</span>
                    </div>
                  )}
                  
                  {player.contract && player.contract.agencies && player.contract.agencies.length > 0 && (
                    <div className="flex flex-col">
                      <span className="text-gray-400 text-sm">{t('playerCompletePage.agencies', 'Agencies')}</span>
                      <span className="text-white">{player.contract.agencies.join(', ')}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlayerCompletePage;