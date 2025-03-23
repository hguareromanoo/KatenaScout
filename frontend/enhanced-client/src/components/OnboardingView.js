import React from 'react';
import { ChevronRight } from 'lucide-react';
import { useTranslation } from '../utils/useTranslation';
import { useUI } from '../contexts';
import { AVAILABLE_LANGUAGES } from '../locales';

/**
 * OnboardingView component - Handles the welcome/language selection screen
 */
const OnboardingView = () => {
  const { t, currentLanguage, setLanguage } = useTranslation();
  const { setOnboardingComplete } = useUI();
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex flex-col items-center justify-center p-4">
      <div className="max-w-md w-full bg-gray-800 rounded-xl shadow-2xl overflow-hidden">
        {/* Header with logo */}
        <div className="bg-gradient-to-r from-green-900 to-blue-900 p-6 text-center">
          <div className="w-20 h-20 mx-auto mb-4 flex items-center justify-center bg-white rounded-full shadow-lg">
            <img src="/logo.svg" alt="Katena Logo" className="w-full h-full" />
          </div>
          <h1 className="text-2xl font-bold text-white">{t('onboarding.welcome')}</h1>
          <p className="text-green-200 mt-2">{t('onboarding.description')}</p>
        </div>
        
        {/* Language selection */}
        <div className="p-6">
          <h2 className="text-white text-lg mb-4 font-medium">{t('onboarding.selectLanguage')}</h2>
          
          <div className="space-y-3">
            {AVAILABLE_LANGUAGES.map(lang => (
              <button
                key={lang.id}
                onClick={() => setLanguage(lang.id)}
                className={`w-full flex items-center p-3 rounded-lg transition-colors ${
                  currentLanguage === lang.id
                    ? 'bg-green-800 bg-opacity-30 border border-green-600 text-white'
                    : 'bg-gray-750 border border-gray-700 text-gray-300 hover:bg-gray-700'
                }`}
              >
                <div className="mr-3 text-xl">{lang.flag}</div>
                <div className="flex flex-col items-start">
                  <span className="font-medium">{lang.native_name}</span>
                  <span className="text-xs text-gray-400">{lang.name}</span>
                </div>
                {currentLanguage === lang.id && (
                  <div className="ml-auto bg-green-500 text-white p-1 rounded-full">
                    <ChevronRight size={16} />
                  </div>
                )}
              </button>
            ))}
          </div>
          
          {/* Continue button */}
          <button 
            onClick={setOnboardingComplete}
            className="w-full mt-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-lg font-medium shadow-lg transition-colors"
          >
            {t('onboarding.continueButton')}
          </button>
          
          {/* Powered by */}
          <div className="mt-6 text-center text-gray-500 text-sm">
            {t('onboarding.poweredBy')}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OnboardingView;