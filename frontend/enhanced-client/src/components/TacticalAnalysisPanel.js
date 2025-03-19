import React, { useState } from 'react';
import { 
  X, Trophy, ArrowLeft, BrainCircuit, Users, 
  TrendingUp, BarChart3, BadgeCheck 
} from 'lucide-react';
import { useTranslation, useComparison, useSession, useLanguage } from '../contexts';
import { playerService } from '../api/api';

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

const TacticalAnalysisPanel = ({ primaryPlayer, secondPlayer, onClose }) => {
  const { t } = useTranslation();
  const { currentLanguage } = useLanguage();
  const { sessionId } = useSession();
  const { 
    setTacticalAnalysisData, tacticalAnalysisData, 
    loadingTacticalAnalysis, setLoadingTacticalAnalysis 
  } = useComparison();
  
  const [selectedStyle, setSelectedStyle] = useState('');
  const [selectedFormation, setSelectedFormation] = useState('');
  
  // Generate tactical analysis
  const generateAnalysis = async () => {
    if (!primaryPlayer || !secondPlayer || !selectedStyle || !selectedFormation) {
      return;
    }
    
    setLoadingTacticalAnalysis(true);
    
    try {
      const result = await playerService.generateTacticalAnalysis({
        player_ids: [
          primaryPlayer.id || primaryPlayer.wyId,
          secondPlayer.id || secondPlayer.wyId
        ],
        session_id: sessionId,
        original_query: "", // Could be passed from search context
        playing_style: selectedStyle,
        formation: selectedFormation,
        language: currentLanguage
      });
      
      if (result.success) {
        // Map the backend response to the component's expected format
        const formattedData = {
          analysis: result.tactical_analysis,
          tactical_comparison: result.tactical_data,
          players: result.players
        };
        setTacticalAnalysisData(formattedData);
      } else {
        console.error("Error generating tactical analysis:", result.message);
      }
    } catch (error) {
      console.error("Exception in tactical analysis:", error);
    } finally {
      setLoadingTacticalAnalysis(false);
    }
  };
  
  // Selection screen (when no analysis has been generated yet)
  if (!tacticalAnalysisData) {
    return (
      <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-80 overflow-y-auto">
        <div className="bg-gray-800 rounded-lg shadow-lg max-w-4xl w-full mx-4 my-8">
          {/* Header */}
          <div className="flex justify-between items-center p-6 border-b border-gray-700">
            <div className="flex items-center">
              <button 
                onClick={onClose} 
                className="mr-3 text-gray-400 hover:text-white"
              >
                <ArrowLeft size={20} />
              </button>
              <h2 className="text-xl font-bold text-white flex items-center">
                <BrainCircuit className="mr-2" size={20} />
                {t('tacticalAnalysis.title', 'Tactical Context Analysis')}
              </h2>
            </div>
            <button 
              onClick={onClose} 
              className="text-gray-400 hover:text-white"
            >
              <X size={20} />
            </button>
          </div>
          
          <div className="p-6">
            <div className="mb-6 text-gray-300">
              Select a playing style and formation to analyze how {primaryPlayer.name} and {secondPlayer.name} would perform in that tactical context.
            </div>
            
            {/* Playing Style Selection */}
            <div className="mb-6">
              <h3 className="text-white font-semibold mb-3 flex items-center">
                <Users className="mr-2" size={18} />
                {t('tacticalAnalysis.selectStyle', 'Select Playing Style')}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {PLAYING_STYLES.map(style => (
                  <button
                    key={style.id}
                    onClick={() => setSelectedStyle(style.id)}
                    className={`p-3 rounded-lg text-left transition ${
                      selectedStyle === style.id
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-750 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    <div className="font-medium">{style.name}</div>
                    <div className="text-sm mt-1 opacity-80">{style.description}</div>
                  </button>
                ))}
              </div>
            </div>
            
            {/* Formation Selection */}
            <div className="mb-6">
              <h3 className="text-white font-semibold mb-3 flex items-center">
                <TrendingUp className="mr-2" size={18} />
                {t('tacticalAnalysis.selectFormation', 'Select Formation')}
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
                {FORMATIONS.map(formation => (
                  <button
                    key={formation}
                    onClick={() => setSelectedFormation(formation)}
                    className={`p-3 rounded-lg text-center transition ${
                      selectedFormation === formation
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-750 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    {formation}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Generate Button */}
            <button
              onClick={generateAnalysis}
              disabled={!selectedStyle || !selectedFormation || loadingTacticalAnalysis}
              className={`w-full py-3 rounded-lg font-medium shadow-md flex items-center justify-center ${
                !selectedStyle || !selectedFormation || loadingTacticalAnalysis
                  ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white'
              }`}
            >
              {loadingTacticalAnalysis ? (
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
        </div>
      </div>
    );
  }
  
  // Analysis results screen
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-80 overflow-y-auto">
      <div className="bg-gray-800 rounded-lg shadow-lg max-w-6xl w-full mx-4 my-8">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-gray-700">
          <div className="flex items-center">
            <button 
              onClick={onClose} 
              className="mr-3 text-gray-400 hover:text-white"
            >
              <ArrowLeft size={20} />
            </button>
            <h2 className="text-xl font-bold text-white flex items-center">
              <BrainCircuit className="mr-2" size={20} />
              {t('tacticalAnalysis.title', 'Tactical Context Analysis')}
            </h2>
          </div>
          <div className="flex items-center px-3 py-1 bg-indigo-900 bg-opacity-50 rounded-lg">
            <span className="text-indigo-300 text-sm font-medium mr-2">
              {tacticalAnalysisData.tactical_comparison?.style_display_name || selectedStyle}
            </span>
            <span className="text-white font-medium">
              {tacticalAnalysisData.tactical_comparison?.formation || selectedFormation}
            </span>
          </div>
          <button 
            onClick={onClose} 
            className="text-gray-400 hover:text-white"
          >
            <X size={20} />
          </button>
        </div>
        
        {/* Content */}
        <div className="p-6">
          {/* Style Description */}
          <div className="bg-gray-750 p-4 rounded-lg mb-6">
            <h3 className="text-white font-semibold mb-2">
              {t('tacticalAnalysis.styleDescription', 'Style Description')}
            </h3>
            <p className="text-gray-300">
              {tacticalAnalysisData.tactical_comparison?.style_description || 
               PLAYING_STYLES.find(s => s.id === selectedStyle)?.description}
            </p>
          </div>
          
          {/* Players Comparison */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Player 1 */}
            <div className={`bg-gray-750 p-4 rounded-lg ${
              tacticalAnalysisData.tactical_comparison?.tactical_winner === 'player1' 
                ? 'border-2 border-yellow-500' 
                : ''
            }`}>
              <div className="flex items-center mb-4">
                <div className="w-14 h-14 rounded-full overflow-hidden bg-gray-700 mr-3">
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
                  <h3 className="text-xl font-bold text-white">{primaryPlayer.name}</h3>
                  <p className="text-gray-300 text-sm">{primaryPlayer.positions?.join(', ')}</p>
                  {tacticalAnalysisData.tactical_comparison?.tactical_winner === 'player1' && (
                    <div className="flex items-center text-yellow-500 mt-1">
                      <Trophy size={16} className="mr-1" />
                      <span className="text-sm font-medium">Better Tactical Fit</span>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Fit Score */}
              <div className="bg-gray-700 p-3 rounded-lg mb-4">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-gray-300 text-sm">
                    {t('tacticalAnalysis.fitScore', 'Tactical Fit Score')}
                  </span>
                  <span className="font-medium text-white">
                    {tacticalAnalysisData.tactical_comparison?.player1_fit?.style_score?.toFixed(1)}/100
                  </span>
                </div>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full"
                    style={{
                      width: `${tacticalAnalysisData.tactical_comparison?.player1_fit?.style_score || 0}%`
                    }}
                  ></div>
                </div>
              </div>
              
              {/* Key Strengths */}
              <h4 className="text-white font-medium mb-2 flex items-center">
                <BadgeCheck size={16} className="mr-1" />
                {t('tacticalAnalysis.keyStrengths', 'Key Strengths')}
              </h4>
              <ul className="text-gray-300 text-sm mb-2 space-y-1">
                {tacticalAnalysisData.tactical_comparison?.player1_fit?.key_strengths?.map((strength, index) => (
                  <li key={index} className="flex justify-between">
                    <span>{strength.metric}</span>
                    <span className="text-blue-300">{strength.value.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            {/* Player 2 */}
            <div className={`bg-gray-750 p-4 rounded-lg ${
              tacticalAnalysisData.tactical_comparison?.tactical_winner === 'player2' 
                ? 'border-2 border-yellow-500' 
                : ''
            }`}>
              <div className="flex items-center mb-4">
                <div className="w-14 h-14 rounded-full overflow-hidden bg-gray-700 mr-3">
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
                  <h3 className="text-xl font-bold text-white">{secondPlayer.name}</h3>
                  <p className="text-gray-300 text-sm">{secondPlayer.positions?.join(', ')}</p>
                  {tacticalAnalysisData.tactical_comparison?.tactical_winner === 'player2' && (
                    <div className="flex items-center text-yellow-500 mt-1">
                      <Trophy size={16} className="mr-1" />
                      <span className="text-sm font-medium">Better Tactical Fit</span>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Fit Score */}
              <div className="bg-gray-700 p-3 rounded-lg mb-4">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-gray-300 text-sm">
                    {t('tacticalAnalysis.fitScore', 'Tactical Fit Score')}
                  </span>
                  <span className="font-medium text-white">
                    {tacticalAnalysisData.tactical_comparison?.player2_fit?.style_score?.toFixed(1)}/100
                  </span>
                </div>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div
                    className="bg-red-500 h-2 rounded-full"
                    style={{
                      width: `${tacticalAnalysisData.tactical_comparison?.player2_fit?.style_score || 0}%`
                    }}
                  ></div>
                </div>
              </div>
              
              {/* Key Strengths */}
              <h4 className="text-white font-medium mb-2 flex items-center">
                <BadgeCheck size={16} className="mr-1" />
                {t('tacticalAnalysis.keyStrengths', 'Key Strengths')}
              </h4>
              <ul className="text-gray-300 text-sm mb-2 space-y-1">
                {tacticalAnalysisData.tactical_comparison?.player2_fit?.key_strengths?.map((strength, index) => (
                  <li key={index} className="flex justify-between">
                    <span>{strength.metric}</span>
                    <span className="text-red-300">{strength.value.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          {/* Key Differences */}
          <div className="bg-gray-750 p-4 rounded-lg mb-6">
            <h3 className="text-white font-semibold mb-3 flex items-center">
              <BarChart3 className="mr-2" size={18} />
              {t('tacticalAnalysis.keyDifferences', 'Key Differences')}
            </h3>
            <div className="space-y-3">
              {tacticalAnalysisData.tactical_comparison?.key_differences?.map((diff, index) => (
                <div key={index} className="grid grid-cols-7 gap-4 items-center">
                  <div className={`col-span-3 text-right ${
                    diff.better_player === 'player1' ? 'text-blue-400 font-medium' : 'text-gray-400'
                  }`}>
                    {diff.player1_value.toFixed(2)}
                  </div>
                  <div className="col-span-1 text-center text-gray-300 text-sm px-1">
                    {diff.metric}
                  </div>
                  <div className={`col-span-3 ${
                    diff.better_player === 'player2' ? 'text-red-400 font-medium' : 'text-gray-400'
                  }`}>
                    {diff.player2_value.toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Analysis Text */}
          <div className="bg-gray-750 p-4 rounded-lg">
            <h3 className="text-white font-semibold mb-3">
              Analysis
            </h3>
            <div className="text-gray-300 whitespace-pre-line">
              {tacticalAnalysisData.analysis || "No analysis available."}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TacticalAnalysisPanel;