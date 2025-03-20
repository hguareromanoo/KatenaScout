import React, { useState } from 'react';
import { Heart, Search, Trash2, User } from 'lucide-react';
import { useTranslation, useFavorites, useSession } from '../contexts';
import { filterItems, formatMetricName } from '../utils';
import { playerService } from '../api/api';
import ErrorBoundary from './ErrorBoundary';

/**
 * FavoritesView component - Displays and manages favorite players
 */
const FavoritesView = () => {
  const { t } = useTranslation();
  const { favorites, toggleFavorite } = useFavorites();
  const { handlePlayerSelected, viewCompleteProfile } = useSession();
  const [searchTerm, setSearchTerm] = useState('');
  
  // Filter favorites based on search term using utility function
  const filteredFavorites = filterItems(favorites, searchTerm, ['name', 'positions']);
  
  return (
    <div className="max-w-5xl mx-auto p-6 pt-20 md:pt-6">
      <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-900 to-blue-900 p-6">
          <h1 className="text-2xl font-bold text-white flex items-center">
            <Heart className="mr-3" />
            {t('favorites.title')}
          </h1>
        </div>
        
        {/* Search Bar */}
        <div className="p-4 border-b border-gray-700">
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
        
        {/* Favorites List */}
        <ErrorBoundary>
          <div className="p-4">
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
                            e.stopPropagation();
                            if (window.confirm(t('favorites.removeConfirm'))) {
                              toggleFavorite(player);
                            }
                          }}
                          className="text-red-400 hover:text-red-300 p-2 rounded-full hover:bg-gray-650"
                          title={t('favorites.removeFromFavorites')}
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
                        onClick={() => {
                          // Call viewCompleteProfile directly to open the complete player page
                          viewCompleteProfile(player);
                        }}
                        className="w-full mt-3 py-2 bg-green-700 hover:bg-green-600 text-white rounded text-sm transition-colors"
                      >
                        {t('playerDashboard.viewCompleteProfile')}
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
  );
};

export default FavoritesView;