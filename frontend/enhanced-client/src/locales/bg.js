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
    },
    unknown: "Неизвестно" // Added fallback translation
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
  metrics: {
    // Единици
    units: {
      percent: '%',
      minutes: 'мин',
      meters: 'м',
      count: ''
    },
    
    // Категории
    categories: {
      participation: "Участие",
      passing: "Подавания",
      attacking: "Атака",
      defensive: "Защита",
      physical: "Физически",
      discipline: "Дисциплина",
      goalkeeper: "Вратарски",
      general: "Общи"
    },
    
    // Участие в мачове
    matches: "Мачове",
    matchesInStart: "Мачове като Титуляр",
    matchesSubstituted: "Пъти Сменен",
    matchesComingOff: "Пъти Влязъл от Пейката",
    minutesOnField: "Изиграни Минути",
    minutesTagged: "Записани Минути",
    
    // Голове и Удари
    goals: "Голове",
    assists: "Асистенции",
    shots: "Удари",
    headShots: "Удари с Глава",
    shotsOnTarget: "Точни Удари",
    headShotsOnTarget: "Точни Удари с Глава",
    shotAssists: "Асистенции за Удар",
    shotOnTargetAssists: "Асистенции за Точен Удар",
    secondAssists: "Втори Асистенции",
    thirdAssists: "Трети Асистенции",
    goalConversion: "Процент Реализирани Голове",
    xgShot: "Очаквани Голове (xG)",
    xgAssist: "Очаквани Асистенции (xA)",
    xgSave: "Очаквани Спасявания (xGS)",
    touchInBox: "Докосвания в Наказателното Поле",
    
    // Картони и Нарушения
    yellowCards: "Жълти Картони",
    redCards: "Червени Картони",
    directRedCards: "Директни Червени Картони",
    fouls: "Извършени Нарушения",
    foulsSuffered: "Претърпени Нарушения",
    yellowCardsPerFoul: "Жълти Картони на Нарушение",
    
    // Дуели
    duels: "Дуели",
    duelsWon: "Спечелени Дуели",
    defensiveDuels: "Защитни Дуели",
    defensiveDuelsWon: "Спечелени Защитни Дуели",
    offensiveDuels: "Офанзивни Дуели",
    offensiveDuelsWon: "Спечелени Офанзивни Дуели",
    aerialDuels: "Въздушни Дуели",
    aerialDuelsWon: "Спечелени Въздушни Дуели",
    fieldAerialDuels: "Въздушни Дуели в Полето",
    fieldAerialDuelsWon: "Спечелени Въздушни Дуели в Полето",
    pressingDuels: "Дуели при Пресинг",
    pressingDuelsWon: "Спечелени Дуели при Пресинг",
    looseBallDuels: "Дуели за Свободна Топка",
    looseBallDuelsWon: "Спечелени Дуели за Свободна Топка",
    
    // Подавания
    passes: "Подавания",
    successfulPasses: "Успешни Подавания",
    smartPasses: "Умни Подавания",
    successfulSmartPasses: "Успешни Умни Подавания",
    passesToFinalThird: "Подавания към Финалната Третина",
    successfulPassesToFinalThird: "Успешни Подавания към Финалната Третина",
    crosses: "Центрирания",
    successfulCrosses: "Успешни Центрирания",
    forwardPasses: "Подавания Напред",
    successfulForwardPasses: "Успешни Подавания Напред",
    backPasses: "Подавания Назад",
    successfulBackPasses: "Успешни Подавания Назад",
    throughPasses: "Извеждащи Подавания",
    successfulThroughPasses: "Успешни Извеждащи Подавания",
    keyPasses: "Ключови Подавания",
    successfulKeyPasses: "Успешни Ключови Подавания",
    verticalPasses: "Вертикални Подавания",
    successfulVerticalPasses: "Успешни Вертикални Подавания",
    longPasses: "Дълги Подавания",
    successfulLongPasses: "Успешни Дълги Подавания",
    passLength: "Средна Дължина на Подаване",
    longPassLength: "Средна Дължина на Дълго Подаване",
    progressivePasses: "Прогресивни Подавания",
    successfulProgressivePasses: "Успешни Прогресивни Подавания",
    lateralPasses: "Странични Подавания",
    successfulLateralPasses: "Успешни Странични Подавания",
    receivedPass: "Получени Подавания",
    
    // Офанзивни Действия
    dribbles: "Дрибъли",
    successfulDribbles: "Успешни Дрибъли",
    attackingActions: "Атакуващи Действия",
    successfulAttackingActions: "Успешни Атакуващи Действия",
    dribbleDistanceFromOpponentGoal: "Средно Разстояние при Дрибъл от Вратата",
    progressiveRun: "Прогресивни Пробиви",
    linkupPlays: "Комбинативни Игри",
    successfulLinkupPlays: "Успешни Комбинативни Игри",
    accelerations: "Ускорения",
    
    // Защитна Игра
    interceptions: "Пресечени Топки",
    defensiveActions: "Защитни Действия",
    successfulDefensiveAction: "Успешни Защитни Действия",
    recoveries: "Възстановени Топки",
    counterpressingRecoveries: "Възстановени при Контрапресинг",
    opponentHalfRecoveries: "Възстановени в Полето на Противника",
    dangerousOpponentHalfRecoveries: "Опасни Възстановени в Полето на Противника",
    slidingTackles: "Шпагати",
    successfulSlidingTackles: "Успешни Шпагати",
    shotsBlocked: "Блокирани Удари",
    clearances: "Изчиствания",
    dribblesAgainst: "Преодолян с Дрибъл", 
    dribblesAgainstWon: "Защита срещу Дрибъл",
    
    // Загуби и Владение
    losses: "Загубени Топки",
    ownHalfLosses: "Загубени в Собствената Половина",
    dangerousOwnHalfLosses: "Опасни Загуби в Собствената Половина",
    missedBalls: "Пропуснати Топки",
    ballRecoveries: "Възстановени Топки",
    
    // Статични Положения
    freeKicks: "Изпълнени Свободни Удари",
    freeKicksOnTarget: "Точни Свободни Удари",
    directFreeKicks: "Директни Свободни Удари",
    directFreeKicksOnTarget: "Точни Директни Свободни Удари",
    corners: "Изпълнени Корнери",
    penalties: "Изпълнени Дузпи",
    successfulPenalties: "Реализирани Дузпи",
    penaltiesConversion: "Процент Реализирани Дузпи",
    
    // Вратарска Статистика
    gkCleanSheets: "Сухи Мрежи",
    gkConcededGoals: "Допуснати Голове",
    gkShotsAgainst: "Удари към Вратата",
    gkSaves: "Спасявания",
    gkExits: "Излизания на Вратаря",
    gkSuccessfulExits: "Успешни Излизания на Вратаря",
    gkAerialDuels: "Въздушни Дуели (Вратар)",
    gkAerialDuelsWon: "Спечелени Въздушни Дуели (Вратар)",
    goalKicks: "Удари от Вратата",
    goalKicksShort: "Къси Удари от Вратата",
    goalKicksLong: "Дълги Удари от Вратата",
    successfulGoalKicks: "Успешни Удари от Вратата",
    
    // Други
    offsides: "Засади",
    win: "Процент Победи",
    
    // Нови метрики (специфични за системата)
    newDuelsWon: "Нови Спечелени Дуели",
    newDefensiveDuelsWon: "Нови Спечелени Защитни Дуели",
    newOffensiveDuelsWon: "Нови Спечелени Офанзивни Дуели",
    newSuccessfulDribbles: "Нови Успешни Дрибъли"
  },
  positions: {
    gk: "Вратар",
    lcb: "Ляв Централен Защитник",
    rcb: "Десен Централен Защитник",
    cb: "Централен Защитник",
    lb: "Ляв Бек",
    rb: "Десен Бек",
    lwb: "Ляв Уинг-Бек",
    rwb: "Десен Уинг-Бек",
    ldmf: "Ляв Дефанзивен Полузащитник",
    rdmf: "Десен Дефанзивен Полузащитник",
    dmf: "Дефанзивен Полузащитник",
    lcmf: "Ляв Централен Полузащитник",
    rcmf: "Десен Централен Полузащитник",
    cmf: "Централен Полузащитник",
    lamf: "Ляв Атакуващ Полузащитник",
    ramf: "Десен Атакуващ Полузащитник",
    amf: "Атакуващ Полузащитник",
    lw: "Ляво Крило",
    rw: "Дясно Крило",
    lwf: "Ляв Нападател",
    rwf: "Десен Нападател",
    cf: "Централен Нападател"
    // Добавете други кодове на позиции при нужда
  },
  player: {
    leftFoot: "Ляв",
    rightFoot: "Десен",
    bothFeet: "И двата"
  }
};
