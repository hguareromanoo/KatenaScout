from services.data_service import get_player_database_by_id, get_average_statistics, find_player_by_id, get_sigma_by_position
import scipy.stats as stats
from models.analysis import TacticalFitAnalysis, SwotAnalysis, AIInsight, DataAnalysis, Stat, RankingItem
from models.player import Player
from typing import Dict, Any, List, Optional
from services.claude_api import call_claude_api

POSITION_KEY_METRICS = {
    # Goleiros
    "goalkeeper": {
        "defensive": ["gkSaves", "gkSavesPercent", "gkCleanSheets", "gkGoalsConceded", "gkExits", "gkSuccessfulExits"],
        "passing": ["passes", "successfulPassesPercent", "longPasses", "successfulLongPassesPercent"],
        "positioning": ["gkShotsAgainst", "gkAerialDuels", "gkAerialDuelsWon"]
    },
    
    # Zagueiros
    "center_backs": {
        "defensive": ["defensiveDuels", "defensiveDuelsWon", "aerialDuels", "aerialDuelsWon", "interceptions", "shotsBlocked", "clearances", "slidingTackles", "successfulSlidingTackles"],
        "attacking": ["goals", "assists", "shotsOnTarget", "headerGoals"],
        "passing": ["passes", "successfulPassesPercent", "longPasses", "successfulLongPassesPercent", "progressivePasses", "successfulProgressivePassesPercent"],
        "possession": ["losses", "duels", "duelsWon", "ballRecoveries"],
        "physical": ["accelerations", "fouls", "foulsSuffered", "aerialDuels", "aerialDuelsWon"]
    },
    
    # Laterais
    "full_backs": {
        "defensive": ["defensiveDuels", "defensiveDuelsWon", "interceptions", "ballRecoveries", "slidingTackles", "successfulSlidingTackles"],
        "attacking": ["assists", "goals", "crosses", "successfulCrossesPercent", "touchInBox"],
        "passing": ["progressivePasses", "successfulProgressivePassesPercent", "passesToFinalThird", "successfulPassesToFinalThirdPercent", "keyPasses"],
        "possession": ["dribbles", "successfulDribblesPercent", "progressiveRun", "receivedPass", "offensiveDuels", "offensiveDuelsWon"],
        "physical": ["accelerations", "duels", "duelsWon", "fouls", "foulsSuffered"]
    },
    
    # Volantes defensivos
    "defensive_midfielders": {
        "defensive": ["defensiveDuels", "defensiveDuelsWon", "interceptions", "ballRecoveries", "counterpressingRecoveries", "opponentHalfRecoveries"],
        "attacking": ["goals", "xgShot", "shots", "shotsOnTarget", "passesToFinalThird"],
        "passing": ["passes", "successfulPassesPercent", "progressivePasses", "successfulProgressivePassesPercent", "forwardPasses", "successfulForwardPassesPercent", "longPasses", "successfulLongPassesPercent"],
        "possession": ["duels", "duelsWon", "losses", "ownHalfLosses", "progressiveRun"],
        "physical": ["accelerations", "aerialDuels", "aerialDuelsWon", "duels", "duelsWon"]
    },
    
    # Meias centrais
    "central_midfielders": {
        "passing": ["passes", "successfulPassesPercent", "progressivePasses", "successfulProgressivePassesPercent", "keyPasses", "smartPasses", "successfulSmartPassesPercent", "passesToFinalThird", "successfulPassesToFinalThird"],
        "attacking": ["xgAssist", "assists", "shots", "shotsOnTarget", "goals", "xgShot", "touchInBox"],
        "defensive": ["defensiveDuels", "defensiveDuelsWon", "ballRecoveries", "interceptions", "counterpressingRecoveries"],
        "possession": ["dribbles", "successfulDribblesPercent", "progressiveRun", "receivedPass", "offensiveDuels", "offensiveDuelsWon"],
        "physical": ["accelerations", "fouls", "foulsSuffered", "duels", "duelsWon"]
    },
    
    # Meias atacantes
    "attacking_midfielders": {
        "attacking": ["goals", "assists", "shots", "shotsOnTarget", "xgShot", "xgAssist", "touchInBox", "keyPasses"],
        "passing": ["smartPasses", "successfulSmartPassesPercent", "throughPasses", "successfulThroughPassesPercent", "successfulPassesPercent"],
        "possession": ["dribbles", "successfulDribblesPercent", "progressiveRun", "receivedPass", "offensiveDuels", "offensiveDuelsWon"],
        "defensive": ["counterpressingRecoveries", "pressingDuels", "pressingDuelsWon", "ballRecoveries", "interceptions"],
        "physical": ["accelerations", "duels", "duelsWon", "fouls", "foulsSuffered"]
    },
    
    # Pontas/alas
    "wingers": {
        "attacking": ["goals", "assists", "xgAssist", "shots", "shotsOnTarget", "touchInBox", "crosses", "successfulCrossesPercent"],
        "possession": ["dribbles", "successfulDribblesPercent", "progressiveRun", "receivedPass", "offensiveDuels", "offensiveDuelsWon"],
        "passing": ["keyPasses", "passesToFinalThird", "successfulPassesToFinalThirdPercent", "successfulPassesPercent", "smartPasses"],
        "defensive": ["counterpressingRecoveries", "pressingDuels", "ballRecoveries", "interceptions", "defensiveDuels"],
        "physical": ["accelerations", "fouls", "foulsSuffered", "duels", "duelsWon"]
    },
    
    # Centroavantes
    "center_forwards": {
        "attacking": ["goals", "shots", "shotsOnTarget", "goalConversion", "xgShot", "touchInBox", "headShots", "headShotsOnTarget"],
        "possession": ["receivedPass", "offensiveDuels", "offensiveDuelsWon", "dribbles", "successfulDribblesPercent"],
        "passing": ["assists", "xgAssist", "keyPasses", "shotAssists", "successfulPassesPercent"],
        "defensive": ["counterpressingRecoveries", "pressingDuels", "pressingDuelsWon", "ballRecoveries"],
        "physical": ["accelerations", "duels", "duelsWon", "aerialDuels", "aerialDuelsWon", "fouls", "foulsSuffered"]
    }
}

# Mapeamento de posições específicas para categorias
POSITION_CATEGORY_MAPPING = {
    # Goleiros
    "gk": "goalkeeper",
    
    # Defensores
    "cb": "center_backs",
    "lcb": "center_backs", 
    "rcb": "center_backs",
    "lb": "full_backs",
    "rb": "full_backs",
    "lwb": "full_backs",
    "rwb": "full_backs",
    
    # Meio-campistas
    "dmf": "defensive_midfielders",
    "ldmf": "defensive_midfielders",
    "rdmf": "defensive_midfielders",
    "cmf": "central_midfielders",
    "lcmf": "central_midfielders",
    "rcmf": "central_midfielders",
    "amf": "attacking_midfielders",
    "lamf": "attacking_midfielders",
    "ramf": "attacking_midfielders",
    
    # Atacantes
    "lw": "wingers",
    "rw": "wingers",
    "lwf": "wingers",
    "rwf": "wingers",
    "cf": "center_forwards"
}
STAT_CATEGORY_MAP = {
    # Total stats (acumulativos)
    "goals": "total",
    "assists": "total",
    "gkCleanSheets": "total",
    "penalties": "total",
    "yellowCards": "total",
    "redCards": "total",
    "directRedCards": "total",
    "matches": "total",
    "matchesInStart": "total",
    "minutesOnField": "total",
    "secondAssists": "total",
    "thirdAssists": "total",
    
    # Percent stats (métricas de eficiência)
    "successfulPasses": "percent",
    "successfulPassesPercent": "percent",
    "successfulDribbles": "percent", 
    "successfulDribblesPercent": "percent",
    "successfulProgressivePasses": "percent",
    "successfulProgressivePassesPercent": "percent",
    "successfulPassesToFinalThird": "percent",
    "successfulPassesToFinalThirdPercent": "percent",
    "defensiveDuelsWon": "percent",
    "defensiveDuelsWonPercent": "percent",
    "offensiveDuelsWon": "percent",
    "offensiveDuelsWonPercent": "percent",
    "aerialDuelsWon": "percent",
    "aerialDuelsWonPercent": "percent",
    "fieldAerialDuelsWon": "percent",
    "pressingDuelsWon": "percent",
    "duelsWon": "percent",
    "duelsWonPercent": "percent",
    "shotsOnTarget": "percent",
    "shotsOnTargetPercent": "percent",
    "goalConversion": "percent",
    "successfulLongPasses": "percent",
    "successfulLongPassesPercent": "percent",
    "successfulForwardPasses": "percent",
    "successfulForwardPassesPercent": "percent",
    "successfulBackPasses": "percent",
    "successfulBackPassesPercent": "percent",
    "successfulThroughPasses": "percent",
    "successfulThroughPassesPercent": "percent",
    "successfulKeyPasses": "percent",
    "successfulVerticalPasses": "percent",
    "successfulVerticalPassesPercent": "percent",
    "successfulLateralPasses": "percent",
    "successfulLateralPassesPercent": "percent",
    "successfulCrosses": "percent",
    "successfulCrossesPercent": "percent",
    "successfulSmartPasses": "percent",
    "successfulSmartPassesPercent": "percent",
    "successfulPenalties": "percent",
    "penaltiesConversion": "percent",
    "successfulSlidingTackles": "percent",
    "successfulSlidingTacklesPercent": "percent",
    "successfulLinkupPlays": "percent",
    "successfulLinkupPlaysPercent": "percent",
    "successfulShotAssists": "percent",
    "dribblesAgainstWon": "percent",
    "dribblesAgainstWonPercent": "percent",
    "gkSaves": "percent",
    "gkSavesPercent": "percent",
    "gkSuccessfulExits": "percent",
    "gkSuccessfulExitsPercent": "percent",
    "gkAerialDuelsWon": "percent",
    "gkAerialDuelsWonPercent": "percent",
    "successfulGoalKicks": "percent",
    "successfulGoalKicksPercent": "percent",
    "headShotsOnTarget": "percent",
    "headShotsOnTargetPercent": "percent",
    "directFreeKicksOnTarget": "percent",
    "directFreeKicksOnTargetPercent": "percent",
    "win": "percent",
    "newDuelsWon": "percent",
    "newDefensiveDuelsWon": "percent",
    "newOffensiveDuelsWon": "percent",
    "newSuccessfulDribbles": "percent",
    "yellowCardsPerFoul": "percent",
    
    # Average stats (métricas por jogo)
    "aerialDuels": "average",
    "recoveries": "average",
    "ballRecoveries": "average",
    "defensiveDuels": "average",
    "offensiveDuels": "average",
    "duels": "average",
    "passes": "average",
    "crosses": "average",
    "progressiveRun": "average",
    "progressivePasses": "average",
    "interceptions": "average",
    "touchInBox": "average",
    "shots": "average",
    "headShots": "average",
    "keyPasses": "average",
    "smartPasses": "average",
    "xg": "average",
    "xgAssist": "average",
    "xgShot": "average",
    "receivedPass": "average",
    "blocks": "average",
    "shotsBlocked": "average",
    "clearances": "average",
    "slidingTackles": "average",
    "pressingDuels": "average",
    "counterpressingRecoveries": "average",
    "forwardPasses": "average",
    "backPasses": "average",
    "throughPasses": "average",
    "verticalPasses": "average",
    "lateralPasses": "average",
    "longPasses": "average",
    "passesToFinalThird": "average",
    "dribbles": "average",
    "dribblesAgainst": "average",
    "successfulDuels": "average",
    "looseBallDuels": "average",
    "looseBallDuelsWon": "average",
    "freeKicks": "average",
    "freeKicksOnTarget": "average",
    "directFreeKicks": "average",
    "corners": "average",
    "shotAssists": "average",
    "shotOnTargetAssists": "average",
    "linkupPlays": "average",
    "opponentHalfRecoveries": "average",
    "dangerousOpponentHalfRecoveries": "average",
    "ballLosses": "average",
    "losses": "average",
    "ownHalfLosses": "average",
    "dangerousOwnHalfLosses": "average",
    "fouls": "average",
    "foulsSuffered": "average",
    "defensiveActions": "average",
    "successfulDefensiveAction": "average",
    "attackingActions": "average",
    "successfulAttackingActions": "average",
    "accelerations": "average",
    "missedBalls": "average",
    "offsides": "average",
    "passLength": "average",
    "longPassLength": "average",
    "dribbleDistanceFromOpponentGoal": "average",
    
    # Goalkeeper metrics
    "gkGoalsConceded": "average", 
    "gkExits": "average",
    "gkShotsAgainst": "average",
    "gkAerialDuels": "average",
    "goalKicks": "average",
    "goalKicksShort": "average",
    "goalKicksLong": "average",
    
    # New metrics that appeared in the sample
    "fieldAerialDuels": "average"
}
def calculate_sigma(min_minutes=180):  # Típico: 2 jogos completos
    """
    Calcula o desvio padrão das estatísticas por posição,
    filtrando jogadores com poucos minutos.
    
    Args:
        min_minutes: Mínimo de minutos jogados para considerar o jogador
        
    Returns:
        Dicionário com desvios padrão por posição e estatística
    """
    db_by_id = get_player_database_by_id()
    avg = get_average_statistics()
    sigma = {}
    
    # Pré-inicializar a estrutura do dicionário
    for position in avg.keys():
        sigma[position] = {}
        for category in ['total', 'percent', 'average']:
            sigma[position][category] = {}
            for stat in avg[position][category]:
                sigma[position][category][stat] = 0
    
    # Calcular desvio padrão
    for position, pos_avg in avg.items():
        position_counts = {}
        valid_players = {}  # Armazenar jogadores válidos por estatística
        
        # Primeiro passo: identificar jogadores válidos por posição
        for player_id, player_stats in db_by_id.items():
            # Filtrar por posição
            if not player_stats.get('positions') or not any(position == p['position']['code'] for p in player_stats['positions']):
                continue
                
            # Filtrar por minutos jogados
            if player_stats.get('total', {}).get('minutesOnField', 0) < min_minutes:
                continue
                
            # Jogador válido para esta posição
            for category in ['total', 'percent', 'average']:
                for stat in pos_avg[category]:
                    if category in player_stats and stat in player_stats[category] and player_stats[category][stat] != 0:
                        # Adicionar jogador à lista de válidos para esta estatística
                        if (category, stat) not in valid_players:
                            valid_players[(category, stat)] = []
                        valid_players[(category, stat)].append(player_id)
        
        # Segundo passo: calcular desvio padrão usando apenas jogadores válidos
        for category in ['total', 'percent', 'average']:
            for stat in pos_avg[category]:
                position_counts[(category, stat)] = 0
                sigma[position][category][stat] = 0
                
                # Usar apenas jogadores válidos para esta estatística
                for player_id in valid_players.get((category, stat), []):
                    player_stats = db_by_id[player_id]
                    
                    # Calcula a diferença quadrada
                    sigma_i = (player_stats[category][stat] - pos_avg[category][stat]) ** 2
                    sigma[position][category][stat] += sigma_i
                    position_counts[(category, stat)] += 1
                
                # Calcular o desvio padrão final
                n = position_counts[(category, stat)]
                if n > 1:  # Precisamos de ao menos 2 jogadores para calcular desvio padrão
                    sigma[position][category][stat] = round((sigma[position][category][stat] / n) ** 0.5, 2)
                else:
                    sigma[position][category][stat] = 0
                    
                print(f"Posição {position}, {category}.{stat}: {n} jogadores válidos")

    return sigma

# Adicionar após as importações existentes


# Métricas onde valores menores são melhores (para inverter percentis)
NEGATIVE_METRICS = [
    "yellowCards", "redCards", "fouls", "losses", 
    "ownHalfLosses", "dangerousOwnHalfLosses", "offsides",
    "gkGoalsConceded", "ballLosses", "dangerousOwnHalfLosses",
    "missedBalls", "directRedCards"
]

# Implementação da função aprimorada
def z_score_and_percentiles_aprimorado(player: Dict[str, Any], min_minutes: int = 180) -> Dict[str, Any]:
    """
    Calcular z-scores e percentis com abordagem robusta e flexível.
    
    Args:
        player: Dicionário com dados do jogador
        min_minutes: Mínimo de minutos jogados para análise confiável
        
    Returns:
        Dicionário com z-scores e percentis organizados por categorias
    """
    # Verificação de minutos jogados
    if player.get('total', {}).get('minutesOnField', 0) < min_minutes:
        return {
            'z_scores': {},
            'percentiles': {},
            'warning': f"Jogador com menos de {min_minutes} minutos jogados. Estatísticas podem não ser representativas."
        }
        
    # Obter estatísticas específicas da posição e médias
    sigma = get_sigma_by_position()
    mu = get_average_statistics()
    
    # Determinar grupo de posição do jogador
    position_group = get_player_position_group(player)
    
    # Definir posição primária para cálculos
    position = player['positions'][0]['position']['code']
    
    # Inicializar estruturas de dados
    z_scores = {}
    percentiles = {}
    
    # PASSO 1: Calcular z-scores e percentis para TODAS as métricas disponíveis
    for category in ['total', 'percent', 'average']:
        z_scores[category] = {}
        percentiles[category] = {}
        
        # Processar todas as métricas disponíveis no jogador
        if category in player:
            for metric, value in player[category].items():
                # Pular valores não numéricos
                if not isinstance(value, (int, float)):
                    continue
                    
                # Verificar se a métrica existe nas médias de posição
                if category in mu[position] and metric in mu[position][category]:
                    if sigma[position][category][metric] == 0:
                        z_scores[category][metric] = 0
                        percentiles[category][metric] = 50
                    else:
                        # Calcular z-score
                        z = (value - mu[position][category][metric]) / sigma[position][category][metric]
                        
                        # Converter para percentil (0-100)
                        p = stats.norm.cdf(z) * 100
                        
                        # Armazenar resultados
                        z_scores[category][metric] = z
                        percentiles[category][metric] = round(p,2)
                        
                        # Inverter percentis para métricas negativas
                        if metric in NEGATIVE_METRICS:
                            z_scores[category][metric] = -z_scores[category][metric]
                            percentiles[category][metric] = 100 - percentiles[category][metric]
    
    # PASSO 2: Criar tabela de mapeamento de aliases para busca flexível
    metric_aliases = create_metric_aliases_map()
    
    # PASSO 3: Organizar percentis por categorias de futebol com base no grupo de posição
    football_categories = organize_percentiles_by_position_group(
        percentiles, 
        position_group, 
        metric_aliases
    )
    
    # Retornar resultados completos
    return {
        'z_scores': z_scores,                    # Z-scores originais (todos)
        'percentiles': percentiles,              # Percentis originais (todos)
        'football_categories': football_categories,  # Percentis organizados por categoria
        'position_group': position_group         # Grupo de posição para contexto
    }

def get_player_position_group(player: Dict[str, Any]) -> str:
    """
    Determinar o grupo de posição do jogador com base na posição principal
    
    Args:
        player: Dicionário com dados do jogador
        
    Returns:
        String com o grupo de posição (ex: "goalkeeper", "center_backs", etc.)
    """
    if not player.get('positions'):
        return "unknown"
    
    primary_position = player['positions'][0]['position']['code'].lower()
    
    # Usar o mapeamento de posição para categoria
    return POSITION_CATEGORY_MAPPING.get(primary_position, "outfield")

def get_player_percentile(player: Dict[str, Any], metric_name: str, category: str = None) -> float:
    """
    Função universal para obter percentil de qualquer métrica do jogador, 
    independente da categoria ou estrutura de dados.
    
    Args:
        player: Dicionário com dados do jogador
        metric_name: Nome da métrica desejada
        category: Categoria opcional para busca específica (ex: "attacking", "defensive")
        
    Returns:
        Valor percentil (0-100) ou 0 se não encontrado
    """
    # Verificar se o jogador já tem percentis calculados
    if '_percentiles_cache' not in player:
        percentile_data = z_score_and_percentiles_aprimorado(player)
        player['_percentiles_cache'] = {
            'percentiles': percentile_data['percentiles'],
            'football_categories': percentile_data.get('football_categories', {})
        }
        # Verificar se já tem percentis calculados em formatos alternativos
    # Acesso aos percentis de forma unificada
    percentiles = player['_percentiles_cache']['percentiles']
    football_categories = player['_percentiles_cache'].get('football_categories', {})
    
    # Buscar na categoria específica de futebol, se fornecida
    if category and category in football_categories and metric_name in football_categories[category]:
        return football_categories[category][metric_name]
    
    # Buscar em todas as categorias de futebol
    for cat, metrics in football_categories.items():
        if metric_name in metrics:
            return metrics[metric_name]
    
    # Buscar nas categorias originais
    for cat in ['total', 'percent', 'average']:
        if cat in percentiles and metric_name in percentiles[cat]:
            return percentiles[cat][metric_name]
    
    # Usar aliases como último recurso
    metric_aliases = create_metric_aliases_map()
    if metric_name in metric_aliases:
        cat, met = metric_aliases[metric_name].split('.')
        if cat in percentiles and met in percentiles[cat]:
            return percentiles[cat][met]
    
    # Tentar encontrar qualquer métrica com nome semelhante (busca flexível)
    for cat in ['total', 'percent', 'average']:
        if cat not in percentiles:
            continue
            
        for key in percentiles[cat].keys():
            if metric_name.lower() in key.lower() or key.lower() in metric_name.lower():
                return percentiles[cat][key]
    
    # Não encontrado após todas as tentativas
    return 0
def create_metric_aliases_map() -> Dict[str, str]:
    """
    Criar mapeamento de aliases para métricas para busca flexível
    
    Returns:
        Dicionário com mapeamento de nomes alternativos para caminhos de métricas
    """
    aliases = {}
    
    # Adicionar mapeamento direto do STAT_CATEGORY_MAP
    for metric, category in STAT_CATEGORY_MAP.items():
        aliases[metric] = f"{category}.{metric}"
    
    # Adicionar aliases comuns para resolver problemas de nomenclatura
    common_aliases = {
        "blocks": ["shotsBlocked", "blockedShots"],
        "recoveries": ["ballRecoveries", "recovery"],
        "aerialDuelsWon": ["fieldAerialDuelsWon"],
        "successfulPasses": ["successfulPass", "passAccuracy"],
        "progressivePasses": ["progressivePass", "progressivePassAccuracy"],
        "shots_on_target": ["shotsOnTarget"],
        "pass_accuracy": ["successfulPassesPercent"],
        "defensive_duels_won": ["defensiveDuelsWon"],
        "aerial_duels_won": ["aerialDuelsWon"],
        "offensive_duels_won": ["offensiveDuelsWon"],
        "progressive_runs": ["progressiveRun"],
        "ball_recoveries": ["ballRecoveries", "recoveries"],
    }
    
    for main_metric, alias_list in common_aliases.items():
        for alias in alias_list:
            if alias in STAT_CATEGORY_MAP:
                category = STAT_CATEGORY_MAP[alias]
                aliases[alias] = f"{category}.{main_metric}"
                aliases[main_metric] = f"{category}.{alias}"
    
    return aliases


def organize_percentiles_by_position_group(
    percentiles: Dict[str, Dict[str, float]], 
    position_group: str,
    metric_aliases: Dict[str, str]
) -> Dict[str, Dict[str, float]]:
    """
    Organizar percentis em categorias relevantes por grupo de posição
    
    Args:
        percentiles: Dicionário com todos os percentis calculados
        position_group: Grupo de posição do jogador
        metric_aliases: Mapeamento de aliases de métricas
        
    Returns:
        Dicionário com percentis organizados por categorias específicas de futebol
    """
    # Inicializar categorias padrão (para jogadores de linha)
    categories = {
        "attacking": {},
        "passing": {},
        "defensive": {},
        "possession": {},
        "physical": {}
    }
    
    # Se for goleiro, usar categorias específicas para goleiro
    if position_group == "goalkeeper":
        categories = {
            "goalkeeping": {},
            "passing": {},
            "positioning": {}
        }
    
    # Função auxiliar para buscar valor percentil de qualquer métrica
    def get_percentile_value(metric_name: str) -> float:
        # Verificar o alias direto primeiro
        if metric_name in metric_aliases:
            category, metric = metric_aliases[metric_name].split('.')
            if category in percentiles and metric in percentiles[category]:
                return percentiles[category][metric]
        
        # Verificar em todas as categorias
        for category in ['total', 'percent', 'average']:
            if category in percentiles and metric_name in percentiles[category]:
                return percentiles[category][metric_name]
        
        # Buscar com aliases
        for alias, full_path in metric_aliases.items():
            if metric_name == alias or metric_name in alias or alias in metric_name:
                category, metric = full_path.split('.')
                if category in percentiles and metric in percentiles[category]:
                    return percentiles[category][metric]
        
        return 0  # Não encontrado
    
    # Obter métricas específicas para este grupo de posição
    if position_group in POSITION_KEY_METRICS:
        for category, metrics in POSITION_KEY_METRICS[position_group].items():
            if category in categories:
                for metric in metrics:
                    value = get_percentile_value(metric)
                    if value > 0:  # Só incluir se tiver um valor válido
                        categories[category][metric] = value
    
    return categories

def calculate_profile_fit(player, profile_data):
    """
    Calculate tactical fit score for a specific profile using the unified percentile system
    
    Args:
        player: Player data dictionary
        profile_data: Profile definition with key_stats and weights
    
    Returns:
        Fit score from 0-100
    """
    if not profile_data.get("key_stats"):
        return 0
        
    total_score = 0
    total_weight = 0
    
    for stat, weight in profile_data["key_stats"].items():
        # Use the universal percentile accessor
        stat_percentile = get_player_percentile(player, stat)
        
        if stat_percentile > 0:  # Only include if metric was found
            total_score += stat_percentile * weight
            total_weight += weight
    
    # Calculate final score
    if total_weight == 0:
        return 0
        
    return round(total_score / total_weight)

def get_stat_from_category(stat_with_category, all_percentiles):
    """
    Get a percentile value for a stat from a specific category.
    
    Args:
        stat_with_category: String in format "category.statName" (e.g., "average.goals")
        all_percentiles: Dictionary with all percentiles
        
    Returns:
        Percentile value for the stat in the specified category, or 0 if not found
    """
    try:
        category, stat_name = stat_with_category.split(".")
        
        if category in all_percentiles and stat_name in all_percentiles[category]:
            return all_percentiles[category][stat_name]
    except (ValueError, AttributeError, KeyError):
        pass
    
    # Return 0 if not found or if there was an error
    return 0

def get_stat_from_calculation(all_percentiles, calc_fn):
    """
    Calculate a derived metric from percentiles.
    
    Args:
        all_percentiles: Dictionary with all percentiles
        calc_fn: Function to calculate a derived metric
        
    Returns:
        Calculated value
    """
    try:
        return calc_fn(all_percentiles)
    except:
        return 0


def get_fit_category(score):
    """
    Convert numerical fit score to category label
    
    Args:
        score: Fit score from 0-100
        
    Returns:
        String category
    """
    if score >= 85:
        return "Perfeito"
    elif score >= 75:
        return "Excelente"  
    elif score >= 65:
        return "Muito bom"
    elif score >= 55:
        return "Bom"
    elif score >= 45:
        return "Regular"
    elif score >= 35:
        return "Abaixo da média"
    else:
        return "Inadequado"
    

def swot_analysis(player, min_percentile_strength=75, max_percentile_weakness=30, min_minutes=180, language='pt'):
    """
    Perform a SWOT analysis on a player based on their statistical percentiles
    
    Args:
        player: Player data dictionary
        min_percentile_strength: Minimum percentile to consider as a strength (default: 75)
        max_percentile_weakness: Maximum percentile to consider as a weakness (default: 30)
        min_minutes: Minimum minutes played for reliable analysis
        language: Language for AI insights ('pt', 'en', 'es', or 'bg')
    
    Returns:
        SwotAnalysis object with strengths, weaknesses, opportunities, and threats
    """
    # Ensure we have percentiles calculated using the improved system
    if  '_percentiles_cache' not in player:
        percentile_data = z_score_and_percentiles_aprimorado(player, min_minutes)
        if 'warning' in percentile_data:
            return SwotAnalysis(
                strengths=[],
                weaknesses=[],
                opportunities=[
                    AIInsight(insight="Insufficient playing time for reliable analysis", based_on=[], importance=3)
                ],
                threats=[
                    AIInsight(insight="Limited data may affect scouting reliability", based_on=[], importance=3)
                ],
                summary="Player has insufficient minutes for a reliable statistical analysis"
            )
        
        # Cache the results for future use
        player['_percentiles_cache'] = {
            'percentiles': percentile_data['percentiles'],
            'football_categories': percentile_data.get('football_categories', {})
        }
    
    # Get position type and group
    is_goalkeeper = is_player_goalkeeper(player)
    position_group = get_player_position_group(player)
    
    # Define relevant categories based on position group
    categories = ["goalkeeping", "passing", "positioning"] if is_goalkeeper else [
        "attacking", "passing", "defensive", "possession", "physical"
    ]
    
    # Get key metrics for this position group from our predefined mappings
    key_metrics = {}
    if position_group in POSITION_KEY_METRICS:
        for category in categories:
            if category in POSITION_KEY_METRICS[position_group]:
                key_metrics[category] = POSITION_KEY_METRICS[position_group][category]
    
    strengths = []
    weaknesses = []
    
    # Check percentiles for key metrics using our universal accessor
    for category, metrics in key_metrics.items():
        for metric in metrics:
            # Use the universal percentile accessor
            value = get_player_percentile(player, metric, category)
            
            # Check if stat is a strength
            if value >= min_percentile_strength:
                strengths.append(Stat(stat_name=metric, percentile=value, category=category))
            
            # Check if stat is a weakness
            elif value <= max_percentile_weakness:
                weaknesses.append(Stat(stat_name=metric, percentile=value, category=category))
    
    # Sort strengths and weaknesses by percentile
    strengths.sort(key=lambda x: x.percentile, reverse=True)
    weaknesses.sort(key=lambda x: x.percentile)
    
    # Generate AI insights
    try:
        # Format the stats for Claude
        formatted_strengths = format_stats_list(strengths)
        formatted_weaknesses = format_stats_list(weaknesses)
        
        # Get player basic info
        player_info = {
            "name": player.get("name", "Unknown"),
            "age": player.get("age", "Unknown"),
            "positions": [pos['position']['name'] for pos in player.get('positions', [])] 
                        if player.get('positions') else ["Unknown"],
            "foot": player.get("foot", "Unknown"),
            "height": player.get("height", "Unknown"),
            "weight": player.get("weight", "Unknown")
        }
        
        position_context = "goalkeeper" if is_goalkeeper else "outfield player"
        
        # Use the appropriate language prompt
        swot_analysis_prompts = {
    "en": f"""Player Profile:
PLAYER: {player_info['name']}
AGE: {player_info['age']}
POSITION(S): {', '.join(player_info['positions'])} ({position_context})
FOOT: {player_info['foot']}
HEIGHT: {player_info['height']} cm
WEIGHT: {player_info['weight']} kg

STATISTICAL STRENGTHS:
{formatted_strengths}

STATISTICAL WEAKNESSES:
{formatted_weaknesses}

Based on these statistics, provide:
1. 3-5 strategic OPPORTUNITIES that leverage the player's strengths
2. 2-4 potential THREATS that could affect the player's performance
3. A brief overall summary of the player's profile (1-2 sentences)
IMPORTANT: RESPOND IN ENGLISH
""",
    
    
    "pt": f"""Perfil do Jogador:
JOGADOR: {player_info['name']}
IDADE: {player_info['age']}
POSIÇÃO(ÕES): {', '.join(player_info['positions'])} ({position_context})
PÉ: {player_info['foot']}
ALTURA: {player_info['height']} cm
PESO: {player_info['weight']} kg

PONTOS FORTES ESTATÍSTICOS:
{formatted_strengths}

PONTOS FRACOS ESTATÍSTICOS:
{formatted_weaknesses}

Com base nessas estatísticas, forneça:
1. 3-5 OPORTUNIDADES estratégicas que aproveitam os pontos fortes do jogador
2. 2-4 AMEAÇAS potenciais que poderiam afetar o desempenho do jogador
3. Um breve resumo geral do perfil do jogador (1-2 frases)
IMPORTANTE: RESPONDA EM PORTUGUÊS
""",
    
    "es": f"""Perfil del Jugador:
JUGADOR: {player_info['name']}
EDAD: {player_info['age']}
POSICIÓN(ES): {', '.join(player_info['positions'])} ({position_context})
PIE: {player_info['foot']}
ALTURA: {player_info['height']} cm
PESO: {player_info['weight']} kg

FORTALEZAS ESTADÍSTICAS:
{formatted_strengths}

DEBILIDADES ESTADÍSTICAS:
{formatted_weaknesses}

Basado en estas estadísticas, proporcione:
1. 3-5 OPORTUNIDADES estratégicas que aprovechen las fortalezas del jugador
2. 2-4 AMENAZAS potenciales que podrían afectar el rendimiento del jugador
3. Un breve resumen general del perfil del jugador (1-2 frases)
IMPORTANTE: RESPONDA EN ESPAÑOL
""",
    
    "bg": f"""Профил на Играча:
ИГРАЧ: {player_info['name']}
ВЪЗРАСТ: {player_info['age']}
ПОЗИЦИЯ(И): {', '.join(player_info['positions'])} ({position_context})
КРАК: {player_info['foot']}
ВИСОЧИНА: {player_info['height']} см
ТЕГЛО: {player_info['weight']} кг

СТАТИСТИЧЕСКИ СИЛНИ СТРАНИ:
{formatted_strengths}

СТАТИСТИЧЕСКИ СЛАБИ СТРАНИ:
{formatted_weaknesses}

Въз основа на тези статистики, предоставете:
1. 3-5 стратегически ВЪЗМОЖНОСТИ, които използват силните страни на играча
2. 2-4 потенциални ЗАПЛАХИ, които биха могли да повлияят на представянето на играча
3. Кратко общо резюме на профила на играча (1-2 изречения)
IMPORTANTE: ОТГОВОРЕТЕ НА БЪЛГАРСКИ
"""
}
        
        # Create system prompt and call API as in original function
        system_prompt = """You are an expert football scout and analyst. 
Analyze a player's statistical strengths and weaknesses to generate strategic insights.
Provide specific opportunities that leverage the player's strengths, and identify 
realistic threats that could limit their effectiveness due to their weaknesses.
<IMPORTANT>
ALWAYS RESPOND IN THE LANGUAGE OF THE USER PROMPT.
</IMPORTANT>"""
        
        user_message = swot_analysis_prompts.get(language, swot_analysis_prompts["pt"])
        tools = [{
            "name": "swot_output",
            "description": "Generate SWOT analysis based on player strengths and weaknesses",
            "input_schema": {
                "type": "object",
                "properties": {
                    "opportunities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "insight": {"type": "string"},
                                "based_on": {"type": "array", "items": {"type": "string"}},
                                "importance": {"type": "integer", "minimum": 1, "maximum": 3}
                            }
                        }
                    },
                    "threats": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "insight": {"type": "string"},
                                "based_on": {"type": "array", "items": {"type": "string"}},
                                "importance": {"type": "integer", "minimum": 1, "maximum": 3}
                            }
                        }
                    },
                    "summary": {"type": "string"}
                }
            }
        }]
        
        # Initialize session and call Claude API
        from core.session import UnifiedSession
        session = UnifiedSession()
        
        response = session.call_claude_api(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
            tools=tools,
            tool_choice={"type": "tool","name": "swot_output"}
        )
        
        # Extract AI insights from response
        ai_output = extract_ai_insights_from_response(response)
        
        # Call Claude API and extract insights
        # [API call code remains unchanged]
        
        # Return SWOT analysis with results
        return SwotAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=ai_output.get('opportunities', []),
            threats=ai_output.get('threats', []),
            summary=ai_output.get('summary', '')
        )
    
    except Exception as e:
        # Fallback for API failures
        print(f"Error generating AI insights: {str(e)}")
        return create_fallback_swot_analysis(strengths, weaknesses)
    
def is_player_goalkeeper(player):
    """Determine if a player is a goalkeeper based on position data"""
    if not player.get('positions'):
        return False
    
    # Check if any position is goalkeeper
    for pos in player['positions']:
        position_code = pos['position']['code'].lower()
        if position_code == 'gk':
            return True
    
    return False

def filter_position_percentiles(percentiles, is_goalkeeper):
    """Filter percentiles to include only position-relevant statistics"""
    filtered_percentiles = {category: {} for category in percentiles}
    
    # Define goalkeeper-specific stats
    gk_stats = [
        "gk", "saves", "goalsConceded", "cleanSheets", "penaltiesSaved", 
        "okpk", "exits", "exitsSuccess", "aerialDuels"
    ]
    
    # Define outfield-specific stats (partial list - these should not appear for GKs)
    outfield_stats = [
        "dribbles", "successfulDribbles", "defensiveDuels", "aerialDuels", 
        "tackles", "interceptions", "shots", "xg", "goals"
    ]
    
    for category in percentiles:
        for stat, value in percentiles[category].items():
            # Include stat if it's for goalkeeper and player is goalkeeper
            if is_goalkeeper and any(gk_term in stat.lower() for gk_term in gk_stats):
                filtered_percentiles[category][stat] = value
            # Include stat if it's for outfield player and player is outfield
            elif not is_goalkeeper and not any(gk_term in stat.lower() for gk_term in gk_stats):
                filtered_percentiles[category][stat] = value
    
    return filtered_percentiles

def format_stats_list(stats_list):
    """Format statistics in a readable way"""
    return "\n".join([f"- {format_stat_name(s.stat_name)}: {s.percentile:.1f}th percentile" 
                      for s in stats_list])

def extract_ai_insights_from_response(response):
    """Extract AI insights from Claude API response"""
    if hasattr(response, 'content') and response.content:
        for content in response.content:
            if hasattr(content, 'type') and content.type == 'tool_use':
                result = content.input
                if isinstance(result, str):
                    # Parse JSON string if the API returns a string instead of a dict
                    try:
                        import json
                        result = json.loads(result)
                    except json.JSONDecodeError:
                        print(f"Error parsing API response string: {result[:100]}...")
                        return {'opportunities': [], 'threats': [], 'summary': ""}
                
                # Create AIInsight objects
                opportunities = [
                    AIInsight(
                        insight=item.get("insight", ""),
                        based_on=item.get("based_on", []),
                        importance=item.get("importance", 2)
                    )
                    for item in result.get("opportunities", [])
                ]
                
                threats = [
                    AIInsight(
                        insight=item.get("insight", ""),
                        based_on=item.get("based_on", []),
                        importance=item.get("importance", 2)
                    )
                    for item in result.get("threats", [])
                ]
                
                return {
                    'opportunities': opportunities,
                    'threats': threats,
                    'summary': result.get("summary", "")
                }
    
    return {'opportunities': [], 'threats': [], 'summary': ""}

def create_fallback_swot_analysis(strengths, weaknesses):
    """Create fallback SWOT analysis when AI generation fails"""
    return SwotAnalysis(
        strengths=strengths,
        weaknesses=weaknesses,
        opportunities=[
            AIInsight(insight="Focus on leveraging strengths in tactical setup", based_on=[], importance=2),
            AIInsight(insight="Consider targeted training to address weaknesses", based_on=[], importance=2)
        ],
        threats=[
            AIInsight(insight="May face challenges against opponents who target weaknesses", based_on=[], importance=2)
        ],
        summary="Player shows a mix of statistical strengths and weaknesses that should be considered in tactical planning."
    )

def format_stat_name(stat_name):
    """Convert camelCase to readable format"""
    import re
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', stat_name).title()

POSITION_KEY_STATS = {
    # Goalkeepers
    "gk": [
        "gkSaves", "gkGoalsConceded", "gkCleanSheets", "gkExits", 
        "aerialDuels", "successfulPasses", "gkSavesPercent"
    ],
    
    # Full-backs
    "lb": ["ballRecoveries", "defensiveDuelsWon", "offensiveDuelsWon", "successfulDribbles", 
            "successfulPasses", "crosses", "progressiveRun", "progressivePasses", 
            "interceptions", "touchInBox"],
    "rb": ["ballRecoveries", "defensiveDuelsWon", "offensiveDuelsWon", "successfulDribbles", 
            "successfulPasses", "crosses", "progressiveRun", "progressivePasses", 
            "interceptions", "touchInBox"],
    "lwb": ["ballRecoveries", "defensiveDuelsWon", "offensiveDuelsWon", "successfulDribbles", 
            "successfulPasses", "crosses", "progressiveRun", "progressivePasses", 
            "assists", "shots"],
    "rwb": ["ballRecoveries", "defensiveDuelsWon", "offensiveDuelsWon", "successfulDribbles", 
            "successfulPasses", "crosses", "progressiveRun", "progressivePasses", 
            "assists", "shots"],
    
    # Central defenders
    "cb": ["ballRecoveries", "defensiveDuelsWon", "aerialDuelsWon", "interceptions", 
            "clearances", "successfulPasses", "progressivePasses", "shotsBlocked"],
    "lcb": ["ballRecoveries", "defensiveDuelsWon", "aerialDuelsWon", "interceptions", 
            "clearances", "successfulPasses", "progressivePasses", "shotsBlocked"],
    "rcb": ["ballRecoveries", "defensiveDuelsWon", "aerialDuelsWon", "interceptions", 
            "clearances", "successfulPasses", "progressivePasses", "shotsBlocked"],
    
    # Midfielders
    "dmf": ["ballRecoveries", "defensiveDuelsWon", "interceptions", "aerialDuelsWon", 
            "successfulPasses", "progressivePasses", "smartPasses", "duelsWon"],
    "cmf": ["successfulPasses", "progressivePasses", "keyPasses", "smartPasses", 
            "defensiveDuelsWon", "ballRecoveries", "duelsWon", "assists", "shots", "goals"],
    "lcmf": ["successfulPasses", "progressivePasses", "keyPasses", "smartPasses", 
                "defensiveDuelsWon", "ballRecoveries", "duelsWon", "assists", "shots", "goals"],
    "rcmf": ["successfulPasses", "progressivePasses", "keyPasses", "smartPasses", 
                "defensiveDuelsWon", "ballRecoveries", "duelsWon", "assists", "shots", "goals"],
    "amf": ["keyPasses", "assists", "smartPasses", "successfulDribbles", "progressiveRun", 
            "shots", "goals", "xgAssist", "touchInBox", "successfulPasses"],
    
    # Forwards
    "cf": ["goals", "shots", "shotsOnTarget", "xg", "touchInBox", "aerialDuelsWon", 
            "offensiveDuelsWon", "goalConversion", "receivedPass"],
    "lw": ["successfulDribbles", "progressiveRun", "crosses", "keyPasses", "assists", 
            "xgAssist", "shots", "goals", "touchInBox", "offensiveDuelsWon"],
    "rw": ["successfulDribbles", "progressiveRun", "crosses", "keyPasses", "assists", 
            "xgAssist", "shots", "goals", "touchInBox", "offensiveDuelsWon"]
}

# Get weighted ranking for different position types
STAT_WEIGHTS = {
    # Goalkeepers
    "gk": {
        "gkSaves": 5, "gkCleanSheets": 5, "gkSavesPercent": 4, "gkGoalsConceded": 3,
        "gkExits": 3, "successfulPasses": 2, "aerialDuels": 2
    },
    
    # Defenders
    "defender": {
        "defensiveDuelsWon": 5, "interceptions": 5, "clearances": 4, "aerialDuelsWon": 4,
        "ballRecoveries": 3, "successfulPasses": 3, "shotsBlocked": 3, "progressivePasses": 2
    },
    
    # Full-backs
    "fullback": {
        "defensiveDuelsWon": 4, "ballRecoveries": 4, "crosses": 3, "progressiveRun": 3,
        "successfulPasses": 3, "interceptions": 3, "offensiveDuelsWon": 2
    },
    
    # Midfielders 
    "midfielder": {
        "successfulPasses": 5, "progressivePasses": 4, "keyPasses": 3, "ballRecoveries": 3,
        "defensiveDuelsWon": 3, "duelsWon": 2, "assists": 2, "shots": 1
    },
    
    # Attacking midfielders
    "attacking_mid": {
        "keyPasses": 5, "assists": 4, "smartPasses": 4, "successfulDribbles": 3,
        "progressiveRun": 3, "shots": 3, "goals": 2, "touchInBox": 2
    },
    
    # Forwards
    "forward": {
        "goals": 5, "shots": 4, "shotsOnTarget": 4, "xg": 3, "touchInBox": 3,
        "goalConversion": 3, "offensiveDuelsWon": 2, "successfulDribbles": 2 
    }
}

# Position to weight category mapping
POSITION_WEIGHT_CATEGORY = {
    "gk": "gk",
    "lb": "fullback", "rb": "fullback", "lwb": "fullback", "rwb": "fullback",
    "cb": "defender", "lcb": "defender", "rcb": "defender",
    "dmf": "midfielder", "cmf": "midfielder", "lcmf": "midfielder", "rcmf": "midfielder",
    "amf": "attacking_mid",
    "cf": "forward", "lw": "forward", "rw": "forward"
}

# Map stats to their appropriate categories
STAT_CATEGORY_MAP = {
    # Total stats
    "goals": "total",
    "assists": "total",
    "gkCleanSheets": "total",
    "penalties": "total",
    
    # Percent stats (efficiency metrics)
    "successfulPasses": "percent",
    "successfulDribbles": "percent", 
    "successfulProgressivePasses": "percent",
    "successfulPassesToFinalThird": "percent",
    "defensiveDuelsWon": "percent",
    "offensiveDuelsWon": "percent",
    "aerialDuelsWon": "percent",
    "pressingDuelsWon": "percent",
    "duelsWon": "percent",
    "shotsOnTarget": "percent",
    "goalConversion": "percent",
    "successfulLongPasses": "percent",
    "successfulPenalties": "percent",
    "successfulSlidingTackles": "percent",
    "gkSavesPercent": "percent",
    "gkSuccessfulExits": "percent",
    "gkAerialDuelsWon": "percent",
    
    # Average stats (per-match metrics)
    "gkSaves": "average",
    "gkGoalsConceded": "average", 
    "gkExits": "average",
    "aerialDuels": "average",
    "ballRecoveries": "average",
    "defensiveDuels": "average",
    "offensiveDuels": "average",
    "successfulDuels": "average",
    "passes": "average",
    "crosses": "average",
    "progressiveRun": "average",
    "progressivePasses": "average",
    "interceptions": "average",
    "touchInBox": "average",
    "shots": "average",
    "headShots": "average",
    "keyPasses": "average",
    "smartPasses": "average",
    "xg": "average",
    "xgAssist": "average",
    "xgShot": "average",
    "receivedPass": "average",
    "shotsBlocked": "average",
    "clearances": "average",
    "slidingTackles": "average",
    "pressingDuels": "average",
    "counterpressingRecoveries": "average",
    "forwardPasses": "average",
    "longPasses": "average",
    "verticalPasses": "average",
    "passesToFinalThird": "average",
    "dribbles": "average",
    "gkShotsAgainst": "average",
    "gkAerialDuels": "average"
}

def calculate_position_score(player, position):
    """
    Calculate a player's score for a specific position using the improved percentile system
    
    Args:
        player: Player data dictionary
        position: Position code (e.g., "cf", "lb", "gk")
        
    Returns:
        tuple: (score, metrics_dict) where score is the weighted average score (0-100) 
               and metrics_dict contains all metrics with their percentile values
    """
    # Get relevant stats and weights
    key_stats = POSITION_KEY_STATS[position]
    weight_category = POSITION_WEIGHT_CATEGORY.get(position, "midfielder")
    weights = STAT_WEIGHTS.get(weight_category, {})
    
    # Calculate weighted average
    weighted_sum = 0
    total_weight = 0
    metrics_dict = {}
    
    # Use the universal percentile accessor for each key stat
    for stat in key_stats:
        # Get the percentile value using the universal accessor
        stat_value = get_player_percentile(player, stat)
        
        # Store the percentile value regardless of weight
        metrics_dict[stat] = stat_value
        
        # Only include in the weighted calculation if valid
        if stat_value > 0:
            weight = weights.get(stat, 1)
            weighted_sum += stat_value * weight
            total_weight += weight
    
    # Calculate final score
    final_score = weighted_sum / total_weight if total_weight > 0 else 0
    
    return (final_score, metrics_dict)

def ranking(player, min_minutes=180):
    """
    Calculate the player's RANKING POSITION among all players for each position they play.
    
    Args:
        player: Player data dictionary
        min_minutes: Minimum minutes played for reliable analysis
    
    Returns:
        List of dictionaries with position rankings (e.g. [{"cf": 5}, {"rw": 12}]) 
        where values represent the player's position in the ranking (1st, 2nd, etc.)
    """
    # Check minimum minutes
    if player.get('total', {}).get('minutesOnField', 0) < min_minutes:
        return [{"error": "Insufficient playing time"}]
    
    # Get player ID and convert to string for consistent comparison
    player_id = str(player.get("playerId", player.get("id", 0)))
    
    # Get all players from database
    all_players = get_player_database_by_id()
    if not all_players:
        return [{"error": "Player database not available"}]
    
    # Calculate rankings for each position
    rankings = []
    
    # Get all positions the player can play
    positions = [pos['position']['code'].lower() for pos in player.get('positions', [])]
    
    for position in positions:
        # Skip if position doesn't have defined key stats
        if position not in POSITION_KEY_STATS:
            continue
        
        # Calculate score for the current player
        player_score, player_metrics = calculate_position_score(player, position)
        
        # Calculate scores for all players in this position
        position_players = []  # Will store (player_id, score) tuples
        
        # Flag to track if our player was included
        player_included = False
        
        for pid_str, other_player in all_players.items():
            # Skip if player doesn't play this position
            if not other_player.get('positions') or not any(
                position == pos['position']['code'].lower() 
                for pos in other_player.get('positions', [])
            ):
                continue
                
            # Skip players with insufficient minutes
            if other_player.get('total', {}).get('minutesOnField', 0) < min_minutes:
                continue
            
            # Calculate score
            other_score, _ = calculate_position_score(other_player, position)
            position_players.append((pid_str, other_score))
            
            # Check if this is our target player
            if pid_str == player_id:
                player_included = True
        
        # Sort players by score (highest first)
        position_players.sort(key=lambda x: x[1], reverse=True)
        
        # If player wasn't included (rare case), add them now
        if not player_included and player_score > 0:
            position_players.append((player_id, player_score))
            position_players.sort(key=lambda x: x[1], reverse=True)
        
        # Find player's rank (position in the sorted list)
        try:
            rank = next(i+1 for i, (pid, _) in enumerate(position_players) if pid == player_id)
        except StopIteration:
            # Player not found in the list (should not happen with our fixes)
            rank = len(position_players) + 1
        
        # Add to rankings with key stats and their percentiles
        key_stats = POSITION_KEY_STATS[position]
        rankings.append({
            position: RankingItem(
                rank=rank, 
                key_metrics=key_stats,
                metrics_percentiles=player_metrics  # Add the metrics with their percentile values
            )
        })
    
    return rankings

# Dictionary of tactical profile translations that match player_profiles.json
TACTICAL_PROFILE_TRANSLATIONS = {
    "pt": {
        # Center forwards
        "Scoring Striker": "Atacante Finalizador",
        "Target Man": "Centroavante Alvo",
        "False 9": "Falso 9",
        "Complete Forward": "Atacante Completo",
        "Mobile Forward": "Atacante Móvel",
        
        # Wingers
        "Inverted Winger": "Ponta Invertido",
        "Traditional Winger": "Ponta Tradicional",
        "Inside Forward": "Atacante Interior",
        "Wide Playmaker": "Meia-Armador Aberto",
        "Wide Midfielder": "Meio-Campista Aberto",
        
        # Full backs
        "Attacking Full-back": "Lateral Ofensivo",
        "Defensive Full-back": "Lateral Defensivo",
        "Inverted Full-back": "Lateral Invertido",
        "Wing-back": "Ala",
        "Balanced Full-back": "Lateral Equilibrado",
        
        # Center backs
        "Ball-playing Defender": "Zagueiro Construtor",
        "Stopper": "Stopper",
        "Covering Defender": "Zagueiro de Cobertura",
        "Libero": "Líbero",
        "Hybrid Defender": "Zagueiro Híbrido",
        
        # Midfielders
        "Destroyer": "Destruidor",
        "Deep-lying Playmaker": "Meia-Armador Recuado",
        "Box-to-box": "Box-to-box",
        "Advanced Playmaker": "Meia-Armador Avançado",
        "Anchor": "Âncora",
        
        # Goalkeepers
        "Shot-stopper": "Goleiro Defensor",
        "Sweeper-keeper": "Goleiro Líbero",
        "Ball-playing Goalkeeper": "Goleiro Construtor",
        "Command Keeper": "Goleiro Comandante",
        "Distribution Specialist": "Especialista em Distribuição"
    },
    "en": {},  # English uses original names
    "es": {
        # Center forwards
        "Scoring Striker": "Delantero Goleador",
        "Target Man": "Delantero Pivote",
        "False 9": "Falso 9",
        "Complete Forward": "Delantero Completo",
        "Mobile Forward": "Delantero Móvil",
        
        # Wingers
        "Inverted Winger": "Extremo Invertido",
        "Traditional Winger": "Extremo Tradicional",
        "Inside Forward": "Delantero Interior",
        "Wide Playmaker": "Mediapunta Lateral",
        "Wide Midfielder": "Mediocampista Lateral",
        
        # Full backs
        "Attacking Full-back": "Lateral Ofensivo",
        "Defensive Full-back": "Lateral Defensivo",
        "Inverted Full-back": "Lateral Invertido",
        "Wing-back": "Carrilero",
        "Balanced Full-back": "Lateral Equilibrado",
        
        # Center backs
        "Ball-playing Defender": "Defensa Constructor",
        "Stopper": "Stopper",
        "Covering Defender": "Defensa de Cobertura",
        "Libero": "Líbero",
        "Hybrid Defender": "Defensa Híbrido",
        
        # Midfielders
        "Destroyer": "Destructor",
        "Deep-lying Playmaker": "Organizador Profundo",
        "Box-to-box": "Box-to-Box",
        "Advanced Playmaker": "Mediapunta Avanzado",
        "Anchor": "Ancla",
        
        # Goalkeepers
        "Shot-stopper": "Portero Parador",
        "Sweeper-keeper": "Portero Líbero",
        "Ball-playing Goalkeeper": "Portero Constructor",
        "Command Keeper": "Portero Comandante",
        "Distribution Specialist": "Especialista en Distribución"
    },
    "bg": {
        # Center forwards
        "Scoring Striker": "Голмайстор",
        "Target Man": "Таран",
        "False 9": "Фалшива Деветка",
        "Complete Forward": "Комплексен нападател",
        "Mobile Forward": "Мобилен нападател",
        
        # Wingers
        "Inverted Winger": "Обратно крило",
        "Traditional Winger": "Традиционно крило",
        "Inside Forward": "Вътрешен нападател",
        "Wide Playmaker": "Широк плеймейкър",
        "Wide Midfielder": "Широк полузащитник",
        
        # Full backs
        "Attacking Full-back": "Атакуващ бек",
        "Defensive Full-back": "Дефанзивен бек",
        "Inverted Full-back": "Обратен бек",
        "Wing-back": "Крилови бек",
        "Balanced Full-back": "Балансиран бек",
        
        # Center backs
        "Ball-playing Defender": "Защитник-разпределител",
        "Stopper": "Стопер",
        "Covering Defender": "Покриващ защитник",
        "Libero": "Либеро",
        "Hybrid Defender": "Хибриден защитник",
        
        # Midfielders
        "Destroyer": "Разрушител",
        "Deep-lying Playmaker": "Дълбок плеймейкър",
        "Box-to-box": "Бокс-ту-бокс",
        "Advanced Playmaker": "Напреднал плеймейкър",
        "Anchor": "Котва",
        
        # Goalkeepers
        "Shot-stopper": "Спасяващ вратар",
        "Sweeper-keeper": "Вратар-либеро",
        "Ball-playing Goalkeeper": "Вратар-разпределител",
        "Command Keeper": "Командващ вратар", 
        "Distribution Specialist": "Специалист по разпределение"
    }
}
# Tactical styles with weighted metrics for each style
TACTICAL_STYLES = {
    "possession_based": {
        "passes": 2.0,
        "pass_accuracy": 2.0,
        "successful_passes_percent": 1.9,
        "forward_passes": 1.7,
        "progressive_passes": 1.8,
        "passes_to_final_third": 1.7,
        "ball_losses": 1.8,
        "received_pass": 1.9,
        "progressive_runs": 1.6,
        "key_passes": 1.7,
        "smart_passes": 1.7,
        "xg_assist": 1.7
    },
    "high_pressing": {
        "counterpressing_recoveries": 2.0,
        "dangerous_opponent_half_recoveries": 2.0,
        "ball_recoveries": 1.9,
        "interceptions": 1.8,
        "defensive_duels_won": 1.7,
        "offensive_duels_won": 1.7,
        "accelerations": 1.8,
        "pressing_duels": 1.9,
        "pressing_duels_won": 1.9
    },
    "counter_attacking": {
        "progressive_runs": 2.0,
        "accelerations": 1.9,
        "successful_through_passes": 1.8,
        "successful_smart_passes": 1.8,
        "xg_assist": 1.8,
        "shots": 1.7,
        "xg_shot": 1.7,
        "ball_recoveries": 1.7,
        "interceptions": 1.6
    },
    "tiki_taka": {
        "passes": 2.0,
        "pass_accuracy": 2.0,
        "successful_passes_percent": 2.0,
        "forward_passes": 1.9,
        "progressive_passes": 1.9,
        "key_passes": 1.8,
        "smart_passes": 1.8,
        "xg_assist": 1.8,
        "ball_losses": 1.9,
        "received_pass": 2.0
    },
    "gegenpressing": {
        "counterpressing_recoveries": 2.0,
        "dangerous_opponent_half_recoveries": 2.0,
        "ball_recoveries": 1.9,
        "pressing_duels": 2.0,
        "pressing_duels_won": 1.9,
        "accelerations": 1.8,
        "defensive_duels_won": 1.7,
        "offensive_duels_won": 1.7
    },
    "direct_play": {
        "long_passes": 2.0,
        "successful_long_passes_percent": 1.9,
        "forward_passes": 1.9,
        "progressive_passes": 1.8,
        "aerial_duels_won": 1.8,
        "shots": 1.7,
        "xg_shot": 1.7,
        "touch_in_box": 1.7
    },
    "fluid_attacking": {
        "progressive_runs": 1.9,
        "successful_dribbles": 1.9,
        "key_passes": 1.8,
        "smart_passes": 1.8,
        "xg_assist": 1.8,
        "shots": 1.7,
        "xg_shot": 1.7,
        "touch_in_box": 1.8,
        "accelerations": 1.8
    },
    "low_block": {
        "defensive_duels_won": 2.0,
        "interceptions": 1.9,
        "ball_recoveries": 1.9,
        "clearances": 1.8,
        "aerial_duels_won": 1.8,
        "successful_sliding_tackles": 1.7,
        "long_passes": 1.7,
        "successful_long_passes_percent": 1.7
    },
    "width_and_depth": {
        "passes_to_final_third": 1.9,
        "successful_crosses": 1.8,
        "progressive_runs": 1.8,
        "touch_in_box": 1.7,
        "successful_smart_passes": 1.7,
        "successful_through_passes": 1.7,
        "xg_assist": 1.7,
        "shots": 1.6
    },
    "balanced_approach": {
        "passes": 1.8,
        "pass_accuracy": 1.8,
        "long_passes": 1.7,
        "progressive_passes": 1.7,
        "ball_recoveries": 1.7,
        "interceptions": 1.7,
        "defensive_duels_won": 1.7,
        "offensive_duels_won": 1.7,
        "shots": 1.6,
        "xg_shot": 1.6,
        "xg_assist": 1.6
    }
}

# Formations and their key positions
FORMATIONS = {
    "4-3-3": ["gk", "rb", "cb", "cb", "lb", "dmf", "cmf", "cmf", "rwf", "cf", "lwf"],
    "4-4-2": ["gk", "rb", "cb", "cb", "lb", "rmf", "cmf", "cmf", "lmf", "cf", "cf"],
    "4-2-3-1": ["gk", "rb", "cb", "cb", "lb", "dmf", "dmf", "amf", "ramf", "lamf", "cf"],
    "3-5-2": ["gk", "cb", "cb", "cb", "rwb", "cmf", "cmf", "cmf", "lwb", "cf", "cf"],
    "3-4-3": ["gk", "cb", "cb", "cb", "rmf", "cmf", "cmf", "lmf", "rwf", "cf", "lwf"],
    "5-3-2": ["gk", "rwb", "cb", "cb", "cb", "lwb", "cmf", "cmf", "cmf", "cf", "cf"],
    "4-1-4-1": ["gk", "rb", "cb", "cb", "lb", "dmf", "rmf", "cmf", "cmf", "lmf", "cf"],
    "4-3-1-2": ["gk", "rb", "cb", "cb", "lb", "dmf", "cmf", "cmf", "amf", "cf", "cf"],
    "4-4-1-1": ["gk", "rb", "cb", "cb", "lb", "rmf", "cmf", "cmf", "lmf", "amf", "cf"],
    "3-4-2-1": ["gk", "cb", "cb", "cb", "rwb", "cmf", "cmf", "lwb", "ramf", "lamf", "cf"]
}
# After the STYLE_DESCRIPTIONS dictionary, add these translation dictionaries:

# Translations for tactical style names
STYLE_DISPLAY_NAMES_TRANSLATIONS = {
    "pt": {
        "possession_based": "Posse de Bola",
        "high_pressing": "Pressing Alto",
        "counter_attacking": "Contra-Ataque",
        "tiki_taka": "Tiki-Taka",
        "gegenpressing": "Gegenpressing",
        "direct_play": "Jogo Direto",
        "fluid_attacking": "Ataque Fluido",
        "low_block": "Bloco Baixo",
        "width_and_depth": "Largura e Profundidade",
        "balanced_approach": "Abordagem Equilibrada"
    },
    "en": {
        "possession_based": "Possession-Based",
        "high_pressing": "High Pressing",
        "counter_attacking": "Counter-Attacking",
        "tiki_taka": "Tiki-Taka",
        "gegenpressing": "Gegenpressing",
        "direct_play": "Direct Play",
        "fluid_attacking": "Fluid Attacking",
        "low_block": "Low Block",
        "width_and_depth": "Width & Depth",
        "balanced_approach": "Balanced Approach"
    },
    "es": {
        "possession_based": "Posesión de Balón",
        "high_pressing": "Pressing Alto",
        "counter_attacking": "Contraataque",
        "tiki_taka": "Tiki-Taka",
        "gegenpressing": "Gegenpressing",
        "direct_play": "Juego Directo",
        "fluid_attacking": "Ataque Fluido",
        "low_block": "Bloque Bajo",
        "width_and_depth": "Amplitud y Profundidad",
        "balanced_approach": "Enfoque Equilibrado"
    },
    "bg": {
        "possession_based": "Владение на топката",
        "high_pressing": "Висок пресинг",
        "counter_attacking": "Контраатака",
        "tiki_taka": "Тики-така",
        "gegenpressing": "Гегенпресинг",
        "direct_play": "Директна игра",
        "fluid_attacking": "Флуидна атака",
        "low_block": "Нисък блок",
        "width_and_depth": "Широчина и дълбочина",
        "balanced_approach": "Балансиран подход"
    }
}
STYLE_DESCRIPTIONS = {
    "possession_based": "Focus on maintaining ball possession with short passing",
    "high_pressing": "Aggressive pressing high up the pitch to win the ball",
    "counter_attacking": "Fast transitions from defense to attack after winning possession",
    "tiki_taka": "Short, quick passing with continuous player movement",
    "gegenpressing": "Immediate counter-press after losing possession",
    "direct_play": "Vertical, forward passing to attackers, often bypassing midfield",
    "fluid_attacking": "Emphasis on player movement, dribbling and creative passing",
    "low_block": "Defensive, compact shape with counters when possession is won",
    "width_and_depth": "Using width and crosses to create scoring opportunities",
    "balanced_approach": "Equal focus on defensive solidity and attacking threat"
}
# Translations for tactical style descriptions
STYLE_DESCRIPTIONS_TRANSLATIONS = {
    "pt": {
        "possession_based": "Foco em manter a posse de bola com passes curtos",
        "high_pressing": "Pressing agressivo na parte alta do campo para recuperar a bola",
        "counter_attacking": "Transições rápidas da defesa para o ataque após recuperar a posse",
        "tiki_taka": "Passes curtos e rápidos com movimento contínuo dos jogadores",
        "gegenpressing": "Contra-pressing imediato após perder a posse",
        "direct_play": "Passes verticais e para frente aos atacantes, frequentemente ultrapassando o meio-campo",
        "fluid_attacking": "Ênfase no movimento dos jogadores, dribles e passes criativos",
        "low_block": "Formação defensiva e compacta com contra-ataques quando a posse é recuperada",
        "width_and_depth": "Usando amplitude e cruzamentos para criar oportunidades de gol",
        "balanced_approach": "Foco igual na solidez defensiva e ameaça ofensiva"
    },
    "en": STYLE_DESCRIPTIONS,  # Reuse existing English descriptions
    "es": {
        "possession_based": "Enfoque en mantener la posesión del balón con pases cortos",
        "high_pressing": "Pressing agresivo en campo contrario para recuperar el balón",
        "counter_attacking": "Transiciones rápidas de defensa a ataque tras recuperar la posesión",
        "tiki_taka": "Pases cortos y rápidos con movimiento continuo de jugadores",
        "gegenpressing": "Contra-pressing inmediato después de perder la posesión",
        "direct_play": "Pases verticales hacia adelante a los atacantes, a menudo saltando el mediocampo",
        "fluid_attacking": "Énfasis en el movimiento de jugadores, regate y pases creativos",
        "low_block": "Forma defensiva y compacta con contraataques al recuperar la posesión",
        "width_and_depth": "Uso de amplitud y centros para crear oportunidades de gol",
        "balanced_approach": "Enfoque equilibrado entre solidez defensiva y amenaza ofensiva"
    },
    "bg": {
        "possession_based": "Фокус върху поддържане на владение на топката с къси пасове",
        "high_pressing": "Агресивен пресинг високо в полето за спечелване на топката",
        "counter_attacking": "Бързи преходи от защита към атака след спечелване на владение",
        "tiki_taka": "Къси, бързи пасове с непрекъснато движение на играчите",
        "gegenpressing": "Незабавен контра-пресинг след загуба на владение",
        "direct_play": "Вертикални подавания напред към нападателите, често пропускайки полузащитата",
        "fluid_attacking": "Акцент върху движението на играчите, дрибъл и креативни пасове",
        "low_block": "Отбранителна, компактна формация с контраатаки при спечелване на владение",
        "width_and_depth": "Използване на ширина и центрирания за създаване на голови възможности",
        "balanced_approach": "Равен фокус върху отбранителна стабилност и атакуваща заплаха"
    }
}


# Map display names to dictionary keys
STYLE_DISPLAY_NAMES = {
    "Possession-Based": "possession_based",
    "High Pressing": "high_pressing",
    "Counter-Attacking": "counter_attacking",
    "Tiki-Taka": "tiki_taka",
    "Gegenpressing": "gegenpressing",
    "Direct Play": "direct_play",
    "Fluid Attacking": "fluid_attacking",
    "Low Block": "low_block",
    "Width & Depth": "width_and_depth",
    "Balanced Approach": "balanced_approach"
}

# Reverse mapping from keys to display names
STYLE_DISPLAY_NAMES_REVERSE = {v: k for k, v in STYLE_DISPLAY_NAMES.items()}

# Display descriptions for use in UI

# Add the translation dictionaries we created earlier:
# TACTICAL_PROFILE_TRANSLATIONS
# STYLE_DISPLAY_NAMES_TRANSLATIONS 
# STYLE_DESCRIPTIONS_TRANSLATIONS

# Helper functions for translation
def get_translated_style_name(style_key, language='pt'):
    """Get translated style name based on language preference"""
    if language in STYLE_DISPLAY_NAMES_TRANSLATIONS and style_key in STYLE_DISPLAY_NAMES_TRANSLATIONS[language]:
        return STYLE_DISPLAY_NAMES_TRANSLATIONS[language][style_key]
    return STYLE_DISPLAY_NAMES_REVERSE.get(style_key, style_key)

def get_translated_style_description(style_key, language='pt'):
    """Get translated style description based on language preference"""
    if language in STYLE_DESCRIPTIONS_TRANSLATIONS and style_key in STYLE_DESCRIPTIONS_TRANSLATIONS[language]:
        return STYLE_DESCRIPTIONS_TRANSLATIONS[language][style_key]
    return STYLE_DESCRIPTIONS.get(style_key, '')

def translate_profile_name(profile_name, language='pt'):
    """Translate a tactical profile name based on language preference"""
    if language in TACTICAL_PROFILE_TRANSLATIONS:
        return TACTICAL_PROFILE_TRANSLATIONS[language].get(profile_name, profile_name)
    return profile_name

# Modify the tactical_role function to accept language parameter
def tactical_role(player, language='pt'):
    """
    Calculate tactical role profiles for all positions a player can play.
    
    Args:
        player: Player data dictionary
        language: Language for translations ('pt', 'en', 'es', 'bg')
    
    Returns:
        TacticalFitAnalysis object with role fits, descriptions, and key metrics
    """
    # Existing code for loading profiles and mappings remains unchanged
    import json
    import os
    
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    profiles_path = os.path.join(current_dir, 'player_profiles.json')
    
    with open(profiles_path, 'r') as f:
        all_profiles = json.load(f)
    
    # Position category mapping
    position_categories = {
        "cf": "center_forwards",
        "lw": "wingers", "rw": "wingers",
        "amf": "midfielders", "dmf": "midfielders", 
        "cmf": "midfielders", "lcmf": "midfielders", "rcmf": "midfielders",
        "lb": "full_backs", "rb": "full_backs", 
        "lwb": "full_backs", "rwb": "full_backs",
        "cb": "center_backs", "lcb": "center_backs", "rcb": "center_backs",
        "gk": "goalkeepers"
    }
    
    positions = [pos['position']['code'].lower() for pos in player.get('positions', [])]
    if not positions:
        return {"error": "Player has no position data"}
    
    position_analysis = {}
    all_profile_fits = []
    
    for position in positions:
        if position not in position_categories:
            continue
            
        profile_category = position_categories[position]
        if profile_category not in all_profiles:
            continue
            
        temp_player = player.copy()
        temp_player['positions'] = [{'position': {'code': position}}]
        
        if '_percentiles_cache' not in temp_player:
            percentile_data = z_score_and_percentiles_aprimorado(temp_player)
            temp_player['_percentiles_cache'] = {
                'percentiles': percentile_data['percentiles'],
                'football_categories': percentile_data.get('football_categories', {})
            }
        
        position_profiles = all_profiles[profile_category]
        profile_fits = {}
        
        for profile_name, profile_data in position_profiles.items():
            fit_score = calculate_profile_fit(temp_player, profile_data)
            
            # Translate the profile name directly
            translated_name = translate_profile_name(profile_name, language)
            
            # Store the profile information with translated name
            profile_fits[translated_name] = {
                "score": fit_score,
                "description": profile_data.get("description", {}).get(language, ""),
                "category": get_fit_category(fit_score),
                "position": position,
                "position_type": profile_category,
                "key_metrics": list(profile_data.get("key_stats", {}).keys())
            }
            
            # Add to global list with translated name
            all_profile_fits.append({
                "position": position,
                "position_type": profile_category,
                "profile": translated_name,  # Use translated name
                "score": fit_score,
                "description": profile_data.get("description", {}).get(language, ""),
                "category": get_fit_category(fit_score),
                "key_metrics": list(profile_data.get("key_stats", {}).keys())
            })
        
        sorted_fits = dict(sorted(profile_fits.items(), key=lambda x: x[1]["score"], reverse=True))
        
        if sorted_fits:
            best_fit_name = next(iter(sorted_fits))
            position_analysis[position] = {
                "profiles": sorted_fits,
                "best_fit": best_fit_name,  # This is already translated
                "best_score": sorted_fits[best_fit_name]["score"],
                "best_description": sorted_fits[best_fit_name]["description"],
                "key_metrics": sorted_fits[best_fit_name]["key_metrics"]
            }
    
    ranked_profiles = sorted(all_profile_fits, key=lambda x: x["score"], reverse=True)
    
    result_dict = {
        "player_name": player.get("name", "Unknown Player"),
        "player_id": player.get("playerId", player.get("id", 0)),
        "primary_position": positions[0] if positions else None,
        "all_positions": positions,
        "by_position": position_analysis,
        "best_fits": ranked_profiles[:5],
        "optimal_role": ranked_profiles[0] if ranked_profiles else None,
        "primary_position_best_fit": (
            position_analysis.get(positions[0], {}).get("best_fit") 
            if positions and positions[0] in position_analysis 
            else None
        ),
        "versatility": {
            "position_count": len(positions),
            "viable_roles_count": sum(1 for fit in ranked_profiles if fit["score"] >= 60)
        }
    }
    
    return TacticalFitAnalysis(**result_dict)

# Update the tactical_fit legacy function
def tactical_fit(player, language='pt'):
    """Legacy function that calls tactical_role for backward compatibility"""
    return tactical_role(player, language)

# Modify calculate_tactical_fit to use translations
def calculate_tactical_fit(
    player: Dict[str, Any],
    style: str = None,
    min_minutes: int = 180,
    language: str = 'pt'
) -> Dict[str, Any]:
    """
    Calculate how well a player fits a tactical style and formation using percentiles.
    If style is None, calculates fit for all styles and returns best matches.
    
    Args:
        player: Player data with stats
        style: Tactical style key (e.g., "possession_based") or None for all styles
        min_minutes: Minimum minutes for reliable analysis
        language: Language code for translations ('pt', 'en', 'es', 'bg')
        
    Returns:
        Dictionary with tactical fit data including descriptions and key metrics
    """
    # Existing checks for minimum minutes and percentile caching remain the same
    if player.get('total', {}).get('minutesOnField', 0) < min_minutes:
        return {
            "error": f"Insufficient playing time (< {min_minutes} minutes)",
            "style_score": 0,
            "position_fit": 0
        }
    
    if '_percentiles_cache' not in player:
        percentile_data = z_score_and_percentiles_aprimorado(player, min_minutes)
        if 'warning' in percentile_data:
            return {
                "error": percentile_data['warning'],
                "style_score": 0,
                "position_fit": 0
            }
        
        player['_percentiles_cache'] = {
            'percentiles': percentile_data['percentiles'],
            'football_categories': percentile_data.get('football_categories', {})
        }
    
    # If no specific style provided, calculate for all styles
    if style is None:
        all_styles_fit = {}
        
        for style_key in TACTICAL_STYLES.keys():
            style_fit = calculate_single_tactical_fit_improved(player, style_key, language)
            if "error" not in style_fit:
                all_styles_fit[style_key] = style_fit
        
        # Sort styles by score
        sorted_styles = sorted(
            all_styles_fit.items(),
            key=lambda x: x[1]["style_score"],
            reverse=True
        )
        
        # Return top 3 styles with detailed information
        top_styles = []
        for style_name, style_data in sorted_styles[:3]:
            metrics_with_percentiles = {}
            for metric_name in style_data.get("key_metrics", []):
                metrics_with_percentiles[metric_name] = {
                    "name": metric_name,
                    "display_name": format_metric_name(metric_name),
                    "percentile": get_player_percentile(player, metric_name)
                }
            
            top_styles.append({
                "style_name": style_data["style_name"],  # Already translated in calculate_single_tactical_fit_improved
                "style_key": style_name,
                "style_description": style_data["style_description"],  # Already translated
                "style_score": style_data["style_score"],
                "style_category": style_data["style_category"],
                "key_metrics": style_data.get("key_strengths", []),
                "key_weaknesses": style_data.get("key_weaknesses", []),
                "metrics_percentiles": metrics_with_percentiles
            })
            
        return {
            "best_fits": top_styles
        }
    else:
        # Calculate for specific style
        if style not in TACTICAL_STYLES:
            return {"error": f"Unknown tactical style: {style}"}
            
        fit_data = calculate_single_tactical_fit_improved(player, style, language)
        
        # Add detailed metrics percentiles
        metrics_with_percentiles = {}
        for metric_name in TACTICAL_STYLES[style].keys():
            metrics_with_percentiles[metric_name] = {
                "name": metric_name,
                "display_name": format_metric_name(metric_name),
                "percentile": get_player_percentile(player, metric_name)
            }
            
        fit_data["metrics_percentiles"] = metrics_with_percentiles
        return fit_data

# Update calculate_single_tactical_fit_improved to use translations
def calculate_single_tactical_fit_improved(player, style, language='pt'):
    """
    Helper function to calculate tactical fit for a single style using the improved percentile system
    
    Args:
        player: Player data dictionary
        style: Tactical style key (e.g., "possession_based")
        language: Language code for translations
        
    Returns:
        Dictionary with tactical fit data
    """
    # Existing code for calculation remains the same
    style_weights = TACTICAL_STYLES[style]
    
    style_score = 0.0
    style_max_score = 0.0
    matched_metrics = 0
    style_analysis = {}
    
    for style_metric, weight in style_weights.items():
        percentile_value = get_player_percentile(player, style_metric)
        
        if percentile_value > 0:
            style_score += percentile_value * weight
            style_max_score += 100 * weight
            matched_metrics += 1
            
            style_analysis[style_metric] = {
                "percentile": percentile_value,
                "weight": weight,
                "weighted_score": percentile_value * weight,
                "display_name": format_metric_name(style_metric)
            }
        else:
            style_analysis[style_metric] = {
                "percentile": None,
                "weight": weight,
                "weighted_score": 0,
                "display_name": format_metric_name(style_metric),
                "missing": True
            }
    
    if style_max_score > 0:
        normalized_style_score = round((style_score / style_max_score) * 100)
    else:
        normalized_style_score = 0
    
    positions = [pos['position']['code'].lower() for pos in player.get('positions', [])]
    
    key_strengths = get_key_strengths(style_analysis, 3)
    key_weaknesses = get_key_weaknesses(style_analysis, 2)
    
    # Use translated name and description
    return {
        "style_name": get_translated_style_name(style, language),
        "style_description": get_translated_style_description(style, language),
        "style_score": normalized_style_score,
        "style_category": get_fit_category(normalized_style_score),
        "total_metrics": len(style_weights),
        "metric_analysis": style_analysis,
        "key_strengths": key_strengths,
        "key_weaknesses": key_weaknesses
    }

# Update complete_data_analysis function to pass language parameter

def get_key_strengths(style_analysis, count=3):
    """Extract key strengths from the style analysis"""
    strengths = []
    
    # Filter out missing metrics and sort by weighted score
    valid_metrics = {k: v for k, v in style_analysis.items() 
                    if v.get('percentile') is not None and v.get('percentile') >= 70}
    
    sorted_metrics = sorted(valid_metrics.items(), 
                           key=lambda x: x[1]['weighted_score'], 
                           reverse=True)
    
    # Take top metrics
    for i, (metric, data) in enumerate(sorted_metrics):
        if i >= count:
            break
            
        strengths.append({
            "metric": metric,
            "display_name": data['display_name'],
            "percentile": data['percentile'],
            "weighted_score": data['weighted_score']
        })
    
    return strengths

def get_key_weaknesses(style_analysis, count=2):
    """Extract key weaknesses from the style analysis"""
    weaknesses = []
    
    # Filter out missing metrics and sort by weighted score (ascending)
    valid_metrics = {k: v for k, v in style_analysis.items() 
                    if v.get('percentile') is not None and v.get('percentile') <= 40}
    
    sorted_metrics = sorted(valid_metrics.items(), 
                           key=lambda x: x[1]['weighted_score'])
    
    # Take bottom metrics
    for i, (metric, data) in enumerate(sorted_metrics):
        if i >= count:
            break
            
        weaknesses.append({
            "metric": metric,
            "display_name": data['display_name'],
            "percentile": data['percentile'],
            "weighted_score": data['weighted_score']
        })
    
    return weaknesses

def format_metric_name(metric):
    """Format a metric name to be more readable"""
    return ' '.join(word.capitalize() for word in metric.replace('_', ' ').split())

def complete_data_analysis(player_id, language='pt'):
    """
    Generate a complete data analysis for a player using the improved percentile system
    
    Args:
        player_id: ID of the player to analyze
        language: Language for AI insights ('pt', 'en', 'es', or 'bg')
        
    Returns:
        DataAnalysis object with all analysis components
    """
    player = find_player_by_id(player_id)
    if player is None:
        return None
        
    # Calculate percentiles once using the improved system
    percentile_data = z_score_and_percentiles_aprimorado(player)
    
    # Em vez de tentar adicionar como atributo, armazene o cache como uma chave do dicionário
    player['_percentiles_cache'] = {
        'percentiles': percentile_data['percentiles'],
        'football_categories': percentile_data.get('football_categories', {})
    }
    
    # Determinar o grupo de posição baseado nas posições do jogador
    position_group = get_player_position_group(player)
    
    # Generate all analyses using the player object with cached percentiles
    tactical_role_analysis = tactical_role(player, language=language)
    tactical_style_analysis = calculate_tactical_fit(player, None, language=language)  # Get top 3 tactical styles
    swot_analysis_result = swot_analysis(player=player, language=language)
    ranking_result = ranking(player, min_minutes=0)
    
    # Create player model that matches the Player model structure
    player_model = {
        "id": player.get("playerId", player.get("id", 0)),
        "name": player.get("name", "Unknown Player"),
        "positions": [{"position": {"code": pos['position']['code']}} for pos in player.get('positions', [])],
        "age": player.get("age", 0),
        "foot": player.get("foot", "Unknown"),
        "height": player.get("height", 0),
        "weight": player.get("weight", 0),
        # Add other fields as needed
    }
    
    # Create and return DataAnalysis object with all components
    return DataAnalysis(
        swot=swot_analysis_result,
        ranking=ranking_result,
        tactical_fit=tactical_role_analysis,
        tactical_styles=tactical_style_analysis,
        player=player_model,
        player_id=str(player_id),
        percentiles=percentile_data['percentiles'],  # Original structure for backward compatibility
        percentiles_by_category=percentile_data.get('football_categories', {}),  # New organized percentiles
        position_group=position_group  # Adicionar o grupo de posição
    )

if __name__ == "__main__":
    analysis = complete_data_analysis(372255)  # Replace with actual player ID
    if analysis:
        print("SWOT Analysis:")
        print(analysis.swot)
        
        print("\nRanking:")
        print(analysis.ranking)
        
        print("\nTactical Fit:")
        print(analysis.tactical_fit)
        
        print("\nPlayer Model:")
        print(analysis.player)
         

        print("\nPercentiles:")
        print(analysis.percentiles)
    else:
        print("Player not found.")


# Em arquivos que podem ser rodados diretamente
if __name__ == "__main__":
    import os
    import sys
    # Adiciona o diretório raiz ao PYTHONPATH
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)

    
