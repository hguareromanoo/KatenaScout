import React from 'react';
import { Globe } from 'lucide-react';
import { useTranslation } from '../utils/useTranslation';
import { AVAILABLE_LANGUAGES } from '../locales';
import { appService } from '../api/api';

/**
 * SettingsView component - Handles application settings
 */
const SettingsView = () => {
  const { t, currentLanguage, setLanguage } = useTranslation();
  
  return (
    <div className="max-w-4xl mx-auto p-6 pt-20 md:pt-6">
      <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-900 to-blue-900 p-6">
          <h1 className="text-2xl font-bold text-white flex items-center">
            <Globe className="mr-3" />
            {t('settings.title')}
          </h1>
        </div>
        
        {/* Settings Content */}
        <div className="p-6 space-y-8">
          {/* Language Settings */}
          <div>
            <h2 className="text-xl font-semibold text-white mb-4">{t('settings.language')}</h2>
            <p className="text-gray-400 mb-4">{t('settings.languageLabel')}</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {AVAILABLE_LANGUAGES.map(lang => (
                <button
                  key={lang.id}
                  onClick={() => setLanguage(lang.id)}
                  className={`flex items-center p-4 rounded-lg transition-colors ${
                    currentLanguage === lang.id
                      ? 'bg-green-700 bg-opacity-30 border border-green-600 text-white'
                      : 'bg-gray-700 border border-gray-600 text-gray-300 hover:bg-gray-650'
                  }`}
                >
                  <div className="mr-3 text-2xl">{lang.flag}</div>
                  <div className="flex flex-col items-start">
                    <span className="font-medium">{lang.native_name}</span>
                    <span className="text-xs text-gray-400">{lang.name}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
          
          {/* Version Information */}
          <div className="pt-4 border-t border-gray-700">
            <p className="text-gray-500 text-sm">
              {t('settings.version')}: {appService.getVersion()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsView;