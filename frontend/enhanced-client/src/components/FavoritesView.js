import React, { useState } from 'react';
import { Heart, Search, Trash2, User, ArrowLeft } from 'lucide-react';
import { useTranslation, useFavorites, useSession, useUI } from '../contexts';
import { filterItems, formatMetricName } from '../utils';
import { playerService } from '../api/api';
import ErrorBoundary from './ErrorBoundary';
import PlayerCompletePage from './PlayerCompletePage';

/**
 * FavoritesView component - Displays and manages favorite players
 */
const FavoritesView = () => {
  const { t } = useTranslation();
  const { favorites, toggleFavorite } = useFavorites();
  const { handlePlayerSelected } = useSession();
  const { setCurrentView } = useUI();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [showingCompleteProfile, setShowingCompleteProfile] = useState(false);
  
  // Filter favorites based on search term using utility function
  const filteredFavorites = filterItems(favorites, searchTerm, ['name', 'positions']);
  
  // Handle viewing complete profile
  const viewCompleteProfile = (player) => {
    setSelectedPlayer(player);
    setShowingCompleteProfile(true);
  };
  
  // Close complete profile view
  const closeCompleteProfile = () => {
    setShowingCompleteProfile(false);
    setSelectedPlayer(null);
  };
  
  return (
    <div className="h-screen flex flex-col">
      {/* Complete Player Profile View - Shown when a user clicks "View Complete Profile" */}
      {showingCompleteProfile && selectedPlayer && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-xl w-full max-w-5xl max-h-[95vh] overflow-hidden relative">
            <ErrorBoundary>
              <PlayerCompletePage 
                player={selectedPlayer}
                onClose={closeCompleteProfile}
              />
            </ErrorBoundary>
          </div>
        </div>
      )}
      
      <div className="max-w-5xl mx-auto w-full p-4 pt-20 md:pt-6 flex-1 overflow-hidden flex flex-col">
        <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden flex flex-col flex-1">
          {/* Header - Fixed */}
          <div className="bg-gradient-to-r from-green-900 to-blue-900 p-4 md:p-6 sticky top-0 z-10">
            <div className="flex items-center justify-between">
              <h1 className="text-xl md:text-2xl font-bold text-white flex items-center">
                <Heart className="mr-2 md:mr-3" />
                {t('favorites.title')}
              </h1>
              
              {/* Back button - only visible on mobile */}
              <button 
                onClick={() => setCurrentView('chat')}
                className="md:hidden text-white hover:text-gray-200 p-1 rounded-full focus:outline-none focus:ring-2 focus:ring-gray-400 flex items-center"
                aria-label={t('common.back')}
              >
                <ArrowLeft size={20} />
                <span className="ml-1 text-sm">{t('common.back')}</span>
              </button>
            </div>
          </div>
          
          {/* Search Bar - Fixed */}
          <div className="p-3 md:p-4 border-b border-gray-700 sticky top-16 md:top-20 z-10 bg-gray-800">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder={t('favorites.searchPlaceholder')}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg py-2 pl-10 pr-4 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
          </div>
          
          {/* Favorites List - Scrollable */}
          <ErrorBoundary>
            <div className="p-4 overflow-y-auto flex-1 scroll-container-mobile custom-scrollbar">
              {filteredFavorites.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-16 h-16 mx-auto mb-4 flex items-center justify-center bg-gray-700 rounded-full">
                    <Heart className="text-gray-500" size={28} />
                  </div>
                  <p className="text-gray-400">{t('favorites.emptyState')}</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filteredFavorites.map((player, index) => (
                  <div 
                    key={player.id || `player-${index}`}
                    className="bg-gray-750 border border-gray-700 rounded-lg overflow-hidden hover:bg-gray-700 transition-colors"
                  >
                    <div className="p-4">
                      <div className="flex items-start">
                        <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                          {player.image_url || player.imageDataURL ? (
                            <img 
                              src={playerService.getPlayerImageUrl(player)} 
                              alt={player.name} 
                              className="w-full h-full rounded-full object-cover"
                              onError={(e) => {
                                // Log error for debugging
                                console.warn(`Favorites: Image load failed for player ${player.name} (ID: ${player.wyId || player.id})`);
                                
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
                            <User className="text-gray-500" size={24} />
                          )}
                        </div>
                        <div className="flex-1">
                          <h3 className="text-white font-medium">{player.name}</h3>
                          <p className="text-gray-400 text-sm">
                            {player.positions && player.positions.join(', ')}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            if (window.confirm(t('favorites.removeConfirm'))) {
                              toggleFavorite(player);
                            }
                          }}
                          type="button"
                          className="text-red-400 hover:text-red-300 p-2 rounded-full hover:bg-gray-650 flex items-center justify-center"
                          title={t('favorites.removeFromFavorites')}
                          aria-label={t('favorites.removeFromFavorites')}
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                      
                      <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                        {player.stats && Object.entries(player.stats).slice(0, 4).map(([key, value]) => (
                          <div key={key} className="bg-gray-800 rounded p-2">
                            <span className="text-gray-400 block">{key.replace(/_/g, ' ')}</span>
                            <span className="text-white font-medium">{value}</span>
                          </div>
                        ))}
                      </div>
                      
                      <button
                        onClick={(e) => {
                          e.preventDefault(); // Prevent default behavior
                          e.stopPropagation(); // Stop event propagation
                          // Call viewCompleteProfile directly to open the complete player page
                          viewCompleteProfile(player);
                        }}
                        type="button"
                        className="w-full mt-3 py-2 bg-green-700 hover:bg-green-600 text-white rounded text-sm transition-colors flex items-center justify-center"
                      >
                        <User className="mr-1" size={14} />
                        <span>{t('playerDashboard.viewCompleteProfile')}</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
            </div>
          </ErrorBoundary>
        </div>
      </div>
    </div>
  );
};

export default FavoritesView;