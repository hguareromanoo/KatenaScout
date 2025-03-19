import React, { createContext, useContext, useState } from 'react';

/**
 * Context for managing player comparison state
 */
const ComparisonContext = createContext();

/**
 * Hook for using the player comparison context
 */
export const useComparison = () => {
  const context = useContext(ComparisonContext);
  if (!context) {
    throw new Error('useComparison must be used within a ComparisonProvider');
  }
  return context;
};

/**
 * Provider component for player comparison functionality
 */
export const ComparisonProvider = ({ children }) => {
  // State for the players being compared
  const [primaryPlayer, setPrimaryPlayer] = useState(null);
  const [secondPlayer, setSecondPlayer] = useState(null);
  
  // State for the player selection mode
  const [selectingSecondPlayer, setSelectingSecondPlayer] = useState(false);
  
  // State for comparison modal visibility
  const [showComparisonModal, setShowComparisonModal] = useState(false);
  
  // State for comparison data
  const [comparisonData, setComparisonData] = useState(null);
  
  // State for loading comparison
  const [loadingComparison, setLoadingComparison] = useState(false);
  
  // State for error messages
  const [comparisonError, setComparisonError] = useState(null);
  
  // State for tactical analysis
  const [tacticalAnalysisMode, setTacticalAnalysisMode] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState('');
  const [selectedFormation, setSelectedFormation] = useState('');
  const [tacticalAnalysisData, setTacticalAnalysisData] = useState(null);
  const [loadingTacticalAnalysis, setLoadingTacticalAnalysis] = useState(false);
  
  /**
   * Start a comparison with the given player as primary
   */
  const startComparison = (player) => {
    setPrimaryPlayer(player);
    setSelectingSecondPlayer(true);
    setShowComparisonModal(true); // Show the modal when starting comparison
    setComparisonData(null);
    setComparisonError(null);
    setTacticalAnalysisMode(false);
    setTacticalAnalysisData(null);
  };
  
  /**
   * Cancel the comparison selection process
   */
  const cancelComparison = () => {
    setSelectingSecondPlayer(false);
    setPrimaryPlayer(null);
  };
  
  /**
   * Complete a comparison with the second player
   */
  const completeComparison = (secondPlayer) => {
    console.log("ComparisonContext: completeComparison called with", secondPlayer?.name);
    // Explicitly set the second player state
    setSecondPlayer(secondPlayer);
    setSelectingSecondPlayer(false);
    setShowComparisonModal(true);
    return { primaryPlayer, secondPlayer };
  };
  
  /**
   * Close the comparison modal
   */
  const closeComparisonModal = () => {
    setShowComparisonModal(false);
    setPrimaryPlayer(null);
    setSecondPlayer(null);
    setComparisonData(null);
    setTacticalAnalysisMode(false);
    setTacticalAnalysisData(null);
    setSelectedStyle('');
    setSelectedFormation('');
  };
  
  /**
   * Enter tactical analysis mode
   */
  const enterTacticalAnalysisMode = () => {
    setTacticalAnalysisMode(true);
    setTacticalAnalysisData(null);
  };
  
  /**
   * Exit tactical analysis mode
   */
  const exitTacticalAnalysisMode = () => {
    setTacticalAnalysisMode(false);
    setTacticalAnalysisData(null);
    setSelectedStyle('');
    setSelectedFormation('');
  };
  
  // Value object for the context
  const value = {
    primaryPlayer,
    secondPlayer,
    selectingSecondPlayer,
    showComparisonModal,
    comparisonData,
    loadingComparison,
    comparisonError,
    
    tacticalAnalysisMode,
    selectedStyle,
    selectedFormation,
    tacticalAnalysisData,
    loadingTacticalAnalysis,
    
    startComparison,
    cancelComparison,
    completeComparison,
    closeComparisonModal,
    setComparisonData,
    setLoadingComparison,
    setComparisonError,
    setSecondPlayer,
    
    enterTacticalAnalysisMode,
    exitTacticalAnalysisMode,
    setSelectedStyle,
    setSelectedFormation,
    setTacticalAnalysisData,
    setLoadingTacticalAnalysis
  };
  
  return (
    <ComparisonContext.Provider value={value}>
      {children}
    </ComparisonContext.Provider>
  );
};

export default ComparisonContext;