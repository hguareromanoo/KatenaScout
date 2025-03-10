import React, { useState, useEffect } from 'react';
import { 
  UserCircle, 
  Share2, 
  Calendar, 
  MapPin,
  BarChart2, 
  Award, 
  Flag, 
  Video,
  Heart,
  ChevronRight,
  ChevronLeft,
  Download,
  ExternalLink
} from 'lucide-react';

const PlayerCompletePage = ({ player, onClose, isPlayerFavorite, toggleFavorite }) => {
  // Get translations based on user's language
  const [translations, setTranslations] = useState({});
  
  useEffect(() => {
    // Get user's language preference from localStorage
    const userLanguage = localStorage.getItem('language') || 'english';
    
    // Load translations
    const allTranslations = {
      english: {
        playerProfile: "Player Profile",
        overview: "Overview",
        detailedStats: "Detailed Stats",
        heatmaps: "Heatmaps",
        videos: "Videos",
        keyPerformanceMetrics: "Key Performance Metrics",
        metrics: "Metrics",
        years: "years",
        currentClub: "Current club",
        contractUntil: "Contract until",
        rating: "Rating",
        playerInformation: "Player Information",
        height: "Height",
        weight: "Weight",
        nationality: "Nationality",
        preferredFoot: "Preferred Foot",
        playingStyle: "Playing Style",
        strengths: "Strengths",
        areasToImprove: "Areas to Improve",
        similarPlayers: "Similar Players",
        similarity: "Similarity",
        completeStatistics: "Complete Statistics",
        attacking: "Attacking",
        passing: "Passing",
        defending: "Defending",
        possession: "Possession",
        exportCompleteStats: "Export Complete Stats",
        percentileRanks: "Percentile Ranks",
        performanceHeatmaps: "Performance Heatmaps",
        tacticalAnalysis: "Tactical Analysis",
        positionalTendencies: "Positional Tendencies",
        tacticalContributions: "Tactical Contributions",
        defensiveResponsibilities: "Defensive Responsibilities",
        setPieceInvolvement: "Set-Piece Involvement",
        performanceVideos: "Performance Videos",
        noVideosAvailable: "No Videos Available",
        noVideosMessage: "There are currently no performance videos available for this player. Check back later or subscribe to receive updates when new content is added.",
        scoutSimilarPlayers: "Scout Similar Players",
        requestVideoAnalysis: "Request Video Analysis",
        requestVideoMessage: "As a professional scout, you can request specialized video analysis for this player. Our analysts will compile highlights and tactical breakdowns.",
        submitAnalysisRequest: "Submit Analysis Request",
        downloadFullHeatmapReport: "Download Full Heatmap Report",
        unknown: "Unknown",
        right: "Right"
      },
      portuguese: {
        playerProfile: "Perfil de Jogador",
        overview: "Visão Geral",
        detailedStats: "Estatísticas Detalhadas",
        heatmaps: "Mapas de Calor",
        videos: "Vídeos",
        keyPerformanceMetrics: "Métricas Chave de Desempenho",
        metrics: "Métricas",
        years: "anos",
        currentClub: "Clube atual",
        contractUntil: "Contrato até",
        rating: "Pontuação",
        playerInformation: "Informações do Jogador",
        height: "Altura",
        weight: "Peso",
        nationality: "Nacionalidade",
        preferredFoot: "Pé Preferido",
        playingStyle: "Estilo de Jogo",
        strengths: "Pontos Fortes",
        areasToImprove: "Áreas para Melhorar",
        similarPlayers: "Jogadores Similares",
        similarity: "Similaridade",
        completeStatistics: "Estatísticas Completas",
        attacking: "Ataque",
        passing: "Passe",
        defending: "Defesa",
        possession: "Posse",
        exportCompleteStats: "Exportar Estatísticas Completas",
        percentileRanks: "Classificações Percentuais",
        performanceHeatmaps: "Mapas de Calor de Desempenho",
        tacticalAnalysis: "Análise Tática",
        positionalTendencies: "Tendências Posicionais",
        tacticalContributions: "Contribuições Táticas",
        defensiveResponsibilities: "Responsabilidades Defensivas",
        setPieceInvolvement: "Envolvimento em Bolas Paradas",
        performanceVideos: "Vídeos de Desempenho",
        noVideosAvailable: "Nenhum Vídeo Disponível",
        noVideosMessage: "Não há vídeos de desempenho disponíveis para este jogador atualmente. Verifique mais tarde ou se inscreva para receber atualizações quando novo conteúdo for adicionado.",
        scoutSimilarPlayers: "Buscar Jogadores Similares",
        requestVideoAnalysis: "Solicitar Análise em Vídeo",
        requestVideoMessage: "Como olheiro profissional, você pode solicitar análise de vídeo especializada para este jogador. Nossos analistas irão compilar destaques e análises táticas.",
        submitAnalysisRequest: "Enviar Solicitação de Análise",
        downloadFullHeatmapReport: "Baixar Relatório Completo de Mapas de Calor",
        unknown: "Desconhecido",
        right: "Direito"
      },
      spanish: {
        playerProfile: "Perfil del Jugador",
        overview: "Vista General",
        detailedStats: "Estadísticas Detalladas",
        heatmaps: "Mapas de Calor",
        videos: "Videos",
        keyPerformanceMetrics: "Métricas Clave de Rendimiento",
        metrics: "Métricas",
        years: "años",
        currentClub: "Club actual",
        contractUntil: "Contrato hasta",
        rating: "Puntuación",
        playerInformation: "Información del Jugador",
        height: "Altura",
        weight: "Peso",
        nationality: "Nacionalidad",
        preferredFoot: "Pie Preferido",
        playingStyle: "Estilo de Juego",
        strengths: "Fortalezas",
        areasToImprove: "Áreas para Mejorar",
        similarPlayers: "Jugadores Similares",
        similarity: "Similitud",
        completeStatistics: "Estadísticas Completas",
        attacking: "Ataque",
        passing: "Pase",
        defending: "Defensa",
        possession: "Posesión",
        exportCompleteStats: "Exportar Estadísticas Completas",
        percentileRanks: "Clasificaciones Percentiles",
        performanceHeatmaps: "Mapas de Calor de Rendimiento",
        tacticalAnalysis: "Análisis Táctico",
        positionalTendencies: "Tendencias Posicionales",
        tacticalContributions: "Contribuciones Tácticas",
        defensiveResponsibilities: "Responsabilidades Defensivas",
        setPieceInvolvement: "Participación en Balones Parados",
        performanceVideos: "Videos de Rendimiento",
        noVideosAvailable: "No Hay Videos Disponibles",
        noVideosMessage: "Actualmente no hay videos de rendimiento disponibles para este jugador. Vuelva más tarde o suscríbase para recibir actualizaciones cuando se añada nuevo contenido.",
        scoutSimilarPlayers: "Buscar Jugadores Similares",
        requestVideoAnalysis: "Solicitar Análisis de Video",
        requestVideoMessage: "Como ojeador profesional, puede solicitar análisis de video especializado para este jugador. Nuestros analistas compilarán destacados y análisis tácticos.",
        submitAnalysisRequest: "Enviar Solicitud de Análisis",
        downloadFullHeatmapReport: "Descargar Informe Completo de Mapas de Calor",
        unknown: "Desconocido",
        right: "Derecho"
      },
      bulgarian: {
        playerProfile: "Профил на играча",
        overview: "Общ преглед",
        detailedStats: "Подробни статистики",
        heatmaps: "Топлинни карти",
        videos: "Видеоклипове",
        keyPerformanceMetrics: "Ключови показатели за ефективност",
        metrics: "Показатели",
        years: "години",
        currentClub: "Настоящ клуб",
        contractUntil: "Договор до",
        rating: "Рейтинг",
        playerInformation: "Информация за играча",
        height: "Височина",
        weight: "Тегло",
        nationality: "Националност",
        preferredFoot: "Предпочитан крак",
        playingStyle: "Стил на игра",
        strengths: "Силни страни",
        areasToImprove: "Области за подобрение",
        similarPlayers: "Подобни играчи",
        similarity: "Сходство",
        completeStatistics: "Пълни статистики",
        attacking: "Атака",
        passing: "Подаване",
        defending: "Защита",
        possession: "Владение",
        exportCompleteStats: "Експортиране на пълни статистики",
        percentileRanks: "Процентилни рангове",
        performanceHeatmaps: "Топлинни карти на представянето",
        tacticalAnalysis: "Тактически анализ",
        positionalTendencies: "Позиционни тенденции",
        tacticalContributions: "Тактически принос",
        defensiveResponsibilities: "Защитни отговорности",
        setPieceInvolvement: "Участие при статични положения",
        performanceVideos: "Видеоклипове на представянето",
        noVideosAvailable: "Няма налични видеоклипове",
        noVideosMessage: "В момента няма налични видеоклипове за този играч. Проверете по-късно или се абонирайте, за да получавате актуализации, когато се добави ново съдържание.",
        scoutSimilarPlayers: "Търсене на подобни играчи",
        requestVideoAnalysis: "Заявка за видео анализ",
        requestVideoMessage: "Като професионален скаут можете да заявите специализиран видео анализ за този играч. Нашите анализатори ще компилират моменти и тактически разбор.",
        submitAnalysisRequest: "Изпратете заявка за анализ",
        downloadFullHeatmapReport: "Изтеглете пълен доклад с топлинни карти",
        unknown: "Неизвестно",
        right: "Десен"
      }
    };
    
    setTranslations(allTranslations[userLanguage] || allTranslations.english);
  }, []);
  
  // If translations aren't loaded yet, use English as fallback
  const t = translations.playerProfile ? translations : {
    playerProfile: "Player Profile",
    overview: "Overview",
    detailedStats: "Detailed Stats",
    heatmaps: "Heatmaps",
    videos: "Videos",
    keyPerformanceMetrics: "Key Performance Metrics",
    unknown: "Unknown"
  };
  const [activeTab, setActiveTab] = useState('overview');
  const [currentHeatMapIndex, setCurrentHeatMapIndex] = useState(0);

  // Mock data for metrics by position
  const positionMetrics = {
    cb: [
      { name: 'Defensive Duels Won', value: 68, avg: 59, unit: '%' },
      { name: 'Aerial Duels Won', value: 64, avg: 52, unit: '%' },
      { name: 'Interceptions', value: 6.8, avg: 5.3, unit: 'per 90' },
      { name: 'Sliding Tackles', value: 2.1, avg: 1.7, unit: 'per 90' },
      { name: 'Ball Recoveries', value: 8.3, avg: 6.2, unit: 'per 90' },
      { name: 'Progressive Passes', value: 9.3, avg: 6.5, unit: 'per 90' }
    ],
    cmf: [
      { name: 'Pass Accuracy', value: 88, avg: 82, unit: '%' },
      { name: 'Progressive Passes', value: 12.4, avg: 8.7, unit: 'per 90' },
      { name: 'Passes to Final Third', value: 9.8, avg: 7.1, unit: 'per 90' },
      { name: 'Key Passes', value: 2.3, avg: 1.8, unit: 'per 90' },
      { name: 'Ball Recoveries', value: 7.2, avg: 5.9, unit: 'per 90' },
      { name: 'Successful Dribbles', value: 2.7, avg: 1.9, unit: 'per 90' }
    ],
    cf: [
      { name: 'Goals per 90', value: 0.62, avg: 0.48, unit: '' },
      { name: 'xG per 90', value: 0.58, avg: 0.42, unit: '' },
      { name: 'Shots on Target', value: 1.8, avg: 1.4, unit: 'per 90' },
      { name: 'Shot Conversion', value: 19, avg: 14, unit: '%' },
      { name: 'Aerial Duels Won', value: 53, avg: 42, unit: '%' },
      { name: 'Touches in Box', value: 6.2, avg: 4.8, unit: 'per 90' }
    ],
    gk: [
      { name: 'Save Percentage', value: 72, avg: 68, unit: '%' },
      { name: 'xG Prevented', value: 0.21, avg: 0.12, unit: 'per 90' },
      { name: 'Successful Exits', value: 2.3, avg: 1.8, unit: 'per 90' },
      { name: 'Successful Long Passes', value: 62, avg: 54, unit: '%' },
      { name: 'Penalty Save Rate', value: 24, avg: 18, unit: '%' },
      { name: 'Clean Sheets', value: 0.36, avg: 0.29, unit: 'per 90' }
    ]
  };

  // Generate some basic mock heatmap data for different positions
  const heatMaps = [
    {
      title: "Defensive Actions",
      description: "Where the player performs defensive actions like tackles and interceptions",
      imageUrl: `https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScuaH_pIGwM7G7SUZeOJQp1I_fBQEDZHgb3g&usqp=CAU`
    },
    {
      title: "Attacking Actions",
      description: "Distribution of offensive contributions across the pitch",
      imageUrl: `https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-m1kU1-DZ2BxarE3QJMTWp7JZh4BWgfp18g&usqp=CAU`
    },
    {
      title: "Ball Progression",
      description: "How the player moves the ball forward through passing and carrying",
      imageUrl: `https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX9zrqScZ9gTAWJOeEF-9FdS07JDBPxF1NcQ&usqp=CAU`
    }
  ];

  // Format player info
  const formatPlayerName = (name) => {
    if (!name) return '';
    return name.replace(/([A-Z])/g, ' $1').trim()
      .replace(/\s+/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const getPositionName = (pos) => {
    const posMap = {
      'cb': 'Center Back',
      'lb': 'Left Back',
      'rb': 'Right Back',
      'dmf': 'Defensive Midfielder',
      'cmf': 'Central Midfielder',
      'amf': 'Attacking Midfielder',
      'lw': 'Left Winger',
      'rw': 'Right Winger',
      'cf': 'Center Forward',
      'gk': 'Goalkeeper',
    };
    return posMap[pos] || pos;
  };

  // Get player's primary position
  const primaryPosition = player.positions?.[0] || 'cmf';
  
  // Get metrics for player's primary position
  const metrics = positionMetrics[primaryPosition] || positionMetrics.cmf;

  // Navigation for heatmaps
  const nextHeatMap = () => {
    setCurrentHeatMapIndex((prev) => (prev + 1) % heatMaps.length);
  };

  const prevHeatMap = () => {
    setCurrentHeatMapIndex((prev) => (prev - 1 + heatMaps.length) % heatMaps.length);
  };

  return (
    <div className="flex-1 h-full bg-gray-950 flex flex-col overflow-hidden">
      {/* Header with player name and actions */}
      <div className="bg-gray-800 p-4 flex justify-between items-center border-b border-gray-700">
        <div className="flex items-center">
          <button 
            onClick={onClose}
            className="mr-3 p-2 rounded-full bg-gray-700 text-gray-300 hover:bg-gray-600"
          >
            <ChevronLeft size={20} />
          </button>
          <h2 className="text-xl font-bold text-white flex items-center">
            {t.playerProfile}
          </h2>
        </div>
        <div className="flex items-center space-x-2">
          {/* Share button */}
          <button className="p-2 rounded-full bg-gray-700 text-gray-300 hover:bg-gray-600">
            <Share2 size={20} />
          </button>
          
          {/* Favorite button */}
          <button 
            onClick={() => toggleFavorite(player)}
            className={`p-2 rounded-full transition-colors ${
              isPlayerFavorite 
                ? 'bg-red-600 text-white hover:bg-red-700' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            <Heart size={20} fill={isPlayerFavorite ? "white" : "none"} />
          </button>
        </div>
      </div>

      {/* Player Banner */}
      <div className="bg-gradient-to-r from-green-900 to-blue-900 py-6 px-8 relative overflow-hidden">
        {/* Soccer field background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="w-full h-full border border-white"></div>
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[60%] h-[70%] border border-white rounded-full"></div>
          <div className="absolute left-1/2 -translate-x-1/2 w-0.5 h-full bg-white opacity-50"></div>
        </div>
        
        <div className="flex relative z-10">
          {/* Player Photo */}
          <div className="h-36 w-36 rounded-xl overflow-hidden bg-gray-800 border-4 border-white shadow-xl mr-6 flex-shrink-0">
            <img 
              src={player.photoUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`}
              alt={player.name}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.target.onerror = null; 
                e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(player.name)}&background=0D8ABC&color=fff&size=256`;
              }}
            />
          </div>
          
          {/* Player Info */}
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-white mb-2">{formatPlayerName(player.name)}</h1>
            
            <div className="flex items-center space-x-4 mb-3">
              <div className="bg-white bg-opacity-20 rounded-full px-3 py-1 text-sm text-white">
                {player.positions?.map(pos => getPositionName(pos)).join(' / ')}
              </div>
              <div className="bg-white bg-opacity-20 rounded-full px-3 py-1 text-sm text-white flex items-center">
                <Calendar className="mr-1" size={14} />
                {player.age} years
              </div>
              <div className="bg-white bg-opacity-20 rounded-full px-3 py-1 text-sm text-white flex items-center">
                <MapPin className="mr-1" size={14} />
                {player.country || 'Unknown'}
              </div>
            </div>
            
            <div className="flex items-center">
              <div className="mr-4">
                <span className="text-gray-300 text-sm">Current club</span>
                <div className="text-white font-medium">{player.club || 'Unknown'}</div>
              </div>
              <div className="mr-4">
                <span className="text-gray-300 text-sm">Contract until</span>
                <div className="text-white font-medium">{player.contractUntil || 'Unknown'}</div>
              </div>
              <div className="flex items-center bg-green-700 bg-opacity-60 rounded-full px-3 py-1 ml-auto">
                <span className="text-white font-bold text-lg mr-1">{player.score || 85}</span>
                <span className="text-white text-xs">Rating</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="flex overflow-x-auto">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-6 py-3 font-medium text-sm ${
              activeTab === 'overview'
                ? 'text-white border-b-2 border-green-500'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {t.overview}
          </button>
          <button
            onClick={() => setActiveTab('stats')}
            className={`px-6 py-3 font-medium text-sm ${
              activeTab === 'stats'
                ? 'text-white border-b-2 border-green-500'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {t.detailedStats}
          </button>
          <button
            onClick={() => setActiveTab('heatmaps')}
            className={`px-6 py-3 font-medium text-sm ${
              activeTab === 'heatmaps'
                ? 'text-white border-b-2 border-green-500'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {t.heatmaps}
          </button>
          <button
            onClick={() => setActiveTab('videos')}
            className={`px-6 py-3 font-medium text-sm ${
              activeTab === 'videos'
                ? 'text-white border-b-2 border-green-500'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {t.videos}
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Key Metrics */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700 flex justify-between items-center">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <Award className="mr-2 text-green-500" size={20} />
                  {t.keyPerformanceMetrics}
                </h3>
                <span className="text-sm text-gray-400">{getPositionName(primaryPosition)} {t.metrics}</span>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {metrics.map((metric, index) => (
                    <div key={index} className="bg-gray-750 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-gray-300">{metric.name}</span>
                        <span className={`text-lg font-bold ${
                          metric.value > metric.avg ? 'text-green-500' : 'text-yellow-500'
                        }`}>
                          {metric.value}{metric.unit}
                        </span>
                      </div>
                      
                      {/* Progress bar compared to average */}
                      <div className="h-2 bg-gray-700 rounded-full overflow-hidden mt-2">
                        <div 
                          className="h-full bg-gradient-to-r from-blue-500 to-green-500" 
                          style={{ width: `${Math.min((metric.value / (metric.avg * 1.5)) * 100, 100)}%` }}
                        ></div>
                      </div>
                      <div className="flex justify-between mt-1 text-xs text-gray-400">
                        <span>League avg: {metric.avg}{metric.unit}</span>
                        <span>{metric.value > metric.avg 
                          ? `+${((metric.value - metric.avg) / metric.avg * 100).toFixed(0)}%` 
                          : `${((metric.value - metric.avg) / metric.avg * 100).toFixed(0)}%`}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Bio & Description */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <UserCircle className="mr-2 text-green-500" size={20} />
                  Player Profile
                </h3>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-white font-medium mb-3">Player Information</h4>
                    
                    <div className="space-y-3">
                      <div className="grid grid-cols-2 gap-2">
                        <div className="bg-gray-750 p-3 rounded">
                          <span className="text-gray-400 text-sm">Height</span>
                          <div className="text-white">{player.height || 180} cm</div>
                        </div>
                        <div className="bg-gray-750 p-3 rounded">
                          <span className="text-gray-400 text-sm">Weight</span>
                          <div className="text-white">{player.weight || 75} kg</div>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2">
                        <div className="bg-gray-750 p-3 rounded">
                          <span className="text-gray-400 text-sm">Nationality</span>
                          <div className="text-white">{player.country || 'Unknown'}</div>
                        </div>
                        <div className="bg-gray-750 p-3 rounded">
                          <span className="text-gray-400 text-sm">Preferred Foot</span>
                          <div className="text-white">{player.foot || 'Right'}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-white font-medium mb-3">Playing Style</h4>
                    <p className="text-gray-300">
                      {player.description || `${formatPlayerName(player.name)} is a ${getPositionName(primaryPosition).toLowerCase()} known for ${
                        primaryPosition === 'cb' ? 'strong defensive abilities and aerial presence' : 
                        primaryPosition === 'cmf' ? 'excellent passing range and vision' :
                        primaryPosition === 'cf' ? 'clinical finishing and movement in the box' :
                        primaryPosition === 'gk' ? 'quick reflexes and commanding presence' :
                        'technical abilities and tactical awareness'
                      }.`}
                    </p>
                    
                    <div className="mt-4 grid grid-cols-2 gap-2">
                      <div className="bg-gray-750 p-3 rounded">
                        <span className="text-gray-400 text-sm">Strengths</span>
                        <div className="text-white text-sm mt-1">
                          • {primaryPosition === 'cb' ? 'Aerial duels' : 
                            primaryPosition === 'cmf' ? 'Vision & passing' :
                            primaryPosition === 'cf' ? 'Finishing' :
                            primaryPosition === 'gk' ? 'Shot stopping' : 'Technical ability'}
                          <br />
                          • {primaryPosition === 'cb' ? 'Positioning' : 
                            primaryPosition === 'cmf' ? 'Ball control' :
                            primaryPosition === 'cf' ? 'Movement' :
                            primaryPosition === 'gk' ? 'Aerial ability' : 'Decision making'}
                        </div>
                      </div>
                      <div className="bg-gray-750 p-3 rounded">
                        <span className="text-gray-400 text-sm">Areas to Improve</span>
                        <div className="text-white text-sm mt-1">
                          • {primaryPosition === 'cb' ? 'Forward passing' : 
                            primaryPosition === 'cmf' ? 'Defensive workrate' :
                            primaryPosition === 'cf' ? 'Defensive contribution' :
                            primaryPosition === 'gk' ? 'Distribution' : 'Consistency'}
                          <br />
                          • {primaryPosition === 'cb' ? 'Speed' : 
                            primaryPosition === 'cmf' ? 'Goal scoring' :
                            primaryPosition === 'cf' ? 'Aerial ability' :
                            primaryPosition === 'gk' ? 'Footwork' : 'Physical strength'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Similar Players */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <UserCircle className="mr-2 text-green-500" size={20} />
                  Similar Players
                </h3>
              </div>
              
              <div className="p-4 overflow-x-auto">
                <div className="flex space-x-4 pb-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="bg-gray-750 rounded-lg p-4 min-w-[220px]">
                      <div className="flex items-center">
                        <div className="w-12 h-12 rounded-full bg-gray-700 mr-3 flex-shrink-0 flex items-center justify-center overflow-hidden">
                          <img 
                            src={`https://ui-avatars.com/api/?name=Player${i}&background=0D8ABC&color=fff&size=128`}
                            alt={`Similar Player ${i}`}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <div>
                          <div className="text-white font-medium">Player Name {i}</div>
                          <div className="text-gray-400 text-sm">{getPositionName(primaryPosition)}</div>
                        </div>
                        <div className="ml-auto bg-green-800 bg-opacity-40 rounded-full w-8 h-8 flex items-center justify-center">
                          <span className="text-green-400 text-xs">{85 + i}</span>
                        </div>
                      </div>
                      <div className="mt-3 pt-3 border-t border-gray-700 flex justify-between text-sm">
                        <span className="text-gray-400">Similarity</span>
                        <span className="text-green-400">{90 - (i * 4)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Stats Tab */}
        {activeTab === 'stats' && (
          <div className="space-y-6">
            {/* Comprehensive Stats Table */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <BarChart2 className="mr-2 text-green-500" size={20} />
                  Complete Statistics
                </h3>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-1">
                  {/* Generate a bunch of stats for the demo */}
                  {[
                    { category: 'Attacking', stats: [
                      { name: 'Goals', value: '12' },
                      { name: 'Assists', value: '8' },
                      { name: 'xG', value: '10.8' },
                      { name: 'xA', value: '7.2' },
                      { name: 'Shots', value: '72' },
                      { name: 'Shots on Target', value: '28' },
                    ]},
                    { category: 'Passing', stats: [
                      { name: 'Pass Accuracy', value: '88%' },
                      { name: 'Progressive Passes', value: '124' },
                      { name: 'Passes to Final Third', value: '98' },
                      { name: 'Key Passes', value: '42' },
                      { name: 'Crosses', value: '86' },
                      { name: 'Through Passes', value: '24' },
                    ]},
                    { category: 'Defending', stats: [
                      { name: 'Tackles', value: '62' },
                      { name: 'Interceptions', value: '48' },
                      { name: 'Clearances', value: '104' },
                      { name: 'Duels Won', value: '58%' },
                      { name: 'Aerial Duels Won', value: '64%' },
                      { name: 'Errors Leading to Shot', value: '2' },
                    ]},
                    { category: 'Possession', stats: [
                      { name: 'Touches', value: '1842' },
                      { name: 'Successful Dribbles', value: '38' },
                      { name: 'Progressive Carries', value: '76' },
                      { name: 'Dispossessed', value: '42' },
                      { name: 'Miscontrols', value: '28' },
                      { name: 'Ball Recoveries', value: '112' },
                    ]}
                  ].map((section, idx) => (
                    <div key={idx} className="mb-6">
                      <h4 className="text-white font-medium mb-3 pb-2 border-b border-gray-700">{section.category}</h4>
                      <div className="space-y-2">
                        {section.stats.map((stat, i) => (
                          <div key={i} className="flex justify-between items-center text-sm py-1">
                            <span className="text-gray-300">{stat.name}</span>
                            <span className="text-white font-medium">{stat.value}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="mt-4 text-center">
                  <button className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white rounded-lg inline-flex items-center">
                    <Download className="mr-2" size={16} />
                    Export Complete Stats
                  </button>
                </div>
              </div>
            </div>
            
            {/* Percentile Ranks */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <BarChart2 className="mr-2 text-green-500" size={20} />
                  Percentile Ranks
                </h3>
              </div>
              
              <div className="p-6">
                <div className="space-y-4">
                  {['Attacking', 'Passing', 'Defending', 'Possession'].map((category, idx) => (
                    <div key={idx}>
                      <h4 className="text-white font-medium mb-3">{category}</h4>
                      <div className="space-y-3">
                        {[...Array(3)].map((_, i) => {
                          const percent = Math.floor(Math.random() * 60) + 40;
                          return (
                            <div key={i} className="mb-2">
                              <div className="flex justify-between text-sm mb-1">
                                <span className="text-gray-400">{
                                  category === 'Attacking' ? ['Goals', 'xG', 'Shots on Target'][i] :
                                  category === 'Passing' ? ['Pass Accuracy', 'Key Passes', 'Progressive Passes'][i] :
                                  category === 'Defending' ? ['Tackles', 'Interceptions', 'Aerial Duels'][i] :
                                  ['Ball Control', 'Progressive Carries', 'Ball Recoveries'][i]
                                }</span>
                                <span className={`font-medium ${
                                  percent > 80 ? 'text-green-400' : percent > 60 ? 'text-blue-400' : 'text-yellow-400'
                                }`}>{percent}th</span>
                              </div>
                              <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                                <div 
                                  className={`h-full ${
                                    percent > 80 ? 'bg-green-500' : percent > 60 ? 'bg-blue-500' : 'bg-yellow-500'
                                  }`}
                                  style={{ width: `${percent}%` }}
                                ></div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="mt-6 text-center text-sm text-gray-400">
                  Percentiles compared to other {getPositionName(primaryPosition).toLowerCase()} in top 5 European leagues
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Heatmaps Tab */}
        {activeTab === 'heatmaps' && (
          <div className="space-y-6">
            {/* Heatmaps Viewer */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <MapPin className="mr-2 text-green-500" size={20} />
                  Performance Heatmaps
                </h3>
              </div>
              
              <div className="p-6">
                <div className="relative mb-4">
                  <h4 className="text-white font-medium mb-2">{heatMaps[currentHeatMapIndex].title}</h4>
                  <p className="text-gray-400 text-sm mb-4">{heatMaps[currentHeatMapIndex].description}</p>
                  
                  <div className="relative">
                    <div className="aspect-video w-full bg-gray-900 rounded-lg overflow-hidden flex items-center justify-center">
                      <img 
                        src={heatMaps[currentHeatMapIndex].imageUrl} 
                        alt={heatMaps[currentHeatMapIndex].title}
                        className="max-w-full max-h-full"
                      />
                    </div>
                    
                    {/* Navigation buttons */}
                    <button 
                      onClick={prevHeatMap}
                      className="absolute left-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black bg-opacity-50 text-white hover:bg-opacity-70"
                    >
                      <ChevronLeft size={20} />
                    </button>
                    <button 
                      onClick={nextHeatMap}
                      className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black bg-opacity-50 text-white hover:bg-opacity-70"
                    >
                      <ChevronRight size={20} />
                    </button>
                    
                    {/* Pagination dots */}
                    <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex space-x-2">
                      {heatMaps.map((_, index) => (
                        <button 
                          key={index} 
                          onClick={() => setCurrentHeatMapIndex(index)}
                          className={`w-2 h-2 rounded-full ${currentHeatMapIndex === index ? 'bg-white' : 'bg-gray-500'}`}
                        />
                      ))}
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 text-center">
                  <div className="text-gray-400 text-sm mb-3">
                    View more detailed heatmaps and analysis
                  </div>
                  <button className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white rounded-lg inline-flex items-center">
                    <Download className="mr-2" size={16} />
                    Download Full Heatmap Report
                  </button>
                </div>
              </div>
            </div>
            
            {/* Tactical Analysis */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <Flag className="mr-2 text-green-500" size={20} />
                  Tactical Analysis
                </h3>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gray-750 rounded-lg p-4">
                    <h4 className="text-white font-medium mb-3 flex items-center">
                      <Flag className="mr-2 text-blue-400" size={16} />
                      Positional Tendencies
                    </h4>
                    <p className="text-gray-300 text-sm">
                      Analysis shows the player tends to operate primarily in the {
                        primaryPosition === 'cb' ? 'central defensive area, occasionally stepping into midfield to initiate attacks' : 
                        primaryPosition === 'cmf' ? 'central areas of the pitch, with a tendency to drift toward the right half-space when attacking' :
                        primaryPosition === 'cf' ? 'central attacking areas, often dropping between the lines to receive the ball' :
                        primaryPosition === 'gk' ? 'penalty area, with occasional advances to sweep behind the defensive line' :
                        'central areas with freedom to roam across the final third'
                      }.
                    </p>
                  </div>
                  
                  <div className="bg-gray-750 rounded-lg p-4">
                    <h4 className="text-white font-medium mb-3 flex items-center">
                      <Flag className="mr-2 text-green-400" size={16} />
                      Tactical Contributions
                    </h4>
                    <p className="text-gray-300 text-sm">
                      Key tactical contributions include {
                        primaryPosition === 'cb' ? 'progressive passing from deep positions and aerial dominance in defensive situations' : 
                        primaryPosition === 'cmf' ? 'ball retention under pressure and progressive passing through defensive lines' :
                        primaryPosition === 'cf' ? 'movement to create space for teammates and clinical finishing in the penalty area' :
                        primaryPosition === 'gk' ? 'commanding the penalty area during set pieces and initiating attacks with accurate distribution' :
                        'creating space with intelligent movement and linking play between midfield and attack'
                      }.
                    </p>
                  </div>
                  
                  <div className="bg-gray-750 rounded-lg p-4">
                    <h4 className="text-white font-medium mb-3 flex items-center">
                      <Flag className="mr-2 text-purple-400" size={16} />
                      Defensive Responsibilities
                    </h4>
                    <p className="text-gray-300 text-sm">
                      Defensively, the player {
                        primaryPosition === 'cb' ? 'excels in one-on-one situations and shows excellent positioning to intercept passes' : 
                        primaryPosition === 'cmf' ? 'contributes through tactical pressing and tracking runners from midfield' :
                        primaryPosition === 'cf' ? 'initiates the press from the front and helps screen passing lanes to defensive midfielders' :
                        primaryPosition === 'gk' ? 'organizes the defensive line effectively and excels in one-on-one situations' :
                        'works diligently to track back and maintain defensive shape when out of possession'
                      }.
                    </p>
                  </div>
                  
                  <div className="bg-gray-750 rounded-lg p-4">
                    <h4 className="text-white font-medium mb-3 flex items-center">
                      <Flag className="mr-2 text-red-400" size={16} />
                      Set-Piece Involvement
                    </h4>
                    <p className="text-gray-300 text-sm">
                      During set-pieces, the player {
                        primaryPosition === 'cb' ? 'targets the near post on attacking corners and defends the central zone on defensive set-pieces' : 
                        primaryPosition === 'cmf' ? 'often takes corner kicks and positions at the edge of the box for second-phase attacks' :
                        primaryPosition === 'cf' ? 'attacks the six-yard box on corners and acts as the wall player for indirect free kicks' :
                        primaryPosition === 'gk' ? 'commands the six-yard box with authority and organizes the defensive setup' :
                        'positions at the penalty spot on attacking corners and marks key opposition threats on defensive set-pieces'
                      }.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Videos Tab */}
        {activeTab === 'videos' && (
          <div className="space-y-6">
            {/* No Videos Available Message */}
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 border-b border-gray-700">
                <h3 className="text-lg font-bold text-white flex items-center">
                  <Video className="mr-2 text-green-500" size={20} />
                  Performance Videos
                </h3>
              </div>
              
              <div className="p-12 flex flex-col items-center justify-center text-center">
                <div className="w-20 h-20 rounded-full bg-gray-700 flex items-center justify-center mb-4">
                  <Video className="text-gray-500" size={32} />
                </div>
                <h4 className="text-xl font-medium text-white mb-2">No Videos Available</h4>
                <p className="text-gray-400 max-w-md">
                  There are currently no performance videos available for this player. Check back later or subscribe to receive updates when new content is added.
                </p>
                
                <div className="mt-6 flex flex-col sm:flex-row gap-3">
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg inline-flex items-center">
                    <ExternalLink className="mr-2" size={16} />
                    Scout Similar Players
                  </button>
                </div>
                
                <div className="mt-12 p-6 bg-gray-750 rounded-lg max-w-md">
                  <h4 className="text-white font-medium mb-3">Request Video Analysis</h4>
                  <p className="text-gray-400 text-sm mb-4">
                    As a professional scout, you can request specialized video analysis for this player. Our analysts will compile highlights and tactical breakdowns.
                  </p>
                  <button className="w-full px-4 py-2 bg-green-700 hover:bg-green-600 text-white rounded-lg">
                    Submit Analysis Request
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlayerCompletePage;