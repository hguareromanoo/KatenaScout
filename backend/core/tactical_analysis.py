"""
Tactical analysis module for player comparisons in specific playing styles

This module evaluates how well players fit into different tactical styles
and playing formations.
"""

from typing import List, Dict, Any, Optional, Tuple
import copy

# Import negative metrics from enhanced_comparison
try:
    from core.enhanced_comparison import NEGATIVE_METRICS
except ImportError:
    # Alternative import path for when running within the package
    try:
        from core.enhanced_comparison import NEGATIVE_METRICS
    except ImportError:
        # Fallback if both fail
        NEGATIVE_METRICS = [
            "ballLosses", "miscontrols", "dispossessed", "challengeLost", 
            "foulsCommitted", "yellowCards", "redCards", "errorLeadToShot",
            "errorLeadToGoal", "penaltyConceded", "ownGoals", "dribbledPast",
            "dangerousOwnHalfLosses", "possessionLost"
        ]

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


def calculate_tactical_fit(
    player: Dict[str, Any],
    style: str,
    formation: str
) -> Dict[str, Any]:
    """
    Calculate how well a player fits a tactical style and formation
    
    Args:
        player: Player data with stats
        style: Tactical style key (e.g., "possession_based")
        formation: Formation string (e.g., "4-3-3")
        
    Returns:
        Dictionary with tactical fit data
    """
    if style not in TACTICAL_STYLES:
        return {"error": f"Unknown tactical style: {style}"}
    
    # Get style weights
    style_weights = TACTICAL_STYLES[style]
    
    # Calculate tactical style score
    style_score = 0.0
    style_max_score = 0.0
    matched_metrics = 0
    player_stats = player.get("stats", {})
    
    # Analyze each metric in the style
    style_analysis = {}
    for metric, weight in style_weights.items():
        if metric in player_stats:
            value = player_stats[metric]
            
            # Skip non-numeric values
            if not isinstance(value, (int, float)):
                continue
                
            # Handle negative metrics (lower is better)
            if metric in NEGATIVE_METRICS:
                # Invert the value for negative metrics so higher is always better
                # Use a simple inversion: 100 - value (assuming 0-100 scale)
                normalized_value = max(0, 100 - value)
                value_for_display = value  # Keep original for display
            else:
                normalized_value = value
                value_for_display = value
                
            style_score += normalized_value * weight
            style_max_score += 100 * weight  # Assuming normalized 0-100 values
            matched_metrics += 1
            
            # Add to metric analysis
            style_analysis[metric] = {
                "value": value_for_display,
                "weight": weight,
                "weighted_score": normalized_value * weight,
                "is_negative": metric in NEGATIVE_METRICS
            }
    
    # Normalize style score (0-100)
    if style_max_score > 0:
        normalized_style_score = (style_score / style_max_score) * 100
    else:
        normalized_style_score = 0
        
    # Get positions and calculate formation fit
    positions = player.get("positions", [])
    formation_positions = FORMATIONS.get(formation, [])
    
    # Check how many of player's positions match formation positions
    position_matches = sum(1 for pos in positions if pos in formation_positions)
    position_fit = position_matches / len(positions) if positions else 0
    
    return {
        "style_score": normalized_style_score,
        "matched_metrics": matched_metrics,
        "total_metrics": len(style_weights),
        "position_fit": position_fit,
        "metric_analysis": style_analysis,
        "key_strengths": get_key_strengths(style_analysis, 3),
        "key_weaknesses": get_key_weaknesses(style_analysis, 2)
    }


def get_key_strengths(metric_analysis: Dict[str, Dict], count: int = 3) -> List[Dict]:
    """Get the top metrics by weighted score"""
    sorted_metrics = sorted(
        [{"metric": m, **data} for m, data in metric_analysis.items()],
        key=lambda x: x["weighted_score"],
        reverse=True
    )
    return sorted_metrics[:count]


def get_key_weaknesses(metric_analysis: Dict[str, Dict], count: int = 2) -> List[Dict]:
    """Get the bottom metrics by weighted score"""
    sorted_metrics = sorted(
        [{"metric": m, **data} for m, data in metric_analysis.items()],
        key=lambda x: x["weighted_score"]
    )
    return sorted_metrics[:count]


def compare_players_tactically(
    players: List[Dict[str, Any]],
    style: str,
    formation: str
) -> Dict[str, Any]:
    """
    Compare two players based on tactical style and formation
    
    Args:
        players: List of two player data dictionaries
        style: Tactical style key
        formation: Formation string
        
    Returns:
        Tactical comparison data
    """
    if len(players) != 2:
        return {"error": "Exactly two players required for tactical comparison"}
    
    if style not in TACTICAL_STYLES:
        style = "balanced_approach"  # Default to balanced if style not found
    
    if formation not in FORMATIONS:
        formation = "4-3-3"  # Default to 4-3-3 if formation not found
    
    player1 = players[0]
    player2 = players[1]
    
    # Calculate fit for each player
    player1_fit = calculate_tactical_fit(player1, style, formation)
    player2_fit = calculate_tactical_fit(player2, style, formation)
    
    # Determine overall tactical winner
    if player1_fit["style_score"] > player2_fit["style_score"]:
        tactical_winner = "player1"
        winner_name = player1.get("name", "Player 1")
        margin = player1_fit["style_score"] - player2_fit["style_score"]
    elif player2_fit["style_score"] > player1_fit["style_score"]:
        tactical_winner = "player2"
        winner_name = player2.get("name", "Player 2")
        margin = player2_fit["style_score"] - player1_fit["style_score"]
    else:
        tactical_winner = "tie"
        winner_name = "Tie"
        margin = 0
    
    # Get metrics where one player is significantly better (at least 20% difference)
    key_differences = []
    style_metrics = TACTICAL_STYLES[style]
    for metric in style_metrics:
        p1_value = player1.get("stats", {}).get(metric, 0)
        p2_value = player2.get("stats", {}).get(metric, 0)
        weight = style_metrics.get(metric, 1.0)
        
        # Skip if both are 0
        if p1_value == 0 and p2_value == 0:
            continue
            
        # Skip if values are not numeric
        if not isinstance(p1_value, (int, float)) or not isinstance(p2_value, (int, float)):
            continue
            
        # Calculate percentage difference
        max_val = max(p1_value, p2_value)
        if max_val > 0:
            diff_percent = abs(p1_value - p2_value) / max_val * 100
            
            # Determine which player is better
            is_negative = metric in NEGATIVE_METRICS
            
            if is_negative:
                # For negative metrics, lower is better
                better_player = "player1" if p1_value < p2_value else "player2"
            else:
                # For positive metrics, higher is better
                better_player = "player1" if p1_value > p2_value else "player2"
            
            if diff_percent >= 20:  # Significant difference threshold
                key_differences.append({
                    "metric": metric,
                    "player1_value": p1_value,
                    "player2_value": p2_value,
                    "weight": weight,
                    "better_player": better_player,
                    "diff_percent": diff_percent
                })
    
    # Sort key differences by weight * difference
    key_differences.sort(
        key=lambda x: x["weight"] * x["diff_percent"], 
        reverse=True
    )
    
    # Get display name for style
    style_display_name = STYLE_DISPLAY_NAMES_REVERSE.get(style, style.replace("_", " ").title())
    
    return {
        "player1_name": player1.get("name", "Player 1"),
        "player2_name": player2.get("name", "Player 2"),
        "player1_fit": player1_fit,
        "player2_fit": player2_fit,
        "tactical_winner": tactical_winner,
        "winner_name": winner_name,
        "margin": margin,
        "key_differences": key_differences[:5],  # Top 5 key differences
        "style": style,
        "style_display_name": style_display_name,
        "style_description": STYLE_DESCRIPTIONS.get(style, ""),
        "formation": formation
    }


def generate_tactical_analysis(
    players: List[Dict[str, Any]],
    original_query: str,
    playing_style: str,
    formation: str,
    session_manager,
    language: str = "english"
) -> Dict[str, Any]:
    """
    Generate a tactical analysis comparing players in a specific context
    
    Args:
        players: List of player data
        original_query: Original search query 
        playing_style: Playing style key or display name
        formation: Formation string
        session_manager: Session manager for API calls
        language: Language for the analysis
        
    Returns:
        TacticalAnalysisResponse as dictionary
    """
    try:
        from models.response import TacticalAnalysisResponse, PlayerTacticalAnalysis
    except ImportError:
        # If models can't be imported, create simple dictionary structure
        def create_response_dict(**kwargs):
            return kwargs
        
        # Fallback return function if models can't be imported
        def create_simple_response(analysis_text, tactical_comparison, style_key, formation, language):
            return {
                "success": True,
                "tactical_description": tactical_comparison['style_description'],
                "players": [
                    {
                        "name": players[0].get('name', 'Player 1'),
                        "description": "Analysis not available in structured format",
                        "fit_score": tactical_comparison['player1_fit']['style_score'],
                        "key_strengths": [],
                        "key_weaknesses": []
                    },
                    {
                        "name": players[1].get('name', 'Player 2'),
                        "description": "Analysis not available in structured format",
                        "fit_score": tactical_comparison['player2_fit']['style_score'],
                        "key_strengths": [],
                        "key_weaknesses": []
                    }
                ],
                "winner": tactical_comparison['winner_name'],
                "language": language,
                "playing_style": style_key,
                "formation": formation,
                "comparison_text": analysis_text
            }
    
    # Get style key from display name if needed
    style_key = STYLE_DISPLAY_NAMES.get(playing_style, playing_style)
    
    # If still not found, convert to snake_case
    if style_key not in TACTICAL_STYLES:
        style_key = playing_style.lower().replace(" ", "_")
    
    # If still not found, default to balanced approach
    if style_key not in TACTICAL_STYLES:
        style_key = "balanced_approach"
    
    # Get tactical comparison data
    tactical_comparison = compare_players_tactically(players, style_key, formation)
    
    if "error" in tactical_comparison:
        error_msg = f"Error in tactical analysis: {tactical_comparison['error']}"
        return {
            "success": False,
            "tactical_description": error_msg,
            "players": [],
            "winner": "",
            "language": language,
            "playing_style": style_key,
            "formation": formation,
            "comparison_text": error_msg
        }
    
    # Create player descriptions with tactical fit info
    player_descriptions = []
    for i, (player, fit_key) in enumerate(
        [(players[0], "player1_fit"), (players[1], "player2_fit")], 1
    ):
        fit = tactical_comparison[fit_key]
        
        # Get stats string focusing on style-relevant metrics
        stats = []
        for metric, weight in TACTICAL_STYLES[style_key].items():
            if metric in player.get("stats", {}):
                value = player.get("stats", {}).get(metric, 0)
                stats.append(f"  - {metric}: {value} (style importance: {weight})")
        
        stats_str = "\n".join(stats)
        
        # Create description
        desc = f"Player {i}: {player.get('name', 'Unknown')}\n"
        desc += f"Positions: {', '.join(player.get('positions', ['Unknown']))}\n"
        desc += f"Tactical style fit score: {fit['style_score']:.1f}/100\n"
        desc += f"Key strengths for this style:\n"
        
        for strength in fit["key_strengths"]:
            desc += f"  - {strength['metric']}: {strength['value']} (weighted importance: {strength['weighted_score']:.1f})\n"
        
        desc += f"Relevant stats for {playing_style} style:\n{stats_str}"
        player_descriptions.append(desc)
    
    all_players_description = "\n\n".join(player_descriptions)
    
    # Create language-specific examples
    examples = ""
    if language == "portuguese":
        examples = """
Exemplo de formato esperado:
TACTICAL_DESCRIPTION: O estilo de jogo de posse de bola exige jogadores com...
PLAYER1_ANALYSIS: Ronaldo demonstra excelentes habilidades de...
PLAYER2_ANALYSIS: Messi, por outro lado, se destaca em...
RECOMMENDATION: Considerando o estilo de jogo de posse, Messi é mais adequado porque...
"""
    elif language == "spanish":
        examples = """
Ejemplo del formato esperado:
TACTICAL_DESCRIPTION: El estilo de juego de posesión requiere jugadores con...
PLAYER1_ANALYSIS: Ronaldo demuestra excelentes habilidades de...
PLAYER2_ANALYSIS: Messi, por otro lado, destaca en...
RECOMMENDATION: Considerando el estilo de juego de posesión, Messi es más adecuado porque...
"""
    elif language == "bulgarian":
        examples = """
Пример за очаквания формат:
TACTICAL_DESCRIPTION: Стилът на игра с притежание изисква играчи с...
PLAYER1_ANALYSIS: Роналдо демонстрира отлични умения за...
PLAYER2_ANALYSIS: Меси, от друга страна, се отличава в...
RECOMMENDATION: Като се има предвид стила на игра с притежание, Меси е по-подходящ, защото...
"""

    # Create the prompt with structured response requirements
    prompt = f"""Compare these players specifically for a {playing_style} style of play in a {formation} formation:

{all_players_description}

Tactical comparison summary:
- Overall tactical winner: {tactical_comparison['winner_name']} 
- Fit score margin: {tactical_comparison['margin']:.1f} points
- Style description: {tactical_comparison['style_description']}

Key metric differences:
{chr(10).join([f"- {d['metric']}: {d['player1_value']} vs {d['player2_value']} (advantage: {tactical_comparison['player1_name'] if d['better_player'] == 'player1' else tactical_comparison['player2_name']})" for d in tactical_comparison['key_differences']])}

Original search query: "{original_query}"

Please provide a detailed tactical analysis comparing these players specifically for a {playing_style} playing style in a {formation} formation, addressing:

1. How each player's strengths and weaknesses align with this playing style
2. Specific roles each player could fulfill in this formation
3. Game situations where one player would be more effective than the other
4. How each player's metrics directly contribute to this tactical approach
5. Final recommendation with clear reasoning

Your response MUST be formatted in a structured way, with these distinct sections:
- TACTICAL_DESCRIPTION: A clear explanation of the {playing_style} system and what this formation requires from players
- PLAYER1_ANALYSIS: A detailed description of {players[0].get('name')}'s tactical fit, strengths, and weaknesses for this system
- PLAYER2_ANALYSIS: A detailed description of {players[1].get('name')}'s tactical fit, strengths, and weaknesses for this system
- RECOMMENDATION: The name of the player who better fits this tactical system and why

{examples}

Be specific and refer to the actual metric values in your analysis.
"""
    
    # Get language-specific system prompt
    try:
        from core.comparison import get_language_specific_prompt
        system_prompt = get_language_specific_prompt(language)
    except ImportError:
        try:
            from core.comparison import get_language_specific_prompt
            system_prompt = get_language_specific_prompt(language)
        except ImportError:
            # Fallback to a default prompt if imports fail
            system_prompt = f"""You are a football expert system that analyzes players based on their statistics and profiles.
            Your task is to provide clear, insightful analysis comparing players in a {playing_style} playing style and {formation} formation.
            Focus on their strengths, weaknesses, playing styles, and how they might fit this specific tactical approach.
            Use football terminology appropriately but ensure explanations remain accessible.
            Always back up your analysis with specific statistical evidence."""
    
    # Add tactical context to system prompt with stronger language instruction
    lang_instruction = ""
    if language == "portuguese":
        lang_instruction = "IMPORTANTE: Você DEVE responder em português. Toda a sua análise deve ser escrita em português."
    elif language == "spanish":
        lang_instruction = "IMPORTANTE: DEBES responder en español. Todo tu análisis debe estar escrito en español."
    elif language == "bulgarian":
        lang_instruction = "ВАЖНО: ТРЯБВА да отговориш на български. Целият ти анализ трябва да бъде написан на български."
    else:
        lang_instruction = "IMPORTANT: You MUST respond in English. All your analysis should be written in English."
    
    system_prompt += f"\nYou are a tactical analyst who understands how player attributes translate to effectiveness in different playing styles and formations. {lang_instruction}"
    
    # Call Claude API
    response = session_manager.call_claude_api(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1800,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the analysis text from the content array
    analysis_text = ""
    if hasattr(response, 'content'):
        for content_item in response.content:
            if hasattr(content_item, 'text'):
                analysis_text += content_item.text
    
    # Parse the structured response
    tactical_description = ""
    player1_analysis = ""
    player2_analysis = ""
    recommendation = ""
    
    # Extract sections using regex or string splitting
    import re
    
    # Try to find sections with regex
    tactical_desc_match = re.search(r"TACTICAL_DESCRIPTION:(.*?)(?=PLAYER1_ANALYSIS:|$)", analysis_text, re.DOTALL)
    player1_match = re.search(r"PLAYER1_ANALYSIS:(.*?)(?=PLAYER2_ANALYSIS:|$)", analysis_text, re.DOTALL)
    player2_match = re.search(r"PLAYER2_ANALYSIS:(.*?)(?=RECOMMENDATION:|$)", analysis_text, re.DOTALL)
    recommendation_match = re.search(r"RECOMMENDATION:(.*?)(?=$)", analysis_text, re.DOTALL)
    
    if tactical_desc_match:
        tactical_description = tactical_desc_match.group(1).strip()
    if player1_match:
        player1_analysis = player1_match.group(1).strip()
    if player2_match:
        player2_analysis = player2_match.group(1).strip()
    if recommendation_match:
        recommendation = recommendation_match.group(1).strip()
    
    # If regex failed, try fallback to simple string partition
    if not tactical_description:
        parts = analysis_text.split("PLAYER1_ANALYSIS:")
        if len(parts) > 1:
            tactical_part = parts[0]
            if "TACTICAL_DESCRIPTION:" in tactical_part:
                tactical_description = tactical_part.split("TACTICAL_DESCRIPTION:")[1].strip()
    
    if not player1_analysis and "PLAYER1_ANALYSIS:" in analysis_text:
        parts = analysis_text.split("PLAYER1_ANALYSIS:")[1].split("PLAYER2_ANALYSIS:")
        if len(parts) > 0:
            player1_analysis = parts[0].strip()
    
    if not player2_analysis and "PLAYER2_ANALYSIS:" in analysis_text:
        parts = analysis_text.split("PLAYER2_ANALYSIS:")[1].split("RECOMMENDATION:")
        if len(parts) > 0:
            player2_analysis = parts[0].strip()
    
    if not recommendation and "RECOMMENDATION:" in analysis_text:
        recommendation = analysis_text.split("RECOMMENDATION:")[1].strip()
    
    # Extract winner name from recommendation (first few words)
    winner_name = tactical_comparison['winner_name']  # Default to calculated winner
    if recommendation:
        # Try to extract player name from the first sentence
        first_sentence = recommendation.split('.')[0]
        for player in players:
            if player.get('name', '') in first_sentence:
                winner_name = player.get('name', '')
                break
    
    # Extract key strengths and weaknesses from fits
    player1_strengths = [s["metric"] for s in tactical_comparison["player1_fit"]["key_strengths"]]
    player1_weaknesses = [w["metric"] for w in tactical_comparison["player1_fit"]["key_weaknesses"]]
    
    player2_strengths = [s["metric"] for s in tactical_comparison["player2_fit"]["key_strengths"]]
    player2_weaknesses = [w["metric"] for w in tactical_comparison["player2_fit"]["key_weaknesses"]]
    
    # Create structured player tactical analysis objects
    player_analyses = [
        {
            "name": players[0].get('name', 'Player 1'),
            "description": player1_analysis,
            "fit_score": tactical_comparison['player1_fit']['style_score'],
            "key_strengths": player1_strengths,
            "key_weaknesses": player1_weaknesses
        },
        {
            "name": players[1].get('name', 'Player 2'),
            "description": player2_analysis,
            "fit_score": tactical_comparison['player2_fit']['style_score'],
            "key_strengths": player2_strengths,
            "key_weaknesses": player2_weaknesses
        }
    ]
    
    # Create TacticalAnalysisResponse
    response_dict = {
        "success": True,
        "tactical_description": tactical_description if tactical_description else tactical_comparison['style_description'],
        "players": player_analyses,
        "winner": winner_name,
        "language": language,
        "playing_style": style_key,
        "formation": formation,
        "comparison_text": analysis_text
    }
    
    # Try to create a proper Pydantic model if available
    try:
        from models.response import TacticalAnalysisResponse, PlayerTacticalAnalysis
        player_models = [
            PlayerTacticalAnalysis(**player_data) for player_data in player_analyses
        ]
        return TacticalAnalysisResponse(
            **{**response_dict, "players": player_models}
        ).model_dump()
    except (ImportError, Exception) as e:
        # Fallback to dictionary if model creation fails
        return response_dict