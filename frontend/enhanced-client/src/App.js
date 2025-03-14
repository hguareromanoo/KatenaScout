import React, { useState, useEffect, Component } from 'react';
import { 
  Send, X, UserCircle, Trophy, TrendingUp, BarChart3, Clock, Package, Calendar,
  Settings, Heart, ChevronRight, Globe, Star, Eye, Search, Trash2, ArrowLeft,
  Menu, User, Footprints as Boot, AlertTriangle
} from 'lucide-react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, Tooltip, Legend 
} from 'recharts';

// Error Boundary Component to catch rendering errors
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to the console
    console.error("Error caught by ErrorBoundary:", error, errorInfo);
    this.setState({ errorInfo });
    
    // You could also log this to an error reporting service
    // logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Render fallback UI
      return (
        <div className="bg-red-900 bg-opacity-20 p-6 rounded-lg border border-red-700 m-4">
          <div className="flex items-center mb-4">
            <AlertTriangle className="text-red-500 mr-2" size={24} />
            <h2 className="text-lg font-bold text-red-300">Oops! Algo deu errado</h2>
          </div>
          <p className="text-red-200 mb-4">
            Ocorreu um erro ao renderizar este componente. Detalhes adicionais foram registrados no console.
          </p>
          {this.props.fallback || (
            <button 
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-white"
              onClick={() => window.location.reload()}
            >
              Recarregar Página
            </button>
          )}
          {process.env.NODE_ENV === 'development' && (
            <details className="mt-4 p-2 bg-black bg-opacity-30 rounded">
              <summary className="text-red-300 cursor-pointer">Detalhes Técnicos</summary>
              <pre className="mt-2 p-2 text-xs text-red-300 overflow-auto max-h-60 whitespace-pre-wrap bg-black bg-opacity-50 rounded">
                {this.state.error && this.state.error.toString()}
                {this.state.errorInfo && this.state.errorInfo.componentStack}
              </pre>
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

// Main App Component
function App() {
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [currentView, setCurrentView] = useState('chat');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [onboardingComplete, setOnboardingComplete] = useState(() => {
    return localStorage.getItem('onboardingComplete') === 'true';
  });
  const [showingCompleteProfile, setShowingCompleteProfile] = useState(false);
  const [completeProfilePlayer, setCompleteProfilePlayer] = useState(null);
  const [favorites, setFavorites] = useState(() => {
    // Initialize favorites from localStorage if available
    const savedFavorites = localStorage.getItem('favorites');
    return savedFavorites ? JSON.parse(savedFavorites) : [];
  });
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    return localStorage.getItem('language') || 'english';
  });

  // Save favorites to localStorage when they change
  useEffect(() => {
    localStorage.setItem('favorites', JSON.stringify(favorites));
  }, [favorites]);
  
  // Save language preference to localStorage
  useEffect(() => {
    localStorage.setItem('language', currentLanguage);
  }, [currentLanguage]);
  
  // Save onboarding status to localStorage
  useEffect(() => {
    localStorage.setItem('onboardingComplete', onboardingComplete);
  }, [onboardingComplete]);

  // Function to handle when a player is selected from the chat
  const handlePlayerSelected = (player, metrics) => {
    setSelectedPlayer(player);
    setMetrics(metrics);
  };
  
  // Function to check if a player is in favorites
  const isPlayerFavorite = (player) => {
    return favorites.some(f => f.id === player.id || f.name === player.name);
  };
  
  // Function to toggle favorite status
  const toggleFavorite = (player) => {
    if (isPlayerFavorite(player)) {
      setFavorites(favorites.filter(f => f.id !== player.id && f.name !== player.name));
    } else {
      setFavorites([...favorites, player]);
    }
  };

  // Create an OnboardingView component to handle the welcome/language selection screen
  const OnboardingView = ({ onComplete, setLanguage, currentLanguage }) => {
    // Translations for the onboarding screen
    const translations = {
      english: {
        welcome: "Welcome to KatenaScout",
        description: "Your AI-powered football scouting assistant",
        selectLanguage: "Please select your preferred language",
        continueButton: "Continue",
        poweredBy: "Powered by Claude AI"
      },
      portuguese: {
        welcome: "Bem-vindo ao KatenaScout",
        description: "Seu assistente de scouting de futebol com IA",
        selectLanguage: "Por favor, selecione seu idioma preferido",
        continueButton: "Continuar",
        poweredBy: "Desenvolvido com Claude AI"
      },
      spanish: {
        welcome: "Bienvenido a KatenaScout",
        description: "Tu asistente de scouting de fútbol con IA",
        selectLanguage: "Por favor, selecciona tu idioma preferido",
        continueButton: "Continuar",
        poweredBy: "Desarrollado con Claude AI"
      },
      bulgarian: {
        welcome: "Добре дошли в KatenaScout",
        description: "Вашият асистент за футболно наблюдение с ИИ",
        selectLanguage: "Моля, изберете предпочитания от вас език",
        continueButton: "Продължи",
        poweredBy: "Създадено с Claude AI"
      }
    };
    
    // Available languages
    const languages = [
      { id: 'english', name: 'English', native_name: 'English', code: 'en', flag: '🇬🇧' },
      { id: 'portuguese', name: 'Portuguese', native_name: 'Português', code: 'pt', flag: '🇧🇷' },
      { id: 'spanish', name: 'Spanish', native_name: 'Español', code: 'es', flag: '🇪🇸' },
      { id: 'bulgarian', name: 'Bulgarian', native_name: 'Български', code: 'bg', flag: '🇧🇬' }
    ];
    
    // Get translations based on current language
    const t = translations[currentLanguage] || translations.english;
    
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex flex-col items-center justify-center p-4">
        <div className="max-w-md w-full bg-gray-800 rounded-xl shadow-2xl overflow-hidden">
          {/* Header with logo */}
          <div className="bg-gradient-to-r from-green-900 to-blue-900 p-6 text-center">
            <div className="w-20 h-20 mx-auto mb-4 flex items-center justify-center bg-white rounded-full shadow-lg">
              <span className="text-green-700 text-4xl">⚽</span>
            </div>
            <h1 className="text-2xl font-bold text-white">{t.welcome}</h1>
            <p className="text-green-200 mt-2">{t.description}</p>
          </div>
          
          {/* Language selection */}
          <div className="p-6">
            <h2 className="text-white text-lg mb-4 font-medium">{t.selectLanguage}</h2>
            
            <div className="space-y-3">
              {languages.map(lang => (
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
              onClick={onComplete}
              className="w-full mt-6 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-lg font-medium shadow-lg transition-colors"
            >
              {t.continueButton}
            </button>
            
            {/* Powered by */}
            <div className="mt-6 text-center text-gray-500 text-sm">
              {t.poweredBy}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return onboardingComplete ? (
    <div className="flex flex-col md:flex-row h-screen bg-gray-900">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-gray-800 shadow-lg transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 md:relative md:translate-x-0`}>
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-4 border-b border-gray-700">
            <h2 className="text-xl font-bold text-white flex items-center">
              <span className="mr-2 text-green-500">⚽</span> KatenaScout
            </h2>
          </div>
          
          {/* Sidebar Menu */}
          <nav className="flex-1 p-4 space-y-2">
            <button 
              onClick={() => {setCurrentView('chat'); setSidebarOpen(false);}}
              className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${currentView === 'chat' ? 'bg-green-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
            >
              <Send className="mr-3" size={18} />
              <span>
                {currentLanguage === 'english' && 'AI Scout Chat'}
                {currentLanguage === 'portuguese' && 'Chat de Scout IA'}
                {currentLanguage === 'spanish' && 'Chat de Scout IA'}
                {currentLanguage === 'bulgarian' && 'Чат с ИИ Скаут'}
              </span>
            </button>
            
            <button 
              onClick={() => {setCurrentView('favorites'); setSidebarOpen(false);}}
              className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${currentView === 'favorites' ? 'bg-green-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
            >
              <Heart className="mr-3" size={18} />
              <span>
                {currentLanguage === 'english' && 'Favorites'}
                {currentLanguage === 'portuguese' && 'Favoritos'}
                {currentLanguage === 'spanish' && 'Favoritos'}
                {currentLanguage === 'bulgarian' && 'Любими'}
              </span>
            </button>
            
            <button 
              onClick={() => {setCurrentView('settings'); setSidebarOpen(false);}}
              className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${currentView === 'settings' ? 'bg-green-700 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
            >
              <Settings className="mr-3" size={18} />
              <span>
                {currentLanguage === 'english' && 'Settings'}
                {currentLanguage === 'portuguese' && 'Configurações'}
                {currentLanguage === 'spanish' && 'Configuración'}
                {currentLanguage === 'bulgarian' && 'Настройки'}
              </span>
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
      
      {/* Toggle Sidebar Button (Mobile) */}
      <button 
        className="fixed bottom-4 left-4 z-50 md:hidden bg-green-600 text-white p-3 rounded-full shadow-lg"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
      </button>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Chat View */}
        {currentView === 'chat' && (
          <>
            <ChatInterface 
              onPlayerSelected={handlePlayerSelected} 
              expanded={!selectedPlayer}
              isPlayerFavorite={isPlayerFavorite}
              toggleFavorite={toggleFavorite}
              currentLanguage={currentLanguage}
              setSidebarOpen={setSidebarOpen}
            />
            
            {/* Player Modal - Only visible when a player is selected */}
            {selectedPlayer && (
              <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-40 p-4">
                <div className="bg-gray-800 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-auto relative shadow-2xl">
                  <ErrorBoundary 
                    fallback={(
                      <div className="p-6">
                        <h3 className="text-xl text-red-400 mb-4">Erro ao exibir dados do jogador</h3>
                        <p className="text-gray-300 mb-4">Não foi possível renderizar os detalhes do jogador. Por favor, tente novamente mais tarde.</p>
                        <button 
                          onClick={() => setSelectedPlayer(null)} 
                          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-white"
                        >
                          Fechar
                        </button>
                      </div>
                    )}
                  >
                    <PlayerDashboard 
                      player={selectedPlayer} 
                      metrics={metrics || []}
                      onClose={() => {
                        console.log("[DEBUG] Closing player dashboard");
                        setSelectedPlayer(null);
                      }}
                      isPlayerFavorite={isPlayerFavorite(selectedPlayer)}
                      toggleFavorite={() => toggleFavorite(selectedPlayer)}
                      currentLanguage={currentLanguage}
                      onViewComplete={(player) => {
                        console.log("[DEBUG] View complete called with player:", player);
                        setSelectedPlayer(null);
                        setCompleteProfilePlayer(player);
                        setShowingCompleteProfile(true);
                      }}
                    />
                  </ErrorBoundary>
                </div>
              </div>
            )}
            
            {/* Complete Player Profile View - Shown when a user clicks "See complete profile" */}
            {showingCompleteProfile && completeProfilePlayer && (
              <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
                <div className="bg-gray-800 rounded-xl w-full max-w-5xl max-h-[95vh] overflow-hidden relative">
                  <PlayerCompletePage 
                    player={completeProfilePlayer}
                    onClose={() => {
                      setShowingCompleteProfile(false);
                      setCompleteProfilePlayer(null);
                    }}
                    isPlayerFavorite={isPlayerFavorite(completeProfilePlayer)}
                    toggleFavorite={() => toggleFavorite(completeProfilePlayer)}
                    currentLanguage={currentLanguage}
                  />
                </div>
              </div>
            )}
          </>
        )}
        
        {/* Favorites View */}
        {currentView === 'favorites' && (
          <FavoritesView 
            favorites={favorites} 
            onSelectPlayer={handlePlayerSelected}
            onRemoveFavorite={toggleFavorite}
            currentLanguage={currentLanguage}
          />
        )}
        
        {/* Settings View */}
        {currentView === 'settings' && (
          <SettingsView 
            currentLanguage={currentLanguage}
            setCurrentLanguage={setCurrentLanguage}
          />
        )}
      </div>
    </div>
  ) : (
    <OnboardingView 
      onComplete={() => setOnboardingComplete(true)}
      setLanguage={setCurrentLanguage}
      currentLanguage={currentLanguage}
    />
  );
}

// Chat Interface Component
const ChatInterface = ({ onPlayerSelected, expanded, isPlayerFavorite, toggleFavorite, currentLanguage = 'english', setSidebarOpen }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [lastMessageWasSatisfactionQuestion, setLastMessageWasSatisfactionQuestion] = useState(false);
  
  // Translations for UI elements
  const translations = {
    english: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Your intelligent scouting assistant",
      inputPlaceholder: "Describe the type of player you're looking for...",
      welcomeTitle: "Hello, Coach!",
      welcomeMessage: "Describe the type of player you're looking for, and I'll find the best options for your team.",
      examplesTitle: "Search examples:",
      example1: "I need an offensive full-back with good crossing ability",
      example2: "Looking for center backs strong in aerial duels with good ball distribution",
      example3: "I want a young striker with good finishing and under 23 years old",
      playersFoundText: "Players found - Select to see details:",
      analyzing: "Analyzing players...",
      showingDetails: "Showing details of ",
      errorMessage: "Sorry, an error occurred while processing your search."
    },
    portuguese: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Seu assistente de scouting inteligente",
      inputPlaceholder: "Descreva o tipo de jogador que você procura...",
      welcomeTitle: "Olá, Técnico!",
      welcomeMessage: "Descreva o tipo de jogador que você está buscando, e eu encontrarei as melhores opções para sua equipe.",
      examplesTitle: "Exemplos de busca:",
      example1: "Preciso de um lateral ofensivo com boa capacidade de cruzamento",
      example2: "Busco zagueiros fortes no jogo aéreo e com boa saída de bola",
      example3: "Quero um atacante jovem com boa finalização e menos de 23 anos",
      playersFoundText: "Jogadores encontrados - Selecione para ver detalhes:",
      analyzing: "Analisando jogadores...",
      showingDetails: "Mostrando detalhes de ",
      errorMessage: "Desculpe, ocorreu um erro ao processar sua busca."
    },
    spanish: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Tu asistente de scouting inteligente",
      inputPlaceholder: "Describe el tipo de jugador que estás buscando...",
      welcomeTitle: "¡Hola, Entrenador!",
      welcomeMessage: "Describe el tipo de jugador que estás buscando, y encontraré las mejores opciones para tu equipo.",
      examplesTitle: "Ejemplos de búsqueda:",
      example1: "Necesito un lateral ofensivo con buena capacidad de centro",
      example2: "Busco defensores centrales fuertes en duelos aéreos y con buena salida de balón",
      example3: "Quiero un delantero joven con buena definición y menos de 23 años",
      playersFoundText: "Jugadores encontrados - Selecciona para ver detalles:",
      analyzing: "Analizando jugadores...",
      showingDetails: "Mostrando detalles de ",
      errorMessage: "Lo siento, ocurrió un error al procesar tu búsqueda."
    },
    bulgarian: {
      headerTitle: "KatenaScout AI",
      headerSubtitle: "Вашият интелигентен скаутинг асистент",
      inputPlaceholder: "Опишете типа играч, който търсите...",
      welcomeTitle: "Здравейте, Треньор!",
      welcomeMessage: "Опишете типа играч, който търсите, и ще намеря най-добрите опции за вашия отбор.",
      examplesTitle: "Примери за търсене:",
      example1: "Нужен ми е офанзивен бек с добра способност за центриране",
      example2: "Търся централни защитници, силни във въздушните дуели и с добро разпределяне на топката",
      example3: "Искам млад нападател с добро завършване и под 23 години",
      playersFoundText: "Намерени играчи - Изберете, за да видите детайли:",
      analyzing: "Анализиране на играчи...",
      showingDetails: "Показване на детайли за ",
      errorMessage: "Съжаляваме, възникна грешка при обработката на вашето търсене."
    }
  };
  
  // Get translations for the current language
  const t = translations[currentLanguage] || translations.english;

  // State to keep track of the session
  const [sessionId] = useState(() => {
    const savedSessionId = localStorage.getItem('chatSessionId');
    return savedSessionId || `session-${Date.now()}`;
  });

  // Store session ID in localStorage when it changes
  React.useEffect(() => {
    localStorage.setItem('chatSessionId', sessionId);
  }, [sessionId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    try {
      setIsLoading(true);
      
      // Check if we're responding to a satisfaction question
      const isSatisfactionResponse = lastMessageWasSatisfactionQuestion && 
        (input.toLowerCase().includes('não') || 
         input.toLowerCase().includes('refinar') || 
         input.toLowerCase().includes('outros') ||
         input.toLowerCase().includes('no') || 
         input.toLowerCase().includes('more') ||
         input.toLowerCase().includes('other') ||
         input.toLowerCase().includes('different'));
         
      // Add user's message to chat
      setMessages(prev => [...prev, { text: input, sender: 'user' }]);

      // Prepare the request body based on whether it's a satisfaction response
      const requestBody = {
        session_id: sessionId,
        query: input,
        is_follow_up: messages.length > 0,
        satisfaction: isSatisfactionResponse ? false : null,
        language: currentLanguage
      };

      const response = await fetch('https://katenascout-backend.onrender.com/enhanced_search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      
      if (data.success) {
        // Use the players data directly from the response if available
        let playersData = data.players || [];

        // Check if the response contains a satisfaction question
        const hasSatisfactionQuestion = 
          data.response.toLowerCase().includes('satisfeito') || 
          data.response.toLowerCase().includes('satisfied') ||
          data.response.toLowerCase().includes('refinar sua busca') ||
          data.response.toLowerCase().includes('refine your search');
        
        setLastMessageWasSatisfactionQuestion(hasSatisfactionQuestion);

        // Add the response to the chat
        setMessages(prev => [...prev, {
          text: data.response,
          sender: 'bot',
          showPlayerSelection: playersData.length > 0,
          players: playersData
        }]);
      } else {
        setMessages(prev => [...prev, { 
          text: data.error || 'Ocorreu um erro ao processar sua busca.',
          sender: 'bot' 
        }]);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        text: 'Desculpe, ocorreu um erro ao processar sua busca.',
        sender: 'bot'
      }]);
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };

  const handlePlayerSelect = (player) => {
    try {
      // Extensive DEBUG logging to track the error
      console.log("[DEBUG] handlePlayerSelect called with player:", player);
      
      // Safety check for player object
      if (!player) {
        console.error("[ERROR] Player is undefined or null");
        setMessages(prev => [...prev, {
          text: "Erro: dados do jogador não encontrados. Por favor, tente novamente.",
          sender: 'bot'
        }]);
        return;
      }
      
      // Check for required fields and log warnings
      if (!player.name) console.warn("[WARNING] Player name is missing");
      if (!player.stats) console.warn("[WARNING] Player stats are missing");
      if (!player.positions) console.warn("[WARNING] Player positions are missing");
      
      // Extract metrics from the player object with validation
      console.log("[DEBUG] Extracting metrics from player.stats:", player.stats);
      
      const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => {
        // Validate each metric value
        if (value === undefined || value === null) {
          console.warn(`[WARNING] Metric ${key} has null/undefined value`);
        }
        
        return {
          name: formatMetricName(key),
          value: value !== undefined && value !== null ? value : 0, // Provide fallback
          key: key,
          originalValue: value // Keep original for debugging
        };
      });
      
      console.log("[DEBUG] Extracted metrics:", playerMetrics);
  
      setMessages(prev => [...prev, {
        text: `Mostrando detalhes de ${player.name || 'jogador'}...`,
        sender: 'bot'
      }]);
      
      // Call the parent component's callback to show the player dashboard
      console.log("[DEBUG] Calling onPlayerSelected with player and metrics");
      onPlayerSelected(player, playerMetrics);
    } catch (error) {
      console.error("[CRITICAL] Error in handlePlayerSelect:", error);
      console.error("[CRITICAL] Error stack:", error.stack);
      // Add a nice error message to the chat
      setMessages(prev => [...prev, {
        text: "Ocorreu um erro ao carregar o perfil do jogador. Por favor, tente novamente.",
        sender: 'bot'
      }]);
    }
  };

  // Helper function to format metric names for display
  const formatMetricName = (key) => {
    return key
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };
  
  // Helper function to format player names with proper spacing
  const formatPlayerName = (name) => {
    if (!name) return '';
    // Add spaces between capital letters if they're not already spaced
    return name.replace(/([A-Z])/g, ' $1').trim()
      // Replace multiple spaces with a single space
      .replace(/\s+/g, ' ')
      // Make sure first letter of each word is capitalized
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="flex flex-col w-full h-full md:h-auto transition-all duration-300 bg-gray-900 border-r border-gray-700 chat-container overflow-hidden">
      {/* Header with soccer theme */}
      <div className="bg-gradient-to-r from-green-900 to-blue-900 p-4 flex items-center border-b border-gray-700 relative overflow-hidden">
        {/* Soccer field pattern in the background */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[30%] h-[120%] border-2 border-white rounded-full"></div>
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-0.5 h-full bg-white"></div>
        </div>
        
        <div className="w-10 h-10 mr-3 flex items-center justify-center bg-white rounded-full shadow-lg">
          <span className="text-green-700 text-2xl">⚽</span>
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">{t.headerTitle}</h1>
          <p className="text-xs text-green-200 opacity-80">{t.headerSubtitle}</p>
        </div>
        <div className="ml-auto">
          <button 
            onClick={() => setSidebarOpen && setSidebarOpen(true)}
            className="text-white md:hidden p-2 rounded-full hover:bg-green-700"
          >
            <Menu size={20} />
          </button>
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
        
        {messages.length === 0 && (
          <div className="text-center py-10 relative z-10">
            <div className="w-20 h-20 mx-auto mb-4 flex items-center justify-center bg-gradient-to-r from-green-600 to-green-700 rounded-full shadow-lg">
              <span className="text-white text-4xl">⚽</span>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">{t.welcomeTitle}</h2>
            <p className="text-gray-300 mb-6 max-w-md mx-auto">{t.welcomeMessage}</p>
            
            <div className="bg-gray-800 rounded-lg p-5 mx-auto max-w-md text-left border-l-4 border-green-500">
              <p className="text-white mb-3 font-medium">{t.examplesTitle}</p>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">1</span>
                  <span>"{t.example1}"</span>
                </li>
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">2</span>
                  <span>"{t.example2}"</span>
                </li>
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">3</span>
                  <span>"{t.example3}"</span>
                </li>
              </ul>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} 
               className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {/* User Avatar (only shown for bot messages) */}
            {message.sender === 'bot' && (
              <div className="w-8 h-8 rounded-full bg-green-700 flex items-center justify-center text-white mr-2 flex-shrink-0 self-start mt-1">
                ⚽
              </div>
            )}
            
            {/* Message bubble */}
            <div className={`rounded-lg p-4 max-w-[80%] shadow-md ${
              message.sender === 'user' 
                ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-tr-none' 
                : message.isSatisfactionQuestion
                  ? 'bg-gradient-to-r from-green-700 to-green-800 text-white rounded-tl-none'
                  : 'bg-gradient-to-r from-gray-800 to-gray-900 text-gray-100 rounded-tl-none'
            }`}>
              <div className="whitespace-pre-wrap message-content">{message.text}</div>
              
              {/* Player Selection Cards */}
              {message.showPlayerSelection && message.players && message.players.length > 0 && (
                <div className="mt-4 space-y-3">
                  <div className="text-sm text-gray-200 font-medium border-b border-gray-700 pb-2 mb-3">
                    {t.playersFoundText}
                  </div>
                  <div className="grid grid-cols-1 gap-3">
                    {message.players.map((player, idx) => (
                      <div
                        key={idx}
                        onClick={() => handlePlayerSelect(player)}
                        className="text-left p-3 rounded bg-gray-700 bg-opacity-50 hover:bg-gray-600 transition-colors flex flex-wrap sm:flex-nowrap items-center border border-gray-600 hover:border-green-500 cursor-pointer relative">
                        {/* Player image */}
                        <div className="w-10 h-10 bg-blue-900 rounded-full flex items-center justify-center text-white text-xs font-bold mr-3 overflow-hidden">
                          {player.imageDataURL || player.id ? (
                            <img 
                              src={player.imageDataURL || (player.id ? `https://katenascout-backend.onrender.com/player-image/${player.id}` : null)}
                              alt={player.name}
                              className="w-full h-full object-cover"
                              onError={(e) => {
                                e.target.onerror = null;
                                e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=64`;
                              }}
                            />
                          ) : (
                            player.positions?.[0]?.toUpperCase() || 'ST'
                          )}
                        </div>
                        
                        <div className="flex-1">
                          <div className="font-medium text-white">{formatPlayerName(player.name)}</div>
                          <div className="text-xs text-gray-300 flex items-center">
                            <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-1"></span>
                            {player.positions?.join(', ') || 'N/A'} • {player.age || '?'} {
                              currentLanguage === 'english' ? 'years' :
                              currentLanguage === 'portuguese' ? 'anos' :
                              currentLanguage === 'spanish' ? 'años' :
                              'години'
                            } • {
                              typeof player.club === 'object' && player.club !== null
                                ? (player.club.name || String(player.club) || (
                                    currentLanguage === 'english' ? 'Unknown club' :
                                    currentLanguage === 'portuguese' ? 'Clube desconhecido' :
                                    currentLanguage === 'spanish' ? 'Club desconocido' :
                                    'Неизвестен клуб'
                                  ))
                                : (player.club || (
                                    currentLanguage === 'english' ? 'Unknown club' :
                                    currentLanguage === 'portuguese' ? 'Clube desconhecido' :
                                    currentLanguage === 'spanish' ? 'Club desconocido' :
                                    'Неизвестен клуб'
                                  ))
                            }
                          </div>
                        </div>
                        
                        {/* Favorite heart in the top right */}
                        <div className="absolute top-2 right-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation(); // Prevent card click
                              toggleFavorite(player);
                            }}
                            className={`p-1.5 rounded-full ${
                              isPlayerFavorite(player)
                                ? 'bg-red-600 text-white hover:bg-red-700'
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                            }`}
                          >
                            <Heart size={14} fill={isPlayerFavorite(player) ? "white" : "none"} />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            {/* User Avatar (only shown for user messages) */}
            {message.sender === 'user' && (
              <div className="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center text-white ml-2 flex-shrink-0 self-start mt-1">
                👤
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="w-8 h-8 rounded-full bg-green-700 flex items-center justify-center text-white mr-2 flex-shrink-0 self-start mt-1">
              ⚽
            </div>
            <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-gray-100 rounded-lg rounded-tl-none p-4 shadow-md">
              <div className="flex items-center space-x-3">
                {/* Simple rotating soccer ball */}
                <div className="w-8 h-8 flex items-center justify-center animate-spin" 
                     style={{animationDuration: '1.5s'}}>
                  <span className="text-xl">⚽</span>
                </div>
                
                <div className="text-green-300 font-medium">{t.analyzing}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t border-gray-700 p-4 bg-gray-900 sticky bottom-0">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t.inputPlaceholder}
            disabled={isLoading}
            className="flex-1 rounded-lg bg-gray-800 text-white p-3 border border-gray-700 focus:outline-none focus:border-green-500 shadow-inner"
          />
          <button 
            type="submit"
            disabled={isLoading}
            className={`text-white rounded-lg px-4 py-3 focus:outline-none flex items-center justify-center shadow-md ${
              isLoading ? 'bg-gray-600' : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'
            }`}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};

// Player Dashboard Component with improved design, player photo, and radar chart
const PlayerDashboard = ({ player, metrics, onClose, isPlayerFavorite, toggleFavorite, currentLanguage = 'english', onViewComplete }) => {
  // Helper function to get a flag emoji based on country name or object
  const getCountryFlag = (country) => {
    // Safety check for undefined or null
    if (!country) return '🌍';
    
    // Handle country as object or string
    const countryName = typeof country === 'object' && country !== null
      ? (country.name || country.alpha3code || country.alpha2code || '') 
      : String(country);
      
    console.log('[DEBUG] Getting flag for country:', countryName, 'Original:', country);
    
    // Map of common country names to their flag emojis
    const countryFlags = {
      'Brazil': '🇧🇷',
      'Brasil': '🇧🇷',
      'Argentina': '🇦🇷',
      'Portugal': '🇵🇹',
      'Spain': '🇪🇸',
      'España': '🇪🇸',
      'France': '🇫🇷',
      'França': '🇫🇷',
      'Germany': '🇩🇪',
      'Alemanha': '🇩🇪',
      'England': '🇬🇧',
      'Inglaterra': '🇬🇧',
      'Italy': '🇮🇹',
      'Itália': '🇮🇹',
      'Netherlands': '🇳🇱',
      'Holanda': '🇳🇱',
      'Belgium': '🇧🇪',
      'Bélgica': '🇧🇪',
      'Uruguay': '🇺🇾',
      'Colombia': '🇨🇴',
      'Colômbia': '🇨🇴',
      'Ecuador': '🇪🇨',
      'Equador': '🇪🇨',
      'Chile': '🇨🇱',
      'Peru': '🇵🇪',
      'Mexico': '🇲🇽',
      'México': '🇲🇽',
      'United States': '🇺🇸',
      'Estados Unidos': '🇺🇸',
      'USA': '🇺🇸',
      'EUA': '🇺🇸',
      'Japan': '🇯🇵',
      'Japão': '🇯🇵',
      'South Korea': '🇰🇷',
      'Coreia do Sul': '🇰🇷',
      'Morocco': '🇲🇦',
      'Marrocos': '🇲🇦',
      'Senegal': '🇸🇳',
      'Egypt': '🇪🇬',
      'Egito': '🇪🇬',
      'Ghana': '🇬🇭',
      'Gana': '🇬🇭',
      'Nigeria': '🇳🇬',
      'Nigéria': '🇳🇬',
      'Cameroon': '🇨🇲',
      'Camarões': '🇨🇲',
      'Australia': '🇦🇺',
      'Austrália': '🇦🇺',
      'New Zealand': '🇳🇿',
      'Nova Zelândia': '🇳🇿',
      'Croatia': '🇭🇷',
      'Croácia': '🇭🇷',
      'Serbia': '🇷🇸',
      'Sérvia': '🇷🇸',
      'Denmark': '🇩🇰',
      'Dinamarca': '🇩🇰',
      'Sweden': '🇸🇪',
      'Suécia': '🇸🇪',
      'Switzerland': '🇨🇭',
      'Suíça': '🇨🇭',
      'Poland': '🇵🇱',
      'Polônia': '🇵🇱',
      'Ukraine': '🇺🇦',
      'Ucrânia': '🇺🇦',
      'Russia': '🇷🇺',
      'Rússia': '🇷🇺',
      'Turkey': '🇹🇷',
      'Turquia': '🇹🇷',
    };
    
    // If we have a flag for this country, return it, otherwise return a globe
    return countryFlags[countryName] || '🌍';
  };

  // Helper function to get a color based on metric value
  const getMetricColor = (metric) => {
    // Placeholder logic - in a real app this would be based on comparison with league averages
    const value = parseFloat(metric.value);
    if (isNaN(value)) return 'text-gray-400';
    
    // Different metrics have different scales
    if (metric.key.includes('percent')) {
      if (value > 80) return 'text-green-500';
      if (value > 60) return 'text-yellow-500';
      return 'text-red-500';
    }
    
    // Default scale for other metrics
    if (value > 7) return 'text-green-500';
    if (value > 4) return 'text-yellow-500';
    return 'text-red-500';
  };

  // Helper function to format player names with proper spacing
  const formatPlayerName = (name) => {
    if (!name) return '';
    // Add spaces between capital letters if they're not already spaced
    return name.replace(/([A-Z])/g, ' $1').trim()
      // Replace multiple spaces with a single space
      .replace(/\s+/g, ' ')
      // Make sure first letter of each word is capitalized
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // We've removed the duplicated safety check and kept the more detailed one
  // Check if player exists before trying to render
  if (!player) {
    console.error("[ERROR] PlayerDashboard received null or undefined player");
    return (
      <div className="p-6 bg-red-900 bg-opacity-20 rounded-lg border border-red-700 text-white">
        <h2 className="text-xl font-bold mb-4 flex items-center">
          <AlertTriangle className="mr-2" size={20} />
          Erro
        </h2>
        <p className="mb-4">Não foi possível carregar os dados do jogador</p>
        <button
          onClick={onClose}
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded"
        >
          Voltar
        </button>
      </div>
    );
  }
  
  console.log("[DEBUG] Rendering PlayerDashboard with player:", player);
  
  // Get player position in a more readable format
  const positionDisplay = (player.positions || []).map(pos => {
    const posMap = {
      'cb': 'Zagueiro',
      'lb': 'Lateral Esquerdo',
      'rb': 'Lateral Direito',
      'dmf': 'Volante',
      'cmf': 'Meio-Campo',
      'amf': 'Meia Atacante',
      'lw': 'Ponta Esquerda',
      'rw': 'Ponta Direita',
      'cf': 'Centroavante',
      'gk': 'Goleiro',
      // Add other positions as needed
    };
    return posMap[pos] || pos;
  }).join(', ');

  // Prepare ALL metrics for a single comprehensive radar chart
  const prepareAllRadarData = (allMetrics, maxMetrics = 15) => {
    if (!allMetrics || allMetrics.length === 0) return [];
    
    // Filter out metrics with no values or invalid values
    const validMetrics = allMetrics.filter(m => m.value !== undefined && m.value !== null);
    
    // Sort by importance (could implement more sophisticated sorting)
    // For now, prioritize key metrics like goals, assists, passes, etc.
    const keyMetricOrder = [
      'goals', 'assists', 'shots_on_target', 'pass_accuracy', 'key_passes',
      'interceptions', 'defensive_duels_won', 'successful_dribbles',
      'progressive_runs', 'aerial_duels_won'
    ];
    
    // Sort metrics by putting key metrics first, then alphabetically
    const sortedMetrics = [...validMetrics].sort((a, b) => {
      const aIndex = keyMetricOrder.indexOf(a.key);
      const bIndex = keyMetricOrder.indexOf(b.key);
      
      if (aIndex !== -1 && bIndex !== -1) return aIndex - bIndex;
      if (aIndex !== -1) return -1;
      if (bIndex !== -1) return 1;
      
      return a.name.localeCompare(b.name);
    });
    
    // Take top N metrics for the radar chart
    const selectedMetrics = sortedMetrics.slice(0, maxMetrics);
    
    // Normalize the values for the radar chart
    const normalizedMetrics = selectedMetrics.map(metric => {
      const value = parseFloat(metric.value);
      
      // If value is NaN, return a placeholder
      if (isNaN(value)) {
        return {
          name: metric.name,
          value: 0,
          fullMark: 100,
          originalValue: 'N/A',
          metricKey: metric.key
        };
      }
      
      // Scale value between 0-100 based on metric type
      let scaledValue = value;
      let fullMark = 100;
      
      // Percentage metrics are already 0-100
      if (metric.key.includes('percent')) {
        scaledValue = value;
      } 
      // For metrics that are typically small numbers (0-10)
      else if (value < 20) {
        scaledValue = value * 10;
      }
      // For metrics that are typically larger numbers
      else {
        scaledValue = Math.min(value, 100);
      }
      
      return {
        name: metric.name.length > 10 ? metric.name.substring(0, 10) + '...' : metric.name,
        value: scaledValue,
        fullMark: fullMark,
        originalValue: value.toFixed(2),
        metricKey: metric.key
      };
    });
    
    return normalizedMetrics;
  };

  // Custom function to render a comprehensive radar chart with all metrics
  const renderComprehensiveRadarChart = () => {
    console.log("[DEBUG] renderComprehensiveRadarChart called with metrics:", metrics);
    
    try {
      // Safety check for metrics
      if (!metrics || !Array.isArray(metrics) || metrics.length === 0) {
        console.warn("[WARNING] No metrics available for radar chart");
        return (
          <div className="flex items-center justify-center h-96 bg-gray-800 rounded-xl">
            <p className="text-gray-400 text-center p-8">
              Sem métricas disponíveis para este jogador.<br/>
              Tente selecionar outro jogador com mais dados estatísticos.
            </p>
          </div>
        );
      }
      
      const data = prepareAllRadarData(metrics);
      console.log("[DEBUG] Prepared radar data:", data);
      
      if (data.length === 0) {
        return (
          <div className="flex items-center justify-center h-96 bg-gray-800 rounded-xl">
            <p className="text-gray-400 text-center p-8">
              Sem métricas disponíveis para este jogador.<br/>
              Tente selecionar outro jogador com mais dados estatísticos.
            </p>
          </div>
        );
      }
    
    // Make sure we have a valid player name for the legend
    const playerName = player && player.name ? formatPlayerName(player.name) : "Jogador";
    
    // Fixed height container instead of aspect ratio to prevent layout bugs
    return (
      <div className="w-full h-[300px] sm:h-[450px]">
        <ErrorBoundary fallback={
          <div className="flex items-center justify-center h-full bg-gray-800 rounded-xl">
            <div className="text-center p-6">
              <AlertTriangle className="mx-auto mb-4 text-yellow-500" size={32} />
              <p className="text-gray-300 mb-2">Erro ao renderizar o gráfico de radar</p>
              <p className="text-gray-400 text-sm">Os dados do jogador podem estar incompletos</p>
            </div>
          </div>
        }>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart 
              cx="50%" 
              cy="50%" 
              outerRadius="65%" 
              data={data}
            >
              <PolarGrid strokeDasharray="3 3" stroke="#4B5563" />
              <PolarAngleAxis 
                dataKey="name" 
                tick={{ fill: '#E5E7EB', fontSize: 12 }}
                stroke="#6B7280"
              />
              <PolarRadiusAxis 
                angle={30} 
                domain={[0, 100]} 
                tick={{ fill: '#9CA3AF' }}
                stroke="#4B5563"
                axisLine={false}
              />
              <Radar
                name={playerName}
                dataKey="value"
                stroke="#10B981"
                fill="#10B981"
                fillOpacity={0.6}
            />
            <Tooltip 
              formatter={(value, name, props) => {
                try {
                  // Safe access to originalValue
                  const originalValue = props?.payload?.originalValue || value;
                  return [originalValue, name];
                } catch (e) {
                  return [value, name];
                }
              }}
              contentStyle={{ 
                backgroundColor: '#1F2937', 
                borderColor: '#374151', 
                color: '#F9FAFB',
                borderRadius: '0.375rem',
                padding: '8px 12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
              }} 
              labelStyle={{ fontWeight: 'bold', marginBottom: '6px' }}
            />
            <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px' }} />
          </RadarChart>
        </ResponsiveContainer>
        </ErrorBoundary>
      </div>
    );
    } catch (error) {
      console.error("[CRITICAL] Error rendering radar chart:", error);
      return (
        <div className="flex items-center justify-center h-96 bg-gray-800 rounded-xl">
          <div className="text-center p-6">
            <AlertTriangle className="mx-auto mb-4 text-red-500" size={32} />
            <p className="text-red-400 font-bold mb-2">Erro ao renderizar o gráfico</p>
            <p className="text-gray-400 text-sm">
              Ocorreu um erro inesperado ao processar os dados do jogador.
            </p>
          </div>
        </div>
      );
    }
  };

  // Player photo URL - use a placeholder if not available
  const getPlayerImageUrl = (player) => {
    console.log("[DEBUG] getPlayerImageUrl called with player:", player);
    
    // Safety check for null/undefined player
    if (!player) {
      console.warn("[WARNING] Player object is null or undefined in getPlayerImageUrl");
      return `https://ui-avatars.com/api/?name=Unknown&background=0D8ABC&color=fff&size=256`;
    }
    
    try {
      // First try imageDataURL which is the direct Base64 image data
      if (player.imageDataURL) {
        console.log("[DEBUG] Using player.imageDataURL");
        return player.imageDataURL;
      }
      
      // Fallback to old methods for backward compatibility
      if (player.photoUrl) {
        console.log("[DEBUG] Using player.photoUrl");
        return player.photoUrl;
      }
      
      // Try to use player ID for the backend image API
      if (player.id) {
        const url = `https://katenascout-backend.onrender.com/player-image/${player.id}`;
        console.log(`[DEBUG] Using backend image API: ${url}`);
        return url;
      }
      
      // Last fallback to UI Avatars API for a consistent placeholder
      const name = player.name || "Unknown";
      const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=0D8ABC&color=fff&size=256`;
      console.log(`[DEBUG] Using UI Avatars fallback: ${avatarUrl}`);
      return avatarUrl;
    } catch (error) {
      console.error("[ERROR] Error in getPlayerImageUrl:", error);
      return `https://ui-avatars.com/api/?name=Error&background=CC0000&color=fff&size=256`;
    }
  };
  
  const playerPhotoUrl = getPlayerImageUrl(player);

  // We no longer display player scores based on requirements

  return (
    <div className="w-full max-w-4xl bg-gray-950 flex flex-col overflow-auto mx-auto shadow-2xl rounded-xl">
      {/* Header with close button */}
      <div className="bg-gray-800 p-4 flex justify-between items-center border-b border-gray-700 sticky top-0 z-10">
        <h2 className="text-xl font-bold text-white flex items-center">
          <div className="w-8 h-8 mr-3 text-green-500 font-bold">⚽</div>
          Dashboard do Jogador
        </h2>
        <div className="flex items-center space-x-2">
          <button 
            onClick={() => toggleFavorite()}
            className={`p-2 rounded-lg ${isPlayerFavorite ? 'bg-red-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
            title={isPlayerFavorite ? "Remove from favorites" : "Add to favorites"}
          >
            <Heart size={20} fill={isPlayerFavorite ? "white" : "none"} />
          </button>
          <button 
            onClick={() => onViewComplete && onViewComplete(player)}
            className="p-2 bg-green-700 text-white rounded-lg hover:bg-green-600"
            title="View complete profile"
          >
            <Eye size={20} />
          </button>
          <button onClick={onClose} className="p-2 bg-gray-700 rounded-lg text-gray-300 hover:bg-gray-600 hover:text-white">
            <X size={20} />
          </button>
        </div>
      </div>

      {/* Player Overview Card */}
      <div className="p-6 overflow-y-auto max-h-[calc(90vh-64px)] custom-scrollbar">
        <div className="bg-gradient-to-r from-green-900 to-blue-900 rounded-xl mb-6 text-white shadow-lg overflow-hidden relative">
          {/* Soccer field background pattern - lower z-index */}
          <div className="absolute inset-0 opacity-10" style={{ zIndex: 0 }}>
            <div className="w-full h-full border border-white"></div>
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[60%] h-[70%] border border-white rounded-full"></div>
            <div className="absolute left-1/2 -translate-x-1/2 w-0.5 h-full bg-white opacity-50"></div>
            <div className="absolute top-[85%] left-[50%] -translate-x-1/2 w-[15%] h-[30%] border border-white rounded-t-full"></div>
            <div className="absolute top-0 left-[50%] -translate-x-1/2 w-[15%] h-[30%] border border-white rounded-b-full"></div>
          </div>
          
          {/* Player card */}
          <div className="relative h-full">
            {/* Photo background area (left side) */}
            <div className="absolute left-0 top-0 bottom-0 w-1/3 bg-gradient-to-r from-black to-transparent opacity-50"></div>
            
            {/* Content wrapper */}
            <div className="relative flex flex-col sm:flex-row p-4 sm:p-6">
              {/* Player Photo - Larger and more prominent */}
              <div className="mb-4 sm:mb-0 sm:mr-6">
                <div className="w-28 h-36 sm:w-36 sm:h-44 mx-auto sm:mx-0 overflow-hidden rounded-lg border-4 border-white bg-gray-800 shadow-xl relative">
                  <ErrorBoundary fallback={
                    <div className="w-full h-full bg-gray-700 flex items-center justify-center">
                      <div className="text-white text-center">
                        <AlertTriangle size={24} className="mx-auto mb-2" />
                        <div className="text-xs">Imagem indisponível</div>
                      </div>
                    </div>
                  }>
                    <img 
                      src={playerPhotoUrl} 
                      alt={player.name || "Jogador"} 
                      className="w-full h-full object-cover"
                      loading="eager"
                      onError={(e) => {
                        console.warn("[WARNING] Player image failed to load:", e);
                        e.target.onerror = null; 
                        const name = player && player.name ? player.name : "Unknown";
                        e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=0D8ABC&color=fff&size=256`;
                      }}
                    />
                  </ErrorBoundary>
                  
                  {/* Position badge */}
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-2 text-center">
                    <div className="text-xs font-bold">{positionDisplay}</div>
                  </div>
                  
                  {/* Position badge at bottom right */}
                  <div className="absolute -bottom-4 -right-4">
                    <div className="w-16 h-16 flex items-center justify-center bg-gradient-to-b from-blue-500 to-blue-700 rounded-full shadow-lg border-2 border-white">
                      <span className="text-2xl font-bold text-white">{player.positions?.[0]?.toUpperCase() || 'ST'}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Player info */}
              <div className="flex-1">
                <div className="flex items-center justify-center sm:justify-start">
                  <div className="mr-3 p-1 bg-white bg-opacity-20 rounded">
                    <img 
                      src={`https://ui-avatars.com/api/?name=${encodeURIComponent(
                        typeof player.club === 'object' && player.club !== null 
                          ? (player.club.name?.substring(0,2) || player.club.alpha3code?.substring(0,2) || 'FC')
                          : (player.club?.substring(0,2) || 'FC')
                      )}&background=111827&color=fff&size=20&font-size=0.5&bold=true`}
                      alt="Club"
                      className="w-6 h-6 rounded-full"
                    />
                  </div>
                  <h1 className="text-3xl font-bold">{formatPlayerName(typeof player.name === 'object' ? 'Jogador' : player.name)}</h1>
                </div>
                
                <div className="flex flex-wrap items-center gap-2 mt-2 mb-4">
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.age} anos</span>
                  </div>
                  
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.height || '--'} cm</span>
                  </div>
                  
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.weight || '--'} kg</span>
                  </div>
                  
                  {player.nationality && (
                    <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                      <span className="text-sm font-medium">
                        {getCountryFlag(player.nationality)} {
                          typeof player.nationality === 'object' && player.nationality !== null
                            ? (player.nationality.name || 
                               player.nationality.alpha3code || 
                               'País')
                            : String(player.nationality)
                        }
                      </span>
                    </div>
                  )}
                  
                  {player.foot && (
                    <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                      {player.foot === 'left' ? (
                        <span className="text-sm font-medium flex items-center">
                          <span className="w-4 h-4 mr-1 inline-flex items-center justify-center bg-blue-600 rounded-full text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-2.5 w-2.5" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clipRule="evenodd" />
                            </svg>
                          </span>
                          Canhoto
                        </span>
                      ) : player.foot === 'right' ? (
                        <span className="text-sm font-medium flex items-center">
                          <span className="w-4 h-4 mr-1 inline-flex items-center justify-center bg-green-600 rounded-full text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-2.5 w-2.5" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                          </span>
                          Destro
                        </span>
                      ) : (
                        <span className="text-sm font-medium flex items-center">
                          <span className="w-4 h-4 mr-1 inline-flex items-center justify-center bg-purple-600 rounded-full text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-2.5 w-2.5" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M3 7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 13a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                            </svg>
                          </span>
                          {player.foot === 'both' ? 'Ambidestro' : player.foot}
                        </span>
                      )}
                    </div>
                  )}
                </div>
                
                {/* Player info cards */}
                <div className="bg-black bg-opacity-30 backdrop-blur-sm rounded-lg p-4 mt-2 border border-white border-opacity-20">
                  <h3 className="text-sm uppercase text-green-300 mb-3 flex items-center">
                    <Trophy className="mr-2" size={14} />
                    Informações do Jogador
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="flex items-center justify-center sm:justify-start">
                        <Package className="mr-2 text-blue-300" size={14} />
                        <span className="text-sm text-gray-300">Clube Atual</span>
                      </div>
                      <div className="font-medium">
                        {typeof player.club === 'object' && player.club !== null
                          ? (player.club.name || String(player.club) || "Informação indisponível")
                          : (player.club || "Informação indisponível")
                        }
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center">
                        <Calendar className="mr-2 text-blue-300" size={14} />
                        <span className="text-sm text-gray-300">Contrato até</span>
                      </div>
                      <div className="font-medium">{player.contractUntil || "Informação indisponível"}</div>
                    </div>
                    
                    {player.nationality && (
                      <div>
                        <div className="flex items-center">
                          <Globe className="mr-2 text-blue-300" size={14} />
                          <span className="text-sm text-gray-300">Nacionalidade</span>
                        </div>
                        <div className="font-medium flex items-center">
                          <span className="mr-2">{getCountryFlag(player.nationality)}</span>
                          <span>
                            {typeof player.nationality === 'object' && player.nationality !== null
                              ? (player.nationality.name || 
                                 player.nationality.alpha3code || 
                                 'País')
                              : String(player.nationality)
                            }
                          </span>
                        </div>
                      </div>
                    )}
                    
                    {player.foot && (
                      <div>
                        <div className="flex items-center">
                          <Boot className="mr-2 text-blue-300" size={14} />
                          <span className="text-sm text-gray-300">Pé Preferido</span>
                        </div>
                        <div className="font-medium flex items-center">
                          {player.foot === 'left' ? (
                            <>
                              <span className="w-5 h-5 mr-2 inline-flex items-center justify-center bg-blue-600 rounded-full text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                  <path fillRule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H15a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clipRule="evenodd" />
                                </svg>
                              </span>
                              <span>Canhoto</span>
                            </>) : 
                           player.foot === 'right' ? (
                            <>
                              <span className="w-5 h-5 mr-2 inline-flex items-center justify-center bg-green-600 rounded-full text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                  <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                                </svg>
                              </span>
                              <span>Destro</span>
                            </>) : (
                            <>
                              <span className="w-5 h-5 mr-2 inline-flex items-center justify-center bg-purple-600 rounded-full text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                  <path fillRule="evenodd" d="M3 7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 13a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                                </svg>
                              </span>
                              <span>{player.foot === 'both' ? 'Ambidestro' : player.foot}</span>
                            </>)
                          }
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Comprehensive Radar Chart Section */}
        <div className="bg-gray-800 rounded-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-white mb-5 flex items-center border-b border-gray-700 pb-3">
            <BarChart3 className="mr-3 text-green-500" size={24} />
            Radar de Performance
          </h2>
          
          {/* Main radar chart with all metrics */}
          {renderComprehensiveRadarChart()}
          
          <div className="mt-5 text-gray-400 text-sm border-t border-gray-700 pt-3">
            <p>O radar mostra os valores normalizados das métricas do jogador. Passe o mouse sobre as métricas para ver os valores originais.</p>
          </div>
        </div>
        
        {/* Metrics Table with scrolling */}
        <div className="bg-gray-800 rounded-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center border-b border-gray-700 pb-3">
            <TrendingUp className="mr-3 text-green-500" size={24} />
            Métricas Detalhadas
          </h2>
          
          {/* Added max-height and overflow for scrolling if too many metrics */}
          <div className="max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 sm:gap-x-10 gap-y-2">
              {metrics.map((metric, idx) => (
                <div key={idx} className="flex justify-between items-center py-2 border-b border-gray-700">
                  <span className="text-gray-300 pr-4">{metric.name}</span>
                  <span className={`font-bold ${getMetricColor(metric)}`}>
                    {typeof metric.value === 'number' ? metric.value.toFixed(2) : metric.value || 'N/A'}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Note about metrics */}
          <div className="mt-4 text-gray-500 text-xs italic">
            Total de {metrics.length} métricas disponíveis para este jogador.
          </div>
        </div>
        
        {/* Action Buttons */}
        <div className="mt-6 flex justify-center space-x-4">
          <button 
            onClick={() => toggleFavorite()}
            className={`px-4 py-2 rounded-lg flex items-center ${
              isPlayerFavorite ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-gray-700 text-white hover:bg-gray-600'
            }`}
          >
            <Heart size={18} className="mr-2" fill={isPlayerFavorite ? "white" : "none"} />
            {isPlayerFavorite ? 'Remove dos Favoritos' : 'Adicionar aos Favoritos'}
          </button>
          
          <button 
            onClick={() => onViewComplete && onViewComplete(player)}
            className="px-4 py-2 bg-green-700 text-white rounded-lg hover:bg-green-600 flex items-center"
          >
            <Eye size={18} className="mr-2" />
            Ver Perfil Completo
          </button>
        </div>
      </div>
    </div>
  );
};

// PlayerCompletePage component for displaying detailed player information
const PlayerCompletePage = ({ player, onClose, isPlayerFavorite, toggleFavorite, currentLanguage = 'english' }) => {
  // Helper function to get position names based on language
  const getPositionMap = () => {
    const positionMaps = {
      english: {
        'cb': 'Center Back',
        'lb': 'Left Back',
        'rb': 'Right Back',
        'dmf': 'Defensive Mid',
        'cmf': 'Central Mid',
        'amf': 'Attacking Mid',
        'lw': 'Left Wing',
        'rw': 'Right Wing',
        'cf': 'Center Forward',
        'gk': 'Goalkeeper',
      },
      portuguese: {
        'cb': 'Zagueiro',
        'lb': 'Lateral Esquerdo',
        'rb': 'Lateral Direito',
        'dmf': 'Volante',
        'cmf': 'Meio-Campo',
        'amf': 'Meia Atacante',
        'lw': 'Ponta Esquerda',
        'rw': 'Ponta Direita',
        'cf': 'Centroavante',
        'gk': 'Goleiro',
      },
      spanish: {
        'cb': 'Defensa Central',
        'lb': 'Lateral Izquierdo',
        'rb': 'Lateral Derecho',
        'dmf': 'Pivote',
        'cmf': 'Mediocentro',
        'amf': 'Mediapunta',
        'lw': 'Extremo Izquierdo',
        'rw': 'Extremo Derecho',
        'cf': 'Delantero Centro',
        'gk': 'Portero',
      },
      bulgarian: {
        'cb': 'Централен Защитник',
        'lb': 'Ляв Бек',
        'rb': 'Десен Бек',
        'dmf': 'Дефанзивен Полузащитник',
        'cmf': 'Централен Полузащитник',
        'amf': 'Атакуващ Полузащитник',
        'lw': 'Ляво Крило',
        'rw': 'Дясно Крило',
        'cf': 'Централен Нападател',
        'gk': 'Вратар',
      }
    };
    
    return positionMaps[currentLanguage] || positionMaps.english;
  };

  // Helper function to format player names with proper spacing
  const formatPlayerName = (name) => {
    if (!name) return '';
    return name.replace(/([A-Z])/g, ' $1').trim()
      .replace(/\s+/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const positionMap = getPositionMap();
  const positionDisplay = player.positions?.map(pos => positionMap[pos] || pos).join(', ');

  // Get player photo URL
  const getPlayerImageUrl = (player) => {
    console.log("[DEBUG] getPlayerImageUrl called with player:", player);
    
    // Safety check for null/undefined player
    if (!player) {
      console.warn("[WARNING] Player object is null or undefined in getPlayerImageUrl");
      return `https://ui-avatars.com/api/?name=Unknown&background=0D8ABC&color=fff&size=256`;
    }
    
    try {
      // First try imageDataURL which is the direct Base64 image data
      if (player.imageDataURL) {
        console.log("[DEBUG] Using player.imageDataURL");
        return player.imageDataURL;
      }
      
      // Fallback to old methods for backward compatibility
      if (player.photoUrl) {
        console.log("[DEBUG] Using player.photoUrl");
        return player.photoUrl;
      }
      
      // Try to use player ID for the backend image API
      if (player.id) {
        const url = `https://katenascout-backend.onrender.com/player-image/${player.id}`;
        console.log(`[DEBUG] Using backend image API: ${url}`);
        return url;
      }
      
      // Last fallback to UI Avatars API for a consistent placeholder
      const name = player.name || "Unknown";
      const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=0D8ABC&color=fff&size=256`;
      console.log(`[DEBUG] Using UI Avatars fallback: ${avatarUrl}`);
      return avatarUrl;
    } catch (error) {
      console.error("[ERROR] Error in getPlayerImageUrl:", error);
      return `https://ui-avatars.com/api/?name=Error&background=CC0000&color=fff&size=256`;
    }
  };
  
  const playerPhotoUrl = getPlayerImageUrl(player);

  // Extract ALL metrics from the player object with error handling
  const metrics = (() => {
    try {
      if (!player || !player.stats) {
        console.warn("[WARNING] Player stats missing or undefined");
        return [];
      }
      
      return Object.entries(player.stats)
        .map(([key, value]) => {
          // Validate each metric value
          if (value === undefined || value === null) {
            console.warn(`[WARNING] Metric ${key} has null/undefined value`);
            value = 0; // Replace with default value
          }
          
          return {
            name: key.replace(/_/g, ' ')
              .split(' ')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' '),
            value: value,
            key: key
          };
        })
        // Sort metrics alphabetically for better organization
        .sort((a, b) => a.name.localeCompare(b.name));
    } catch (error) {
      console.error("[ERROR] Failed to process player metrics:", error);
      return []; // Return empty array on error
    }
  })();

  // Helper function to get a color based on metric value
  const getMetricColor = (metric) => {
    // Placeholder logic - in a real app this would be based on comparison with league averages
    const value = parseFloat(metric.value);
    if (isNaN(value)) return 'text-gray-400';
    
    // Different metrics have different scales
    if (metric.key.includes('percent')) {
      if (value > 80) return 'text-green-500';
      if (value > 60) return 'text-yellow-500';
      return 'text-red-500';
    }
    
    // Default scale for other metrics
    if (value > 7) return 'text-green-500';
    if (value > 4) return 'text-yellow-500';
    return 'text-red-500';
  };

  // Translations for player complete page
  const translations = {
    english: {
      playerProfile: "Player Profile",
      basicInfo: "Basic Information",
      position: "Position",
      age: "Age",
      height: "Height",
      weight: "Weight",
      club: "Current Club",
      contractUntil: "Contract Until",
      statistics: "Player Statistics",
      back: "Back to Favorites",
      years: "years",
      cm: "cm",
      kg: "kg",
      addToFavorites: "Add to Favorites",
      removeFromFavorites: "Remove from Favorites",
      generalStats: "General Statistics",
      noStats: "No statistics available for this player",
      nationality: "Nationality",
      foot: "Preferred Foot",
      leftFoot: "Left",
      rightFoot: "Right",
      totalMetrics: "Total metrics"
    },
    portuguese: {
      playerProfile: "Perfil do Jogador",
      basicInfo: "Informações Básicas",
      position: "Posição",
      age: "Idade",
      height: "Altura",
      weight: "Peso",
      club: "Clube Atual",
      contractUntil: "Contrato Até",
      statistics: "Estatísticas do Jogador",
      back: "Voltar aos Favoritos",
      years: "anos",
      cm: "cm",
      kg: "kg",
      addToFavorites: "Adicionar aos Favoritos",
      removeFromFavorites: "Remover dos Favoritos",
      generalStats: "Estatísticas Gerais",
      noStats: "Não há estatísticas disponíveis para este jogador",
      nationality: "Nacionalidade",
      foot: "Pé Preferido",
      leftFoot: "Canhoto",
      rightFoot: "Destro",
      totalMetrics: "Total de métricas"
    },
    spanish: {
      playerProfile: "Perfil del Jugador",
      basicInfo: "Información Básica",
      position: "Posición",
      age: "Edad",
      height: "Altura",
      weight: "Peso",
      club: "Club Actual",
      contractUntil: "Contrato Hasta",
      statistics: "Estadísticas del Jugador",
      back: "Volver a Favoritos",
      years: "años",
      cm: "cm",
      kg: "kg",
      addToFavorites: "Añadir a Favoritos",
      removeFromFavorites: "Quitar de Favoritos",
      generalStats: "Estadísticas Generales",
      noStats: "No hay estadísticas disponibles para este jugador",
      nationality: "Nacionalidad",
      foot: "Pie Preferido",
      leftFoot: "Izquierdo",
      rightFoot: "Derecho",
      totalMetrics: "Total de métricas"
    },
    bulgarian: {
      playerProfile: "Профил на Играча",
      basicInfo: "Основна Информация",
      position: "Позиция",
      age: "Възраст",
      height: "Височина",
      weight: "Тегло",
      club: "Настоящ Клуб",
      contractUntil: "Договор До",
      statistics: "Статистика на Играча",
      back: "Обратно към Любими",
      years: "години",
      cm: "см",
      kg: "кг",
      addToFavorites: "Добави в Любими",
      removeFromFavorites: "Премахни от Любими",
      generalStats: "Обща Статистика",
      noStats: "Няма налична статистика за този играч",
      nationality: "Националност",
      foot: "Предпочитан Крак",
      leftFoot: "Ляв",
      rightFoot: "Десен",
      totalMetrics: "Общ брой показатели"
    }
  };

  // Get translations for the current language
  const t = translations[currentLanguage] || translations.english;

  return (
    <div className="flex-1 bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-900 to-blue-900 p-4 flex justify-between items-center relative">
        <button
          onClick={onClose}
          className="text-white flex items-center"
        >
          <ArrowLeft className="mr-2" size={20} />
          <span>{t.back}</span>
        </button>
        <h2 className="text-xl font-bold text-white absolute left-1/2 transform -translate-x-1/2">
          {t.playerProfile}
        </h2>
        <button
          onClick={toggleFavorite}
          className={`p-2 rounded-lg ${
            isPlayerFavorite
              ? 'bg-red-600 text-white'
              : 'bg-gray-700 text-white'
          }`}
        >
          <Heart size={20} fill={isPlayerFavorite ? "white" : "none"} />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {/* Player Hero Section */}
        <div className="bg-gradient-to-r from-gray-800 to-gray-700 rounded-xl mb-6 overflow-hidden shadow-lg">
          <div className="p-6 flex flex-col md:flex-row items-center md:items-start gap-6">
            {/* Player Image */}
            <div className="relative">
              <div className="w-32 h-40 rounded-lg overflow-hidden border-4 border-white shadow-lg bg-gray-200">
                <img 
                  src={playerPhotoUrl}
                  alt={player.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.onerror = null; 
                    e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                  }}
                />
              </div>
              <div className="absolute -bottom-3 -right-3 bg-blue-600 text-white text-sm font-bold p-2 rounded-full shadow-lg">
                {player.positions?.[0]?.toUpperCase() || 'ST'}
              </div>
            </div>

            {/* Player Basic Info */}
            <div className="flex-1 text-center md:text-left">
              <h1 className="text-2xl font-bold text-white mb-2">{formatPlayerName(player.name)}</h1>
              <div className="text-green-300 mb-4">{positionDisplay}</div>
              
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                <div className="bg-gray-900 bg-opacity-50 rounded-lg p-3">
                  <div className="text-gray-400 mb-1">{t.age}</div>
                  <div className="text-white font-medium">{player.age} {t.years}</div>
                </div>
                <div className="bg-gray-900 bg-opacity-50 rounded-lg p-3">
                  <div className="text-gray-400 mb-1">{t.height}</div>
                  <div className="text-white font-medium">{player.height || '–'} {t.cm}</div>
                </div>
                <div className="bg-gray-900 bg-opacity-50 rounded-lg p-3">
                  <div className="text-gray-400 mb-1">{t.weight}</div>
                  <div className="text-white font-medium">{player.weight || '–'} {t.kg}</div>
                </div>
                
                {player.nationality && (
                  <div className="bg-gray-900 bg-opacity-50 rounded-lg p-3">
                    <div className="text-gray-400 mb-1">{t.nationality || 'Nationality'}</div>
                    <div className="text-white font-medium">
                      {typeof player.nationality === 'object' && player.nationality !== null
                        ? (player.nationality.name || 
                           player.nationality.alpha3code || 
                           'País')
                        : String(player.nationality)
                      }
                    </div>
                  </div>
                )}
                
                {player.foot && (
                  <div className="bg-gray-900 bg-opacity-50 rounded-lg p-3">
                    <div className="text-gray-400 mb-1">{t.foot || 'Preferred Foot'}</div>
                    <div className="text-white font-medium">
                      {player.foot === 'left' ? '👈 ' + (t.leftFoot || 'Left') : 
                       player.foot === 'right' ? '👉 ' + (t.rightFoot || 'Right') : 
                       player.foot}
                    </div>
                  </div>
                )}
                
                <div className="bg-gray-900 bg-opacity-50 rounded-lg p-3 md:col-span-1">
                  <div className="text-gray-400 mb-1">{t.club}</div>
                  <div className="text-white font-medium">
                    {typeof player.club === 'object' && player.club !== null
                      ? (player.club.name || String(player.club) || 'Unknown')
                      : (player.club || 'Unknown')
                    }
                  </div>
                </div>
                
                <div className="bg-gray-900 bg-opacity-50 rounded-lg p-3">
                  <div className="text-gray-400 mb-1">{t.contractUntil}</div>
                  <div className="text-white font-medium">{player.contractUntil || '–'}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Statistics Section */}
        <div className="bg-gray-800 rounded-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-white mb-4 border-b border-gray-700 pb-3">
            {t.statistics}
          </h2>

          {metrics.length > 0 ? (
            <div className="max-h-[600px] overflow-y-auto custom-scrollbar pr-2">
              {/* Group metrics by categories */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-3">
                {metrics.map((metric, idx) => (
                  <div key={idx} className="flex justify-between items-center py-2 border-b border-gray-700 hover:bg-gray-750 px-2 rounded transition-colors">
                    <span className="text-gray-300 truncate mr-2">{metric.name}</span>
                    <span className={`font-bold ${getMetricColor(metric)} tabular-nums`}>
                      {typeof metric.value === 'number' ? metric.value.toFixed(2) : metric.value || 'N/A'}
                    </span>
                  </div>
                ))}
              </div>
              
              {/* Total metrics count */}
              <div className="mt-6 text-right text-sm text-gray-500">
                {t.totalMetrics || 'Total metrics'}: {metrics.length}
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400">
              {t.noStats}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// FavoritesView component for displaying saved favorite players
const FavoritesView = ({ favorites, onSelectPlayer, onRemoveFavorite, currentLanguage = 'english' }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFavoritePlayer, setSelectedFavoritePlayer] = useState(null);
  
  // Filter favorites based on search query
  const filteredFavorites = favorites.filter(player => {
    if (searchQuery.trim() === '') return true;
    
    const query = searchQuery.toLowerCase();
    return (
      player.name?.toLowerCase().includes(query) ||
      player.club?.toLowerCase().includes(query) ||
      player.positions?.some(pos => pos.toLowerCase().includes(query))
    );
  });
  
  // Helper function to format player names with proper spacing
  const formatPlayerName = (name) => {
    if (!name) return '';
    return name.replace(/([A-Z])/g, ' $1').trim()
      .replace(/\s+/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };
  
  // Helper function to get position names based on language
  const getPositionMap = () => {
    const positionMaps = {
      english: {
        'cb': 'Center Back',
        'lb': 'Left Back',
        'rb': 'Right Back',
        'dmf': 'Defensive Mid',
        'cmf': 'Central Mid',
        'amf': 'Attacking Mid',
        'lw': 'Left Wing',
        'rw': 'Right Wing',
        'cf': 'Center Forward',
        'gk': 'Goalkeeper',
      },
      portuguese: {
        'cb': 'Zagueiro',
        'lb': 'Lateral Esquerdo',
        'rb': 'Lateral Direito',
        'dmf': 'Volante',
        'cmf': 'Meio-Campo',
        'amf': 'Meia Atacante',
        'lw': 'Ponta Esquerda',
        'rw': 'Ponta Direita',
        'cf': 'Centroavante',
        'gk': 'Goleiro',
      },
      spanish: {
        'cb': 'Defensa Central',
        'lb': 'Lateral Izquierdo',
        'rb': 'Lateral Derecho',
        'dmf': 'Pivote',
        'cmf': 'Mediocentro',
        'amf': 'Mediapunta',
        'lw': 'Extremo Izquierdo',
        'rw': 'Extremo Derecho',
        'cf': 'Delantero Centro',
        'gk': 'Portero',
      },
      bulgarian: {
        'cb': 'Централен Защитник',
        'lb': 'Ляв Бек',
        'rb': 'Десен Бек',
        'dmf': 'Дефанзивен Полузащитник',
        'cmf': 'Централен Полузащитник',
        'amf': 'Атакуващ Полузащитник',
        'lw': 'Ляво Крило',
        'rw': 'Дясно Крило',
        'cf': 'Централен Нападател',
        'gk': 'Вратар',
      }
    };
    
    return positionMaps[currentLanguage] || positionMaps.english;
  };
  
  const positionMap = getPositionMap();
  
  // Get position display string for a position code
  const getPositionName = (pos) => positionMap[pos] || pos;
  
  // Handle selecting a player for detailed view
  const handlePlayerSelect = (player) => {
    if (selectedFavoritePlayer) {
      // We're already viewing a player, go back to the list
      setSelectedFavoritePlayer(null);
    } else {
      // Show the selected player in the PlayerCompletePage
      setSelectedFavoritePlayer(player);
    }
  };
  
  // Handle selecting a player for the modal view
  const handleModalView = (player) => {
    // Extract metrics from the player object to display in the dashboard
    const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => ({
      name: key.replace(/_/g, ' ')
              .split(' ')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' '),
      value: value,
      key: key
    }));
    
    // Call the parent component's callback to show the player dashboard
    onSelectPlayer(player, playerMetrics);
  };
  
  // Translations for the FavoritesView component
  const translations = {
    english: {
      title: "Favorite Players",
      searchPlaceholder: "Search your favorites...",
      noFavorites: "No favorite players yet",
      noFavoritesDescription: "Use the chat to find and add players to your favorites.",
      viewDetails: "View Details",
      completeProfile: "Complete Profile",
      remove: "Remove",
      age: "years old"
    },
    portuguese: {
      title: "Jogadores Favoritos",
      searchPlaceholder: "Buscar nos favoritos...",
      noFavorites: "Nenhum jogador favorito ainda",
      noFavoritesDescription: "Use o chat para encontrar e adicionar jogadores aos seus favoritos.",
      viewDetails: "Ver Detalhes",
      completeProfile: "Perfil Completo",
      remove: "Remover",
      age: "anos"
    },
    spanish: {
      title: "Jugadores Favoritos",
      searchPlaceholder: "Buscar en favoritos...",
      noFavorites: "Aún no hay jugadores favoritos",
      noFavoritesDescription: "Usa el chat para encontrar y añadir jugadores a tus favoritos.",
      viewDetails: "Ver Detalles",
      completeProfile: "Perfil Completo",
      remove: "Eliminar",
      age: "años"
    },
    bulgarian: {
      title: "Любими Играчи",
      searchPlaceholder: "Търсете в любимите...",
      noFavorites: "Все още няма любими играчи",
      noFavoritesDescription: "Използвайте чата, за да намерите и добавите играчи към любимите си.",
      viewDetails: "Преглед",
      completeProfile: "Пълен Профил",
      remove: "Премахване",
      age: "години"
    }
  };
  
  // Get translations for the current language
  const t = translations[currentLanguage] || translations.english;
  
  // If a player is selected, show the PlayerCompletePage
  if (selectedFavoritePlayer) {
    const isPlayerFav = favorites.some(f => 
      f.id === selectedFavoritePlayer.id || f.name === selectedFavoritePlayer.name
    );
    
    return (
      <PlayerCompletePage
        player={selectedFavoritePlayer}
        onClose={() => setSelectedFavoritePlayer(null)}
        isPlayerFavorite={isPlayerFav}
        toggleFavorite={() => onRemoveFavorite(selectedFavoritePlayer)}
        currentLanguage={currentLanguage}
      />
    );
  }
  
  return (
    <div className="flex-1 bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <Heart className="mr-3 text-red-500" size={24} />
          {t.title}
        </h2>
      </div>
      
      {/* Search Bar */}
      {favorites.length > 0 && (
        <div className="bg-gray-800 p-4 border-b border-gray-700">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="search"
              className="block w-full bg-gray-700 border border-gray-600 rounded-lg py-2 pl-10 pr-3 text-gray-300 placeholder-gray-400 focus:outline-none focus:border-green-500"
              placeholder={t.searchPlaceholder}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
      )}
      
      {/* Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        {favorites.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-20 h-20 rounded-full bg-gray-800 flex items-center justify-center mb-4">
              <Heart className="text-gray-600" size={40} />
            </div>
            <h3 className="text-xl font-medium text-gray-300 mb-2">{t.noFavorites}</h3>
            <p className="text-gray-500 max-w-md">
              {t.noFavoritesDescription}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredFavorites.map((player, index) => (
              <div 
                key={index} 
                className="bg-gray-800 rounded-xl overflow-hidden border border-gray-700 hover:border-green-500 transition-colors shadow-md"
              >
                <div className="p-4">
                  {/* Player Name & Position */}
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h3 className="text-lg font-bold text-white">{formatPlayerName(player.name)}</h3>
                      <div className="text-sm text-gray-400">
                        {player.positions?.map(pos => getPositionName(pos)).join(', ')}
                      </div>
                    </div>
                    
                    {/* Remove button */}
                    <button 
                      onClick={() => onRemoveFavorite(player)}
                      className="p-2 bg-red-600 text-white rounded-full hover:bg-red-700"
                      title={t.remove}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                  
                  {/* Player Info */}
                  <div className="flex items-center mb-4">
                    {/* Player Image */}
                    <div className="w-16 h-16 bg-gray-700 rounded-full overflow-hidden mr-3">
                      <img 
                        src={player.imageDataURL || player.photoUrl || (player.id ? `https://katenascout-backend.onrender.com/player-image/${player.id}` : `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=128`)}
                        alt={player.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.target.onerror = null; 
                          e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=128`;
                        }}
                      />
                    </div>
                    
                    <div>
                      <div className="text-gray-300">
                        {typeof player.club === 'object' && player.club !== null
                          ? (player.club.name || String(player.club) || 'Unknown Club')
                          : (player.club || 'Unknown Club')
                        }
                      </div>
                      <div className="text-gray-400 text-sm">{player.age} {t.age}</div>
                    </div>
                  </div>
                  
                  {/* Key Stats if available */}
                  {player.stats && Object.keys(player.stats).length > 0 && (
                    <div className="grid grid-cols-3 gap-2 mb-4">
                      {Object.entries(player.stats).slice(0, 3).map(([key, value], idx) => (
                        <div key={idx} className="bg-gray-750 p-1 rounded text-center">
                          <div className="text-xs text-gray-400">{key.split('_')[0]}</div>
                          <div className="text-sm font-medium text-white">{value}</div>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  {/* Action Button */}
                  <div className="flex justify-center">
                    {/* View Complete Profile Button */}
                    <button 
                      onClick={() => handlePlayerSelect(player)}
                      className="py-2 px-4 bg-green-700 hover:bg-green-600 text-white rounded-lg flex items-center justify-center"
                    >
                      <User size={16} className="mr-2" />
                      {t.completeProfile}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// SettingsView component for language settings
const SettingsView = ({ currentLanguage, setCurrentLanguage }) => {
  // Fetch available languages
  const [availableLanguages, setAvailableLanguages] = useState([
    { id: 'english', name: 'English', native_name: 'English', code: 'en' },
    { id: 'portuguese', name: 'Portuguese', native_name: 'Português', code: 'pt' },
    { id: 'spanish', name: 'Spanish', native_name: 'Español', code: 'es' },
    { id: 'bulgarian', name: 'Bulgarian', native_name: 'Български', code: 'bg' }
  ]);
  
  // Try to fetch languages from backend if available
  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const response = await fetch('https://katenascout-backend.onrender.com/languages');
        const data = await response.json();
        
        if (data.success && data.languages) {
          // Transform from object to array
          const languagesArray = Object.entries(data.languages).map(([id, langData]) => ({
            id,
            ...langData
          }));
          
          setAvailableLanguages(languagesArray);
        }
      } catch (error) {
        console.error("Error fetching languages:", error);
        // Keep using the default languages
      }
    };
    
    fetchLanguages();
  }, []);
  
  // Translations for settings
  const translations = {
    english: {
      title: "Settings",
      languageSettings: "Language Settings",
      languageChange: "Select your preferred language",
      languageChangeImmediate: "Language will change immediately",
      aboutTitle: "About KatenaScout",
      aboutDescription: "KatenaScout is an AI-powered football scouting assistant. It helps scouts and coaches find players matching specific criteria through natural language search.",
      version: "Version",
      poweredBy: "Powered by Claude AI"
    },
    portuguese: {
      title: "Configurações",
      languageSettings: "Configurações de Idioma",
      languageChange: "Selecione seu idioma preferido",
      languageChangeImmediate: "O idioma mudará imediatamente",
      aboutTitle: "Sobre o KatenaScout",
      aboutDescription: "KatenaScout é um assistente de scouting de futebol com IA. Ajuda scouts e técnicos a encontrar jogadores que correspondam a critérios específicos através de busca em linguagem natural.",
      version: "Versão",
      poweredBy: "Desenvolvido com Claude AI"
    },
    spanish: {
      title: "Configuración",
      languageSettings: "Configuración de Idioma",
      languageChange: "Selecciona tu idioma preferido",
      languageChangeImmediate: "El idioma cambiará inmediatamente",
      aboutTitle: "Acerca de KatenaScout",
      aboutDescription: "KatenaScout es un asistente de scouting de fútbol con IA. Ayuda a los scouts y entrenadores a encontrar jugadores que coincidan con criterios específicos a través de búsqueda en lenguaje natural.",
      version: "Versión",
      poweredBy: "Desarrollado con Claude AI"
    },
    bulgarian: {
      title: "Настройки",
      languageSettings: "Настройки на езика",
      languageChange: "Изберете предпочитания от вас език",
      languageChangeImmediate: "Езикът ще се промени веднага",
      aboutTitle: "За KatenaScout",
      aboutDescription: "KatenaScout е асистент за футболно наблюдение, поддържан от изкуствен интелект. Помага на скаути и треньори да намират играчи, отговарящи на специфични критерии чрез търсене на естествен език.",
      version: "Версия",
      poweredBy: "Създадено с Claude AI"
    }
  };
  
  // Get translations for current language
  const t = translations[currentLanguage] || translations.english;

  return (
    <div className="flex-1 bg-gray-900 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <Settings className="mr-3 text-green-500" size={24} />
          {t.title}
        </h2>
      </div>
      
      {/* Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-2xl mx-auto space-y-8">
          {/* Language Settings */}
          <div className="bg-gray-800 rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center border-b border-gray-700 pb-3">
              <Globe className="mr-3 text-blue-400" size={20} />
              {t.languageSettings}
            </h3>
            
            <p className="text-gray-300 mb-4">{t.languageChange}</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
              {availableLanguages.map(lang => (
                <button
                  key={lang.id}
                  onClick={() => setCurrentLanguage(lang.id)}
                  className={`flex items-center p-3 rounded-lg transition-colors ${
                    currentLanguage === lang.id
                      ? 'bg-green-800 bg-opacity-30 border border-green-600 text-white'
                      : 'bg-gray-750 border border-gray-700 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  <div className="mr-3 text-xl">
                    {lang.code === 'en' && '🇬🇧'}
                    {lang.code === 'pt' && '🇧🇷'}
                    {lang.code === 'es' && '🇪🇸'}
                    {lang.code === 'bg' && '🇧🇬'}
                  </div>
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
            
            <p className="text-sm text-green-400 italic">{t.languageChangeImmediate}</p>
          </div>
          
          {/* About Section */}
          <div className="bg-gray-800 rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center border-b border-gray-700 pb-3">
              <Star className="mr-3 text-yellow-400" size={20} />
              {t.aboutTitle}
            </h3>
            
            <p className="text-gray-300 mb-4">{t.aboutDescription}</p>
            
            <div className="flex items-center justify-between mt-6 text-sm text-gray-400">
              <div>{t.version} 1.0.0</div>
              <div className="flex items-center">
                {t.poweredBy}
                <span className="ml-2 text-purple-400">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M12 2L4.5 9.5L7 12l5-5 5 5 2.5-2.5L12 2zm0 20l7.5-7.5L17 12l-5 5-5-5-2.5 2.5L12 22z" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
