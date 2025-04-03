/**
 * Bulgarian translations for KatenaScout
 */
export default {
  playingStyles: {
    tikiTaka: {
      name: "Тики-Така",
      description: "Кратки, бързи подавания с непрекъснато движение на играчите (стил на Барселона)"
    },
    possessionBased: {
      name: "Владение на Топката",
      description: "Фокус върху поддържане на владението на топката"
    },
    counterAttacking: {
      name: "Контраатака",
      description: "Бързи преходи от защита към атака"
    },
    highPressing: {
      name: "Висок Пресинг",
      description: "Агресивен пресинг високо в полето на противника"
    },
    gegenpressing: {
      name: "Гегенпресинг",
      description: "Незабавен контрапресинг след загуба на владение (стил на Юрген Клоп)"
    },
    directPlay: {
      name: "Директна Игра",
      description: "Вертикални, преки подавания към нападателите"
    },
    fluidAttacking: {
      name: "Гъвкава Атака",
      description: "Акцент върху движението на играчите и креативни подавания"
    },
    lowBlock: {
      name: "Нисък Блок",
      description: "Защитна, компактна формация с контраатаки"
    },
    widthAndDepth: {
      name: "Широчина и Дълбочина",
      description: "Използване на широчина и центрирания за създаване на възможности"
    },
    balancedApproach: {
      name: "Балансиран Подход",
      description: "Равен фокус върху защита и атака"
    }
  },
  common: {
    appName: "KatenaScout",
    loading: "Зареждане...",
    error: "Съжаляваме, възникна грешка",
    back: "Назад"
  },
  navigation: {
    chat: "Чат с ИИ Скаут",
    favorites: "Любими",
    settings: "Настройки"
  },
  onboarding: {
    welcome: "Добре дошли в KatenaScout",
    description: "Вашият асистент за футболно наблюдение с ИИ",
    selectLanguage: "Моля, изберете предпочитания от вас език",
    continueButton: "Продължи",
    poweredBy: "Създадено с Claude AI"
  },
  chat: {
    headerTitle: "KatenaScout AI",
    headerSubtitle: "Вашият интелигентен скаутинг асистент",
    inputPlaceholder: "Опишете типа играч, който търсите...",
    welcomeTitle: "Здравейте, аз съм Scout AI",
    welcomeMessage: "Опишете типа играч, който търсите, и ще намеря най-добрите опции за вашия отбор.",
    examplesTitle: "Примери за търсене:",
    example1: "Нужен ми е офанзивен бек с добра способност за центриране",
    example2: "Търся централни защитници, силни във въздушните дуели и с добро разпределяне на топката",
    example3: "Искам млад нападател с добро завършване и под 23 години",
    playersFoundText: "Намерени играчи - Изберете, за да видите детайли:",
    analyzing: "Анализиране на играчи...",
    thinking: "Обмисляне...",
    showingDetails: "Показване на детайли за ",
    errorMessage: "Съжаляваме, възникна грешка при обработката на вашето търсене.",
    comparePlayersButton: "Сравни Играчи",
    cancelCompare: "Отмени Сравнението",
    compareSelectedButton: "Сравни Избраните Играчи",
    selectedPlayersCount: "Избрани Играчи",
    selectTwoPlayers: "Моля, изберете 2 играча за сравнение",
    statsExplanationTitle: "Обяснение на Статистиката",
    comparisonAspectsTitle: "Аспекти на Сравнението"
  },
  playerDashboard: {
    overview: "Преглед на Играча",
    statistics: "Статистика",
    details: "Детайли",
    addToFavorites: "Добави в Любими",
    removeFromFavorites: "Премахни от Любими",
    position: "Позиция",
    age: "Възраст",
    foot: "Предпочитан Крак",
    height: "Височина",
    weight: "Тегло",
    value: "Пазарна Стойност",
    viewCompleteProfile: "Виж Пълния Профил",
    comparePlayer: "Сравни Играча",
    close: "Затвори",
    noMetrics: "Няма налични метрики за този играч."
  },
  
  playerCompletePage: {
    performanceOverview: "Преглед на Представянето",
    playerInformation: "Информация за Играча",
    keyAttributes: "Ключови Атрибути",
    completeStatistics: "Пълна Статистика",
    playerDetails: "Детайли за Играча",
    personalInformation: "Лична Информация",
    professionalInformation: "Професионална Информация",
    fullName: "Пълно Име",
    nationality: "Националност",
    currentClub: "Настоящ Клуб",
    contractUntil: "Договор До",
    contractExpiration: "Дата на изтичане на договора",
    agencies: "Агенции",
    years: "години",
    cm: "см",
    kg: "кг",
    average: "Средно",
    positionAvg: "Средно за позиция",
    lowerIsBetter: "По-ниско е по-добре",
    noStatsAvailable: "Няма налична статистика за този играч.",
    categoryStats: {
      attacking: "Нападателна Статистика",
      passing: "Статистика за Подаване",
      defending: "Защитна Статистика",
      possession: "Статистика за Владение",
      physical: "Физическа Статистика",
      goalkeeping: "Вратарска Статистика"
    }
  },
  
  loading: {
    fetchingPlayerData: "Извличане на данни за играча..."
  },
  
  playerComparison: {
    title: "Сравнение на Играчи",
    loading: "Сравняване на играчи...",
    retry: "Опитай отново",
    selectPlayerToCompare: "Избери Играч за Сравнение",
    selectPlayerPrompt: "Моля, изберете друг играч за сравнение",
    radarComparison: "Сравнение на Ключови Метрики",
    aiAnalysis: "ИИ Анализ",
    generatingAnalysis: "Генериране на анализ...",
    tacticalAnalysis: "Анализ на Тактически Контекст",
    generateAnalysis: "Генерирай Анализ",
    closeTooltip: "Затвори",
    overallWinner: "Общ Победител",
    score: "Резултат",
    vs: "СРЕЩУ",
    noMetrics: "Няма налични метрики за радарната графика"
  },
  
  tacticalAnalysis: {
    title: "Анализ на Тактически Контекст",
    loading: "Анализиране на играчи...",
    selectStyle: "Избери Стил на Игра",
    selectFormation: "Избери Формация",
    generateAnalysis: "Генерирай Анализ",
    analyzing: "Анализиране...",
    fitScore: "Оценка на Тактическо Съответствие",
    keyStrengths: "Ключови Силни Страни",
    keyDifferences: "Ключови Разлики",
    styleDescription: "Описание на Стила",
    backToComparison: "Обратно към Сравнението",
    betterTacticalFit: "По-добро Тактическо Съответствие",
    analysis: "Анализ",
    noAnalysisAvailable: "Няма наличен анализ.",
    introText: "Изберете стил на игра и формация, за да анализирате как играчите биха се представили в този тактически контекст."
  },
  favorites: {
    title: "Любими Играчи",
    emptyState: "Все още нямате любими играчи",
    searchPlaceholder: "Търсене в любими...",
    removeConfirm: "Премахване от любими?",
    removeFromFavorites: "Премахни от Любими"
  },
  settings: {
    title: "Настройки",
    language: "Език",
    languageLabel: "Изберете вашия език",
    theme: "Тема",
    themeLight: "Светла",
    themeDark: "Тъмна",
    themeSys: "Системна",
    resetApp: "Нулиране на Приложението",
    resetWarning: "Това ще изтрие всички ваши данни и ще нулира приложението",
    resetConfirm: "Сигурни ли сте?",
    version: "Версия"
  },
  errors: {
    playerNotFound: "Данните за играча не са намерени. Моля, опитайте отново.",
    loadingFailed: "Неуспешно зареждане на детайли за играча. Моля, опитайте отново.",
    requestFailed: "Неуспешно свързване със сървъра. Моля, проверете връзката си.",
    comparisonFailed: "Неуспешно сравнение на играчи. Моля, опитайте отново.",
    notEnoughPlayers: "Няма достатъчно играчи за сравнение. Моля, изберете поне двама играчи.",
    sameSearchOnly: "Можете да сравнявате само играчи от едни и същи резултати от търсене.",
    selectTwoPlayers: "Моля, изберете точно 2 играча за сравнение.",
    serverError: "Сървърът срещна грешка. Моля, опитайте по-късно.",
    parsingError: "Възникна грешка при обработката на отговора. Моля, опитайте отново."
  },
  positions: {
    // Защитници
    lcb: "Ляв Централен Защитник",
    rcb: "Десен Централен Защитник",
    cb: "Централен Защитник",
    lb: "Ляв Бек",
    rb: "Десен Бек",
    lwb: "Ляво Крило",
    rwb: "Дясно Крило",
    sw: "Либеро",
    
    // Полузащитници
    cdm: "Дефанзивен Полузащитник",
    ldm: "Ляв Дефанзивен Полузащитник",
    rdm: "Десен Дефанзивен Полузащитник",
    cm: "Централен Полузащитник",
    lcm: "Ляв Централен Полузащитник",
    rcm: "Десен Централен Полузащитник",
    cam: "Атакуващ Полузащитник",
    lam: "Ляв Атакуващ Полузащитник",
    ram: "Десен Атакуващ Полузащитник",
    lm: "Ляв Полузащитник",
    rm: "Десен Полузащитник",
    
    // Нападатели
    lw: "Ляво Крило",
    rw: "Дясно Крило",
    lf: "Ляв Нападател",
    rf: "Десен Нападател",
    cf: "Централен Нападател",
    st: "Нападател"
  },
  
  player: {
    leftFoot: "Ляв",
    rightFoot: "Десен",
    bothFeet: "И двата"
  },
  metrics: {
    // General
    matches: "Мачове",
    matchesInStart: "Мачове като Титуляр",
    matchesSubstituted: "Мачове като Резерва",
    matchesComingOff: "Смяни",
    minutesOnField: "Минути на Терена",
    minutesTagged: "Регистрирани Минути",
    
    // Goals and Assists
    goals: "Голове",
    assists: "Асистенции",
    secondAssists: "Втори Асистенции",
    thirdAssists: "Трети Асистенции",
    shotAssists: "Асистенции за Удар",
    shotOnTargetAssists: "Асистенции за Удар във Вратата",
    
    // Shots
    shots: "Удари",
    shotsOnTarget: "Удари във Вратата",
    headShots: "Удари с Глава",
    shotsBlocked: "Блокирани Удари",
    xgShot: "xG (Очаквани Голове)",
    xgAssist: "xA (Очаквани Асистенции)",
    
    // Passing
    passes: "Подавания",
    successfulPasses: "Точни Подавания",
    smartPasses: "Умни Подавания",
    successfulSmartPasses: "Точни Умни Подавания",
    passesToFinalThird: "Подавания в Последна Трета",
    successfulPassesToFinalThird: "Точни Подавания в Последна Трета",
    crosses: "Центрирания",
    successfulCrosses: "Точни Центрирания",
    forwardPasses: "Подавания Напред",
    successfulForwardPasses: "Точни Подавания Напред",
    backPasses: "Подавания Назад",
    successfulBackPasses: "Точни Подавания Назад",
    throughPasses: "Подавания в Дълбочина",
    successfulThroughPasses: "Точни Подавания в Дълбочина",
    keyPasses: "Ключови Подавания",
    successfulKeyPasses: "Точни Ключови Подавания",
    verticalPasses: "Вертикални Подавания",
    successfulVerticalPasses: "Точни Вертикални Подавания",
    longPasses: "Дълги Подавания",
    successfulLongPasses: "Точни Дълги Подавания",
    lateralPasses: "Странични Подавания",
    successfulLateralPasses: "Точни Странични Подавания",
    progressivePasses: "Прогресивни Подавания",
    successfulProgressivePasses: "Точни Прогресивни Подавания",
    
    // Dribbling
    dribbles: "Дрибъл",
    successfulDribbles: "Успешен Дрибъл",
    dribblesAgainst: "Дрибъл срещу",
    dribblesAgainstWon: "Спечелен Дрибъл срещу",
    
    // Duels
    duels: "Дуели",
    duelsWon: "Спечелени Дуели",
    defensiveDuels: "Защитни Дуели",
    defensiveDuelsWon: "Спечелени Защитни Дуели",
    offensiveDuels: "Атакуващи Дуели",
    offensiveDuelsWon: "Спечелени Атакуващи Дуели",
    aerialDuels: "Въздушни Дуели",
    aerialDuelsWon: "Спечелени Въздушни Дуели",
    fieldAerialDuels: "Въздушни Дуели на Терена",
    fieldAerialDuelsWon: "Спечелени Въздушни Дуели на Терена",
    pressingDuels: "Дуели при Прес",
    pressingDuelsWon: "Спечелени Дуели при Прес",
    looseBallDuels: "Дуели за Свободна Топка",
    looseBallDuelsWon: "Спечелени Дуели за Свободна Топка",
    
    // Defensive Actions
    interceptions: "Прихващания",
    defensiveActions: "Защитни Действия",
    successfulDefensiveAction: "Успешни Защитни Действия",
    slidingTackles: "Хлъзгащи Отнемания",
    successfulSlidingTackles: "Успешни Хлъзгащи Отнемания",
    clearances: "Изчиствания",
    
    // Attacking Actions
    attackingActions: "Атакуващи Действия",
    successfulAttackingActions: "Успешни Атакуващи Действия",
    linkupPlays: "Свързващи Игри",
    successfulLinkupPlays: "Успешни Свързващи Игри",
    touchInBox: "Докосвания в Наказателното",
    progressiveRun: "Прогресивни Пробягвания",
    
    // Set Pieces
    freeKicks: "Свободни Удари",
    freeKicksOnTarget: "Свободни Удари във Вратата",
    directFreeKicks: "Директни Свободни Удари",
    directFreeKicksOnTarget: "Директни Свободни Удари във Вратата",
    corners: "Корнери",
    penalties: "Дузпи",
    successfulPenalties: "Вкарани Дузпи",
    
    // Physical
    accelerations: "Ускорения",
    recoveries: "Възвръщания",
    opponentHalfRecoveries: "Възвръщания в Чуждата Половина",
    dangerousOpponentHalfRecoveries: "Опасни Възвръщания в Чуждата Половина",
    counterpressingRecoveries: "Възвръщания при Контрапрес",
    
    // Losses
    losses: "Загуби",
    ownHalfLosses: "Загуби в Собствената Половина",
    dangerousOwnHalfLosses: "Опасни Загуби в Собствената Половина",
    missedBalls: "Пропуснати Топки",
    
    // Goalkeeping
    gkCleanSheets: "Сухи Мрежи",
    gkConcededGoals: "Допуснати Голове",
    gkShotsAgainst: "Удари срещу",
    gkExits: "Излизания",
    gkSuccessfulExits: "Успешни Излизания",
    gkAerialDuels: "Въздушни Дуели на Вратаря",
    gkAerialDuelsWon: "Спечелени Въздушни Дуели на Вратаря",
    gkSaves: "Спасявания",
    goalKicks: "Големи Удари",
    goalKicksShort: "Кратки Големи Удари",
    goalKicksLong: "Дълги Големи Удари",
    successfulGoalKicks: "Точни Големи Удари",
    xgSave: "xG Спасен",
    
    // Cards and Fouls
    yellowCards: "Жълти Картони",
    redCards: "Червени Картони",
    directRedCards: "Директни Червени Картони",
    fouls: "Направени Фаулове",
    foulsSuffered: "Получени Фаулове",
    offsides: "Засади"
  }
};