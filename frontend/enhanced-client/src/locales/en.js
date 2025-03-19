/**
 * English translations for KatenaScout
 */
export default {
  common: {
    appName: "KatenaScout",
    loading: "Loading...",
    error: "Sorry, an error occurred"
  },
  navigation: {
    chat: "AI Scout Chat",
    favorites: "Favorites",
    settings: "Settings"
  },
  onboarding: {
    welcome: "Welcome to KatenaScout",
    description: "Your AI-powered football scouting assistant",
    selectLanguage: "Please select your preferred language",
    continueButton: "Continue",
    poweredBy: "Powered by Claude AI"
  },
  chat: {
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
    thinking: "Thinking...",
    showingDetails: "Showing details of ",
    errorMessage: "Sorry, an error occurred while processing your search.",
    comparePlayersButton: "Compare Players",
    cancelCompare: "Cancel Compare",
    compareSelectedButton: "Compare Selected Players",
    selectedPlayersCount: "Selected Players",
    selectTwoPlayers: "Please select 2 players to compare",
    statsExplanationTitle: "Statistics Explained",
    comparisonAspectsTitle: "Comparison Aspects"
  },
  playerDashboard: {
    overview: "Player Overview",
    statistics: "Statistics",
    details: "Details",
    addToFavorites: "Add to Favorites",
    removeFromFavorites: "Remove from Favorites",
    position: "Position",
    age: "Age",
    foot: "Preferred Foot",
    height: "Height",
    weight: "Weight",
    value: "Market Value",
    viewCompleteProfile: "View Complete Profile",
    comparePlayer: "Compare Player",
    close: "Close"
  },
  
  playerComparison: {
    title: "Player Comparison",
    loading: "Comparing players...",
    retry: "Retry",
    selectPlayerToCompare: "Select Player to Compare",
    selectPlayerPrompt: "Please select another player to compare with",
    radarComparison: "Key Metrics Comparison",
    aiAnalysis: "AI Analysis",
    generatingAnalysis: "Generating analysis...",
    tacticalAnalysis: "Tactical Context Analysis",
    closeTooltip: "Close",
    overallWinner: "Overall Winner",
    score: "Score",
    vs: "VS"
  },
  
  tacticalAnalysis: {
    title: "Tactical Context Analysis",
    loading: "Analyzing players...",
    selectStyle: "Select Playing Style",
    selectFormation: "Select Formation",
    generateAnalysis: "Generate Analysis",
    analyzing: "Analyzing...",
    fitScore: "Tactical Fit Score",
    keyStrengths: "Key Strengths",
    keyDifferences: "Key Differences",
    styleDescription: "Style Description",
    backToComparison: "Back to Comparison"
  },
  favorites: {
    title: "Favorite Players",
    emptyState: "You have no favorite players yet",
    searchPlaceholder: "Search favorites...",
    removeConfirm: "Remove from favorites?",
    removeFromFavorites: "Remove from Favorites"
  },
  settings: {
    title: "Settings",
    language: "Language",
    languageLabel: "Select your language",
    theme: "Theme",
    themeLight: "Light",
    themeDark: "Dark",
    themeSys: "System",
    resetApp: "Reset Application",
    resetWarning: "This will clear all your data and reset the application",
    resetConfirm: "Are you sure?",
    version: "Version"
  },
  errors: {
    playerNotFound: "Player data not found. Please try again.",
    loadingFailed: "Failed to load player details. Please try again.",
    requestFailed: "Failed to connect to the server. Please check your connection.",
    comparisonFailed: "Failed to compare players. Please try again.",
    notEnoughPlayers: "Not enough players to compare. Please select at least two players.",
    sameSearchOnly: "You can only compare players from the same search results.",
    selectTwoPlayers: "Please select exactly 2 players to compare.",
    serverError: "The server encountered an error. Please try again later.",
    parsingError: "There was an error processing the response. Please try again."
  }
};