import React, { useState, useEffect, useMemo } from 'react';
import { 
  X, Trophy, User, UserCircle, GitCompare, 
  TrendingUp, ListFilter, BrainCircuit, 
  ChevronRight, ChevronDown, Users as UsersIcon
} from 'lucide-react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, 
  PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend 
} from 'recharts';
import { useTranslation, useComparison, useSession, useLanguage } from '../contexts';
import { playerService } from '../api/api';
import { NEGATIVE_STATS } from '../utils/playerUtils';
import { formatMetricName } from '../utils/formatters';
import TacticalAnalysisPanel from './TacticalAnalysisPanel';

// Playing styles for tactical analysis
const PLAYING_STYLES = [
  { id: 'tiki_taka', name: 'Tiki-Taka', description: 'Short, quick passing with continuous player movement' },
  { id: 'possession_based', name: 'Possession-Based', description: 'Focus on maintaining ball possession' },
  { id: 'counter_attacking', name: 'Counter-Attacking', description: 'Fast transitions from defense to attack' },
  { id: 'high_pressing', name: 'High Pressing', description: 'Aggressive pressing high up the pitch' },
  { id: 'gegenpressing', name: 'Gegenpressing', description: 'Immediate counter-press after losing possession' },
  { id: 'direct_play', name: 'Direct Play', description: 'Vertical, forward passing to attackers' },
  { id: 'fluid_attacking', name: 'Fluid Attacking', description: 'Emphasis on player movement and creative passing' },
  { id: 'low_block', name: 'Low Block', description: 'Defensive, compact shape with counters' },
  { id: 'width_and_depth', name: 'Width & Depth', description: 'Using width and crosses to create opportunities' },
  { id: 'balanced_approach', name: 'Balanced Approach', description: 'Equal focus on defense and attack' },
];

// Formations
const FORMATIONS = [
  '4-3-3', '4-4-2', '4-2-3-1', '3-5-2', '3-4-3', 
  '5-3-2', '4-1-4-1', '4-3-1-2', '4-4-1-1', '3-4-2-1'
];

// Category mapping for UI display
const CATEGORY_LABELS = {
  'attacking': 'Attacking',
  'passing': 'Passing',
  'defending': 'Defending',
  'possession': 'Possession',
  'physical': 'Physical',
  'goalkeeping': 'Goalkeeping',
  'other': 'Other Metrics'
};

// The main component
const PlayerComparisonModal = () => {
  const { t } = useTranslation();
  const { currentLanguage } = useLanguage();
  const { sessionId, currentSearchResults } = useSession();
  const { 
    primaryPlayer, secondPlayer, showComparisonModal, closeComparisonModal,
    comparisonData, setComparisonData, loadingComparison, setLoadingComparison,
    comparisonError, setComparisonError, tacticalAnalysisMode, enterTacticalAnalysisMode,
    exitTacticalAnalysisMode, tacticalAnalysisData, setTacticalAnalysisData,
    loadingTacticalAnalysis, setLoadingTacticalAnalysis, completeComparison, setSecondPlayer
  } = useComparison();
  
  // State for active tab
  const [activeCategory, setActiveCategory] = useState('attacking');
  
  // State for showing AI analysis
  const [showAiAnalysis, setShowAiAnalysis] = useState(false);
  const [aiAnalysisText, setAiAnalysisText] = useState(null);
  const [loadingAiAnalysis, setLoadingAiAnalysis] = useState(false);
  
  // State for style selector modal
  const [showStyleSelector, setShowStyleSelector] = useState(false);
  const [selectedAnalysisStyle, setSelectedAnalysisStyle] = useState('');
  const [selectedAnalysisFormation, setSelectedAnalysisFormation] = useState('');
  
  // State for expanded metrics
  const [expandedMetrics, setExpandedMetrics] = useState({});
  
  // Fetch the comparison data when players are selected
  useEffect(() => {
    console.log("PlayerComparisonModal: Checking conditions for fetchComparisonData");
    console.log("- primaryPlayer:", primaryPlayer ? primaryPlayer.name : "not set");
    console.log("- secondPlayer:", secondPlayer ? secondPlayer.name : "not set");
    console.log("- comparisonData:", comparisonData ? "exists" : "not set");
    console.log("- loadingComparison:", loadingComparison);
    
    if (primaryPlayer && secondPlayer && !comparisonData && !loadingComparison) {
      console.log("All conditions met, fetching comparison data...");
      fetchComparisonData();
    }
  }, [primaryPlayer, secondPlayer, comparisonData, loadingComparison]);
  
  // Reset state when modal is closed
  useEffect(() => {
    if (!showComparisonModal) {
      setActiveCategory('attacking');
      setShowAiAnalysis(false);
      setAiAnalysisText(null);
      setExpandedMetrics({});
      exitTacticalAnalysisMode();
    }
  }, [showComparisonModal, exitTacticalAnalysisMode]);
  
  // Fetch comparison data from API
  const fetchComparisonData = async () => {
    if (!primaryPlayer || !secondPlayer) return;
    
    setLoadingComparison(true);
    setComparisonError(null);
    
    try {
      const result = await playerService.comparePlayer({
        player_ids: [
          primaryPlayer.id || primaryPlayer.wyId,
          secondPlayer.id || secondPlayer.wyId
        ],
        session_id: sessionId,
        language: currentLanguage
      });
      
      if (result.success) {
        setComparisonData(result);
        
        // Set initial active category based on available metrics
        if (result.categorized_metrics) {
          const categories = Object.keys(result.categorized_metrics);
          if (categories.length > 0 && !categories.includes(activeCategory)) {
            setActiveCategory(categories[0]);
          }
        }
      } else {
        setComparisonError(result.message || 'Failed to compare players');
      }
    } catch (error) {
      setComparisonError(error.message || 'An error occurred during comparison');
    } finally {
      setLoadingComparison(false);
    }
  };
  
  // Generate AI analysis
  const generateAiAnalysis = async () => {
    if (!primaryPlayer || !secondPlayer || !comparisonData) return;
    
    // Validate style and formation selections
    if (!selectedAnalysisStyle || !selectedAnalysisFormation) {
      setComparisonError('Please select a playing style and formation first');
      return;
    }
    
    setLoadingAiAnalysis(true);
    
    try {
      const result = await playerService.comparePlayer({
        player_ids: [
          primaryPlayer.id || primaryPlayer.wyId,
          secondPlayer.id || secondPlayer.wyId
        ],
        session_id: sessionId,
        language: currentLanguage,
        include_ai_analysis: true,
        playing_style: selectedAnalysisStyle,
        formation: selectedAnalysisFormation
      });
      
      if (result.success && result.comparison) {
        setAiAnalysisText(result.comparison);
        setShowAiAnalysis(true);
      } else {
        setComparisonError(result.message || 'Failed to generate analysis');
      }
    } catch (error) {
      setComparisonError(error.message || 'An error occurred generating analysis');
    } finally {
      setLoadingAiAnalysis(false);
    }
  };
  
  // Toggle expanded state for a category
  const toggleCategory = (category) => {
    setExpandedMetrics(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };
  
  // Select metrics for radar chart
  const radarMetrics = useMemo(() => {
    if (!comparisonData || !comparisonData.players || comparisonData.players.length < 2) {
      return [];
    }
    
    const player1 = comparisonData.players[0];
    const player2 = comparisonData.players[1];
    
    // Get up to 6-8 metrics for radar chart
    let selectedMetrics = [];
    
    // Try to get a balance of metrics from different categories
    if (comparisonData.categorized_metrics) {
      Object.entries(comparisonData.categorized_metrics).forEach(([category, metrics]) => {
        // Skip goalkeeping if not relevant
        if (category === 'goalkeeping' && 
            (!player1.positions || !player1.positions.includes('gk')) && 
            (!player2.positions || !player2.positions.includes('gk'))) {
          return;
        }
        
        // Add 1-2 metrics from each category
        const categoryMetrics = metrics.slice(0, 2);
        selectedMetrics.push(...categoryMetrics);
      });
    }
    
    // Limit to 8 metrics total
    selectedMetrics = selectedMetrics.slice(0, 8);
    
    // Format for radar data
    const radarData = selectedMetrics.map(metric => {
      const val1 = player1.stats?.[metric];
      const val2 = player2.stats?.[metric];
      const isNegative = NEGATIVE_STATS.includes(metric);
      
      // Create data point for radar chart
      return {
        name: formatMetricName(metric),
        metricName: metric,
        player1Value: normalize(val1, isNegative),
        player2Value: normalize(val2, isNegative),
        player1Original: val1,
        player2Original: val2
      };
    });
    
    return radarData;
    
    // Helper to normalize values for radar chart (0-100 scale)
    function normalize(value, isNegative) {
      if (value === undefined || value === null) return 0;
      
      // Simple normalization for radar chart visualization
      // This is a basic approach for visualization purposes
      let normalizedValue;
      
      if (isNegative) {
        // For negative stats (lower is better)
        // Invert the scale: 0 is best (100 on chart), high values are worse
        normalizedValue = Math.max(0, 100 - Math.min(value * 10, 100));
      } else {
        // For positive stats (higher is better)
        // Direct scale: higher is better
        normalizedValue = Math.min(value * 10, 100);
      }
      
      return Math.max(0, normalizedValue);
    }
  }, [comparisonData]);
  
  // Reset the selector state when the modal is closed
  useEffect(() => {
    if (!showComparisonModal) {
      setShowStyleSelector(false);
      setShowAiAnalysis(false);
      setSelectedAnalysisStyle('');
      setSelectedAnalysisFormation('');
      setAiAnalysisText(null);
    }
  }, [showComparisonModal]);
  
  // If the modal isn't showing or we don't have a primary player, render nothing
  if (!showComparisonModal || !primaryPlayer) {
    return null;
  }
  
  // When second player is not selected (old flow from ChatInterface direct selection)
  // This should rarely happen now with our new flow, but keeping for compatibility
  if (!secondPlayer) {
    // Filter out the primary player from the search results
    // Use multiple properties for better matching
    const otherPlayersInSearch = currentSearchResults.filter(player => {
      // Check ID match (handle both string and number comparisons)
      const idMatch = player.id && primaryPlayer.id && 
                     String(player.id) === String(primaryPlayer.id);
      
      // Check wyId match (handle both string and number comparisons)  
      const wyIdMatch = player.wyId && primaryPlayer.wyId && 
                       String(player.wyId) === String(primaryPlayer.wyId);
      
      // Check name match (case-insensitive)
      const nameMatch = player.name && primaryPlayer.name && 
                       player.name.toLowerCase() === primaryPlayer.name.toLowerCase();
      
      // Exclude player if ANY of the identifiers match
      return !idMatch && !wyIdMatch && !nameMatch;
    });
    
    console.log(`Found ${otherPlayersInSearch.length} other players for comparison`, 
      otherPlayersInSearch.map(p => p.name).join(', '));
    
    // Handle player selection
    const handlePlayerSelect = (player) => {
      // First set the second player
      setSecondPlayer(player);
      // Then complete the comparison process
      completeComparison(player);
    };
    
    return (
      <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-80">
        <div className="bg-gray-800 rounded-lg shadow-lg max-w-md w-full mx-4 p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-white">{t('playerComparison.selectPlayerToCompare', 'Select Player to Compare')}</h2>
            <button 
              onClick={closeComparisonModal} 
              className="text-gray-400 hover:text-white"
            >
              <X size={24} />
            </button>
          </div>
          
          <div className="mb-3">
            <p className="text-gray-300">
              {t('chat.showingDetails', 'Showing details of')} <span className="font-semibold text-white">{primaryPlayer.name}</span>.
              {t('playerComparison.selectPlayerPrompt', 'Please select another player to compare with')}
            </p>
          </div>
          
          {/* Show other players from same search */}
          {otherPlayersInSearch.length > 0 ? (
            <div className="mb-4">
              <h3 className="text-sm font-semibold text-gray-300 mb-2">{t('chat.playersFoundText', 'Players found - Select to see details:')}:</h3>
              <div className="space-y-2 max-h-60 overflow-y-auto custom-scrollbar">
                {otherPlayersInSearch.map((player) => (
                  <div
                    key={player.id || player.name}
                    className="bg-gray-750 hover:bg-gray-700 rounded-lg p-3 cursor-pointer transition-colors"
                    onClick={() => handlePlayerSelect(player)}
                  >
                    <div className="flex items-center">
                      <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center mr-2">
                        {player.image_url || player.imageDataURL ? (
                          <img
                            src={player.image_url || player.imageDataURL || playerService.getPlayerImageUrl(player)}
                            alt={player.name}
                            className="w-full h-full rounded-full object-cover"
                            onError={(e) => {
                              e.target.onerror = null;
                              e.target.src = "";
                              e.target.parentNode.innerHTML = '<span class="text-gray-500 text-xl">⚽</span>';
                            }}
                          />
                        ) : (
                          <User className="text-gray-500" size={20} />
                        )}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-white">{player.name}</div>
                        <div className="text-xs text-gray-400">
                          {player.positions && player.positions.join(', ')}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="text-gray-300 mb-4">
              <p className="mb-2">No other players from this search are available for comparison.</p>
              <p className="mb-4">You need to select at least 2 players in the same search results to compare them.</p>
              <p className="text-yellow-400 font-medium mt-4">Suggestions:</p>
              <ul className="list-disc pl-5 space-y-2 mt-2">
                <li>Go back and search for multiple players with a query like "Find me forwards with good shooting"</li>
                <li>Try a direct comparison query like "Compare Messi and Ronaldo"</li>
                <li>Find players from the same team: "Show me Barcelona midfielders"</li>
              </ul>
            </div>
          )}
          
          <button
            onClick={closeComparisonModal}
            className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }
  
  // Tactical Analysis Mode
  if (tacticalAnalysisMode) {
    return (
      <TacticalAnalysisPanel
        primaryPlayer={primaryPlayer}
        secondPlayer={secondPlayer}
        onClose={exitTacticalAnalysisMode}
      />
    );
  }
  
  // Full comparison modal
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-80 overflow-y-auto py-4">
      <div className="bg-gray-800 rounded-lg shadow-lg max-w-6xl w-full mx-4 my-8 max-h-[90vh] overflow-y-auto custom-scrollbar">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-gray-700">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <GitCompare className="mr-2" size={24} />
            {t('playerComparison.title', 'Player Comparison')}
          </h2>
          <button 
            onClick={closeComparisonModal} 
            className="text-gray-400 hover:text-white"
          >
            <X size={24} />
          </button>
        </div>
        
        {/* Loading State */}
        {loadingComparison && (
          <div className="p-8 flex flex-col items-center justify-center min-h-[400px]">
            <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-gray-300">{t('playerComparison.loading', 'Comparing players...')}</p>
          </div>
        )}
        
        {/* Error State */}
        {comparisonError && (
          <div className="p-8 text-center">
            <div className="bg-red-900 bg-opacity-30 text-red-300 p-4 rounded mb-4">
              {comparisonError}
            </div>
            <button
              onClick={fetchComparisonData}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
            >
              {t('playerComparison.retry', 'Retry')}
            </button>
          </div>
        )}
        
        {/* Comparison Content */}
        {!loadingComparison && !comparisonError && comparisonData && (
          <div className="p-6">
            {/* Players Header */}
            <div className="grid grid-cols-7 gap-4 mb-8">
              {/* Player 1 */}
              <div className={`col-span-3 bg-gray-750 p-4 rounded-lg ${
                comparisonData.overall_winner?.winner === 'player1' ? 'border-2 border-yellow-500' : ''
              }`}>
                <div className="flex items-center mb-3">
                  <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-700 mr-3">
                    <img 
                      src={playerService.getPlayerImageUrl(primaryPlayer)}
                      alt={primaryPlayer.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI1MCIgZmlsbD0iIzNmNDk1ZSIvPjxwYXRoIGZpbGw9IiM2MjczODYiIGQ9Ik01MCwzNWMtOC4yODcsMC0xNSw2LjcxNS0xNSwxNXM2LjcxMywxNSwxNSwxNWM4LjI4NCwwLDE1LTYuNzE1LDE1LTE1UzU4LjI4NCwzNSw1MCwzNXoiLz48cGF0aCBmaWxsPSIjNjI3Mzg2IiBkPSJNODAsODQuNjc5YzAtMjMuNTg3LTEzLjQwMy0yOS4yLTMwLTI5LjJzLTMwLDUuNjEzLTMwLDI5LjJDMzIuMjAzLDk0LjM0LDc2LjI4OSw5Nyw4MCw4NC42Nzl6Ii8+PC9zdmc+';
                      }}
                    />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white truncate">{primaryPlayer.name}</h3>
                    <p className="text-gray-300 text-sm">{primaryPlayer.positions?.join(', ')}</p>
                    {comparisonData.overall_winner?.winner === 'player1' && (
                      <div className="flex items-center text-yellow-500 mt-1">
                        <Trophy size={16} className="mr-1" />
                        <span className="text-sm font-medium">{t('playerComparison.overallWinner', 'Overall Winner')}</span>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Player 1 Score */}
                <div className="bg-gray-700 rounded p-3">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-gray-300 text-sm">{t('playerComparison.score', 'Score')}</span>
                    <span className="font-medium text-white">{comparisonData.overall_winner?.player1_score?.toFixed(1)}</span>
                  </div>
                  <div className="w-full bg-gray-600 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{
                        width: `${(comparisonData.overall_winner?.player1_score / (comparisonData.overall_winner?.player1_score + comparisonData.overall_winner?.player2_score) * 100).toFixed(1)}%`
                      }}
                    ></div>
                  </div>
                </div>
              </div>
              
              {/* Middle - Radar Chart */}
              <div className="col-span-1 flex items-center justify-center">
                <div className="bg-gray-700 w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-lg">
                  {t('playerComparison.vs', 'VS')}
                </div>
              </div>
              
              {/* Player 2 */}
              <div className={`col-span-3 bg-gray-750 p-4 rounded-lg ${
                comparisonData.overall_winner?.winner === 'player2' ? 'border-2 border-yellow-500' : ''
              }`}>
                <div className="flex items-center mb-3">
                  <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-700 mr-3">
                    <img 
                      src={playerService.getPlayerImageUrl(secondPlayer)}
                      alt={secondPlayer.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI1MCIgZmlsbD0iIzNmNDk1ZSIvPjxwYXRoIGZpbGw9IiM2MjczODYiIGQ9Ik01MCwzNWMtOC4yODcsMC0xNSw2LjcxNS0xNSwxNXM2LjcxMywxNSwxNSwxNWM4LjI4NCwwLDE1LTYuNzE1LDE1LTE1UzU4LjI4NCwzNSw1MCwzNXoiLz48cGF0aCBmaWxsPSIjNjI3Mzg2IiBkPSJNODAsODQuNjc5YzAtMjMuNTg3LTEzLjQwMy0yOS4yLTMwLTI5LjJzLTMwLDUuNjEzLTMwLDI5LjJDMzIuMjAzLDk0LjM0LDc2LjI4OSw5Nyw4MCw4NC42Nzl6Ii8+PC9zdmc+';
                      }}
                    />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white truncate">{secondPlayer.name}</h3>
                    <p className="text-gray-300 text-sm">{secondPlayer.positions?.join(', ')}</p>
                    {comparisonData.overall_winner?.winner === 'player2' && (
                      <div className="flex items-center text-yellow-500 mt-1">
                        <Trophy size={16} className="mr-1" />
                        <span className="text-sm font-medium">{t('playerComparison.overallWinner', 'Overall Winner')}</span>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Player 2 Score */}
                <div className="bg-gray-700 rounded p-3">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-gray-300 text-sm">{t('playerComparison.score', 'Score')}</span>
                    <span className="font-medium text-white">{comparisonData.overall_winner?.player2_score?.toFixed(1)}</span>
                  </div>
                  <div className="w-full bg-gray-600 rounded-full h-2">
                    <div
                      className="bg-red-500 h-2 rounded-full"
                      style={{
                        width: `${(comparisonData.overall_winner?.player2_score / (comparisonData.overall_winner?.player1_score + comparisonData.overall_winner?.player2_score) * 100).toFixed(1)}%`
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Radar Chart */}
            <div className="bg-gray-750 p-4 rounded-lg mb-8">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center">
                <TrendingUp className="mr-2" size={18} />
                {t('playerComparison.radarComparison', 'Key Metrics Comparison')}
              </h3>
              
              <div className="h-80">
                {radarMetrics.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart outerRadius="70%" data={radarMetrics}>
                      <PolarGrid stroke="#4a5568" />
                      <PolarAngleAxis 
                        dataKey="name" 
                        tick={{ fill: '#e2e8f0', fontSize: 12 }} 
                      />
                      <PolarRadiusAxis 
                        angle={90} 
                        domain={[0, 100]} 
                        tick={{ fill: '#718096' }} 
                        axisLine={{ stroke: '#4a5568' }} 
                      />
                      <Radar 
                        name={primaryPlayer.name} 
                        dataKey={`player1Value`}
                        stroke="#2563eb" 
                        fill="#2563eb" 
                        fillOpacity={0.3} 
                      />
                      <Radar 
                        name={secondPlayer.name}
                        dataKey={`player2Value`} 
                        stroke="#e11d48" 
                        fill="#e11d48" 
                        fillOpacity={0.3} 
                      />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }}
                        itemStyle={{ color: '#f8fafc' }}
                        formatter={(value, name, props) => {
                          const metric = props.payload;
                          const isNegative = NEGATIVE_STATS.includes(metric.metricName);
                          const originalValue = isNegative 
                            ? metric[`${name.includes(primaryPlayer.name) ? 'player1Original' : 'player2Original'}`]
                            : metric[`${name.includes(primaryPlayer.name) ? 'player1Original' : 'player2Original'}`];
                          
                          return [
                            `${originalValue?.toFixed(2) || value} ${isNegative ? '(Lower is better)' : ''}`,
                            name
                          ];
                        }}
                      />
                      <Legend 
                        verticalAlign="bottom" 
                        align="center" 
                        wrapperStyle={{ color: '#e2e8f0' }}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-full flex items-center justify-center text-gray-400">
                    {t('playerComparison.noMetrics', 'No metrics available for radar chart')}
                  </div>
                )}
              </div>
            </div>
            
            {/* Category Tabs */}
            <div className="bg-gray-750 rounded-lg overflow-hidden mb-8">
              <div className="flex overflow-x-auto bg-gray-700">
                {Object.entries(comparisonData.categorized_metrics || {}).map(([category, metrics]) => (
                  <button
                    key={category}
                    onClick={() => setActiveCategory(category)}
                    className={`px-4 py-3 whitespace-nowrap ${
                      activeCategory === category
                        ? 'bg-gray-750 text-white font-medium'
                        : 'text-gray-300 hover:bg-gray-750 hover:text-white'
                    }`}
                  >
                    {CATEGORY_LABELS[category] || category}
                    {comparisonData.category_winners?.[category] && (
                      <span className={`ml-2 inline-block w-2 h-2 rounded-full ${
                        comparisonData.category_winners[category] === 'player1' 
                          ? 'bg-blue-500' 
                          : comparisonData.category_winners[category] === 'player2'
                            ? 'bg-red-500'
                            : 'bg-gray-500'
                      }`}></span>
                    )}
                  </button>
                ))}
              </div>
              
              {/* Metrics List */}
              <div className="p-4">
                {(comparisonData.categorized_metrics?.[activeCategory] || []).map(metric => {
                  const player1Value = comparisonData.players[0]?.stats?.[metric];
                  const player2Value = comparisonData.players[1]?.stats?.[metric];
                  const winner = comparisonData.metric_winners?.[metric];
                  const isNegative = (comparisonData.negative_metrics || []).includes(metric);
                  
                  return (
                    <div 
                      key={metric} 
                      className="grid grid-cols-7 gap-4 py-3 border-b border-gray-700 last:border-0 items-center"
                    >
                      {/* Player 1 Value */}
                      <div className={`col-span-3 flex justify-end items-center ${
                        winner === 'player1' ? 'text-blue-400 font-semibold' : 'text-gray-300'
                      }`}>
                        {typeof player1Value === 'number' 
                          ? player1Value.toFixed(2) 
                          : player1Value || '—'}
                        {winner === 'player1' && (
                          <Trophy size={16} className="ml-2 text-yellow-500" />
                        )}
                      </div>
                      
                      {/* Metric Name */}
                      <div className="col-span-1 text-center text-sm text-gray-400 px-1">
                        <div className="truncate">{metric}</div>
                        {isNegative && (
                          <span className="text-xs text-gray-500">({t('playerCompletePage.lowerIsBetter', 'Lower is better')})</span>
                        )}
                      </div>
                      
                      {/* Player 2 Value */}
                      <div className={`col-span-3 flex items-center ${
                        winner === 'player2' ? 'text-red-400 font-semibold' : 'text-gray-300'
                      }`}>
                        {winner === 'player2' && (
                          <Trophy size={16} className="mr-2 text-yellow-500" />
                        )}
                        {typeof player2Value === 'number' 
                          ? player2Value.toFixed(2) 
                          : player2Value || '—'}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            
            {/* Single AI Analysis Section - combining tactical and AI features */}
            <div className="mb-6">
              <button
                onClick={() => setShowStyleSelector(!showStyleSelector)}
                className="w-full flex items-center justify-center gap-2 p-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors font-medium"
              >
                <BrainCircuit size={20} />
                {t('tacticalAnalysis.title', 'Tactical Context Analysis')}
                <ChevronDown 
                  size={16} 
                  className={`text-white transition-transform ${
                    showStyleSelector ? 'rotate-180' : ''
                  }`} 
                />
              </button>
              
              {/* Style & Formation Selection Section */}
              {showStyleSelector && (
                <div className="mt-3 bg-gray-750 rounded-lg p-4 border border-gray-700 transition-all">
                  <p className="text-gray-300 mb-4">
                    {t('tacticalAnalysis.introText', 'Select a playing style and formation to analyze how the players would perform in that tactical context.')}
                  </p>
                
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    {/* Style Selection */}
                    <div>
                      <label className="block text-gray-300 mb-2 text-sm font-medium">{t('tacticalAnalysis.selectStyle', 'Playing Style')}</label>
                      <select 
                        value={selectedAnalysisStyle}
                        onChange={(e) => setSelectedAnalysisStyle(e.target.value)}
                        className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white"
                      >
                        <option value="">{t('tacticalAnalysis.selectStyle', 'Select Playing Style')}</option>
                        {PLAYING_STYLES.map(style => (
                          <option key={style.id} value={style.id}>
                            {style.name}
                          </option>
                        ))}
                      </select>
                      {selectedAnalysisStyle && (
                        <p className="mt-1 text-xs text-gray-400">
                          {PLAYING_STYLES.find(s => s.id === selectedAnalysisStyle)?.description}
                        </p>
                      )}
                    </div>
                    
                    {/* Formation Selection */}
                    <div>
                      <label className="block text-gray-300 mb-2 text-sm font-medium">{t('tacticalAnalysis.selectFormation', 'Formation')}</label>
                      <select 
                        value={selectedAnalysisFormation}
                        onChange={(e) => setSelectedAnalysisFormation(e.target.value)}
                        className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-white"
                      >
                        <option value="">{t('tacticalAnalysis.selectFormation', 'Select Formation')}</option>
                        {FORMATIONS.map(formation => (
                          <option key={formation} value={formation}>
                            {formation}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                  
                  {/* Generate Button - Acts like before but also sets tactical mode */}
                  <button
                    onClick={generateAiAnalysis}
                    disabled={!selectedAnalysisStyle || !selectedAnalysisFormation || loadingAiAnalysis}
                    className={`w-full py-3 rounded-md font-medium flex items-center justify-center ${
                      !selectedAnalysisStyle || !selectedAnalysisFormation || loadingAiAnalysis
                        ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                    type="button"
                  >
                    {loadingAiAnalysis ? (
                      <>
                        <div className="w-5 h-5 border-2 border-t-transparent border-white rounded-full animate-spin mr-2"></div>
                        {t('tacticalAnalysis.analyzing', 'Analyzing...')}
                      </>
                    ) : (
                      <>
                        <BrainCircuit className="mr-2" size={18} />
                        {t('tacticalAnalysis.generateAnalysis', 'Generate Analysis')}
                      </>
                    )}
                  </button>
                </div>
              )}
              
              {/* Analysis Results */}
              {aiAnalysisText && (
                <div className="mt-3 bg-gray-750 rounded-lg overflow-hidden">
                  <div className="flex justify-between items-center px-4 py-3 border-b border-gray-700">
                    <h3 className="text-white font-medium flex items-center">
                      <Trophy size={16} className="mr-2 text-yellow-500" />
                      {t('tacticalAnalysis.title', 'Tactical Context Analysis')}
                    </h3>
                    <div className="flex items-center">
                      <span className="text-gray-400 text-sm mr-3">
                        {selectedAnalysisStyle && PLAYING_STYLES.find(s => s.id === selectedAnalysisStyle)?.name} • {selectedAnalysisFormation}
                      </span>
                    </div>
                  </div>
                  <div className="p-4 max-h-80 overflow-y-auto custom-scrollbar">
                    <div className="text-gray-300 whitespace-pre-line">
                      {aiAnalysisText}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlayerComparisonModal;