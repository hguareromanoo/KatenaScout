"""
Player comparison functionality for KatenaScout
"""

from typing import List, Dict, Any, Optional
from models.parameters import SearchParameters

def compare_players(
    players: List[Dict[str, Any]], 
    session_manager,
    language: str = "english",
    search_weights: Dict[str, float] = None,
    playing_style: str = "",
    formation: str = ""
) -> Dict[str, Any]:
    """
    Generate a comparison between players
    
    Args:
        players: List of player data to compare (at least 2)
        session_manager: The session manager for API calls
        language: Language for the comparison
        search_weights: Optional weights from search parameters
        
    Returns:
        Dictionary with comparison text and aspects compared
    """
    # Ensure we have at least 2 players to compare
    if len(players) < 2:
        return {
            "comparison": "Not enough players to compare.",
            "comparison_aspects": [],
            "enhanced_data": None
        }
    
    # Extract key information for each player to include in the comparison
    player_info = []
    for player in players:
        # Create a simplified player data structure for the prompt
        player_data = {
            "name": player.get("name", "Unknown"),
            "positions": player.get("positions", []),
            "age": player.get("age"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "foot": player.get("foot"),
            "nationality": player.get("nationality"),
            "stats": player.get("stats", {})
        }
        player_info.append(player_data)

    # Format player data for the prompt
    player_descriptions = []
    for i, p in enumerate(player_info, 1):
        # Format each player's data for the prompt
        stats_str = "\n".join([f"  - {k}: {v}" for k, v in p.get("stats", {}).items()])
        desc = f"Player {i}: {p['name']}\n"
        desc += f"Positions: {', '.join(p.get('positions', ['Unknown']))}\n"
        if p.get('age'):
            desc += f"Age: {p['age']}\n"
        if p.get('height'):
            desc += f"Height: {p['height']} cm\n"
        if p.get('nationality'):
            desc += f"Nationality: {p['nationality']}\n"
        if p.get('foot'):
            desc += f"Preferred Foot: {p['foot']}\n"
        desc += f"Stats:\n{stats_str}"
        player_descriptions.append(desc)
    
    all_players_description = "\n\n".join(player_descriptions)
    
    # Generate system prompt based on language
    system_prompt = get_language_specific_prompt(language)
    
    # Create tactical context if provided
    tactical_context = {
        "english": f"\nPlease analyze them specifically for a {playing_style.replace('_', ' ').title()} style of play in a {formation} formation.",
        "portuguese": f"\nPor favor, analise-os especificamente para um estilo de jogo {playing_style.replace('_', ' ').title()} em uma formação {formation}.",
        "spanish": f"\nPor favor, analízalos específicamente para un estilo de juego {playing_style.replace('_', ' ').title()} en una formación {formation}.",
        "bulgarian": f"\nМоля, анализирайте ги специално за стил на игра {playing_style.replace('_', ' ').title()} във формация {formation}."
    } if playing_style and formation else {
        "english": "",
        "portuguese": "",
        "spanish": "",
        "bulgarian": ""
    }
    
    # Get language-specific user prompts
    user_prompts = {
        "english": f"""Please compare the following players:

{all_players_description}{tactical_context["english"]}

Compare these players focusing on their strengths, weaknesses, and how they differ from each other. Consider their statistics, positions, and overall profiles.

First, provide a detailed comparison highlighting the main differences between these players in terms of their strengths, weaknesses, and playing styles.

Then, identify the key aspects you compared (like "Passing", "Shooting", "Physical Presence", etc.) and list them separately at the end as "Key comparison aspects: [aspect1], [aspect2], etc."
""",
        "portuguese": f"""Por favor, compare os seguintes jogadores:

{all_players_description}{tactical_context["portuguese"]}

Compare estes jogadores focando em seus pontos fortes, pontos fracos e como eles diferem um do outro. Considere suas estatísticas, posições e perfis gerais.

Primeiro, forneça uma comparação detalhada destacando as principais diferenças entre estes jogadores em termos de pontos fortes, pontos fracos e estilos de jogo.

Em seguida, identifique os principais aspectos que você comparou (como "Passe", "Finalização", "Presença Física", etc.) e liste-os separadamente no final como "Aspectos chave de comparação: [aspecto1], [aspecto2], etc."
""",
        "spanish": f"""Por favor, compara los siguientes jugadores:

{all_players_description}{tactical_context["spanish"]}

Compara estos jugadores centrándote en sus fortalezas, debilidades y cómo se diferencian entre sí. Considera sus estadísticas, posiciones y perfiles generales.

Primero, proporciona una comparación detallada destacando las principales diferencias entre estos jugadores en términos de sus fortalezas, debilidades y estilos de juego.

Luego, identifica los aspectos clave que comparaste (como "Pases", "Tiro", "Presencia Física", etc.) y enuméralos por separado al final como "Aspectos clave de comparación: [aspecto1], [aspecto2], etc."
""",
        "bulgarian": f"""Моля, сравнете следните играчи:

{all_players_description}{tactical_context["bulgarian"]}

Сравнете тези играчи, фокусирайки се върху техните силни страни, слаби страни и как се различават един от друг. Вземете предвид техните статистики, позиции и цялостни профили.

Първо, предоставете подробно сравнение, подчертаващо основните разлики между тези играчи по отношение на техните силни страни, слаби страни и стилове на игра.

След това, идентифицирайте ключовите аспекти, които сте сравнили (като "Подаване", "Стрелба", "Физическо присъствие" и т.н.) и ги изброете отделно в края като "Ключови аспекти на сравнение: [аспект1], [аспект2], и т.н."
"""
    }
    
    # Get the appropriate user message based on language
    user_message = user_prompts.get(language, user_prompts["english"])

    # Call Claude API to generate the comparison
    response = session_manager.call_claude_api(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    # Extract the comparison text from the content array
    comparison_text = ""
    for content_item in response.content:
        if hasattr(content_item, 'text'):
            comparison_text += content_item.text
    
    # Extract comparison aspects from the response
    aspects = []
    if "Key comparison aspects:" in comparison_text:
        try:
            # Try to extract the aspects list
            aspects_text = comparison_text.split("Key comparison aspects:")[1].strip()
            aspects_text = aspects_text.split("\n")[0].strip()  # Take just the first line
            
            # Remove common formatting like brackets, quotes
            aspects_text = aspects_text.replace("[", "").replace("]", "")
            aspects_text = aspects_text.replace("'", "").replace("\"", "")
            
            # Split the comma-separated list
            aspects = [aspect.strip() for aspect in aspects_text.split(",")]
        except Exception as e:
            print(f"Error extracting comparison aspects: {e}")
            # Fall back to default aspects
            aspects = ["Technical Ability", "Physical Attributes", "Tactical Understanding", "Experience"]
    else:
        # Fall back to default aspects if not found
        aspects = ["Technical Ability", "Physical Attributes", "Tactical Understanding", "Experience"]
    
    # Use enhanced comparison module to get metric-by-metric analysis
    try:
        from core.enhanced_comparison import enhance_player_comparison
        enhanced_data = enhance_player_comparison(
            players=players,
            comparison_text=comparison_text,
            search_weights=search_weights
        )
    except Exception as e:
        print(f"Error in enhanced comparison: {str(e)}")
        enhanced_data = None
    
    return {
        "comparison": comparison_text,
        "comparison_aspects": aspects,
        "enhanced_data": enhanced_data
    }

def find_players_for_comparison(
    session_manager,
    session_id: str,
    player_identifiers: List[str],  # Changed from player_ids to be more generic
    language: str = "english"
) -> List[Dict[str, Any]]:
    """
    Find players for comparison based on provided IDs or names
    
    Args:
        session_manager: The session manager for API calls
        session_id: Session ID for tracking
        player_identifiers: List of player IDs or names to find
        language: Language for the comparison
        
    Returns:
        List of player data dictionaries
    """
    result_players = []
    
    # Get the session
    session = session_manager.get_session(session_id, language)
    print(f"Looking for players with identifiers: {player_identifiers}")
    
    # Step 1: Try to find players in memory first (from previous searches)
    if hasattr(session, "selected_players") and session.selected_players:
        for identifier in player_identifiers:
            # First try to find player in memory by exact ID match
            memory_player = next(
                (p for p in session.selected_players if str(p.get("id", "")) == str(identifier) or
                 str(p.get("wyId", "")) == str(identifier)),
                None
            )
            
            # If not found by ID, try by name (case-insensitive)
            if not memory_player:
                memory_player = next(
                    (p for p in session.selected_players if 
                     p.get("name", "").lower() == identifier.lower() or
                     identifier.lower() in p.get("name", "").lower()),
                    None
                )
            
            if memory_player:
                print(f"Found player in memory: {memory_player.get('name')}")
                result_players.append(memory_player)
    
    # Step 2: Determine which identifiers we still need to find
    remaining_identifiers = []
    for identifier in player_identifiers:
        # Check if we already found this player by ID
        id_found = any(
            str(p.get("id", "")) == str(identifier) or str(p.get("wyId", "")) == str(identifier)
            for p in result_players
        )
        
        # Check if we already found this player by name
        name_found = any(
            p.get("name", "").lower() == identifier.lower() or 
            identifier.lower() in p.get("name", "").lower()
            for p in result_players
        )
        
        # If neither found, add to remaining list
        if not id_found and not name_found:
            remaining_identifiers.append(identifier)
    
    # Step 3: For remaining identifiers, try direct ID lookup first
    for identifier in remaining_identifiers[:]:  # Use a copy to safely remove items
        try:
            # Try to get player by ID directly first
            print(f"Trying direct ID lookup for: {identifier}")
            player_info = session_manager.get_players_info(identifier)
            
            if player_info and not player_info.get('error'):
                print(f"Found player by ID lookup: {player_info.get('name')}")
                result_players.append(player_info)
                remaining_identifiers.remove(identifier)  # Remove from remaining list
        except Exception as e:
            print(f"Error in direct ID lookup for {identifier}: {e}")
            # Continue to try other methods
    
    # Step 4: For any still remaining, try name search (prioritize those with spaces)
    # First sort identifiers to check those with spaces first (likely names)
    remaining_identifiers.sort(key=lambda x: 0 if ' ' in x else 1)
    
    for identifier in remaining_identifiers:
        try:
            # Search for players by name
            from models.parameters import SearchParameters
            search_params = SearchParameters(
                player_name=identifier,
                is_name_search=True
            )
            
            print(f"Searching for player by name: {identifier}")
            search_results = session_manager.search_players(search_params)
            
            if search_results and len(search_results) > 0:
                # Take the first match
                player = search_results[0]
                print(f"Found player by name search: {player.get('name')}")
                
                # Check if this player is already in results
                is_duplicate = False
                for existing_player in result_players:
                    # Check by name since IDs might be missing
                    if existing_player.get("name") == player.get("name"):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    print(f"Adding player from name search: {player.get('name')}")
                    result_players.append(player)
                else:
                    print(f"Skipping duplicate player: {player.get('name')}")
            else:
                print(f"No players found for identifier: {identifier}")
        except Exception as e:
            print(f"Error searching for player by name {identifier}: {e}")
    
    # Step 5: Final check and logging
    print(f"Found {len(result_players)} players for comparison")
    if len(result_players) < 2:
        print(f"WARNING: Not enough players found for comparison. Need at least 2, found {len(result_players)}")
    
    return result_players

def get_language_specific_prompt(language: str) -> str:
    """Get language-specific system prompt for player comparison"""
    prompts = {
        "english": """You are a football expert system that compares players based on their statistics and profiles.
Your task is to provide clear, insightful comparisons highlighting key differences between players.
Focus on their strengths, weaknesses, playing styles, and how they might fit different tactical systems.
Use football terminology appropriately but ensure explanations remain accessible.
Always back up your comparisons with specific statistical evidence.
End your analysis by listing the key aspects you compared.""",

        "portuguese": """Você é um sistema especialista em futebol que compara jogadores com base em suas estatísticas e perfis.
Sua tarefa é fornecer comparações claras e perspicazes destacando as principais diferenças entre jogadores.
Concentre-se em seus pontos fortes, pontos fracos, estilos de jogo e como eles podem se adequar a diferentes sistemas táticos.
Use terminologia de futebol adequadamente, mas garanta que as explicações permaneçam acessíveis.
Sempre apoie suas comparações com evidências estatísticas específicas.
Termine sua análise listando os principais aspectos que você comparou.""",

        "spanish": """Eres un sistema experto en fútbol que compara jugadores según sus estadísticas y perfiles.
Tu tarea es proporcionar comparaciones claras y perspicaces destacando las diferencias clave entre jugadores.
Concéntrate en sus fortalezas, debilidades, estilos de juego y cómo podrían adaptarse a diferentes sistemas tácticos.
Utiliza la terminología futbolística de manera apropiada pero asegúrate de que las explicaciones sigan siendo accesibles.
Respalda siempre tus comparaciones con evidencia estadística específica.
Finaliza tu análisis enumerando los aspectos clave que comparaste.""",

        "bulgarian": """Вие сте експертна футболна система, която сравнява играчи въз основа на техните статистики и профили.
Вашата задача е да предоставите ясни, проницателни сравнения, подчертавайки ключовите разлики между играчите.
Фокусирайте се върху техните силни страни, слабости, стилове на игра и как биха паснали в различни тактически системи.
Използвайте футболна терминология по подходящ начин, но се уверете, че обясненията остават достъпни.
Винаги подкрепяйте сравненията си с конкретни статистически доказателства.
Завършете анализа си, като изброите ключовите аспекти, които сте сравнили."""
    }
    
    return prompts.get(language, prompts["english"])