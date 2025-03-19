/**
 * UI context for managing global UI state
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { getFromStorage, setToStorage } from '../utils/storage';

// Create the context
const UIContext = createContext();

/**
 * Provider component for UI context
 */
export const UIProvider = ({ children }) => {
  // Navigation state
  const [currentView, setCurrentView] = useState(() => {
    return getFromStorage('currentView', 'chat');
  });
  
  // Sidebar state (mobile)
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  // Onboarding state
  const [onboardingComplete, setOnboardingComplete] = useState(() => {
    return getFromStorage('onboardingComplete', false) === 'true';
  });
  
  // Loading states
  const [isLoading, setIsLoading] = useState(false);
  
  // Save persistent state to localStorage
  useEffect(() => {
    setToStorage('currentView', currentView);
  }, [currentView]);
  
  useEffect(() => {
    setToStorage('onboardingComplete', onboardingComplete.toString());
  }, [onboardingComplete]);
  
  // Toggle sidebar (for mobile)
  const toggleSidebar = () => {
    setSidebarOpen(prev => !prev);
  };
  
  // Navigation helpers
  const navigateTo = (view) => {
    setCurrentView(view);
    setSidebarOpen(false); // Close sidebar on navigation
  };
  
  // Complete onboarding
  const completeOnboarding = () => {
    setOnboardingComplete(true);
  };
  
  // Value provided by the context
  const value = {
    currentView,
    setCurrentView: navigateTo,
    sidebarOpen,
    setSidebarOpen,
    toggleSidebar,
    onboardingComplete,
    setOnboardingComplete: completeOnboarding,
    isLoading,
    setIsLoading
  };
  
  return (
    <UIContext.Provider value={value}>
      {children}
    </UIContext.Provider>
  );
};

/**
 * Custom hook to use the UI context
 */
export const useUI = () => {
  const context = useContext(UIContext);
  if (!context) {
    throw new Error('useUI must be used within a UIProvider');
  }
  return context;
};

export default UIContext;