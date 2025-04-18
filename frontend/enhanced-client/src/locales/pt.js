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
    unknown: "Desconhecido",
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
    }
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
  metrics: {
    // Attacking metrics
    goals: "Gols",
    assists: "Assistências",
    shots: "Finalizações",
    shotsOnTarget: "Finalizações no Gol",
    headShots: "Cabeceios",
    xgShot: "Gols Esperados (xG)",
    xgAssist: "Assistências Esperadas (xA)",
    shotAssists: "Assistências para Finalização",
    shotOnTargetAssists: "Assistências para Finalização no Gol",
    secondAssists: "Segundas Assistências",
    thirdAssists: "Terceiras Assistências",
    shotsBlocked: "Finalizações Bloqueadas",
    goalConversion: "Conversão de Gols",
    touchInBox: "Toques na Área",
    
    // Passing metrics
    passes: "Passes",
    successfulPasses: "Passes Precisos",
    smartPasses: "Passes Inteligentes",
    successfulSmartPasses: "Passes Inteligentes Precisos",
    passesToFinalThird: "Passes para Último Terço",
    successfulPassesToFinalThird: "Passes Precisos para Último Terço",
    crosses: "Cruzamentos",
    successfulCrosses: "Cruzamentos Precisos",
    forwardPasses: "Passes para Frente",
    successfulForwardPasses: "Passes Precisos para Frente",
    backPasses: "Passes para Trás",
    successfulBackPasses: "Passes Precisos para Trás",
    throughPasses: "Passes em Profundidade",
    successfulThroughPasses: "Passes Precisos em Profundidade",
    keyPasses: "Passes-Chave",
    successfulKeyPasses: "Passes-Chave Precisos",
    verticalPasses: "Passes Verticais",
    successfulVerticalPasses: "Passes Verticais Precisos",
    longPasses: "Passes Longos",
    successfulLongPasses: "Passes Longos Precisos",
    lateralPasses: "Passes Laterais",
    successfulLateralPasses: "Passes Laterais Precisos",
    progressivePasses: "Passes Progressivos",
    successfulProgressivePasses: "Passes Progressivos Precisos",
    linkupPlays: "Jogadas de Ligação",
    successfulLinkupPlays: "Jogadas de Ligação Bem-Sucedidas",
    
    // Defending metrics
    interceptions: "Interceptações",
    defensiveActions: "Ações Defensivas",
    successfulDefensiveAction: "Ações Defensivas Bem-Sucedidas",
    clearances: "Cortes",
    slidingTackles: "Carrinhos",
    successfulSlidingTackles: "Carrinhos Bem-Sucedidos",
    defensiveDuels: "Duelos Defensivos",
    defensiveDuelsWon: "Duelos Defensivos Vencidos",
    newDefensiveDuelsWon: "Novos Duelos Defensivos Vencidos",
    counterpressingRecoveries: "Recuperações de Contra-Pressão",
    
    // Possession metrics
    duels: "Duelos",
    duelsWon: "Duelos Vencidos",
    newDuelsWon: "Novos Duelos Vencidos",
    offensiveDuels: "Duelos Ofensivos",
    offensiveDuelsWon: "Duelos Ofensivos Vencidos",
    newOffensiveDuelsWon: "Novos Duelos Ofensivos Vencidos",
    aerialDuels: "Duelos Aéreos",
    aerialDuelsWon: "Duelos Aéreos Vencidos",
    fieldAerialDuels: "Duelos Aéreos em Campo",
    fieldAerialDuelsWon: "Duelos Aéreos em Campo Vencidos",
    dribbles: "Dribles",
    successfulDribbles: "Dribles Bem-Sucedidos",
    newSuccessfulDribbles: "Novos Dribles Bem-Sucedidos",
    dribblesAgainst: "Dribles Sofridos",
    dribblesAgainstWon: "Dribles Sofridos Vencidos",
    progressiveRun: "Corridas Progressivas",
    ballRecoveries: "Recuperações de Bola",
    opponentHalfRecoveries: "Recuperações no Campo Adversário",
    dangerousOpponentHalfRecoveries: "Recuperações Perigosas no Campo Adversário",
    losses: "Perdas de Bola",
    ownHalfLosses: "Perdas no Próprio Campo",
    dangerousOwnHalfLosses: "Perdas Perigosas no Próprio Campo",
    
    // Physical metrics
    accelerations: "Acelerações",
    pressingDuels: "Duelos de Pressão",
    pressingDuelsWon: "Duelos de Pressão Vencidos",
    looseBallDuels: "Duelos por Bola Solta",
    looseBallDuelsWon: "Duelos por Bola Solta Vencidos",
    missedBalls: "Bolas Perdidas",
    fouls: "Faltas",
    foulsSuffered: "Faltas Sofridas",
    yellowCards: "Cartões Amarelos",
    redCards: "Cartões Vermelhos",
    directRedCards: "Cartões Vermelhos Diretos",
    offsides: "Impedimentos",
    
    // Goalkeeping metrics
    gkSaves: "Defesas",
    gkConcededGoals: "Gols Sofridos",
    gkShotsAgainst: "Finalizações Contra",
    gkExits: "Saídas",
    gkSuccessfulExits: "Saídas Bem-Sucedidas",
    gkAerialDuels: "Duelos Aéreos",
    gkAerialDuelsWon: "Duelos Aéreos Vencidos",
    gkCleanSheets: "Jogos sem Sofrer Gols",
    xgSave: "Gols Esperados Salvos (xGS)",
    goalKicks: "Tiro de Meta",
    goalKicksShort: "Tiros de Meta Curtos",
    goalKicksLong: "Tiros de Meta Longos",
    successfulGoalKicks: "Tiros de Meta Bem-Sucedidos",
    
    // Set pieces
    freeKicks: "Cobranças de Falta",
    freeKicksOnTarget: "Cobranças de Falta no Gol",
    directFreeKicks: "Cobranças de Falta Diretas",
    directFreeKicksOnTarget: "Cobranças de Falta Diretas no Gol",
    corners: "Escanteios",
    penalties: "Pênaltis",
    successfulPenalties: "Pênaltis Convertidos"
  },
  positions: {
    // Defensores
    lcb: "Zagueiro Esquerdo",
    rcb: "Zagueiro Direito",
    cb: "Zagueiro Central",
    lb: "Lateral Esquerdo",
    rb: "Lateral Direito",
    lwb: "Ala Esquerdo",
    rwb: "Ala Direito",
    sw: "Zagueiro-Líbero",
    
    // Meio-campistas
    cdm: "Volante",
    ldm: "Volante Esquerdo",
    rdm: "Volante Direito",
    cm: "Meio-campista",
    lcm: "Meio-campista Esquerdo",
    rcm: "Meio-campista Direito",
    cam: "Meia-Armador",
    lam: "Meia-Armador Esquerdo",
    ram: "Meia-Armador Direito",
    lm: "Meia Esquerdo",
    rm: "Meia Direito",
    
    // Atacantes
    lw: "Ponta Esquerda",
    rw: "Ponta Direita",
    lf: "Segundo Atacante Esquerdo",
    rf: "Segundo Atacante Direito",
    cf: "Centroavante",
    st: "Atacante"
  },
  
  player: {
    leftFoot: "Esquerdo",
    rightFoot: "Direito",
    bothFeet: "Ambos"
  }
};