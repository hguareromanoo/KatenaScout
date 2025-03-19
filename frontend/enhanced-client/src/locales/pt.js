/**
 * Portuguese translations for KatenaScout
 */
export default {
  common: {
    appName: "KatenaScout",
    loading: "Carregando...",
    error: "Desculpe, ocorreu um erro"
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
    welcomeTitle: "Olá, Técnico!",
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
    close: "Fechar"
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
    vs: "VS"
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
    backToComparison: "Voltar para a Comparação"
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
  }
};