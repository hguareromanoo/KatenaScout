"""
Player comparison functionality for KatenaScout
"""

from typing import List, Dict, Any, Optional
from models.parameters import SearchParameters
import json # Added for formatting player data
import os # Added for path joining
import unicodedata # Added for name normalization

# Import constants related to player images
from config import PLAYER_IMAGES_DIR
# Import necessary functions from data_service (assuming it exists)
# If these functions are defined elsewhere, adjust the import path
try:
    from services.data_service import find_player_by_id, find_player_by_name
except ImportError:
    print("Warning: Could not import find_player_by_id or find_player_by_name from services.data_service.")
    # Define dummy functions if needed for the code to run without the service
    def find_player_by_id(player_id_str): return None
    def find_player_by_name(name_identifier): return None


# Helper function to get language-specific prompts (moved to top for clarity)
def get_language_specific_comparison_prompt(language: str) -> str:
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

def generate_in_chat_comparison_text(
    players: List[Dict[str, Any]],
    session_manager,
    language: str = "english",
    original_query: str = None, # Added original query for context
    
) -> str:
    """
    Generates a concise textual comparison summary suitable for chat, focusing on relevant stats.

    Args:
        players: List of player data dictionaries (at least 2). Should contain stats fetched by get_players_info.
        session_manager: The session manager instance to call the LLM.
        language: The language for the response.
        original_query: The user's original query that triggered the comparison.
        aspect_params: The parameters extracted from the comparison query, used to determine focus.

    Returns:
        A string containing the comparison text.
    """
    if len(players) < 2:
        return "Cannot generate comparison text, need at least two players."

    player_to_compare =[]

    for player in players:

        player_to_compare.append({
            "name": player.get("name", "Unknown"),
            "positions": player.get("positions", []),
            "age": player.get("age"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "foot": player.get("foot"),
            "contract_expiration": player.get("contractUntil"),
            "stats": player.get("stats", {})
        })
    # System prompt focused on concise chat summary, emphasizing the *provided* stats
    system_prompt = f"""You are a concise football analyst providing quick comparison summaries in {language}. 
Focus on the main differences and key strengths/weaknesses based *only* on the provided data fields (name, positions, age, stats, height, weight). 
Keep the response suitable for a chat interface (a few paragraphs maximum). Do NOT list 'Key comparison aspects'."""

    # User prompt including the potentially filtered player data and original query
    # Use ensure_ascii=False for potentially non-ASCII characters in names/stats
    user_prompt = f"""Based *only* on the provided data below, briefly compare these two players according to the user's request "{original_query or 'compare players'}":

Player 1: {json.dumps(player_to_compare[0], indent=2, ensure_ascii=False)}

Player 2: {json.dumps(player_to_compare[1], indent=2, ensure_ascii=False)}

Provide a short summary comparing their main characteristics and suitability based *specifically on the stats provided* and the user's request. Respond in {language}."""

    try:
        print(f"DEBUG: Calling LLM for in-chat comparison text generation.")
        response = session_manager.call_claude_api(
            model="claude-3-5-sonnet-20241022", # Consider a faster/smaller model if needed
            max_tokens=500, # Limit token usage for chat response
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        # Extract the comparison text
        comparison_text = ""
        if response.content:
             for content_item in response.content:
                  if hasattr(content_item, 'text'):
                       comparison_text += content_item.text
        
        print(f"DEBUG: LLM comparison text generated successfully.")
        return comparison_text if comparison_text else "I couldn't generate a comparison for these players right now."

    except Exception as e:
        print(f"Error generating in-chat comparison text: {str(e)}")
        return f"Sorry, I encountered an error trying to compare the players ({str(e)})."


def compare_players(
    players: List[Dict[str, Any]], 
    session_manager,
    language: str = "english",
    search_weights: Dict[str, float] = None,
    playing_style: str = "",
    formation: str = ""
) -> Dict[str, Any]:
    """
    Generate a detailed comparison between players for the comparison page.
    
    Args:
        players: List of player data to compare (at least 2)
        session_manager: The session manager for API calls
        language: Language for the comparison
        search_weights: Optional weights from search parameters
        playing_style: Optional tactical playing style context
        formation: Optional tactical formation context
        
    Returns:
        Dictionary with detailed comparison text, aspects, and enhanced data.
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
        # Include more stats for detailed comparison
        player_data = {
            "name": player.get("name", "Unknown"),
            "positions": player.get("positions", []),
            "age": player.get("age"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "foot": player.get("foot"),
            "nationality": player.get("nationality"),
            # Use complete_profile stats if available, otherwise fallback to main stats
            "stats": player.get("complete_profile", {}).get("stats", player.get("stats", {})) 
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
    system_prompt = get_language_specific_comparison_prompt(language) # Use helper
    
    # Create tactical context if provided
    tactical_context_dict = {
        "english": f"\nPlease analyze them specifically for a {playing_style.replace('_', ' ').title()} style of play in a {formation} formation.",
        "portuguese": f"\nPor favor, analise-os especificamente para um estilo de jogo {playing_style.replace('_', ' ').title()} em uma formação {formation}.",
        "spanish": f"\nPor favor, analízalos específicamente para un estilo de juego {playing_style.replace('_', ' ').title()} en una formación {formation}.",
        "bulgarian": f"\nМоля, анализирайте ги специално за стил на игра {playing_style.replace('_', ' ').title()} във формация {formation}."
    } if playing_style and formation else { lang: "" for lang in ["english", "portuguese", "spanish", "bulgarian"]}
    
    tactical_context = tactical_context_dict.get(language, "")

    # Get language-specific user prompts
    user_prompts = {
        "english": f"""Please compare the following players:

{all_players_description}{tactical_context}

Compare these players focusing on their strengths, weaknesses, and how they differ from each other. Consider their statistics, positions, and overall profiles.

First, provide a detailed comparison highlighting the main differences between these players in terms of their strengths, weaknesses, and playing styles.

Then, identify the key aspects you compared (like "Passing", "Shooting", "Physical Presence", etc.) and list them separately at the end as "Key comparison aspects: [aspect1], [aspect2], etc."
""",
        "portuguese": f"""Por favor, compare os seguintes jogadores:

{all_players_description}{tactical_context}

Compare estes jogadores focando em seus pontos fortes, pontos fracos e como eles diferem um do outro. Considere suas estatísticas, posições e perfis gerais.

Primeiro, forneça uma comparação detalhada destacando as principais diferenças entre estes jogadores em termos de pontos fortes, pontos fracos e estilos de jogo.

Em seguida, identifique os principais aspectos que você comparou (como "Passe", "Finalização", "Presença Física", etc.) e liste-os separadamente no final como "Aspectos chave de comparação: [aspecto1], [aspecto2], etc."
""",
        "spanish": f"""Por favor, compara los siguientes jugadores:

{all_players_description}{tactical_context}

Compara estos jugadores centrándote en sus fortalezas, debilidades y cómo se diferencian entre sí. Considera sus estadísticas, posiciones y perfiles generales.

Primero, proporciona una comparación detallada destacando las principales diferencias entre estos jugadores en términos de sus fortalezas, debilidades y estilos de juego.

Luego, identifica los aspectos clave que comparaste (como "Pases", "Tiro", "Presencia Física", etc.) y enuméralos por separado al final como "Aspectos clave de comparación: [aspecto1], [aspecto2], etc."
""",
        "bulgarian": f"""Моля, сравнете следните играчи:

{all_players_description}{tactical_context}

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
        max_tokens=1500, # Allow more tokens for detailed comparison
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    # Extract the comparison text from the content array
    comparison_text = ""
    if response.content:
        for content_item in response.content:
            if hasattr(content_item, 'text'):
                comparison_text += content_item.text
    
    # Extract comparison aspects from the response
    aspects = []
    aspects_marker = "Key comparison aspects:"
    if aspects_marker in comparison_text:
        try:
            # Try to extract the aspects list
            aspects_text = comparison_text.split(aspects_marker)[1].strip()
            aspects_text = aspects_text.split("\n")[0].strip()  # Take just the first line
            
            # Remove common formatting like brackets, quotes
            aspects_text = aspects_text.replace("[", "").replace("]", "")
            aspects_text = aspects_text.replace("'", "").replace("\"", "")
            
            # Split the comma-separated list
            aspects = [aspect.strip() for aspect in aspects_text.split(",") if aspect.strip()] # Ensure no empty strings
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
            comparison_text=comparison_text, # Pass the generated text
            search_weights=search_weights
        )
    except Exception as e:
        print(f"Error in enhanced comparison: {str(e)}")
        enhanced_data = None
    
    return {
        "comparison": comparison_text, # The detailed text
        "comparison_aspects": aspects,
        "enhanced_data": enhanced_data # The structured data
    }

def find_players_for_comparison(
    session_manager,
    session_id: str,
    player_identifiers: List[str],  # Changed from player_ids to be more generic
    language: str = "english",
    source: str = "api",  # 'api' or 'chat' to indicate the source of the request
    original_query: str = None  # Original user query for additional context
) -> List[Dict[str, Any]]:
    """
    Find players for comparison based on provided IDs or names
    
    Args:
        session_manager: The session manager for API calls
        session_id: Session ID for tracking
        player_identifiers: List of player IDs or names to find
        language: Language for the comparison
        source: Source of the request - 'api' (direct API call) or 'chat' (from chat interface)
               This affects how we handle identifiers. API calls typically use IDs, 
               while chat interface uses names extracted from natural language.
        
    Returns:
        List of player data dictionaries (stubs with basic info like name, id, wyId)
    """
    # Log source and identifiers for debugging
    print(f"Finding players for comparison from source: {source}")
    print(f"Player identifiers: {player_identifiers}")
    if original_query:
        print(f"Original query: {original_query}")
    
    # Adapt search strategy based on source
    is_chat_source = source == "chat"
    result_players = [] # This will store player stubs (basic info)
    
    # Get the session
    session = session_manager.get_session(session_id, language)
    print(f"Looking for players with identifiers: {player_identifiers}")
    
    # Helper function to normalize a name for comparison
    def normalize_name(name):
        import unicodedata
        # Convert to lowercase and remove accents
        name = name.lower()
        name = unicodedata.normalize('NFKD', name)
        name = ''.join([c for c in name if not unicodedata.combining(c)])
        return name
    
    # Helper function to check if a name is contained within another
    def is_name_part_of(partial_name, full_name):
        if not isinstance(partial_name, str) or not isinstance(full_name, str):
            return False
        
        # Normalize names for comparison
        norm_partial = normalize_name(partial_name)
        norm_full = normalize_name(full_name)
        
        # Check if normalized partial name is in normalized full name
        if norm_partial in norm_full:
            return True
        
        # Check if all words in partial name are in full name
        partial_words = norm_partial.split()
        full_words = norm_full.split()
        return all(word in full_words for word in partial_words)
    
    # Step 1: Try to find players in memory first (from previous searches) with improved matching
    if hasattr(session, "selected_players") and session.selected_players:
        for identifier in player_identifiers:
            # First try to find player in memory by exact ID match
            memory_player = next(
                (p for p in session.selected_players if isinstance(p, dict) and (str(p.get("id", "")) == str(identifier) or str(p.get("wyId", "")) == str(identifier))),
                None
            )
            
            # If not found by ID, try by name with improved matching - only for string identifiers
            if not memory_player and isinstance(identifier, str):
                # Try exact match first (case-insensitive)
                memory_player = next(
                    (p for p in session.selected_players if isinstance(p, dict) and normalize_name(p.get("name", "")) == normalize_name(identifier)),
                    None
                )
                
                # If still not found, try partial name matching
                if not memory_player:
                    memory_player = next(
                        (p for p in session.selected_players if isinstance(p, dict) and (is_name_part_of(identifier, p.get("name", "")) or is_name_part_of(p.get("name", ""), identifier))),
                        None
                    )
            
            if memory_player:
                # Avoid adding duplicates based on name
                if not any(rp.get("name") == memory_player.get("name") for rp in result_players):
                     print(f"Found player in memory: {memory_player.get('name')}")
                     # Add only essential info for the stub
                     result_players.append({
                         "name": memory_player.get("name"),
                         "id": memory_player.get("id"),
                         "wyId": memory_player.get("wyId"),
                         "positions": memory_player.get("positions", []) # Include positions if available
                     })
                else:
                     print(f"Skipping duplicate player from memory: {memory_player.get('name')}")

    
    # Step 2: Determine which identifiers we still need to find
    remaining_identifiers = []
    for identifier in player_identifiers:
        player_found = False
        # Check by ID
        for player in result_players:
            if (str(player.get("id", "")) == str(identifier) or 
                str(player.get("wyId", "")) == str(identifier)):
                player_found = True
                break
        # Check by name
        if not player_found and isinstance(identifier, str):
            for player in result_players:
                if is_name_part_of(identifier, player.get("name", "")):
                    player_found = True
                    break
        if not player_found:
            remaining_identifiers.append(identifier)
    
    print(f"DEBUG: Remaining identifiers after memory check: {remaining_identifiers}")

    # Step 3: For remaining identifiers, try direct ID lookup using find_player_by_id
    if remaining_identifiers:
        ids_to_lookup = [str(id_val) for id_val in remaining_identifiers if isinstance(id_val, (int, float)) or (isinstance(id_val, str) and id_val.isdigit())]
        print(f"DEBUG: Attempting direct ID lookup for: {ids_to_lookup}")
        for player_id_str in ids_to_lookup:
             try:
                  player_data = find_player_by_id(player_id_str) # Use service directly
                  if player_data:
                       # Avoid duplicates
                       if not any(rp.get("name") == player_data.get("name") for rp in result_players):
                            print(f"Found player by ID lookup: {player_data.get('name')}")
                            result_players.append({
                                "name": player_data.get("name"),
                                "id": player_data.get("id"),
                                "wyId": player_data.get("wyId"),
                                "positions": player_data.get("positions", [])
                            })
                            # Attempt to remove the found ID from remaining_identifiers
                            if player_id_str in remaining_identifiers:
                                 remaining_identifiers.remove(player_id_str)
                            # Handle case where identifier might have been int
                            try: 
                                 if int(player_id_str) in remaining_identifiers:
                                      remaining_identifiers.remove(int(player_id_str))
                            except ValueError: pass # Ignore if not an int
                       else:
                            print(f"Skipping duplicate player from ID lookup: {player_data.get('name')}")
                            # Still remove if found
                            if player_id_str in remaining_identifiers:
                                 remaining_identifiers.remove(player_id_str)
                            try:
                                 if int(player_id_str) in remaining_identifiers:
                                      remaining_identifiers.remove(int(player_id_str))
                            except ValueError: pass
             except Exception as e:
                  print(f"Error in direct ID lookup for {player_id_str}: {e}")

    print(f"DEBUG: Remaining identifiers after ID lookup: {remaining_identifiers}")

    # Step 4: For any still remaining (likely names), try name lookup using find_player_by_name
    if remaining_identifiers:
        remaining_names = [name for name in remaining_identifiers if isinstance(name, str)]
        print(f"DEBUG: Attempting name lookup for: {remaining_names}")
        for name_identifier in remaining_names:
            try:
                player_data = find_player_by_name(name_identifier) # Use service directly
                if player_data:
                    # Avoid duplicates
                    if not any(rp.get("name") == player_data.get("name") for rp in result_players):
                        print(f"Found player by name lookup: {player_data.get('name')}")
                        result_players.append({
                            "name": player_data.get("name"),
                            "id": player_data.get("id"),
                            "wyId": player_data.get("wyId"),
                            "positions": player_data.get("positions", [])
                        })
                    else:
                        print(f"Skipping duplicate player from name lookup: {player_data.get('name')}")
                else:
                    print(f"No player found via name lookup for identifier: {name_identifier}")
            except Exception as e:
                print(f"Error in name lookup for {name_identifier}: {e}")

    # Step 5: Final check and logging
    print(f"Found {len(result_players)} players for comparison")
    if len(result_players) < 2:
        print(f"WARNING: Not enough players found for comparison. Need at least 2, found {len(result_players)}")
    
    # Return only the number of players requested initially, prioritizing best matches found
    # Note: This function now returns stubs, the handler needs to fetch full data
    return result_players[:len(player_identifiers)] 

# Note: get_language_specific_prompt was moved to the top
