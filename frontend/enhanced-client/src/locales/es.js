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
    }
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
  positions: {
    // Defensores
    lcb: "Defensor Central Izquierdo",
    rcb: "Defensor Central Derecho",
    cb: "Defensor Central",
    lb: "Lateral Izquierdo",
    rb: "Lateral Derecho",
    lwb: "Carrilero Izquierdo",
    rwb: "Carrilero Derecho",
    sw: "Libero",
    
    // Centrocampistas
    cdm: "Mediocentro Defensivo",
    ldm: "Mediocentro Defensivo Izquierdo",
    rdm: "Mediocentro Defensivo Derecho",
    cm: "Centrocampista",
    lcm: "Centrocampista Izquierdo",
    rcm: "Centrocampista Derecho",
    cam: "Mediocentro Ofensivo",
    lam: "Mediocentro Ofensivo Izquierdo",
    ram: "Mediocentro Ofensivo Derecho",
    lm: "Medio Izquierdo",
    rm: "Medio Derecho",
    
    // Delanteros
    lw: "Extremo Izquierdo",
    rw: "Extremo Derecho",
    lf: "Delantero Izquierdo",
    rf: "Delantero Derecho",
    cf: "Delantero Centro",
    st: "Delantero"
  },
  
  player: {
    leftFoot: "Izquierdo",
    rightFoot: "Derecho",
    bothFeet: "Ambos"
  },
  metrics: {
    // General
    matches: "Partidos",
    matchesInStart: "Partidos como Titular",
    matchesSubstituted: "Partidos como Suplente",
    matchesComingOff: "Sustituciones",
    minutesOnField: "Minutos en Cancha",
    minutesTagged: "Minutos Registrados",
    
    // Goals and Assists
    goals: "Goles",
    assists: "Asistencias",
    secondAssists: "Segundas Asistencias",
    thirdAssists: "Terceras Asistencias",
    shotAssists: "Asistencias de Tiro",
    shotOnTargetAssists: "Asistencias de Tiro al Arco",
    
    // Shots
    shots: "Tiros",
    shotsOnTarget: "Tiros al Arco",
    headShots: "Tiros de Cabeza",
    shotsBlocked: "Tiros Bloqueados",
    xgShot: "xG (Goles Esperados)",
    xgAssist: "xA (Asistencias Esperadas)",
    
    // Passing
    passes: "Pases",
    successfulPasses: "Pases Precisos",
    smartPasses: "Pases Inteligentes",
    successfulSmartPasses: "Pases Inteligentes Precisos",
    passesToFinalThird: "Pases al Último Tercio",
    successfulPassesToFinalThird: "Pases Precisos al Último Tercio",
    crosses: "Centros",
    successfulCrosses: "Centros Precisos",
    forwardPasses: "Pases Adelante",
    successfulForwardPasses: "Pases Adelante Precisos",
    backPasses: "Pases Atrás",
    successfulBackPasses: "Pases Atrás Precisos",
    throughPasses: "Pases en Profundidad",
    successfulThroughPasses: "Pases en Profundidad Precisos",
    keyPasses: "Pases Clave",
    successfulKeyPasses: "Pases Clave Precisos",
    verticalPasses: "Pases Verticales",
    successfulVerticalPasses: "Pases Verticales Precisos",
    longPasses: "Pases Largos",
    successfulLongPasses: "Pases Largos Precisos",
    lateralPasses: "Pases Laterales",
    successfulLateralPasses: "Pases Laterales Precisos",
    progressivePasses: "Pases Progresivos",
    successfulProgressivePasses: "Pases Progresivos Precisos",
    
    // Dribbling
    dribbles: "Regates",
    successfulDribbles: "Regates Exitosos",
    dribblesAgainst: "Regates Sufridos",
    dribblesAgainstWon: "Regates Sufridos Ganados",
    
    // Duels
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
    
    // Defensive Actions
    interceptions: "Intercepciones",
    defensiveActions: "Acciones Defensivas",
    successfulDefensiveAction: "Acciones Defensivas Exitosas",
    slidingTackles: "Entradas",
    successfulSlidingTackles: "Entradas Exitosas",
    clearances: "Despejes",
    
    // Attacking Actions
    attackingActions: "Acciones Ofensivas",
    successfulAttackingActions: "Acciones Ofensivas Exitosas",
    linkupPlays: "Jugadas de Enlace",
    successfulLinkupPlays: "Jugadas de Enlace Exitosas",
    touchInBox: "Toques en Área",
    progressiveRun: "Carreras Progresivas",
    
    // Set Pieces
    freeKicks: "Tiros Libres",
    freeKicksOnTarget: "Tiros Libres al Arco",
    directFreeKicks: "Tiros Libres Directos",
    directFreeKicksOnTarget: "Tiros Libres Directos al Arco",
    corners: "Córners",
    penalties: "Penaltis",
    successfulPenalties: "Penaltis Convertidos",
    
    // Physical
    accelerations: "Aceleraciones",
    recoveries: "Recuperaciones",
    opponentHalfRecoveries: "Recuperaciones en Campo Rival",
    dangerousOpponentHalfRecoveries: "Recuperaciones Peligrosas en Campo Rival",
    counterpressingRecoveries: "Recuperaciones por Contrapresión",
    
    // Losses
    losses: "Pérdidas",
    ownHalfLosses: "Pérdidas en Campo Propio",
    dangerousOwnHalfLosses: "Pérdidas Peligrosas en Campo Propio",
    missedBalls: "Balones Perdidos",
    
    // Goalkeeping
    gkCleanSheets: "Vallas Invictas",
    gkConcededGoals: "Goles Recibidos",
    gkShotsAgainst: "Tiros Recibidos",
    gkExits: "Salidas",
    gkSuccessfulExits: "Salidas Exitosas",
    gkAerialDuels: "Duelos Aéreos de Portero",
    gkAerialDuelsWon: "Duelos Aéreos de Portero Ganados",
    gkSaves: "Paradas",
    goalKicks: "Saques de Meta",
    goalKicksShort: "Saques de Meta Cortos",
    goalKicksLong: "Saques de Meta Largos",
    successfulGoalKicks: "Saques de Meta Precisos",
    xgSave: "xG Salvado",
    
    // Cards and Fouls
    yellowCards: "Tarjetas Amarillas",
    redCards: "Tarjetas Rojas",
    directRedCards: "Tarjetas Rojas Directas",
    fouls: "Faltas Cometidas",
    foulsSuffered: "Faltas Recibidas",
    offsides: "Fuera de Juego"
  }
};