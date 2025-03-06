import React, { useState } from 'react';
import { Send, X, UserCircle, Trophy, TrendingUp, BarChart3, Clock, Package, Calendar } from 'lucide-react';
import { 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  ResponsiveContainer, Tooltip, Legend 
} from 'recharts';

// Main App Component
function App() {
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [metrics, setMetrics] = useState([]);

  // Function to handle when a player is selected from the chat
  const handlePlayerSelected = (player, metrics) => {
    setSelectedPlayer(player);
    setMetrics(metrics);
  };

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Chat Interface (Left Side) */}
      <ChatInterface onPlayerSelected={handlePlayerSelected} expanded={!selectedPlayer} />
      
      {/* Player Dashboard (Right Side) - Only visible when a player is selected */}
      {selectedPlayer && (
        <PlayerDashboard 
          player={selectedPlayer} 
          metrics={metrics}
          onClose={() => setSelectedPlayer(null)} 
        />
      )}
    </div>
  );
}

// Chat Interface Component
const ChatInterface = ({ onPlayerSelected, expanded }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [lastMessageWasSatisfactionQuestion, setLastMessageWasSatisfactionQuestion] = useState(false);
  
  // Initialize or get session ID
  React.useEffect(() => {
    if (!localStorage.getItem('chatSessionId')) {
      localStorage.setItem('chatSessionId', `session-${Date.now()}`);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    try {
      setIsLoading(true);
      
      // Check if this is responding to a satisfaction question
      const isSatisfactionResponse = lastMessageWasSatisfactionQuestion && 
        (input.toLowerCase().includes('não') || 
         input.toLowerCase().includes('refinar') || 
         input.toLowerCase().includes('outros') ||
         input.toLowerCase().includes('no') || 
         input.toLowerCase().includes('more') ||
         input.toLowerCase().includes('other') ||
         input.toLowerCase().includes('different'));
      
      console.log("Response to satisfaction question:", isSatisfactionResponse);
      
      setMessages(prev => [...prev, { text: input, sender: 'user' }]);

      const response = await fetch('http://localhost:5001/enhanced_search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          session_id: localStorage.getItem('chatSessionId') || `session-${Date.now()}`,
          query: input,
          is_follow_up: messages.length > 0,
          satisfaction: isSatisfactionResponse ? false : null
        }),
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
          data.response.toLowerCase().includes('refine your search') ||
          data.response.toLowerCase().includes('gostaria de refinar');
        
        setLastMessageWasSatisfactionQuestion(hasSatisfactionQuestion);
        console.log("Is satisfaction question:", hasSatisfactionQuestion);

        // Add the response to the chat
        setMessages(prev => [...prev, {
          text: data.response,
          sender: 'bot',
          showPlayerSelection: playersData.length > 0,
          players: playersData,
          isSatisfactionQuestion: hasSatisfactionQuestion
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
    // Extract metrics from the player object to display in the dashboard
    const playerMetrics = Object.entries(player.stats || {}).map(([key, value]) => ({
      name: formatMetricName(key),
      value: value,
      key: key
    }));

    setMessages(prev => [...prev, {
      text: `Mostrando detalhes de ${player.name}...`,
      sender: 'bot'
    }]);
    
    // Call the parent component's callback to show the player dashboard
    onPlayerSelected(player, playerMetrics);
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
    <div className={`flex flex-col ${expanded ? 'w-full' : 'w-1/2'} transition-all duration-300 bg-gray-900 border-r border-gray-700`}>
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
          <h1 className="text-xl font-bold text-white">KatenaScout AI</h1>
          <p className="text-xs text-green-200 opacity-80">Seu assistente de scouting inteligente</p>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900 bg-opacity-90 relative custom-scrollbar">
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
            <h2 className="text-2xl font-bold text-white mb-2">Olá, Técnico!</h2>
            <p className="text-gray-300 mb-6 max-w-md mx-auto">Descreva o tipo de jogador que você está buscando, e eu encontrarei as melhores opções para sua equipe.</p>
            
            <div className="bg-gray-800 rounded-lg p-5 mx-auto max-w-md text-left border-l-4 border-green-500">
              <p className="text-white mb-3 font-medium">Exemplos de busca:</p>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">1</span>
                  <span>"Preciso de um lateral ofensivo com boa capacidade de cruzamento"</span>
                </li>
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">2</span>
                  <span>"Busco zagueiros fortes no jogo aéreo e com boa saída de bola"</span>
                </li>
                <li className="flex items-start">
                  <span className="bg-green-700 text-white rounded-full flex items-center justify-center w-5 h-5 text-xs mr-2 mt-0.5">3</span>
                  <span>"Quero um atacante jovem com boa finalização e menos de 23 anos"</span>
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
                : 'bg-gradient-to-r from-gray-800 to-gray-900 text-gray-100 rounded-tl-none'
            }`}>
              <div className="whitespace-pre-wrap">{message.text}</div>
              
              {/* Player Selection Cards */}
              {message.showPlayerSelection && message.players && message.players.length > 0 && (
                <div className="mt-4 space-y-3">
                  <div className="text-sm text-gray-200 font-medium border-b border-gray-700 pb-2 mb-3">
                    Jogadores encontrados - Selecione para ver detalhes:
                  </div>
                  <div className="grid grid-cols-1 gap-3">
                    {message.players.map((player, idx) => (
                      <button
                        key={idx}
                        onClick={() => handlePlayerSelect(player)}
                        className="text-left p-3 rounded bg-gray-700 bg-opacity-50 hover:bg-gray-600 transition-colors flex items-center border border-gray-600 hover:border-green-500"
                      >
                        {/* Player simple avatar */}
                        <div className="w-10 h-10 bg-blue-900 rounded-full flex items-center justify-center text-white text-xs font-bold mr-3">
                          {player.positions?.[0]?.toUpperCase() || 'ST'}
                        </div>
                        
                        <div className="flex-1">
                          <div className="font-medium text-white">{formatPlayerName(player.name)}</div>
                          <div className="text-xs text-gray-300 flex items-center">
                            <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-1"></span>
                            {player.positions?.join(', ') || 'N/A'} • {player.age || '?'} anos • {player.club || 'Clube desconhecido'}
                          </div>
                        </div>
                        
                        {/* Position indicator instead of score */}
                        <div className="ml-2 w-9 h-9 flex-shrink-0 rounded-full bg-gradient-to-b from-blue-500 to-blue-700 flex items-center justify-center text-white font-bold text-sm">
                          {player.positions?.[0]?.toUpperCase() || 'ST'}
                        </div>
                      </button>
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
                
                <div className="text-green-300 font-medium">Analisando jogadores...</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t border-gray-700 p-4 bg-gray-900">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Descreva o tipo de jogador que você procura..."
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
const PlayerDashboard = ({ player, metrics, onClose }) => {
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

  // Get player position in a more readable format
  const positionDisplay = player.positions?.map(pos => {
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
    const data = prepareAllRadarData(metrics);
    
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
    
    // Fixed height container instead of aspect ratio to prevent layout bugs
    return (
      <div className="w-full h-[450px]">
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
              name={formatPlayerName(player.name)}
              dataKey="value"
              stroke="#10B981"
              fill="#10B981"
              fillOpacity={0.6}
              dot={{ fill: '#10B981', strokeWidth: 2, r: 4, stroke: '#FFFFFF' }}
              isAnimationActive={true}
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
      </div>
    );
  };

  // Player photo URL - use a placeholder if not available
  const getPlayerImageUrl = (player) => {
    // First try photoUrl if it exists
    if (player.photoUrl) {
      return player.photoUrl;
    }
    
    // Try to use player ID for the image
    const playerId = player.wyId || player.id;
    if (playerId) {
      // Try to use the backend API to get player image (assuming it's implemented)
      return `http://localhost:5001/player-image/${playerId}`;
    }
    
    // Fallback to UI Avatars API
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
  };
  
  const playerPhotoUrl = getPlayerImageUrl(player);

  // We no longer display player scores based on requirements

  return (
    <div className="w-1/2 h-full bg-gray-950 flex flex-col overflow-hidden">
      {/* Header with close button */}
      <div className="bg-gray-800 p-4 flex justify-between items-center border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          <div className="w-8 h-8 mr-3 text-green-500 font-bold">⚽</div>
          Dashboard do Jogador
        </h2>
        <button onClick={onClose} className="text-gray-400 hover:text-white">
          <X size={24} />
        </button>
      </div>

      {/* Player Overview Card */}
      <div className="p-6 overflow-y-auto custom-scrollbar">
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
            <div className="relative flex p-6">
              {/* Player Photo - Larger and more prominent */}
              <div className="mr-6">
                <div className="w-36 h-44 overflow-hidden rounded-lg border-4 border-white bg-gray-800 shadow-xl relative">
                  <img 
                    src={playerPhotoUrl} 
                    alt={player.name} 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.onerror = null; 
                      e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
                    }}
                  />
                  
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
                <div className="flex items-center">
                  <div className="mr-3 p-1 bg-white bg-opacity-20 rounded">
                    <img 
                      src={`https://ui-avatars.com/api/?name=${encodeURIComponent(player.club?.substring(0,2) || 'FC')}&background=111827&color=fff&size=20&font-size=0.5&bold=true`}
                      alt="Club"
                      className="w-6 h-6 rounded-full"
                    />
                  </div>
                  <h1 className="text-3xl font-bold">{formatPlayerName(player.name)}</h1>
                </div>
                
                <div className="flex items-center mt-2 mb-4">
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.age} anos</span>
                  </div>
                  <div className="h-4 border-r border-white border-opacity-30 mx-3"></div>
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.height || '--'} cm</span>
                  </div>
                  <div className="h-4 border-r border-white border-opacity-30 mx-3"></div>
                  <div className="flex items-center bg-white bg-opacity-10 rounded-full px-3 py-1">
                    <span className="text-sm font-medium">{player.weight || '--'} kg</span>
                  </div>
                </div>
                
                {/* Contract info in a modern card */}
                <div className="bg-black bg-opacity-30 backdrop-blur-sm rounded-lg p-4 mt-2 border border-white border-opacity-20">
                  <h3 className="text-sm uppercase text-green-300 mb-3 flex items-center">
                    <Trophy className="mr-2" size={14} />
                    Informações Contratuais
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="flex items-center">
                        <Package className="mr-2 text-blue-300" size={14} />
                        <span className="text-sm text-gray-300">Clube Atual</span>
                      </div>
                      <div className="font-medium">{player.club || "Informação indisponível"}</div>
                    </div>
                    <div>
                      <div className="flex items-center">
                        <Calendar className="mr-2 text-blue-300" size={14} />
                        <span className="text-sm text-gray-300">Contrato até</span>
                      </div>
                      <div className="font-medium">{player.contractUntil || "Informação indisponível"}</div>
                    </div>
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
            <div className="grid grid-cols-2 gap-x-10 gap-y-2">
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
      </div>
    </div>
  );
};

export default App;