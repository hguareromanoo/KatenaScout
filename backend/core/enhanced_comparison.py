"""
Enhanced player comparison functionality for KatenaScout

This module provides metric-by-metric comparison between players,
determining winners for each metric and calculating an overall winner.
"""

from typing import List, Dict, Any, Optional, Tuple
import copy

# Metrics where lower values are better (negative metrics)
NEGATIVE_METRICS = [
    "ballLosses", "miscontrols", "dispossessed", "challengeLost", 
    "foulsCommitted", "yellowCards", "redCards", "errorLeadToShot",
    "errorLeadToGoal", "penaltyConceded", "ownGoals", "dribbledPast",
    "dangerousOwnHalfLosses", "possessionLost"
]

# Metric categories and their associated metrics
METRIC_CATEGORIES = {
    "attacking": [
        "goals", "assists", "shots", "shotsOnTarget", "xG", "goalConversion", 
        "headedGoals", "npxG", "shotsFromBox", "shotsFromOutOfBox", "dribbles",
        "successfulDribbles", "dribbleSuccessRate", "crossingAccuracy"
    ],
    "passing": [
        "assists", "assistsPerGame", "expectedAssists", "keyPasses", "accuratePasses", 
        "passAccuracy", "progressivePasses", "passesIntoFinalThird", "crossingAccuracy",
        "longBallAccuracy", "throughBalls", "smartPasses"
    ],
    "defending": [
        "tackles", "interceptions", "clearances", "duelsWon", "aerialDuelsWon", 
        "blocks", "cleanSheets", "slidingTackles", "standingTackles", "tackleSuccessRate",
        "pressures", "successfulPressures"
    ],
    "possession": [
        "touches", "passAccuracy", "possessionLost", "ballRecoveries", 
        "dribbleSuccessRate", "successfulProgressivePasses", "ballLosses",
        "miscontrols", "dispossessed", "progressiveRuns"
    ],
    "goalkeeping": [
        "saves", "savePercentage", "cleanSheets", "goalsConceded", "penaltiesSaved", 
        "shotsOnTargetAgainst", "goalsPrevented", "highClaims", "punches", "runs",
        "successfulRunsOut", "passAccuracy", "longPassAccuracy"
    ],
    "physical": [
        "distanceCovered", "sprintDistance", "topSpeed", "accelerations", 
        "intensityRuns", "foulsWon", "foulsCommitted", "duelsWon", "aerialDuelsWon"
    ]
}

# Default weights for metrics (used when specific weights aren't provided)
DEFAULT_METRIC_WEIGHTS = {
    "goals": 2.0, "assists": 1.8, "xG": 1.8, "expectedAssists": 1.7,
    "passAccuracy": 1.6, "dribbles": 1.5, "tackles": 1.5, "interceptions": 1.5,
    "keyPasses": 1.6, "shotsOnTarget": 1.7, "progressivePasses": 1.6,
    "duelsWon": 1.5, "aerialDuelsWon": 1.5, "saves": 1.8, "cleanSheets": 1.8
}

def categorize_metrics(metrics: List[str]) -> Dict[str, List[str]]:
    """
    Organize metrics into categories
    
    Args:
        metrics: List of metric names
        
    Returns:
        Dictionary with categories as keys and lists of metrics as values
    """
    result = {}
    
    # Initialize categories
    for category in METRIC_CATEGORIES.keys():
        result[category] = []
    
    # Uncategorized metrics will go here
    result["other"] = []
    
    # Categorize each metric
    for metric in metrics:
        categorized = False
        for category, category_metrics in METRIC_CATEGORIES.items():
            if metric in category_metrics:
                result[category].append(metric)
                categorized = True
                break
        
        if not categorized:
            result["other"].append(metric)
    
    # Remove empty categories
    return {k: v for k, v in result.items() if v}


def determine_metric_winners(
    player1: Dict[str, Any], 
    player2: Dict[str, Any],
    skip_zero_values: bool = False
) -> Dict[str, str]:
    """
    Determine which player has the better value for each metric
    
    Args:
        player1: First player data
        player2: Second player data
        skip_zero_values: Skip metrics where both players have 0 value
        
    Returns:
        Dictionary mapping metric names to winner ("player1", "player2", or "tie")
    """
    winners = {}
    player1_stats = player1.get("stats", {})
    player2_stats = player2.get("stats", {})
    
    # Ensure we have stats to compare
    if not player1_stats or not player2_stats:
        print("Warning: One or both players have no stats dictionary")
        return {}
    
    # Get common metrics between players (using direct calculation to avoid circular import)
    common_metrics = []
    for metric in set(player1_stats.keys()) & set(player2_stats.keys()):
        val1 = player1_stats.get(metric)
        val2 = player2_stats.get(metric)
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            common_metrics.append(metric)
    
    # If no common metrics, return empty dict
    if not common_metrics:
        print("Warning: No common metrics found between players")
        return {}
    
    for metric in common_metrics:
        # Get values
        val1 = player1_stats.get(metric, 0)
        val2 = player2_stats.get(metric, 0)
        
        # Skip if both values are 0 and we're skipping zero values
        if skip_zero_values and val1 == 0 and val2 == 0:
            continue
            
        # Verify values are numeric
        if not isinstance(val1, (int, float)) or not isinstance(val2, (int, float)):
            print(f"Warning: Non-numeric value for metric {metric}: {val1} vs {val2}")
            continue
        
        # Check if this is a metric where lower is better
        is_negative = metric in NEGATIVE_METRICS
        
        # Determine winner
        if is_negative:
            # For negative metrics, lower is better
            if val1 < val2:
                winners[metric] = "player1"
            elif val2 < val1:
                winners[metric] = "player2"
            else:
                winners[metric] = "tie"
        else:
            # For positive metrics, higher is better
            if val1 > val2:
                winners[metric] = "player1"
            elif val2 > val1:
                winners[metric] = "player2"
            else:
                winners[metric] = "tie"
    
    return winners


def get_metric_weight(metric: str, search_weights: Dict[str, float] = None) -> float:
    """
    Get the weight (importance) of a metric, using search weights if available
    
    Args:
        metric: Metric name
        search_weights: Optional weights from search parameters
        
    Returns:
        Weight value (higher means more important)
    """
    # If search weights provided, use those first
    if search_weights and metric in search_weights:
        return search_weights[metric]
    
    # Otherwise fall back to default weights
    return DEFAULT_METRIC_WEIGHTS.get(metric, 1.0)


def calculate_overall_winner(
    winners: Dict[str, str],
    player1: Dict[str, Any],
    player2: Dict[str, Any],
    search_weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Calculate the overall winner based on weighted metrics
    
    Args:
        winners: Dictionary mapping metrics to winners
        player1: First player data
        player2: Second player data
        search_weights: Optional weights from search parameters
        
    Returns:
        Dictionary with overall winner info
    """
    p1_score = 0.0
    p2_score = 0.0
    
    # Count weighted metric wins
    for metric, winner in winners.items():
        # Get weight for this metric
        weight = get_metric_weight(metric, search_weights)
        
        if winner == "player1":
            p1_score += weight
        elif winner == "player2":
            p2_score += weight
        # Ties don't contribute to either score
    
    # Determine overall winner
    if p1_score > p2_score:
        winner = "player1"
        winner_name = player1.get("name", "Player 1")
        winner_score = p1_score
        loser_score = p2_score
    elif p2_score > p1_score:
        winner = "player2"
        winner_name = player2.get("name", "Player 2")
        winner_score = p2_score
        loser_score = p1_score
    else:
        winner = "tie"
        winner_name = "Tie"
        winner_score = p1_score
        loser_score = p2_score
    
    # Calculate win margin percentage
    if winner_score + loser_score > 0:
        margin_percentage = int(100 * (winner_score - loser_score) / (winner_score + loser_score))
    else:
        margin_percentage = 0
    
    return {
        "winner": winner,
        "winner_name": winner_name,
        "player1_score": p1_score,
        "player2_score": p2_score,
        "margin_percentage": margin_percentage
    }


def get_common_metrics(player1: Dict[str, Any], player2: Dict[str, Any]) -> List[str]:
    """
    Get metrics that both players have in common
    
    Args:
        player1: First player data
        player2: Second player data
        
    Returns:
        List of common metric names
    """
    player1_stats = player1.get("stats", {})
    player2_stats = player2.get("stats", {})
    
    # Ensure both players have stats dictionaries
    if not player1_stats or not player2_stats:
        print("Warning: One or both players have no stats")
        return []
    
    # Find common metrics
    common_metrics = set(player1_stats.keys()) & set(player2_stats.keys())
    
    # Verify we have actual values for these metrics
    valid_metrics = []
    for metric in common_metrics:
        val1 = player1_stats.get(metric)
        val2 = player2_stats.get(metric)
        
        # Only include metrics with valid numerical values
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            valid_metrics.append(metric)
    
    return valid_metrics


def enhance_player_comparison(
    players: List[Dict[str, Any]],
    comparison_text: str,
    search_weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Enhance the player comparison with metric-by-metric analysis
    
    Args:
        players: List of player data (exactly 2 players)
        comparison_text: Natural language comparison text
        search_weights: Optional weights from search parameters
        
    Returns:
        Enhanced comparison data
    """
    if len(players) != 2:
        return {
            "error": "Enhanced comparison requires exactly 2 players",
            "original_comparison": comparison_text
        }
    
    player1 = players[0]
    player2 = players[1]
    
    # Get common metrics between the two players
    common_metrics = get_common_metrics(player1, player2)
    
    # Determine winner for each metric
    metric_winners = determine_metric_winners(player1, player2)
    
    # Calculate overall winner
    overall_winner = calculate_overall_winner(
        metric_winners, player1, player2, search_weights
    )
    
    # Categorize metrics
    categorized_metrics = categorize_metrics(common_metrics)
    
    # Add metric-specific winner info to each player's stats
    # Make deep copies to avoid modifying the original data
    enhanced_player1 = copy.deepcopy(player1)
    enhanced_player2 = copy.deepcopy(player2)
    
    # Add winner flags to stats
    for metric, winner in metric_winners.items():
        if metric in enhanced_player1.get("stats", {}):
            enhanced_player1["stats"][f"{metric}_winner"] = (winner == "player1" or winner == "tie")
        
        if metric in enhanced_player2.get("stats", {}):
            enhanced_player2["stats"][f"{metric}_winner"] = (winner == "player2" or winner == "tie")
    
    # Get winner counts by category
    category_winners = {}
    for category, metrics in categorized_metrics.items():
        p1_wins = sum(1 for m in metrics if metric_winners.get(m) == "player1")
        p2_wins = sum(1 for m in metrics if metric_winners.get(m) == "player2")
        ties = sum(1 for m in metrics if metric_winners.get(m) == "tie")
        
        if p1_wins > p2_wins:
            category_winners[category] = "player1"
        elif p2_wins > p1_wins:
            category_winners[category] = "player2"
        else:
            category_winners[category] = "tie"
    
    # Return enhanced comparison data
    return {
        "players": [enhanced_player1, enhanced_player2],
        "metric_winners": metric_winners,
        "overall_winner": overall_winner,
        "categorized_metrics": categorized_metrics,
        "category_winners": category_winners,
        "comparison_text": comparison_text,
        "negative_metrics": NEGATIVE_METRICS
    }
