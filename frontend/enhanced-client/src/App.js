import React, { useEffect } from 'react';
import { Menu, X, Globe } from 'lucide-react';
import { useTranslation, useFavorites, useSession, useUI, useComparison } from './contexts';
import { appService } from './api/api';

// Import components
import OnboardingView from './components/OnboardingView';
import ChatInterface from './components/ChatInterface';
import PlayerDashboard from './components/PlayerDashboard';
import PlayerCompletePage from './components/PlayerCompletePage';
import PlayerComparisonModal from './components/PlayerComparisonModal';
import FavoritesView from './components/FavoritesView';
import SettingsView from './components/SettingsView';
import ErrorBoundary from './components/ErrorBoundary';

/**
 * Main App Component
 */
function App() {
  const { t, currentLanguage } = useTranslation();
  const { } = useFavorites(); // We need the context but don't use favorites directly
  const { currentView, setCurrentView, sidebarOpen, setSidebarOpen, toggleSidebar, onboardingComplete } = useUI();
  const { 
    selectedPlayer, playerMetrics, handlePlayerSelected, closePlayerView,
    completeProfilePlayer, showingCompleteProfile, viewCompleteProfile, closeCompleteProfile
  } = useSession();
  const { showComparisonModal } = useComparison();
  
  // Check API health on app load
  useEffect(() => {
    const checkAPIHealth = async () => {
      try {
        const health = await appService.checkHealth();
        if (health.status === 'online') {
          console.log('API is online:', health.version);
        } else {
          console.error('API is offline:', health.message);
        }
      } catch (error) {
        console.error('Failed to check API health:', error);
      }
    };
    
    checkAPIHealth();
  }, []);
  
  // Return onboarding view if onboarding is not complete
  if (!onboardingComplete) {
    return <OnboardingView />;
  }

  // Main app layout
  return (
    <div className="flex flex-col md:flex-row h-screen bg-gray-900">
      {/* Mobile backdrop - only visible on mobile when sidebar is open */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden" 
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}
      
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-80 bg-gray-800 shadow-lg transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 md:relative md:w-64 md:translate-x-0`}>
        <div className="flex flex-col h-full">
          {/* Sidebar Header with Close Button for Mobile */}
          <div className="p-4 border-b border-gray-700 flex justify-between items-center">
            <h2 className="text-xl font-bold text-white flex items-center">
              <span className="mr-2 text-green-500">⚽</span> {t('common.appName')}
            </h2>
            {/* Close button - only visible on mobile */}
            <button 
              onClick={() => setSidebarOpen(false)}
              className="md:hidden text-gray-400 hover:text-white p-1 rounded-full focus:outline-none focus:ring-2 focus:ring-gray-500"
              aria-label="Close menu"
            >
              <X size={24} />
            </button>
          </div>
          
          {/* Sidebar Menu */}
          <nav className="flex-1 p-4 space-y-3">
            <button 
              onClick={() => {
                setSidebarOpen(false);
                setCurrentView('chat');
              }}
              className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${currentView === 'chat' ? 'bg-green-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
            >
              <span className="text-base">{t('navigation.chat')}</span>
            </button>
            
            <button 
              onClick={() => {
                setSidebarOpen(false);
                setCurrentView('favorites');
              }}
              className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${currentView === 'favorites' ? 'bg-green-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
            >
              <span className="text-base">{t('navigation.favorites')}</span>
            </button>
            
            <button 
              onClick={() => {
                setSidebarOpen(false);
                setCurrentView('settings');
              }}
              className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${currentView === 'settings' ? 'bg-green-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
            >
              <span className="text-base">{t('navigation.settings')}</span>
            </button>
          </nav>
          
          {/* Current Language */}
          <div className="p-4 border-t border-gray-700">
            <div className="flex items-center text-gray-400 text-sm">
              <Globe className="mr-2" size={14} />
              <span>
                {currentLanguage === 'english' && 'English'}
                {currentLanguage === 'portuguese' && 'Português'}
                {currentLanguage === 'spanish' && 'Español'}
                {currentLanguage === 'bulgarian' && 'Български'}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Remove the floating menu button - we'll add it to the header instead */}
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Mobile Header with Menu Button - only visible on mobile */}
        <div className="md:hidden fixed top-0 left-0 right-0 z-30 bg-gray-800 border-b border-gray-700 p-3 px-4 flex items-center">
          <button 
            onClick={toggleSidebar}
            className="text-gray-300 hover:text-white p-1 rounded-full focus:outline-none focus:ring-2 focus:ring-gray-500 flex items-center"
          >
            <Menu size={24} />
            <span className="ml-2 font-semibold">{t('common.appName')}</span>
          </button>
        </div>

        {/* Chat View */}
        {currentView === 'chat' && (
          <ErrorBoundary>
            <ChatInterface 
              onPlayerSelected={handlePlayerSelected} 
              expanded={!selectedPlayer}
              setSidebarOpen={setSidebarOpen}
            />
            
            {/* Player Modal - Only visible when a player is selected */}
            {selectedPlayer && (
              <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-40 p-4">
                <div className="bg-gray-800 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-auto relative shadow-2xl">
                  <ErrorBoundary>
                    <PlayerDashboard 
                      player={selectedPlayer} 
                      metrics={playerMetrics || []}
                      onClose={closePlayerView}
                      onViewComplete={viewCompleteProfile}
                    />
                  </ErrorBoundary>
                </div>
              </div>
            )}
            
            {/* Complete Player Profile View - Shown when a user clicks "See complete profile" */}
            {showingCompleteProfile && completeProfilePlayer && (
              <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
                <div className="bg-gray-800 rounded-xl w-full max-w-5xl max-h-[95vh] overflow-hidden relative">
                  <ErrorBoundary>
                    <PlayerCompletePage 
                      player={completeProfilePlayer}
                      onClose={closeCompleteProfile}
                    />
                  </ErrorBoundary>
                </div>
              </div>
            )}
            
            {/* Player Comparison Modal - Shown when comparing players */}
            {showComparisonModal && (
              <ErrorBoundary>
                <PlayerComparisonModal />
              </ErrorBoundary>
            )}
          </ErrorBoundary>
        )}
        
        {/* Favorites View */}
        {currentView === 'favorites' && (
          <ErrorBoundary>
            <FavoritesView onSelectPlayer={handlePlayerSelected} />
          </ErrorBoundary>
        )}
        
        {/* Settings View */}
        {currentView === 'settings' && (
          <ErrorBoundary>
            <SettingsView />
          </ErrorBoundary>
        )}
      </div>
    </div>
  );
}

export default App;