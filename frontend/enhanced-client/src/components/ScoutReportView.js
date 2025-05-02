import React, { useState, useRef, useEffect } from 'react';
import { Search, X, User, FileText, Loader, AlertCircle, Trash2 } from 'lucide-react';
import { useTranslation, useSession } from '../contexts';
import appService from '../api/appService';
import { debounce } from 'lodash';
import { playerService } from '../api/api';

/**
 * ScoutReportView Component - Interface for generating advanced scout reports
 */
const ScoutReportView = () => {
  const { t, currentLanguage } = useTranslation();
  const { sessionId } = useSession();
  
  // States for search and selection
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState('');
  const [error, setError] = useState('');
  const [reportUrl, setReportUrl] = useState('');
  const [recentSearches, setRecentSearches] = useState([]);
  const [isFirstSearch, setIsFirstSearch] = useState(true);
  const [allPlayers, setAllPlayers] = useState([]); // This will store all players for client-side filtering
  const [isLoading, setIsLoading] = useState(true);
  const [isSearchFocused, setIsSearchFocused] = useState(false); // New state to track search focus
  
  // Refs
  const searchInputRef = useRef(null);
  const dropAreaRef = useRef(null);
  const draggedPlayerRef = useRef(null);
  
  // Load all players once on component mount
  useEffect(() => {
    const loadAllPlayers = async () => {
      try {
        setIsLoading(true);
        // Get all players from backend - we'll use an empty query to get all players
        const players = await appService.searchPlayersByName('', { limit: 1000 });
        setAllPlayers(players || []);
        console.log(`Loaded ${players.length} players for quick search`);
      } catch (error) {
        console.error('Error loading players:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadAllPlayers();
  }, []);
  
  // Load recent searches from localStorage on component mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem('recentPlayerSearches');
      if (saved) {
        const parsed = JSON.parse(saved);
        setRecentSearches(Array.isArray(parsed) ? parsed.slice(0, 5) : []);
      }
    } catch (e) {
      console.error("Error loading recent searches", e);
    }
  }, []);
  
  // Save recent search to localStorage
  const saveRecentSearch = (player) => {
    try {
      // Get existing or create new array
      const existing = JSON.parse(localStorage.getItem('recentPlayerSearches') || '[]');
      // Filter out duplicates of this player
      const filtered = existing.filter(p => (p.wyId || p.id) !== (player.wyId || player.id));
      // Add this player at the start
      const updated = [player, ...filtered].slice(0, 5); // Keep only 5 most recent
      localStorage.setItem('recentPlayerSearches', JSON.stringify(updated));
      setRecentSearches(updated);
    } catch (e) {
      console.error("Error saving recent search", e);
    }
  };
  
  // Remove a player from recent searches
  const removeFromRecentSearches = (e, playerId) => {
    e.stopPropagation(); // Prevent the click from selecting the player
    try {
      const existing = JSON.parse(localStorage.getItem('recentPlayerSearches') || '[]');
      const filtered = existing.filter(p => (p.wyId || p.id) !== playerId);
      localStorage.setItem('recentPlayerSearches', JSON.stringify(filtered));
      setRecentSearches(filtered);
    } catch (e) {
      console.error("Error removing player from recent searches", e);
    }
  };

  // Clear all recent searches
  const clearRecentSearches = () => {
    try {
      localStorage.removeItem('recentPlayerSearches');
      setRecentSearches([]);
    } catch (e) {
      console.error("Error clearing recent searches", e);
    }
  };
  
  // Filter players instantly as user types (no debounce needed for client-side filtering)
  useEffect(() => {
    if (!searchQuery) {
      setSearchResults([]);
      return;
    }
    
    setIsSearching(true);
    
    const query = searchQuery.toLowerCase().trim();
    
    // Simple client-side filtering
    const filteredPlayers = allPlayers.filter(player => 
      player.name.toLowerCase().includes(query)
    ).slice(0, 15); // Limit to 15 results for performance
    
    // Sort by relevance (exact match, starts with, contains)
    filteredPlayers.sort((a, b) => {
      const aName = a.name.toLowerCase();
      const bName = b.name.toLowerCase();
      
      // Exact match gets highest priority
      if (aName === query && bName !== query) return -1;
      if (bName === query && aName !== query) return 1;
      
      // Starts with gets next priority
      if (aName.startsWith(query) && !bName.startsWith(query)) return -1;
      if (bName.startsWith(query) && !aName.startsWith(query)) return 1;
      
      // Default to alphabetical
      return aName.localeCompare(bName);
    });
    
    setSearchResults(filteredPlayers);
    setIsSearching(false);
    
  }, [searchQuery, allPlayers]);
  
  // Handle player selection with recent search saving
  const handlePlayerSelect = (player) => {
    setSelectedPlayer(player);
    setSearchQuery('');
    setSearchResults([]);
    saveRecentSearch(player);
  };
  
  // Handle drag start
  const handleDragStart = (e, player) => {
    draggedPlayerRef.current = player;
    
    // Set drag image (optional)
    if (e.dataTransfer.setDragImage) {
      const dragImage = document.createElement('div');
      dragImage.classList.add('drag-image');
      dragImage.innerHTML = `
        <div class="bg-gray-800 p-2 rounded-lg shadow-lg border border-green-600 flex items-center">
          <div class="w-8 h-8 bg-gray-700 rounded-full mr-2 flex items-center justify-center overflow-hidden">
            ${player.image_url ? `<img src="${playerService.getPlayerImageUrl(player.id)}" alt="" />` : '⚽'}
          </div>
          <span class="text-white text-sm font-medium">${player.name}</span>
        </div>
      `;
      document.body.appendChild(dragImage);
      e.dataTransfer.setDragImage(dragImage, 0, 0);
      
      // Remove the element after drag starts
      setTimeout(() => {
        document.body.removeChild(dragImage);
      }, 0);
    }
    
    e.dataTransfer.setData('text/plain', JSON.stringify({ id: player.wyId || player.id }));
    e.dataTransfer.effectAllowed = 'move';
  };
  
  // Handle drag over
  const handleDragOver = (e) => {
    e.preventDefault();
    if (dropAreaRef.current) {
      dropAreaRef.current.classList.add('border-green-500');
      dropAreaRef.current.classList.add('bg-green-900');
      dropAreaRef.current.classList.add('bg-opacity-20');
    }
  };
  
  // Handle drag leave
  const handleDragLeave = () => {
    if (dropAreaRef.current) {
      dropAreaRef.current.classList.remove('border-green-500');
      dropAreaRef.current.classList.remove('bg-green-900');
      dropAreaRef.current.classList.remove('bg-opacity-20');
    }
  };
  
  // Handle drop
  const handleDrop = (e) => {
    e.preventDefault();
    handleDragLeave();
    
    if (draggedPlayerRef.current) {
      setSelectedPlayer(draggedPlayerRef.current);
      setSearchQuery('');
      setSearchResults([]);
      saveRecentSearch(draggedPlayerRef.current);
    }
  };
  
  // Clear selected player
  const clearSelectedPlayer = () => {
    setSelectedPlayer(null);
    setReportUrl('');
  };
  
  // Generate report
  const generateReport = async () => {
    if (!selectedPlayer) return;
    
    try {
      setIsGenerating(true);
      setError('');
      setReportUrl('');
      
      // Simulate generation steps
      const steps = [
        'searchingDatabase',
        'analyzingMatches',
        'analyzingStats',
        'analyzingHistory',
        'generatingReport'
      ];
      
      // Call the scout report API
      const playerId = selectedPlayer.wyId || selectedPlayer.id;
      const language = currentLanguage === 'english' ? 'en' : 
                      currentLanguage === 'portuguese' ? 'pt' : 
                      currentLanguage === 'spanish' ? 'es' : 
                      currentLanguage === 'bulgarian' ? 'bg' : 'pt';
      
      // Simulate steps with delays
      for (const step of steps) {
        setGenerationStep(step);
        // Wait for a short time to show the step
        await new Promise(resolve => setTimeout(resolve, 800));
      }
      
      // Make the actual API call
      const response = await appService.generateScoutReport({
        session_id: sessionId,
        player_id: playerId,
        language: language,
        format: 'html'
      });
      
      // Create a blob URL for the HTML content
      const blob = new Blob([response], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      setReportUrl(url);
      
    } catch (error) {
      console.error('Error generating report:', error);
      setError(t('scoutReport.generationFailed'));
    } finally {
      setIsGenerating(false);
      setGenerationStep('');
    }
  };
  
  // Render loading animation based on current step
  const renderLoadingAnimation = () => {
    return (
      <div className="flex flex-col items-center justify-center p-8">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-gray-600 border-t-green-500 rounded-full animate-spin mb-4"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <FileText className="text-green-500" size={20} />
          </div>
        </div>
        
        <div className="mt-4 space-y-2 w-64">
          {['searchingDatabase', 'analyzingMatches', 'analyzingStats', 'analyzingHistory', 'generatingReport'].map((step) => (
            <div 
              key={step} 
              className={`flex items-center p-2 rounded ${
                generationStep === step 
                  ? 'bg-green-900 bg-opacity-30 border border-green-700' 
                  : generationStep && steps.indexOf(generationStep) > steps.indexOf(step)
                    ? 'text-gray-500' 
                    : 'text-gray-600'
              }`}
            >
              {generationStep && steps.indexOf(generationStep) > steps.indexOf(step) ? (
                <div className="w-4 h-4 mr-2 rounded-full bg-green-500 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-white" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              ) : generationStep === step ? (
                <div className="w-4 h-4 mr-2 rounded-full border-2 border-green-500 border-t-transparent animate-spin"></div>
              ) : (
                <div className="w-4 h-4 mr-2 rounded-full border border-gray-600"></div>
              )}
              <span>{t(`scoutReport.steps.${step}`)}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  // Define steps array for the loading animation
  const steps = ['searchingDatabase', 'analyzingMatches', 'analyzingStats', 'analyzingHistory', 'generatingReport'];
  
  // Render search results with recent searches
  const renderSearchResults = () => {
    // Show recent searches if we have them, no query, and the search is focused
    if (!searchQuery && recentSearches.length > 0 && isSearchFocused) {
      return (
        <div className="mt-2 bg-gray-800 border border-gray-700 rounded-lg shadow-lg max-h-80 overflow-y-auto">
          <div className="p-2 border-b border-gray-700 flex justify-between items-center">
            <p className="text-xs text-gray-400 uppercase tracking-wider px-2 py-1">
              {t('scoutReport.recentSearches')}
            </p>
            <button 
              onClick={clearRecentSearches}
              className="text-xs text-gray-400 hover:text-white flex items-center px-2 py-1 hover:bg-gray-700 rounded transition-colors"
            >
              <Trash2 size={14} className="mr-1" />
              {t('scoutReport.clearSearchHistory')}
            </button>
          </div>
          <div className="p-2">
            {recentSearches.map((player) => (
              <div key={`recent-${player.wyId || player.id}`} className="relative group">
                <PlayerSearchResult 
                  player={player} 
                  onSelect={handlePlayerSelect}
                  onDragStart={handleDragStart}
                  t={t}
                />
                <button
                  onClick={(e) => removeFromRecentSearches(e, player.wyId || player.id)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-white hover:bg-gray-600 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                  title={t('common.remove')}
                >
                  <X size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>
      );
    }
    
    // Show search results if we have them
    if (searchResults.length > 0) {
      return (
        <div className="mt-2 bg-gray-800 border border-gray-700 rounded-lg shadow-lg max-h-80 overflow-y-auto">
          <div className="p-2">
            {searchResults.map((player) => (
              <PlayerSearchResult 
                key={player.wyId || player.id} 
                player={player} 
                onSelect={handlePlayerSelect}
                onDragStart={handleDragStart}
                t={t}
              />
            ))}
          </div>
        </div>
      );
    }
    
    // No results message
    if (searchQuery && searchResults.length === 0 && !isSearching) {
      return (
        <div className="mt-2 p-4 bg-gray-800 border border-gray-700 rounded-lg text-gray-400 text-center">
          {t('scoutReport.noResults')}
        </div>
      );
    }
    
    return null;
  };
  
  return (
    <div className="flex flex-col w-full h-full bg-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-900 to-blue-900 p-4 flex items-center border-b border-gray-700 relative overflow-hidden">
        {/* Glitch effect patterns */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-grid-pattern"></div>
          <div className="absolute right-0 top-0 w-1/3 h-full opacity-15 glitch-bar"></div>
          <div className="absolute left-0 bottom-0 w-2/3 h-1/4 opacity-10 glitch-pixels"></div>
        </div>
        
        <div className="w-10 h-10 mr-3 flex items-center justify-center shadow-lg">
          <FileText className="text-white" size={24} />
        </div>
        <div className="glitch-text">
          <h1 className="text-xl font-bold text-white relative">{t('scoutReport.headerTitle')}</h1>
          <p className="text-xs text-green-200 opacity-80">{t('scoutReport.headerSubtitle')}</p>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-4xl mx-auto">
          {/* Introduction */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-2">{t('scoutReport.title')}</h2>
            <p className="text-gray-300">{t('scoutReport.description')}</p>
          </div>
          
          {/* Search Section */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-white mb-4">{t('scoutReport.searchTitle')}</h3>
            
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="text-gray-400" size={20} />
              </div>
              
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onFocus={() => setIsSearchFocused(true)}
                onBlur={() => setTimeout(() => setIsSearchFocused(false), 200)} // Small delay to allow clicking on results
                placeholder={isLoading ? "Loading players..." : t('scoutReport.searchPlaceholder')}
                className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                disabled={isLoading}
              />
              
              {isLoading && (
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <Loader className="text-gray-400 animate-spin" size={20} />
                </div>
              )}
            </div>
            
            {/* Render search results with the new function */}
            {renderSearchResults()}
          </div>
          
          {/* Selected Player Section */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-white mb-4">{t('scoutReport.selectedPlayerTitle')}</h3>
            
            <div
              ref={dropAreaRef}
              className={`border-2 border-dashed border-gray-700 rounded-lg p-6 transition-colors ${
                selectedPlayer ? 'bg-gray-800' : 'bg-gray-850'
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              {selectedPlayer ? (
                <div className="flex items-center">
                 <div className="w-16 h-16 bg-gray-700 rounded-full mr-4 flex items-center justify-center overflow-hidden">
                  {selectedPlayer.image_url || selectedPlayer.imageDataURL ? (
                    <img 
                      src={playerService.getPlayerImageUrl(selectedPlayer)} 
                      alt={selectedPlayer.name} 
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        // Log error for debugging
                        console.warn(`Image load failed for player ${selectedPlayer.name} (ID: ${selectedPlayer.wyId || selectedPlayer.id})`);
                        
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
                          img.className = "w-10 h-10 fallback-icon";
                          parent.appendChild(img);
                        }
                      }}
                    />
                  ) : (
                    <User className="text-gray-500" size={32} />
                  )}
                </div>
                  
                  <div className="flex-1">
                    <div className="text-xl font-semibold text-white">{selectedPlayer.name}</div>
                    <div className="text-gray-400">
                      {selectedPlayer.team?.name || t('scoutReport.unknownTeam')}
                    </div>
                    <div className="flex mt-1 text-sm text-gray-400">
                      {selectedPlayer.positions && (
                        <span className="mr-3">{selectedPlayer.positions.join(', ')}</span>
                      )}
                      {selectedPlayer.age && (
                        <span>{selectedPlayer.age} {t('playerDashboard.age')}</span>
                      )}
                    </div>
                  </div>
                  
                  <button
                    onClick={clearSelectedPlayer}
                    className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-full transition-colors"
                    title={t('scoutReport.clearSelection')}
                  >
                    <X size={20} />
                  </button>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center text-center py-8">
                  <div className="w-16 h-16 bg-gray-800 rounded-full mb-4 flex items-center justify-center">
                    <User className="text-gray-600" size={32} />
                  </div>
                  <p className="text-gray-400 mb-2">{t('scoutReport.noPlayerSelected')}</p>
                  <p className="text-gray-500 text-sm">{t('scoutReport.selectPlayer')}</p>
                </div>
              )}
            </div>
          </div>
          
          {/* Action Section */}
          {selectedPlayer && !isGenerating && !reportUrl && (
            <div className="mb-8">
              <button
                onClick={generateReport}
                className="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center"
              >
                <FileText className="mr-2" size={18} />
                {t('scoutReport.generateButton')}
              </button>
              
              {error && (
                <div className="mt-4 p-4 bg-red-900 bg-opacity-20 border border-red-700 rounded-lg text-red-200 flex items-center">
                  <AlertCircle className="mr-2 flex-shrink-0" size={20} />
                  <span>{error}</span>
                </div>
              )}
            </div>
          )}
          
          {/* Loading State */}
          {isGenerating && (
            <div className="mb-8">
              {renderLoadingAnimation()}
            </div>
          )}
          
          {/* Report Display */}
          {reportUrl && !isGenerating && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">{t('scoutReport.resultTitle')}</h3>
                <a
                  href={reportUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-400 hover:text-green-300 text-sm flex items-center"
                >
                  {t('scoutReport.openNewTab')} <svg className="ml-1" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                  </svg>
                </a>
              </div>
              
              <div className="bg-white rounded-lg shadow-lg overflow-hidden h-[600px]">
                <iframe 
                  src={reportUrl} 
                  title={`${selectedPlayer.name} - Scout Report`} 
                  className="w-full h-full border-0"
                ></iframe>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Player search result component
const PlayerSearchResult = ({ player, onSelect, onDragStart, t }) => {
  return (
    <div
      data-player-id={player.wyId || player.id}
      className="flex items-center p-2 hover:bg-gray-700 rounded-lg cursor-pointer transition-colors"
      onClick={() => onSelect(player)}
      draggable
      onDragStart={(e) => onDragStart(e, player)}
    >
      <div className="w-10 h-10 bg-gray-700 rounded-full mr-3 flex items-center justify-center overflow-hidden">
        {player.image_url || player.imageDataURL ? (
          <img 
            src={playerService.getPlayerImageUrl(player)} 
            alt={player.name} 
            className="w-full h-full object-cover"
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
      
      <div className="flex-1">
        <div className="font-medium text-white">{player.name}</div>
        <div className="text-sm text-gray-400">
          {player.team?.name || t('scoutReport.unknownTeam')}
        </div>
      </div>
    </div>
  );
};

export default ScoutReportView;