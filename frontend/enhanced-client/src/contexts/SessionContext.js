/**
 * Session context for managing chat session data
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { getFromStorage, setToStorage } from '../utils/storage';

// Create the context
const SessionContext = createContext();

/**
 * Provider component for session context
 */
export const SessionProvider = ({ children }) => {
  // Initialize session ID from localStorage or create a new one
  const [sessionId] = useState(() => {
    return getFromStorage('chatSessionId', `session-${Date.now()}`);
  });

  // State for chat history and selected player
  const [chatHistory, setChatHistory] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [playerMetrics, setPlayerMetrics] = useState([]);
  const [completeProfilePlayer, setCompleteProfilePlayer] = useState(null);
  const [showingCompleteProfile, setShowingCompleteProfile] = useState(false);
  
  // State to track the current search results (for player comparison)
  // Initialize from localStorage if available
  const [currentSearchResults, setCurrentSearchResults] = useState(() => {
    return getFromStorage('currentSearchResults', []);
  });

  // Save session ID to localStorage
  useEffect(() => {
    setToStorage('chatSessionId', sessionId);
  }, [sessionId]);

  // Add a message to chat history
  const addMessage = (message) => {
    // If the message contains player results, save them for comparison later
    if (message.sender === 'bot' && message.players && message.players.length > 0) {
      // For player search results, always replace the current results
      // This ensures we only compare players from the current search
      console.log(`Setting current search results to ${message.players.length} players from latest search`);
      
      // Update state with the new player list
      setCurrentSearchResults(message.players);
      
      // Store in localStorage for persistence
      setToStorage('currentSearchResults', message.players);
    }
    
    setChatHistory(prev => [...prev, message]);
  };

  // Clear chat history
  const clearChatHistory = () => {
    setChatHistory([]);
    // We deliberately don't clear currentSearchResults here 
    // to maintain player data for comparison
  };

  // Handle player selection
  const handlePlayerSelected = (player, metrics = []) => {
    setSelectedPlayer(player);
    setPlayerMetrics(metrics);
  };

  // Handle viewing complete profile
  const viewCompleteProfile = (player) => {
    setSelectedPlayer(null);
    setCompleteProfilePlayer(player);
    setShowingCompleteProfile(true);
  };

  // Close player view
  const closePlayerView = () => {
    setSelectedPlayer(null);
  };

  // Close complete profile view
  const closeCompleteProfile = () => {
    setShowingCompleteProfile(false);
    setCompleteProfilePlayer(null);
  };

  // Update search results explicitly if needed
  const updateSearchResults = (players) => {
    if (players && players.length > 0) {
      // Simply replace the current results
      setCurrentSearchResults(players);
      setToStorage('currentSearchResults', players);
      console.log(`Updated search results to ${players.length} players`);
    }
  };

  // Value provided by the context
  const value = {
    sessionId,
    chatHistory,
    addMessage,
    clearChatHistory,
    selectedPlayer,
    playerMetrics,
    handlePlayerSelected,
    closePlayerView,
    completeProfilePlayer,
    showingCompleteProfile,
    viewCompleteProfile,
    closeCompleteProfile,
    currentSearchResults,
    updateSearchResults
  };

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
};

/**
 * Custom hook to use the session context
 */
export const useSession = () => {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
};

export default SessionContext;