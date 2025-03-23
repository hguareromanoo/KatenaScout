import React, { useState, useRef, useEffect } from 'react';
import { Send, Menu, User } from 'lucide-react';
import { useTranslation, useSession, useUI, useComparison } from '../contexts';
import { chatService, playerService } from '../api/api';
import { formatMetricName } from '../utils/formatters';

/**
 * ChatInterface Component - Handles user chat interaction and player search
 */
const ChatInterface = ({ expanded = true }) => {
  const { t, currentLanguage } = useTranslation();
  const { setSidebarOpen } = useUI();
  const { sessionId, handlePlayerSelected, chatHistory, addMessage, updateSearchResults } = useSession();
  const { startComparison, completeComparison } = useComparison();
  
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isPlayerSearch, setIsPlayerSearch] = useState(false);
  const [lastMessageWasSatisfactionQuestion, setLastMessageWasSatisfactionQuestion] = useState(false);
  
  // States for player comparison selection
  const [isComparisonMode, setIsComparisonMode] = useState(false);
  const [selectedPlayersForComparison, setSelectedPlayersForComparison] = useState([]);
  const [lastSearchResults, setLastSearchResults] = useState([]);
  
  const messagesEndRef = useRef(null);
  
  // Scroll to bottom when chat history changes
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory]);

  /**
   * Handle form submission to send message
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    try {
      setIsLoading(true);
      
      // Check if it looks like a player search query
      const playerSearchKeywords = [
        'player', 'jogador', 'attacking', 'midfielder', 'defender', 'goalkeeper', 
        'goleiro', 'forward', 'striker', 'find', 'search', 'buscar', 'procurar',
        'midfielder', 'meio-campista', 'defense', 'attack', 'zagueiro', 'atacante',
        'fast', 'tall', 'rápido', 'alto', 'shooting', 'passing', 'dribbling'
      ];
      
      // Check if any keywords are in the input (case insensitive)
      const lowerInput = input.toLowerCase();
      setIsPlayerSearch(playerSearchKeywords.some(word => lowerInput.includes(word.toLowerCase())));
      
      // Check if we're responding to a satisfaction question
      const isSatisfactionResponse = lastMessageWasSatisfactionQuestion && 
        (lowerInput.includes('não') || 
         lowerInput.includes('refinar') || 
         lowerInput.includes('outros') ||
         lowerInput.includes('no') || 
         lowerInput.includes('more') ||
         lowerInput.includes('other') ||
         lowerInput.includes('different'));
         
      // Add user's message to chat
      addMessage({ text: input, sender: 'user' });

      // Prepare the request body for the unified backend
      const requestBody = {
        session_id: sessionId,
        query: input,
        is_follow_up: chatHistory.length > 0,
        satisfaction: isSatisfactionResponse ? false : null,
        language: currentLanguage
      };

      const data = await chatService.enhancedSearch(requestBody);
      
      if (data.success) {
        // Get players from the response based on the type of response
        let playersData = [];
        let responseText = '';
        let responseType = '';
        
        // Handle different response types from unified backend
        if (data.players) {
          // Standard search results
          playersData = data.players;
          responseText = data.response;
          responseType = 'search';
          // Confirm it was a player search
          setIsPlayerSearch(true);
          console.log(`Found ${playersData.length} players in search results:`, 
            playersData.map(p => p.name).join(', '));
          
          // Explicitly update search results for comparison
          if (playersData.length > 0) {
            // Store in session context
            updateSearchResults(playersData);
            
            // Also store in local state for comparison feature
            setLastSearchResults(playersData);
            
            // Exit comparison mode when new search results arrive
            if (isComparisonMode) {
              setIsComparisonMode(false);
              setSelectedPlayersForComparison([]);
            }
          }
        } else if (data.comparison) {
          // Comparison results
          playersData = data.players || [];
          // Ensure responseText is a string - data.comparison could be an object or null
          responseText = typeof data.comparison === 'string' 
            ? data.comparison 
            : (data.text || data.response || t('playerComparison.defaultText', 'Player comparison results'));
          responseType = 'comparison';
          // Comparison is related to players
          setIsPlayerSearch(true);
          console.log(`Found ${playersData.length} players in comparison results:`, 
            playersData.map(p => p.name).join(', '));
          
          // Explicitly update search results for comparison
          if (playersData.length > 0) {
            updateSearchResults(playersData);
          }
        } else if (data.explanations) {
          // Stats explanation
          responseText = data.text || data.response;
          responseType = 'explanation';
          // Stats explanation is not directly a player search
          setIsPlayerSearch(false);
        } else {
          // Text-only response (like casual conversation)
          responseText = data.response;
          responseType = 'conversation';
          // Generic conversation is not a player search
          setIsPlayerSearch(false);
        }

        // Check if the response contains a satisfaction question (with safety check for undefined responseText)
        const hasSatisfactionQuestion = responseText && typeof responseText === 'string' ? (
          responseText.toLowerCase().includes('satisfeito') || 
          responseText.toLowerCase().includes('satisfied') ||
          responseText.toLowerCase().includes('refinar sua busca') ||
          responseText.toLowerCase().includes('refine your search')
        ) : false;
        
        setLastMessageWasSatisfactionQuestion(hasSatisfactionQuestion);

        // Add the response to the chat
        addMessage({
          text: responseText,
          sender: 'bot',
          showPlayerSelection: playersData.length > 0,
          players: playersData,
          // Add metadata for special responses
          responseType: responseType,
          explanations: data.explanations,
          comparison_aspects: data.comparison_aspects
        });
        
        // For player comparison results, potentially trigger comparison view
        if (data.comparison && playersData && playersData.length >= 2) {
          // This could trigger a comparison view or another action
          console.log('Comparison results available:', playersData.length, 'players');
        }
      } else {
        // Handle error response
        addMessage({ 
          text: data.message || data.error || t('chat.errorMessage'),
          sender: 'bot',
          isError: true
        });
      }
    } catch (error) {
      console.error('Error:', error);
      addMessage({
        text: t('chat.errorMessage'),
        sender: 'bot',
        isError: true
      });
    } finally {
      setIsLoading(false);
      setInput('');
      // Reset the player search status for the next query
      // We'll set it again when the next query is submitted
      setTimeout(() => setIsPlayerSearch(false), 500);
    }
  };

  /**
   * Handle player selection from search results
   */
  const handlePlayerSelect = (player) => {
    try {
      // Safety check for player object
      if (!player) {
        console.error("[ERROR] Player is undefined or null");
        addMessage({
          text: t('errors.playerNotFound'),
          sender: 'bot',
          isError: true
        });
        return;
      }
      
      // Extract metrics from the player object with validation
      const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => {
        return {
          name: formatMetricName(key),
          value: value !== undefined && value !== null ? value : 0, // Provide fallback
          key: key,
          originalValue: value // Keep original for debugging
        };
      });
      
      // Ensure this player is in the search results
      // This will allow it to be used for comparison
      updateSearchResults([player]);
  
      addMessage({
        text: `${t('chat.showingDetails')} ${player.name || t('playerDashboard.player')}...`,
        sender: 'bot'
      });
      
      // Call the session context method to show the player dashboard
      handlePlayerSelected(player, playerMetrics);
    } catch (error) {
      console.error("[CRITICAL] Error in handlePlayerSelect:", error);
      // Add a nice error message to the chat
      addMessage({
        text: t('errors.loadingFailed'),
        sender: 'bot',
        isError: true
      });
    }
  };
  
  /**
   * Toggle comparison selection mode
   */
  const toggleComparisonMode = () => {
    // If turning off comparison mode, clear selections
    if (isComparisonMode) {
      setSelectedPlayersForComparison([]);
    }
    setIsComparisonMode(!isComparisonMode);
  };

  /**
   * Handle player selection/deselection for comparison
   */
  const handlePlayerSelectionForComparison = (player) => {
    setSelectedPlayersForComparison(prev => {
      // Check if player is already selected
      const isAlreadySelected = prev.some(p => 
        (p.id && player.id && p.id === player.id) || 
        (p.wyId && player.wyId && p.wyId === player.wyId) ||
        (p.name && player.name && p.name === player.name)
      );
      
      if (isAlreadySelected) {
        // Remove player if already selected
        return prev.filter(p => 
          !((p.id && player.id && p.id === player.id) || 
            (p.wyId && player.wyId && p.wyId === player.wyId) ||
            (p.name && player.name && p.name === player.name))
        );
      } else {
        // Add player if not already selected (limit to 2 players)
        if (prev.length < 2) {
          return [...prev, player];
        } else {
          // Already have 2 players - replace the oldest one
          return [prev[1], player];
        }
      }
    });
  };

  /**
   * Start the comparison with selected players
   */
  const startComparisonWithSelected = async () => {
    if (selectedPlayersForComparison.length < 2) {
      console.error("[ERROR] Need to select 2 players for comparison");
      addMessage({
        text: t('errors.selectTwoPlayers', 'Please select 2 players to compare'),
        sender: 'bot',
        isError: true
      });
      return;
    }
    
    // Exit comparison mode
    setIsComparisonMode(false);
    
    try {
      console.log("Selected players for comparison:", selectedPlayersForComparison);
      
      // Get the two players for comparison
      const player1 = selectedPlayersForComparison[0];
      const player2 = selectedPlayersForComparison[1];
      
      // Trigger the visual comparison modal
      startComparison(player1);
      completeComparison(player2);
      
      // Success message in chat
      addMessage({
        text: t('chat.comparisonStarted', 'Opening comparison between {player1} and {player2}.')
          .replace('{player1}', player1.name)
          .replace('{player2}', player2.name),
        sender: 'bot'
      });
    } catch (error) {
      console.error("[ERROR] Starting comparison failed:", error);
      addMessage({
        text: t('errors.comparisonFailed', 'Failed to start player comparison'),
        sender: 'bot',
        isError: true
      });
    } finally {
      setSelectedPlayersForComparison([]); // Clear selections after comparison
    }
  };

  /**
   * Legacy handler for direct player comparison (keeping for compatibility)
   */
  const handleComparePlayersSelect = async (players) => {
    if (!players || players.length < 2) {
      console.error("[ERROR] Not enough players for comparison");
      addMessage({
        text: t('errors.notEnoughPlayers', 'Not enough players to compare'),
        sender: 'bot',
        isError: true
      });
      return;
    }
    
    try {
      console.log("Players for direct comparison:", players);
      
      // Get the two players for comparison
      const player1 = players[0];
      const player2 = players[1];
      
      // Trigger the visual comparison modal
      startComparison(player1);
      completeComparison(player2);
      
      // Success message in chat
      addMessage({
        text: t('chat.comparisonStarted', 'Opening comparison between {player1} and {player2}.')
          .replace('{player1}', player1.name)
          .replace('{player2}', player2.name),
        sender: 'bot'
      });
    } catch (error) {
      console.error("[ERROR] Starting comparison failed:", error);
      addMessage({
        text: t('errors.comparisonFailed', 'Failed to start player comparison'),
        sender: 'bot',
        isError: true
      });
    }
  };

  return (
    <div className="flex flex-col w-full h-full md:h-auto transition-all duration-300 bg-gray-900 border-r border-gray-700 chat-container overflow-hidden">
      {/* Mokoto Glitch styled header */}
      <div className="bg-gradient-to-r from-green-900 to-blue-900 p-4 flex items-center border-b border-gray-700 relative overflow-hidden">
        {/* Glitch effect patterns */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-grid-pattern"></div>
          <div className="absolute right-0 top-0 w-1/3 h-full opacity-15 glitch-bar"></div>
          <div className="absolute left-0 bottom-0 w-2/3 h-1/4 opacity-10 glitch-pixels"></div>
        </div>
        
        {/* Mobile Menu Toggle - shown only on mobile */}
        <button 
          onClick={() => setSidebarOpen && setSidebarOpen(true)}
          className="text-white md:hidden p-2 mr-2 rounded-md hover:bg-blue-600 transition flex items-center justify-center"
          aria-label="Open menu"
        >
          <Menu size={22} />
        </button>
        
        <div className="w-10 h-10 mr-3 flex items-center justify-center shadow-lg">
          <img src="/logo.png" alt="Katena Logo" className="w-full h-full" />
        </div>
        <div className="glitch-text">
          <h1 className="text-xl font-bold text-white relative">{t('chat.headerTitle')}</h1>
          <p className="text-xs text-green-200 opacity-80">{t('chat.headerSubtitle')}</p>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900 bg-opacity-90 relative custom-scrollbar" style={{ maxHeight: 'calc(100vh - 140px)' }}>
        {/* Soccer field background pattern */}
        <div className="absolute inset-0 opacity-5 pointer-events-none">
          <div className="w-full h-full border-2 border-white"></div>
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-white"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 border-2 border-white rounded-full"></div>
        </div>
        
        {chatHistory.length === 0 && (
          <div className="text-center py-10 relative z-10">
            <div className="w-20 h-20 mx-auto mb-4 flex items-center justify-center shadow-lg">
              <img src="/logo.png" alt="Katena Logo" className="w-full h-full" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">{t('chat.welcomeTitle')}</h2>
            <p className="text-gray-300 mb-6 max-w-md mx-auto">{t('chat.welcomeMessage')}</p>
            
            <div className="bg-gray-800 rounded-lg p-5 mx-auto max-w-md text-left border-l-4 border-green-500">
              <p className="text-white mb-3 font-medium">{t('chat.examplesTitle')}</p>
              <div className="space-y-2">
                <div className="bg-gray-700 rounded-lg p-3 text-sm text-gray-300">
                  {t('chat.example1')}
                </div>
                <div className="bg-gray-700 rounded-lg p-3 text-sm text-gray-300">
                  {t('chat.example2')}
                </div>
                <div className="bg-gray-700 rounded-lg p-3 text-sm text-gray-300">
                  {t('chat.example3')}
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Display Chat Messages */}
        {chatHistory.map((message, index) => (
          <div key={index} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] md:max-w-[75%] rounded-lg p-3 ${
              message.sender === 'user' 
                ? 'bg-green-700 text-white' 
                : 'bg-gray-800 text-gray-200'
            }`}>
              {/* Message Content */}
              <div className={`whitespace-pre-wrap ${message.isError ? 'text-red-300' : ''}`}>{message.text}</div>
              
              {/* Player Selection Section */}
              {message.showPlayerSelection && message.players && message.players.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-700">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-gray-300 font-medium">{t('chat.playersFoundText')}</h3>
                    
                    {/* Compare Players Toggle Button - Only show if we have multiple players */}
                    {message.players.length > 1 && (
                      <button
                        onClick={() => toggleComparisonMode()}
                        className={`text-sm px-3 py-1 rounded ${
                          isComparisonMode 
                            ? 'bg-red-600 hover:bg-red-700 text-white' 
                            : 'bg-blue-600 hover:bg-blue-700 text-white'
                        }`}
                      >
                        {isComparisonMode 
                          ? t('chat.cancelCompare', 'Cancel Compare') 
                          : t('chat.comparePlayersButton', 'Compare Players')}
                      </button>
                    )}
                  </div>
                  
                  {/* Player list for selection */}
                  <div className="space-y-2 max-h-60 overflow-y-auto pr-1 custom-scrollbar">
                    {message.players.map(player => {
                      // Check if this player is selected for comparison
                      const isSelected = selectedPlayersForComparison.some(p => 
                        (p.id && player.id && p.id === player.id) || 
                        (p.wyId && player.wyId && p.wyId === player.wyId) ||
                        (p.name && player.name && p.name === player.name)
                      );
                      
                      return (
                        <div 
                          key={player.id || player.name}
                          className={`${
                            isComparisonMode 
                              ? isSelected ? 'bg-blue-700 hover:bg-blue-600' : 'bg-gray-750 hover:bg-gray-700' 
                              : 'bg-gray-750 hover:bg-gray-700'
                          } rounded-lg p-2 cursor-pointer transition-colors ${
                            isSelected ? 'border-2 border-blue-400' : ''
                          }`}
                          onClick={() => isComparisonMode 
                            ? handlePlayerSelectionForComparison(player) 
                            : handlePlayerSelect(player)
                          }
                        >
                          <div className="flex items-center">
                            {/* Checkbox for comparison mode */}
                            {isComparisonMode && (
                              <div className="mr-2">
                                <div className={`w-5 h-5 rounded flex items-center justify-center ${
                                  isSelected ? 'bg-blue-500 text-white' : 'bg-gray-700'
                                }`}>
                                  {isSelected && <span>✓</span>}
                                </div>
                              </div>
                            )}
                            
                            <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center mr-2">
                              {player.image_url || player.imageDataURL ? (
                                <img 
                                  src={playerService.getPlayerImageUrl(player)} 
                                  alt={player.name} 
                                  className="w-full h-full rounded-full object-cover"
                                  onError={(e) => {
                                    // Log error for debugging
                                    console.warn(`Image load failed for player ${player.name} (ID: ${player.wyId || player.id})`);
                                    
                                    // Prevent infinite error loop
                                    e.target.onerror = null;
                                    // Hide the broken image
                                    e.target.style.display = 'none';
                                    // Replace with Katena logo
                                    const parent = e.target.parentNode;
                                    if (!parent.querySelector('.fallback-icon')) {
                                      const img = document.createElement("img");
                                      img.src = "/logo.png";
                                      img.alt = "Player";
                                      img.className = "w-7 h-7 fallback-icon";
                                      parent.appendChild(img);
                                    }
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
                      );
                    })}
                  </div>
                  
                  {/* Comparison Controls - Only show if in comparison mode */}
                  {isComparisonMode && (
                    <div className="mt-4 flex flex-col">
                      <div className="mb-2 text-sm text-gray-300">
                        {t('chat.selectedPlayersCount', 'Selected Players')}: {selectedPlayersForComparison.length}/2
                      </div>
                      <button
                        onClick={startComparisonWithSelected}
                        disabled={selectedPlayersForComparison.length < 2}
                        className={`w-full py-2 rounded-lg text-white font-medium ${
                          selectedPlayersForComparison.length < 2
                            ? 'bg-gray-600 cursor-not-allowed'
                            : 'bg-green-600 hover:bg-green-700'
                        }`}
                      >
                        {t('chat.compareSelectedButton', 'Compare Selected Players')}
                      </button>
                    </div>
                  )}
                </div>
              )}
              
              {/* Stats Explanation Section */}
              {message.responseType === 'explanation' && message.explanations && (
                <div className="mt-4 pt-4 border-t border-gray-700">
                  <h3 className="text-gray-300 mb-2 font-medium">{t('chat.statsExplanationTitle', 'Statistics Explained')}</h3>
                  <div className="space-y-3 mt-2">
                    {Object.entries(message.explanations).map(([stat, explanation]) => (
                      <div key={stat} className="bg-gray-750 rounded-lg p-3">
                        <div className="font-medium text-green-400 mb-1">{stat}</div>
                        <div className="text-sm text-gray-300">{explanation}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Comparison Results Section */}
              {message.responseType === 'comparison' && message.comparison_aspects && message.comparison_aspects.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-700">
                  <h3 className="text-gray-300 mb-2 font-medium">{t('chat.comparisonAspectsTitle', 'Comparison Aspects')}</h3>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {message.comparison_aspects.map(aspect => (
                      <span key={aspect} className="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">
                        {aspect}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {/* Loading Message */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 text-gray-300 rounded-lg p-3 flex items-center">
              {isPlayerSearch ? (
                /* Logo loader for player search */
                <div className="soccer-loader">
                  <img src="/logo.png" alt="Katena Logo" className="w-6 h-6 animate-bounce" />
                </div>
              ) : (
                /* Jumping dots with gradient for general queries */
                <div className="jumping-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              )}
              {isPlayerSearch ? t('chat.analyzing') : t('chat.thinking', 'Thinking...')}
            </div>
          </div>
        )}
        
        {/* Invisible element to scroll to */}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area - fixed at bottom of chat */}
      <div className="border-t border-gray-700 p-3 bg-gray-800 sticky bottom-0 left-0 right-0 z-20">
        <form onSubmit={handleSubmit} className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 bg-gray-700 border border-gray-600 rounded-l-lg py-3 px-4 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder={t('chat.inputPlaceholder')}
            disabled={isLoading}
          />
          <button
            type="submit"
            className={`bg-green-700 hover:bg-green-600 text-white px-4 rounded-r-lg flex items-center justify-center ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={isLoading}
            aria-label="Send message"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;