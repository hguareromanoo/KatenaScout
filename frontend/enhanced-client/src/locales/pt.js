/**
 * Portuguese translations for KatenaScout
 */
export default {
  playingStyles: {
    tikiTaka: {
      name: "Tiki-Taka",
      description: "Passes curtos e rápidos com movimento contínuo dos jogadores (estilo Barcelona)"
    },
    possessionBased: {
      name: "Posse de Bola",
      description: "Foco em manter a posse de bola"
    },
    counterAttacking: {
      name: "Contra-Ataque",
      description: "Transições rápidas da defesa para o ataque"
    },
    highPressing: {
      name: "Pressão Alta",
      description: "Pressão agressiva no campo adversário"
    },
    gegenpressing: {
      name: "Gegenpressing",
      description: "Contra-pressão imediata após perder a posse (estilo de Jürgen Klopp)"
    },
    directPlay: {
      name: "Jogo Direto",
      description: "Passes verticais e diretos para os atacantes"
    },
    fluidAttacking: {
      name: "Ataque Fluido",
      description: "Ênfase no movimento dos jogadores e passes criativos"
    },
    lowBlock: {
      name: "Bloco Baixo",
      description: "Forma defensiva compacta com contra-ataques"
    },
    widthAndDepth: {
      name: "Amplitude e Profundidade",
      description: "Uso da amplitude e cruzamentos para criar oportunidades"
    },
    balancedApproach: {
      name: "Abordagem Equilibrada",
      description: "Equilíbrio entre defesa e ataque"
    }
  },
  common: {
    appName: "KatenaScout",
    loading: "Carregando...",
    error: "Desculpe, ocorreu um erro",
    back: "Voltar"
  },
  navigation: {
    chat: "Chat de Scout IA",
    favorites: "Favoritos",
    settings: "Configurações"
  },
  onboarding: {
    welcome: "Bem-vindo ao KatenaScout",
    description: "Seu assistente de scouting de futebol com IA",
    selectLanguage: "Por favor, selecione seu idioma preferido",
    continueButton: "Continuar",
    poweredBy: "Desenvolvido com Claude AI"
  },
  chat: {
    headerTitle: "KatenaScout AI",
    headerSubtitle: "Seu assistente de scouting inteligente",
    inputPlaceholder: "Descreva o tipo de jogador que você procura...",
    welcomeTitle: "Olá, eu sou o Scout AI",
    welcomeMessage: "Descreva o tipo de jogador que você está buscando, e eu encontrarei as melhores opções para sua equipe.",
    examplesTitle: "Exemplos de busca:",
    example1: "Preciso de um lateral ofensivo com boa capacidade de cruzamento",
    example2: "Busco zagueiros fortes no jogo aéreo e com boa saída de bola",
    example3: "Quero um atacante jovem com boa finalização e menos de 23 anos",
    playersFoundText: "Jogadores encontrados - Selecione para ver detalhes:",
    analyzing: "Analisando jogadores...",
    thinking: "Pensando...",
    showingDetails: "Mostrando detalhes de ",
    errorMessage: "Desculpe, ocorreu um erro ao processar sua busca.",
    comparePlayersButton: "Comparar Jogadores",
    cancelCompare: "Cancelar Comparação",
    compareSelectedButton: "Comparar Jogadores Selecionados",
    selectedPlayersCount: "Jogadores Selecionados",
    selectTwoPlayers: "Por favor, selecione 2 jogadores para comparar",
    statsExplanationTitle: "Estatísticas Explicadas",
    comparisonAspectsTitle: "Aspectos da Comparação"
  },
  playerDashboard: {
    overview: "Visão Geral do Jogador",
    statistics: "Estatísticas",
    details: "Detalhes",
    addToFavorites: "Adicionar aos Favoritos",
    removeFromFavorites: "Remover dos Favoritos",
    position: "Posição",
    age: "Idade",
    foot: "Pé Preferido",
    height: "Altura",
    weight: "Peso",
    value: "Valor de Mercado",
    viewCompleteProfile: "Ver Perfil Completo",
    comparePlayer: "Comparar Jogador",
    close: "Fechar",
    noMetrics: "Não há métricas disponíveis para este jogador."
  },
  
  playerCompletePage: {
    performanceOverview: "Visão Geral de Desempenho",
    playerInformation: "Informações do Jogador",
    keyAttributes: "Atributos Chave",
    completeStatistics: "Estatísticas Completas",
    playerDetails: "Detalhes do Jogador",
    personalInformation: "Informações Pessoais",
    professionalInformation: "Informações Profissionais",
    fullName: "Nome Completo",
    nationality: "Nacionalidade",
    currentClub: "Clube Atual",
    contractUntil: "Contrato Até",
    contractExpiration: "Expiração do Contrato",
    agencies: "Agências",
    years: "anos",
    cm: "cm",
    kg: "kg",
    average: "Média",
    positionAvg: "Média posição",
    lowerIsBetter: "Menor é melhor",
    noStatsAvailable: "Não há estatísticas disponíveis para este jogador.",
    categoryStats: {
      attacking: "Estatísticas de Ataque",
      passing: "Estatísticas de Passe",
      defending: "Estatísticas de Defesa",
      possession: "Estatísticas de Posse",
      physical: "Estatísticas Físicas",
      goalkeeping: "Estatísticas de Goleiro"
    },
    unknown: "Desconhecido" // Added fallback translation
  },
  
  loading: {
    fetchingPlayerData: "Buscando dados do jogador..."
  },
  
  playerComparison: {
    title: "Comparação de Jogadores",
    loading: "Comparando jogadores...",
    retry: "Tentar Novamente",
    selectPlayerToCompare: "Selecionar Jogador para Comparar",
    selectPlayerPrompt: "Por favor, selecione outro jogador para comparar",
    radarComparison: "Comparação de Métricas Chave",
    aiAnalysis: "Análise de IA",
    generatingAnalysis: "Gerando análise...",
    tacticalAnalysis: "Análise de Contexto Tático",
    generateAnalysis: "Gerar Análise",
    closeTooltip: "Fechar",
    overallWinner: "Vencedor Geral",
    score: "Pontuação",
    vs: "VS",
    noMetrics: "Não há métricas disponíveis para o gráfico de radar"
  },
  
  tacticalAnalysis: {
    title: "Análise de Contexto Tático",
    loading: "Analisando jogadores...",
    selectStyle: "Selecionar Estilo de Jogo",
    selectFormation: "Selecionar Formação",
    generateAnalysis: "Gerar Análise",
    analyzing: "Analisando...",
    fitScore: "Pontuação de Adequação Tática",
    keyStrengths: "Pontos Fortes Chave",
    keyDifferences: "Diferenças Chave",
    styleDescription: "Descrição do Estilo",
    backToComparison: "Voltar para a Comparação",
    betterTacticalFit: "Melhor Ajuste Tático",
    analysis: "Análise",
    noAnalysisAvailable: "Nenhuma análise disponível.",
    introText: "Selecione um estilo de jogo e formação para analisar como os jogadores se sairiam nesse contexto tático."
  },
  favorites: {
    title: "Jogadores Favoritos",
    emptyState: "Você ainda não tem jogadores favoritos",
    searchPlaceholder: "Buscar favoritos...",
    removeConfirm: "Remover dos favoritos?",
    removeFromFavorites: "Remover dos Favoritos"
  },
  settings: {
    title: "Configurações",
    language: "Idioma",
    languageLabel: "Selecione seu idioma",
    theme: "Tema",
    themeLight: "Claro",
    themeDark: "Escuro",
    themeSys: "Sistema",
    resetApp: "Redefinir Aplicativo",
    resetWarning: "Isso apagará todos os seus dados e redefinirá o aplicativo",
    resetConfirm: "Tem certeza?",
    version: "Versão"
  },
  metrics: {
    // Unidades
    units: {
      percent: '%',
      minutes: 'min',
      meters: 'm',
      count: ''
    },
    
    // Categorias
    categories: {
      participation: "Participação",
      passing: "Passes",
      attacking: "Ataque",
      defensive: "Defesa",
      physical: "Físico",
      discipline: "Disciplina",
      goalkeeper: "Goleiro",
      general: "Geral"
    },
    
    // Participação em jogos
    matches: "Partidas",
    matchesInStart: "Partidas como Titular",
    matchesSubstituted: "Vezes Substituído",
    matchesComingOff: "Vezes que Saiu do Banco",
    minutesOnField: "Minutos Jogados",
    minutesTagged: "Minutos Registrados",
    
    // Estatísticas de Gols e Finalizações
    goals: "Gols",
    assists: "Assistências",
    shots: "Finalizações",
    headShots: "Cabeceios",
    shotsOnTarget: "Finalizações no Gol",
    headShotsOnTarget: "Cabeceios no Gol",
    shotAssists: "Assistências para Finalização",
    shotOnTargetAssists: "Assistências para Finalização no Gol",
    secondAssists: "Pré-Assistências",
    thirdAssists: "Assistências Terciárias",
    goalConversion: "Taxa de Conversão de Gols",
    xgShot: "Expectativa de Gols (xG)",
    xgAssist: "Expectativa de Assistências (xA)",
    xgSave: "Expectativa de Defesas (xGS)",
    touchInBox: "Toques na Área",
    
    // Cartões e Faltas
    yellowCards: "Cartões Amarelos",
    redCards: "Cartões Vermelhos",
    directRedCards: "Cartões Vermelhos Diretos",
    fouls: "Faltas Cometidas",
    foulsSuffered: "Faltas Sofridas",
    yellowCardsPerFoul: "Cartões Amarelos por Falta",
    
    // Duelos
    duels: "Duelos",
    duelsWon: "Duelos Vencidos",
    defensiveDuels: "Duelos Defensivos",
    defensiveDuelsWon: "Duelos Defensivos Vencidos",
    offensiveDuels: "Duelos Ofensivos",
    offensiveDuelsWon: "Duelos Ofensivos Vencidos",
    aerialDuels: "Duelos Aéreos",
    aerialDuelsWon: "Duelos Aéreos Vencidos",
    fieldAerialDuels: "Duelos Aéreos em Campo",
    fieldAerialDuelsWon: "Duelos Aéreos em Campo Vencidos",
    pressingDuels: "Duelos de Pressão",
    pressingDuelsWon: "Duelos de Pressão Vencidos",
    looseBallDuels: "Duelos por Bola Solta",
    looseBallDuelsWon: "Duelos por Bola Solta Vencidos",
    
    // Passes
    passes: "Passes",
    successfulPasses: "Passes Bem-sucedidos",
    smartPasses: "Passes Inteligentes",
    successfulSmartPasses: "Passes Inteligentes Bem-sucedidos",
    passesToFinalThird: "Passes para Terço Final",
    successfulPassesToFinalThird: "Passes para Terço Final Bem-sucedidos",
    crosses: "Cruzamentos",
    successfulCrosses: "Cruzamentos Bem-sucedidos",
    forwardPasses: "Passes para Frente",
    successfulForwardPasses: "Passes para Frente Bem-sucedidos",
    backPasses: "Passes para Trás",
    successfulBackPasses: "Passes para Trás Bem-sucedidos",
    throughPasses: "Passes em Profundidade",
    successfulThroughPasses: "Passes em Profundidade Bem-sucedidos",
    keyPasses: "Passes-Chave",
    successfulKeyPasses: "Passes-Chave Bem-sucedidos",
    verticalPasses: "Passes Verticais",
    successfulVerticalPasses: "Passes Verticais Bem-sucedidos",
    longPasses: "Passes Longos",
    successfulLongPasses: "Passes Longos Bem-sucedidos",
    passLength: "Comprimento Médio do Passe",
    longPassLength: "Comprimento Médio do Passe Longo",
    progressivePasses: "Passes Progressivos",
    successfulProgressivePasses: "Passes Progressivos Bem-sucedidos",
    lateralPasses: "Passes Laterais",
    successfulLateralPasses: "Passes Laterais Bem-sucedidos",
    receivedPass: "Passes Recebidos",
    
    // Ações ofensivas
    dribbles: "Dribles",
    successfulDribbles: "Dribles Bem-sucedidos",
    attackingActions: "Ações de Ataque",
    successfulAttackingActions: "Ações de Ataque Bem-sucedidas",
    dribbleDistanceFromOpponentGoal: "Distância Média de Drible do Gol",
    progressiveRun: "Corridas Progressivas",
    linkupPlays: "Jogadas de Combinação",
    successfulLinkupPlays: "Jogadas de Combinação Bem-sucedidas",
    accelerations: "Acelerações",
    
    // Jogo defensivo
    interceptions: "Interceptações",
    defensiveActions: "Ações Defensivas",
    successfulDefensiveAction: "Ações Defensivas Bem-sucedidas",
    recoveries: "Recuperações de Bola",
    counterpressingRecoveries: "Recuperações em Contrapressão",
    opponentHalfRecoveries: "Recuperações no Campo Adversário",
    dangerousOpponentHalfRecoveries: "Recuperações Perigosas no Campo Adversário",
    slidingTackles: "Carrinhos",
    successfulSlidingTackles: "Carrinhos Bem-sucedidos",
    shotsBlocked: "Finalizações Bloqueadas",
    clearances: "Afastamentos",
    dribblesAgainst: "Dribles Sofridos", 
    dribblesAgainstWon: "Dribles Sofridos Defensados",
    
    // Perdas de bola e posse
    losses: "Perdas de Bola",
    ownHalfLosses: "Perdas de Bola no Próprio Campo",
    dangerousOwnHalfLosses: "Perdas Perigosas no Próprio Campo",
    missedBalls: "Bolas Perdidas",
    ballRecoveries: "Recuperações de Bola",
    
    // Bolas paradas
    freeKicks: "Cobranças de Falta",
    freeKicksOnTarget: "Cobranças de Falta no Gol",
    directFreeKicks: "Faltas Diretas",
    directFreeKicksOnTarget: "Faltas Diretas no Gol",
    corners: "Escanteios",
    penalties: "Pênaltis",
    successfulPenalties: "Pênaltis Convertidos",
    penaltiesConversion: "Taxa de Conversão de Pênaltis",
    
    // Estatísticas de goleiro
    gkCleanSheets: "Jogos sem Sofrer Gol",
    gkConcededGoals: "Gols Sofridos",
    gkShotsAgainst: "Chutes Contra",
    gkSaves: "Defesas",
    gkExits: "Saídas do Gol",
    gkSuccessfulExits: "Saídas do Gol Bem-sucedidas",
    gkAerialDuels: "Duelos Aéreos (Goleiro)",
    gkAerialDuelsWon: "Duelos Aéreos Vencidos (Goleiro)",
    goalKicks: "Tiros de Meta",
    goalKicksShort: "Tiros de Meta Curtos",
    goalKicksLong: "Tiros de Meta Longos",
    successfulGoalKicks: "Tiros de Meta Bem-sucedidos",
    
    // Outros
    offsides: "Impedimentos",
    win: "Taxa de Vitórias",
    
    // Novas métricas (específicas do sistema)
    newDuelsWon: "Duelos Vencidos (Novo Cálculo)",
    newDefensiveDuelsWon: "Duelos Defensivos Vencidos (Novo Cálculo)",
    newOffensiveDuelsWon: "Duelos Ofensivos Vencidos (Novo Cálculo)",
    newSuccessfulDribbles: "Dribles Bem-sucedidos (Novo Cálculo)"
  },
  errors: {
    playerNotFound: "Dados do jogador não encontrados. Por favor, tente novamente.",
    loadingFailed: "Falha ao carregar detalhes do jogador. Por favor, tente novamente.",
    requestFailed: "Falha ao conectar com o servidor. Por favor, verifique sua conexão.",
    comparisonFailed: "Falha ao comparar jogadores. Por favor, tente novamente.",
    notEnoughPlayers: "Não há jogadores suficientes para comparar. Por favor, selecione pelo menos dois jogadores.",
    sameSearchOnly: "Você só pode comparar jogadores dos mesmos resultados de busca.",
    selectTwoPlayers: "Por favor, selecione exatamente 2 jogadores para comparar.",
    serverError: "O servidor encontrou um erro. Por favor, tente novamente mais tarde.",
    parsingError: "Houve um erro ao processar a resposta. Por favor, tente novamente."
  },
  positions: {
    gk: "Goleiro",
    lcb: "Zagueiro Esquerdo",
    rcb: "Zagueiro Direito",
    cb: "Zagueiro Central",
    lb: "Lateral Esquerdo",
    rb: "Lateral Direito",
    lwb: "Ala Esquerdo",
    rwb: "Ala Direito",
    ldmf: "Volante Esquerdo",
    rdmf: "Volante Direito",
    dmf: "Volante Central",
    lcmf: "Meia Central Esquerdo",
    rcmf: "Meia Central Direito",
    cmf: "Meia Central",
    lamf: "Meia Atacante Esquerdo",
    ramf: "Meia Atacante Direito",
    amf: "Meia Atacante Central",
    lw: "Ponta Esquerda",
    rw: "Ponta Direita",
    lwf: "Atacante Esquerdo",
    rwf: "Atacante Direito",
    cf: "Centroavante"
    // Adicione outros códigos de posição conforme necessário
  },
  player: {
    leftFoot: "Esquerdo",
    rightFoot: "Direito",
    bothFeet: "Ambos"
  }
};
