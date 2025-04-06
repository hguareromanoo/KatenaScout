/**
 * Spanish translations for KatenaScout
 */
export default {
  playingStyles: {
    tikiTaka: {
      name: "Tiki-Taka",
      description: "Pases cortos y rápidos con movimiento continuo de jugadores (estilo Barcelona)"
    },
    possessionBased: {
      name: "Posesión",
      description: "Enfoque en mantener la posesión del balón"
    },
    counterAttacking: {
      name: "Contraataque",
      description: "Transiciones rápidas de defensa a ataque"
    },
    highPressing: {
      name: "Presión Alta",
      description: "Presión agresiva en campo contrario"
    },
    gegenpressing: {
      name: "Gegenpressing",
      description: "Contrapresión inmediata tras perder la posesión (estilo de Jürgen Klopp)"
    },
    directPlay: {
      name: "Juego Directo",
      description: "Pases verticales y directos hacia los delanteros"
    },
    fluidAttacking: {
      name: "Ataque Fluido",
      description: "Énfasis en el movimiento de jugadores y pases creativos"
    },
    lowBlock: {
      name: "Bloque Bajo",
      description: "Forma defensiva compacta con contraataques"
    },
    widthAndDepth: {
      name: "Amplitud y Profundidad",
      description: "Uso de la amplitud y centros para crear oportunidades"
    },
    balancedApproach: {
      name: "Enfoque Equilibrado",
      description: "Equilibrio entre defensa y ataque"
    }
  },
  common: {
    appName: "KatenaScout",
    loading: "Cargando...",
    error: "Lo siento, ocurrió un error",
    back: "Volver"
  },
  navigation: {
    chat: "Chat de Scout IA",
    favorites: "Favoritos",
    settings: "Configuración"
  },
  onboarding: {
    welcome: "Bienvenido a KatenaScout",
    description: "Tu asistente de scouting de fútbol con IA",
    selectLanguage: "Por favor, selecciona tu idioma preferido",
    continueButton: "Continuar",
    poweredBy: "Desarrollado con Claude AI"
  },
  chat: {
    headerTitle: "KatenaScout AI",
    headerSubtitle: "Tu asistente de scouting inteligente",
    inputPlaceholder: "Describe el tipo de jugador que estás buscando...",
    welcomeTitle: "Hola, soy Scout AI",
    welcomeMessage: "Describe el tipo de jugador que estás buscando, y encontraré las mejores opciones para tu equipo.",
    examplesTitle: "Ejemplos de búsqueda:",
    example1: "Necesito un lateral ofensivo con buena capacidad de centro",
    example2: "Busco defensores centrales fuertes en duelos aéreos y con buena salida de balón",
    example3: "Quiero un delantero joven con buena definición y menos de 23 años",
    playersFoundText: "Jugadores encontrados - Selecciona para ver detalles:",
    analyzing: "Analizando jugadores...",
    thinking: "Pensando...",
    showingDetails: "Mostrando detalles de ",
    errorMessage: "Lo siento, ocurrió un error al procesar tu búsqueda.",
    comparePlayersButton: "Comparar Jugadores",
    cancelCompare: "Cancelar Comparación",
    compareSelectedButton: "Comparar Jugadores Seleccionados",
    selectedPlayersCount: "Jugadores Seleccionados",
    selectTwoPlayers: "Por favor, selecciona 2 jugadores para comparar",
    statsExplanationTitle: "Estadísticas Explicadas",
    comparisonAspectsTitle: "Aspectos de Comparación"
  },
  playerDashboard: {
    overview: "Visión General del Jugador",
    statistics: "Estadísticas",
    details: "Detalles",
    addToFavorites: "Añadir a Favoritos",
    removeFromFavorites: "Quitar de Favoritos",
    position: "Posición",
    age: "Edad",
    foot: "Pie Preferido",
    height: "Altura",
    weight: "Peso",
    value: "Valor de Mercado",
    viewCompleteProfile: "Ver Perfil Completo",
    comparePlayer: "Comparar Jugador",
    close: "Cerrar",
    noMetrics: "No hay métricas disponibles para este jugador."
  },
  
  playerCompletePage: {
    performanceOverview: "Visión General del Rendimiento",
    playerInformation: "Información del Jugador",
    keyAttributes: "Atributos Clave",
    completeStatistics: "Estadísticas Completas",
    playerDetails: "Detalles del Jugador",
    personalInformation: "Información Personal",
    professionalInformation: "Información Profesional",
    fullName: "Nombre Completo",
    nationality: "Nacionalidad",
    currentClub: "Club Actual",
    contractUntil: "Contrato Hasta",
    contractExpiration: "Vencimiento del Contrato",
    agencies: "Agencias",
    years: "años",
    cm: "cm",
    kg: "kg",
    average: "Prom",
    positionAvg: "Prom posición",
    lowerIsBetter: "Menor es mejor",
    noStatsAvailable: "No hay estadísticas disponibles para este jugador.",
    categoryStats: {
      attacking: "Estadísticas de Ataque",
      passing: "Estadísticas de Pase",
      defending: "Estadísticas de Defensa",
      possession: "Estadísticas de Posesión",
      physical: "Estadísticas Físicas",
      goalkeeping: "Estadísticas de Portero"
    },
    unknown: "Desconocido" // Added fallback translation
  },
  
  loading: {
    fetchingPlayerData: "Obteniendo datos del jugador..."
  },
  
  playerComparison: {
    title: "Comparación de Jugadores",
    loading: "Comparando jugadores...",
    retry: "Reintentar",
    selectPlayerToCompare: "Seleccionar Jugador para Comparar",
    selectPlayerPrompt: "Por favor, selecciona otro jugador para comparar",
    radarComparison: "Comparación de Métricas Clave",
    aiAnalysis: "Análisis de IA",
    generatingAnalysis: "Generando análisis...",
    tacticalAnalysis: "Análisis de Contexto Táctico",
    generateAnalysis: "Generar Análisis",
    closeTooltip: "Cerrar",
    overallWinner: "Ganador General",
    score: "Puntuación",
    vs: "VS",
    noMetrics: "No hay métricas disponibles para el gráfico de radar"
  },
  
  tacticalAnalysis: {
    title: "Análisis de Contexto Táctico",
    loading: "Analizando jugadores...",
    selectStyle: "Seleccionar Estilo de Juego",
    selectFormation: "Seleccionar Formación",
    generateAnalysis: "Generar Análisis",
    analyzing: "Analizando...",
    fitScore: "Puntuación de Ajuste Táctico",
    keyStrengths: "Fortalezas Clave",
    keyDifferences: "Diferencias Clave",
    styleDescription: "Descripción del Estilo",
    backToComparison: "Volver a la Comparación",
    betterTacticalFit: "Mejor Ajuste Táctico",
    analysis: "Análisis",
    noAnalysisAvailable: "No hay análisis disponible.",
    introText: "Seleccione un estilo de juego y formación para analizar cómo los jugadores se desempeñarían en ese contexto táctico."
  },
  favorites: {
    title: "Jugadores Favoritos",
    emptyState: "Aún no tienes jugadores favoritos",
    searchPlaceholder: "Buscar favoritos...",
    removeConfirm: "¿Quitar de favoritos?",
    removeFromFavorites: "Quitar de Favoritos"
  },
  settings: {
    title: "Configuración",
    language: "Idioma",
    languageLabel: "Selecciona tu idioma",
    theme: "Tema",
    themeLight: "Claro",
    themeDark: "Oscuro",
    themeSys: "Sistema",
    resetApp: "Restablecer Aplicación",
    resetWarning: "Esto borrará todos tus datos y restablecerá la aplicación",
    resetConfirm: "¿Estás seguro?",
    version: "Versión"
  },
  errors: {
    playerNotFound: "Datos del jugador no encontrados. Por favor, inténtalo de nuevo.",
    loadingFailed: "Error al cargar detalles del jugador. Por favor, inténtalo de nuevo.",
    requestFailed: "Error al conectar con el servidor. Por favor, verifica tu conexión.",
    comparisonFailed: "Error al comparar jugadores. Por favor, inténtalo de nuevo.",
    notEnoughPlayers: "No hay suficientes jugadores para comparar. Por favor, selecciona al menos dos jugadores.",
    sameSearchOnly: "Solo puedes comparar jugadores de los mismos resultados de búsqueda.",
    selectTwoPlayers: "Por favor, selecciona exactamente 2 jugadores para comparar.",
    serverError: "El servidor encontró un error. Por favor, inténtalo más tarde.",
    parsingError: "Hubo un error al procesar la respuesta. Por favor, inténtalo de nuevo."
  },
  metrics: {
    // Unidades
    units: {
      percent: '%',
      minutes: 'min',
      meters: 'm',
      count: ''
    },
    
    // Categorías
    categories: {
      participation: "Participación",
      passing: "Pases",
      attacking: "Ataque",
      defensive: "Defensa",
      physical: "Físico",
      discipline: "Disciplina",
      goalkeeper: "Portero",
      general: "General"
    },
    
    // Participación en partidos
    matches: "Partidos",
    matchesInStart: "Partidos como Titular",
    matchesSubstituted: "Veces Sustituido",
    matchesComingOff: "Veces Entró desde Banquillo",
    minutesOnField: "Minutos Jugados",
    minutesTagged: "Minutos Registrados",
    
    // Goles y Tiros
    goals: "Goles",
    assists: "Asistencias",
    shots: "Tiros",
    headShots: "Remates de Cabeza",
    shotsOnTarget: "Tiros a Puerta",
    headShotsOnTarget: "Remates de Cabeza a Puerta",
    shotAssists: "Asistencias de Tiro",
    shotOnTargetAssists: "Asistencias de Tiro a Puerta",
    secondAssists: "Segundas Asistencias",
    thirdAssists: "Terceras Asistencias",
    goalConversion: "Tasa de Conversión de Goles",
    xgShot: "Goles Esperados (xG)",
    xgAssist: "Asistencias Esperadas (xA)",
    xgSave: "Paradas Esperadas (xGS)",
    touchInBox: "Toques en el Área",
    
    // Tarjetas y Faltas
    yellowCards: "Tarjetas Amarillas",
    redCards: "Tarjetas Rojas",
    directRedCards: "Tarjetas Rojas Directas",
    fouls: "Faltas Cometidas",
    foulsSuffered: "Faltas Sufridas",
    yellowCardsPerFoul: "Tarjetas Amarillas por Falta",
    
    // Duelos
    duels: "Duelos",
    duelsWon: "Duelos Ganados",
    defensiveDuels: "Duelos Defensivos",
    defensiveDuelsWon: "Duelos Defensivos Ganados",
    offensiveDuels: "Duelos Ofensivos",
    offensiveDuelsWon: "Duelos Ofensivos Ganados",
    aerialDuels: "Duelos Aéreos",
    aerialDuelsWon: "Duelos Aéreos Ganados",
    fieldAerialDuels: "Duelos Aéreos en Campo",
    fieldAerialDuelsWon: "Duelos Aéreos en Campo Ganados",
    pressingDuels: "Duelos de Presión",
    pressingDuelsWon: "Duelos de Presión Ganados",
    looseBallDuels: "Duelos por Balón Suelto",
    looseBallDuelsWon: "Duelos por Balón Suelto Ganados",
    
    // Pases
    passes: "Pases",
    successfulPasses: "Pases Exitosos",
    smartPasses: "Pases Inteligentes",
    successfulSmartPasses: "Pases Inteligentes Exitosos",
    passesToFinalThird: "Pases al Último Tercio",
    successfulPassesToFinalThird: "Pases Exitosos al Último Tercio",
    crosses: "Centros",
    successfulCrosses: "Centros Exitosos",
    forwardPasses: "Pases Hacia Adelante",
    successfulForwardPasses: "Pases Hacia Adelante Exitosos",
    backPasses: "Pases Hacia Atrás",
    successfulBackPasses: "Pases Hacia Atrás Exitosos",
    throughPasses: "Pases Filtrados",
    successfulThroughPasses: "Pases Filtrados Exitosos",
    keyPasses: "Pases Clave",
    successfulKeyPasses: "Pases Clave Exitosos",
    verticalPasses: "Pases Verticales",
    successfulVerticalPasses: "Pases Verticales Exitosos",
    longPasses: "Pases Largos",
    successfulLongPasses: "Pases Largos Exitosos",
    passLength: "Longitud Media de Pase",
    longPassLength: "Longitud Media de Pase Largo",
    progressivePasses: "Pases Progresivos",
    successfulProgressivePasses: "Pases Progresivos Exitosos",
    lateralPasses: "Pases Laterales",
    successfulLateralPasses: "Pases Laterales Exitosos",
    receivedPass: "Pases Recibidos",
    
    // Acciones Ofensivas
    dribbles: "Regates",
    successfulDribbles: "Regates Exitosos",
    attackingActions: "Acciones de Ataque",
    successfulAttackingActions: "Acciones de Ataque Exitosas",
    dribbleDistanceFromOpponentGoal: "Distancia Media de Regate a Portería",
    progressiveRun: "Carreras Progresivas",
    linkupPlays: "Jugadas de Combinación",
    successfulLinkupPlays: "Jugadas de Combinación Exitosas",
    accelerations: "Aceleraciones",
    
    // Juego Defensivo
    interceptions: "Intercepciones",
    defensiveActions: "Acciones Defensivas",
    successfulDefensiveAction: "Acciones Defensivas Exitosas",
    recoveries: "Recuperaciones de Balón",
    counterpressingRecoveries: "Recuperaciones en Contrapresión",
    opponentHalfRecoveries: "Recuperaciones en Campo Contrario",
    dangerousOpponentHalfRecoveries: "Recuperaciones Peligrosas en Campo Contrario",
    slidingTackles: "Entradas Deslizantes",
    successfulSlidingTackles: "Entradas Deslizantes Exitosas",
    shotsBlocked: "Tiros Bloqueados",
    clearances: "Despejes",
    dribblesAgainst: "Regateado", 
    dribblesAgainstWon: "Regates Defendidos",
    
    // Pérdidas y Posesión
    losses: "Pérdidas de Balón",
    ownHalfLosses: "Pérdidas en Campo Propio",
    dangerousOwnHalfLosses: "Pérdidas Peligrosas en Campo Propio",
    missedBalls: "Balones Perdidos",
    ballRecoveries: "Recuperaciones de Balón",
    
    // Balón Parado
    freeKicks: "Tiros Libres Ejecutados",
    freeKicksOnTarget: "Tiros Libres a Puerta",
    directFreeKicks: "Tiros Libres Directos",
    directFreeKicksOnTarget: "Tiros Libres Directos a Puerta",
    corners: "Córners Ejecutados",
    penalties: "Penaltis Ejecutados",
    successfulPenalties: "Penaltis Marcados",
    penaltiesConversion: "Tasa de Conversión de Penaltis",
    
    // Estadísticas de Portero
    gkCleanSheets: "Porterías a Cero",
    gkConcededGoals: "Goles Recibidos",
    gkShotsAgainst: "Tiros Recibidos",
    gkSaves: "Paradas",
    gkExits: "Salidas del Portero",
    gkSuccessfulExits: "Salidas Exitosas del Portero",
    gkAerialDuels: "Duelos Aéreos (Portero)",
    gkAerialDuelsWon: "Duelos Aéreos Ganados (Portero)",
    goalKicks: "Saques de Puerta",
    goalKicksShort: "Saques de Puerta Cortos",
    goalKicksLong: "Saques de Puerta Largos",
    successfulGoalKicks: "Saques de Puerta Exitosos",
    
    // Otros
    offsides: "Fueras de Juego",
    win: "Tasa de Victorias",
    
    // Nuevas métricas (específicas del sistema)
    newDuelsWon: "Nuevos Duelos Ganados",
    newDefensiveDuelsWon: "Nuevos Duelos Defensivos Ganados",
    newOffensiveDuelsWon: "Nuevos Duelos Ofensivos Ganados",
    newSuccessfulDribbles: "Nuevos Regates Exitosos"
  },
  positions: {
    gk: "Portero",
    lcb: "Defensa Central Izquierdo",
    rcb: "Defensa Central Derecho",
    cb: "Defensa Central",
    lb: "Lateral Izquierdo",
    rb: "Lateral Derecho",
    lwb: "Carrilero Izquierdo",
    rwb: "Carrilero Derecho",
    ldmf: "Mediocentro Defensivo Izquierdo",
    rdmf: "Mediocentro Defensivo Derecho",
    dmf: "Mediocentro Defensivo",
    lcmf: "Mediocentro Izquierdo",
    rcmf: "Mediocentro Derecho",
    cmf: "Mediocentro",
    lamf: "Mediocentro Ofensivo Izquierdo",
    ramf: "Mediocentro Ofensivo Derecho",
    amf: "Mediocentro Ofensivo",
    lw: "Extremo Izquierdo",
    rw: "Extremo Derecho",
    lwf: "Delantero Izquierdo",
    rwf: "Delantero Derecho",
    cf: "Delantero Centro"
    // Añadir otros códigos de posición según sea necesario
  },
  player: {
    leftFoot: "Izquierdo",
    rightFoot: "Derecho",
    bothFeet: "Ambos"
  }
};
