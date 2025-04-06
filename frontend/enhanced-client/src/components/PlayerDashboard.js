import React, { useState, useEffect } from 'react';
import { X, Heart, User, UserCircle, Trophy, TrendingUp, BarChart3, Clock, 
        Package, Calendar, Footprints, GitCompare } from 'lucide-react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, Tooltip, Legend 
} from 'recharts';
import { useTranslation, useFavorites, useComparison, useSession } from '../contexts';
import { playerService } from '../api/api';
import { isValidPlayer } from '../utils';
import { 
  playerStatsToMetricsWithColors, 
  normalizeMetricsForRadar, 
  NEGATIVE_STATS 
} from '../utils/playerUtils';
import { 
  formatMetricName, getMetricIcon, getMetricCategory, 
  formatPlayerPositionCode, formatPreferredFoot // Import new formatters
} from '../utils/formatters';

/**
 * PlayerDashboard Component - Displays player information in a modal
 */
const PlayerDashboard = ({ player, metrics = [], onClose, onViewComplete }) => {
  const { t } = useTranslation();
  const { isPlayerFavorite, toggleFavorite } = useFavorites();
  const { startComparison } = useComparison();
  const { sessionId, currentSearchResults } = useSession();
  
  // Add local state for immediate feedback
  const [localFavorite, setLocalFavorite] = useState(isPlayerFavorite(player));
  
  // Sync local state with global state
  useEffect(() => {
    setLocalFavorite(isPlayerFavorite(player));
  }, [player, isPlayerFavorite]);
  
  // We no longer need this effect since we're using the current search results directly
  
  const isFavorite = isPlayerFavorite(player);
  
  // Convert metrics with color data if not already passed in
  const playerMetrics = metrics.length ? metrics : 
    playerStatsToMetricsWithColors(player);
    
  // Prepare normalized metrics for radar chart
  const radarMetrics = normalizeMetricsForRadar(playerMetrics);
  
  // Select key metrics for the radar chart - no more than 6 for readability in dashboard
  const selectRadarMetrics = (allMetrics) => {
    const keyMetricNames = [
      // Attacking
      "goals", "assists", "xgShot", 
      // Passing
      "successfulPasses", "progressivePasses", "keyPasses",
      // Defending
      "defensiveDuelsWon", "interceptions",
      // Possession
      "successfulDribbles", "progressiveRun" 
    ];
    
    // If goalkeeper, show different key metrics
    if (player.is_goalkeeper) {
      const metrics = allMetrics.filter(m => 
        ["gkSaves", "gkSuccessfulExits", "goalkeeperExitsPerformed", 
         "successfulPasses", "successfulLongPasses"].some(term => m.key?.includes(term))
      ).slice(0, 6);
      
      // Traduzir os nomes das métricas
      return metrics.map(metric => ({
        ...metric,
        name: formatMetricName(metric.key, t)
      }));
    }
    
    // Filter to key metrics that exist in the data
    const metrics = allMetrics.filter(m => 
      keyMetricNames.some(key => m.key?.includes(key))
    ).slice(0, 6); // Limit to 6 metrics for readability
    
    // Traduzir os nomes das métricas
    return metrics.map(metric => ({
      ...metric,
      name: formatMetricName(metric.key, t)
    }));
  };
  // Get selected metrics for radar
  const selectedRadarMetrics = selectRadarMetrics(radarMetrics);

  // Check if player object has required data using validation utility
  if (!isValidPlayer(player)) {
    return (
      <div className="p-6">
        <h3 className="text-xl text-red-400 mb-4">{t('errors.playerNotFound')}</h3>
        <p className="text-gray-300 mb-4">{t('errors.loadingFailed')}</p>
        <button 
          onClick={onClose} 
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-white"
        >
          {t('playerDashboard.close')}
        </button>
      </div>
    );
  }

  // Use playerService to format values
  const formatValue = playerService.formatValue;

  return (
    <div className="relative">
      {/* Close button */}
      <button 
        onClick={onClose}
        className="absolute top-3 right-3 text-gray-400 hover:text-white p-1 rounded-full hover:bg-gray-700 z-10"
      >
        <X size={24} />
      </button>
      
      {/* Player Header */}
      <div className="bg-gradient-to-r from-gray-800 to-gray-750 p-6 flex items-center relative overflow-hidden">
        {/* Background pattern */}
        <div className="absolute inset-0 opacity-10 bg-pattern"></div>
        
        {/* Player image */}
        <div className="w-20 h-20 bg-gray-700 rounded-full mr-5 flex items-center justify-center overflow-hidden relative">
          {player.image_url || player.imageDataURL ? (
            <img 
              src={playerService.getPlayerImageUrl(player)} 
              alt={player.name} 
              className="w-full h-full object-cover"
              onError={(e) => {
                // Log error for debugging
                console.warn(`Dashboard: Image load failed for player ${player.name} (ID: ${player.wyId || player.id})`);
                
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
            {/* Format positions using the new function */}
            {player.positions && player.positions.length > 0 && (
              <span className="flex items-center">
                <UserCircle className="mr-1" size={16} />
                {player.positions.map(pos => formatPlayerPositionCode(pos, t)).join(', ')}
              </span>
            )}
            {player.age && (
              <span className="flex items-center">
                <Calendar className="mr-1" size={16} />
                {player.age} {t('playerDashboard.age')}
              </span>
            )}
          </div>
        </div>
        
        // ...existing code...



{/* Favorite button */}
<button
  onClick={(e) => {
    e.stopPropagation();
    // Atualizar estado local imediatamente para feedback instantâneo
    setLocalFavorite(!localFavorite);
    // Atualizar estado global
    toggleFavorite(player);
  }}
  className={`p-2 rounded-full transition-all duration-300 transform hover:scale-110 active:scale-95 ${
    localFavorite 
      ? 'bg-red-500 bg-opacity-20 text-red-400 hover:bg-opacity-30' 
      : 'bg-gray-700 text-gray-400 hover:text-white hover:bg-gray-650'
  }`}
  aria-pressed={localFavorite}
  role="button"
  title={localFavorite ? t('playerDashboard.removeFromFavorites') : t('playerDashboard.addToFavorites')}
>
  <Heart 
    size={20} 
    fill={localFavorite ? '#f56565' : 'none'} 
    className={`transition-transform duration-300 ease-in-out ${
      localFavorite ? 'scale-125' : 'scale-100'
    }`}
  />
</button>

      </div>
      
      {/* Player Content */}
      <div className="p-6 grid grid-cols-1 md:grid-cols-5 gap-6">
        {/* Player Details Column */}
        <div className="md:col-span-2 space-y-6">
          <div className="bg-gray-750 rounded-lg p-5">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <User className="mr-2" size={18} />
              {t('playerDashboard.details')}
            </h3>
            
            <div className="space-y-3">
              {/* Position */}
              {/* Format positions using the new function */}
              {player.positions && player.positions.length > 0 && (
                <div className="flex">
                  <div className="w-1/3 text-gray-400">{t('playerDashboard.position')}</div>
                  <div className="w-2/3 text-white">
                    {player.positions.map(pos => formatPlayerPositionCode(pos, t)).join(', ')}
                  </div>
                </div>
              )}
              
              {/* Age */}
              {player.age && (
                <div className="flex">
                  <div className="w-1/3 text-gray-400">{t('playerDashboard.age')}</div>
                  <div className="w-2/3 text-white">{player.age}</div>
                </div>
              )}
              
              {/* Preferred Foot */}
              {/* Format preferred foot using the new function */}
              {player.foot && (
                <div className="flex">
                  <div className="w-1/3 text-gray-400">{t('playerDashboard.foot')}</div>
                  <div className="w-2/3 text-white">{formatPreferredFoot(player.foot, t)}</div>
                </div>
              )}
              
              {/* Height */}
              {player.height && (
                <div className="flex">
                  <div className="w-1/3 text-gray-400">{t('playerDashboard.height')}</div>
                  <div className="w-2/3 text-white">{player.height} cm</div>
                </div>
              )}
              
              {/* Weight */}
              {player.weight && (
                <div className="flex">
                  <div className="w-1/3 text-gray-400">{t('playerDashboard.weight')}</div>
                  <div className="w-2/3 text-white">{player.weight} kg</div>
                </div>
              )}
              
              {/* Market Value */}
              {player.value && (
                <div className="flex">
                  <div className="w-1/3 text-gray-400">{t('playerDashboard.value')}</div>
                  <div className="w-2/3 text-white">{formatValue(player.value)}</div>
                </div>
              )}
            </div>
          </div>
          
         {/* Key stats grid */}
<div className="bg-gray-750 rounded-lg p-5">
  <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
    <BarChart3 className="mr-2" size={18} />
    {t('playerDashboard.statistics')}
  </h3>
  
  <div className="grid grid-cols-2 gap-3">
    {playerMetrics.slice(0, 6).map((metric, index) => {
      // Obter o nome formatado usando a função de tradução
      const name = formatMetricName(metric.key, t);
      
      // Obter o ícone e categoria separadamente
      const iconName = getMetricIcon(metric.key);
      const category = getMetricCategory(metric.key);
      
      return (
        <div key={index} className={`bg-gray-800 rounded-lg p-3 metric-${category}`}>
          <div className="flex items-center gap-2 text-xs text-gray-400 mb-1">
            {/* Renderizar o ícone usando a classe de ícone */}
            <span className={`icon icon-${iconName} text-gray-500`} style={{fontSize: '14px'}} />
            {name}
          </div>
          <div className="flex justify-between items-center">
            <div className={`${metric.colorClass || 'text-white'} font-medium`}>
              {metric.value}
            </div>
            {metric.positionAverage && (
              <div className="text-xs text-gray-400">
                avg: {metric.positionAverage.toFixed(1)}
              </div>
            )}
          </div>
        </div>
      );
    })}
  </div>
</div>
          
          {/* View Complete Profile Button */}
          <button
            onClick={() => onViewComplete(player)}
            className="w-full py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-lg font-medium shadow-md flex items-center justify-center"
          >
            <UserCircle className="mr-2" size={18} />
            {t('playerDashboard.viewCompleteProfile')}
          </button>
        </div>
        
        {/* Radar Chart Column */}
        <div className="md:col-span-3">
          <div className="bg-gray-750 rounded-lg p-5 h-full flex flex-col">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <TrendingUp className="mr-2" size={18} />
              {t('playerDashboard.overview')}
            </h3>
            
            <div className="flex-1 mt-2">
              {selectedRadarMetrics.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%" minHeight={300}>
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
                      name={player.name}
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
                              {metric.value}
                            </p>
                            {metric.positionAverage && (
                              <div className="flex justify-between text-xs mt-1">
                                <span className="text-gray-400">Avg:</span>
                                <span className="text-gray-300">{metric.positionAverage.toFixed(1)}</span>
                              </div>
                            )}
                            {isNegative && (
                              <div className="text-xs text-gray-400 mt-1 italic">
                                *Lower is better
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
                  No metrics available for this player.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlayerDashboard;
