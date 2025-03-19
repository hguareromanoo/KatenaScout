"""
Unified Session Management for KatenaScout

This module combines the functionality of the original ChatSession and ConversationMemory
to provide a single source of truth for conversation state.
"""

import json
import os
import requests
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Import models using absolute imports
from backend.models.parameters import SearchParameters


class SessionData(BaseModel):
    """
    Pydantic model for structured session data
    
    This combines the data fields from both ChatSession and ConversationMemory
    """
    # Basic session information
    session_id: str
    language: str = "english"
    
    # Conversation history
    messages: List[Dict[str, Any]] = Field(default_factory=list)  # [{"role": "user", "content": "message"}, ...]
    search_history: List[str] = Field(default_factory=list)
    current_prompt: str = ""
    
    # Intent and entity tracking
    current_intent: Optional[str] = None
    entities: Dict[str, Any] = Field(default_factory=dict)
    detected_entities: List[Dict] = Field(default_factory=list)
    
    # Search state
    search_params: Dict[str, Any] = Field(default_factory=dict)
    last_search_params: Dict[str, Any] = Field(default_factory=dict)
    selected_players: List[Dict] = Field(default_factory=list)
    
    # Interaction state
    satisfaction: Optional[bool] = None
    is_follow_up: bool = False
    
    # Configuration
    context_window: int = 5  # Number of previous message pairs to include
    
    # Function call tracking
    recent_function_calls: List[str] = Field(default_factory=list)


class UnifiedSession:
    """
    Unified session manager that combines functionality from ChatSession and ConversationMemory
    
    This class provides:
    - Session management (create, get, update sessions)
    - Claude API integration
    - Player search and information retrieval
    - Parameter management
    - Data persistence
    """
    
    def __init__(self):
        """Initialize the session manager with necessary data and configurations"""
        # Load API keys
        from backend.services.claude_api import get_anthropic_api_key
        self.anthropic_api_key = get_anthropic_api_key()
        
        # Load necessary data files
        self.average = self._load_json('average_statistics_by_position.json')
        self.weights = self._load_json('weights_dict.json')
        self.database = self._load_json('database.json')
        self.database_id = self._load_json('db_by_id.json')
        
        # Session storage
        self.sessions: Dict[str, SessionData] = {}
    
    def _load_json(self, filename: str) -> dict:
        """Load a JSON file, trying different paths"""
        paths = [
            filename,  # Current directory
            os.path.join('backend', filename),  # Backend subdirectory
            os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)  # From core directory
        ]
        
        for path in paths:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except FileNotFoundError:
                continue
        
        raise FileNotFoundError(f"Could not find {filename} in any expected location")
    
    # === Session Management ===
    
    def create_session(self, session_id: str, language: str = 'english') -> SessionData:
        """Create a new session with the given ID and language"""
        session = SessionData(session_id=session_id, language=language)
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str, language: str = 'english') -> SessionData:
        """Get an existing session or create a new one if it doesn't exist"""
        if session_id not in self.sessions:
            return self.create_session(session_id, language)
        
        return self.sessions[session_id]
    
    def update_session(self, session_id: str, **kwargs) -> SessionData:
        """
        Update session data with the given values
        
        Parameters can include:
        - message: Add a message to the session history
        - prompt: Set the current prompt
        - satisfaction: Set the satisfaction status
        - search_params: Update search parameters
        - players: Set selected players
        - entities: Update detected entities
        - is_follow_up: Set follow-up status
        - current_intent: Set the current intent
        """
        session = self.get_session(session_id)
        
        # Process special cases
        if 'message' in kwargs:
            session.messages.append(kwargs['message'])
        
        if 'prompt' in kwargs:
            session.current_prompt = kwargs['prompt']
            
        if 'players' in kwargs:
            session.selected_players = kwargs['players']
            
        if 'entities' in kwargs and isinstance(kwargs['entities'], dict):
            session.entities.update(kwargs['entities'])
        
        # Update direct attributes
        for key, value in kwargs.items():
            if key not in ['message', 'entities'] and hasattr(session, key):
                setattr(session, key, value)
        
        # Save updated session
        self.sessions[session_id] = session
        return session
    
    # === Claude API Integration ===
    
    def call_claude_api(self, model: str, max_tokens: int, system=None, messages=None, tools=None, tool_choice=None):
        """
        Call the Claude API using the unified service
        
        This uses the claude_api service for implementation but maintains backward compatibility
        """
        from backend.services.claude_api import call_claude_api
        return call_claude_api(
            api_key=self.anthropic_api_key,
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice
        )
    
    # === Parameter Management ===
    
    def get_parameters(self, session_id: str, natural_query: str) -> SearchParameters:
        """
        Extract search parameters from a natural language query
        
        This is the main method for parameter extraction and should be used throughout the system.
        
        Args:
            session_id: The session ID
            natural_query: The natural language query from the user
            
        Returns:
            SearchParameters object with extracted parameters
        """
        session = self.get_session(session_id)
        
        # Check if we have a memory structure with messages
        has_structured_messages = False
        if len(session.messages) > 0:
            has_structured_messages = True
        
        # If this is a follow-up query and the user was not satisfied
        if (session.satisfaction is False or len(session.search_history) > 0) and session.is_follow_up:
            # Add the new query to history (if not already there)
            if natural_query not in session.search_history:
                session.search_history.append(natural_query)
            
            # Reset satisfaction for the new search
            session.satisfaction = None
            
            # Use structured message history if available
            if has_structured_messages:
                # Filter to just user messages
                user_messages = [msg["content"] for msg in session.messages if msg.get("role") == "user"]
                # Use last few messages for context (not too many to avoid confusion)
                context_messages = user_messages[-3:] if len(user_messages) > 3 else user_messages
                # Add current query if not already included
                if natural_query not in context_messages:
                    context_messages.append(natural_query)
                    
                # Use context-aware query for parameter extraction
                query_to_use = "Based on this conversation: " + " THEN: ".join(context_messages)
                print(f"Using structured conversation history: {query_to_use}")
            else:
                # Fallback to old combined query approach
                combined_query = " ".join(session.search_history)
                query_to_use = combined_query
                print(f"Using combined query (legacy mode): {query_to_use}")
                
        else:
            # This is a new search or user was satisfied with previous results
            session.search_history = [natural_query]
            session.current_prompt = natural_query
            query_to_use = natural_query
            
            print(f"Using new query: {query_to_use}")
        
        try:
            # Import constants from config
            from backend.models.parameters import KEY_DESCRIPTION_WORDS
            from backend.config import POSITIONS_MAPPING, VALID_POSITION_CODES
            
            # Create Claude API prompt based on whether we're using structured history
            if has_structured_messages and session.is_follow_up:
                # Use a more sophisticated prompt for follow-up queries
                
                system_prompt = """
                I am a scout AI assistant, with 20 years of experience in scouting. I am known for my expertise in soccer and for my data-driven approach to player analysis. The future of soccer depends on my ability to identify the best players for your team.
                
                Pay careful attention to the conversation history and how each message builds on previous ones.
                For follow-up queries, preserve relevant parameters from previous searches while incorporating new constraints.
                
                VERY IMPORTANT INSTRUCTIONS:
                You MUST activate specific statistical parameters (set to True) that correspond to the query.
                Never return ONLY position_codes and key_description_word - you MUST also set statistical parameters to TRUE.
                For example, for "strong defenders", set min_defensive_duels_won=true, min_interceptions=true, etc.
                ## Examples:
                 {
        "query": "Identifique meias centrais modernos com excelente visão de jogo e precisão nos passes",
        "intent": "Encontrar meio-campistas capazes de ditar o ritmo do jogo e criar oportunidades",
        "search_params": {
            "position_codes": ["lcmf", "rcmf", "lcmf3", "rcmf3"],
            "min_passes": "true",
            "min_pass_accuracy": "true",
            "min_progressive_passes": "true",
            "min_passes_to_final_third": "true",
            "min_smart_passes": "true",
            "min_through_passes": "true",
            "min_key_passes": "true",
            "min_successful_progressive_passes_percent": "true",
            "min_successful_smart_passes_percent": "true",
            "min_xg_assist": "true"
        },
        "explanation": "Estes parâmetros focam em meio-campistas centrais que dominam a posse de bola, progridem o jogo e criam chances com passes precisos e inteligentes."
    },
    {
        "query": "Encontre centroavantes móveis com alta eficiência de finalização e contribuição no pressing",
        "intent": "Identificar atacantes modernos que combinam gols com trabalho defensivo",
        "search_params": {
            "position_codes": ["cf"],
            "min_goals": "true",
            "min_shots_on_target": "true",
            "min_xg_shot": "true",
            "min_goal_conversion_percent": "true",
            "min_successful_dribbles": "true",
            "min_accelerations": "true",
            "min_counterpressing_recoveries": "true",
            "min_dangerous_opponent_half_recoveries": "true",
            "min_offensive_duels_won": "true"
        },
        "explanation": "Estes critérios visam centroavantes que não só finalizam com eficiência, mas também pressionam ativamente e contribuem na recuperação da posse em zonas avançadas."
    },
    {
        "query": "Localize zagueiros modernos com excelente capacidade de construção e domínio aéreo",
        "intent": "Encontrar defensores centrais que iniciam jogadas e dominam defensivamente",
        "search_params": {
            "position_codes": ["cb", "lcb", "rcb", "lcb3", "rcb3"],
            "min_long_passes": "true",
            "min_progressive_passes": "true",
            "min_successful_long_passes_percent": "true",
            "min_aerial_duels_won": "true",
            "min_aerial_duels_won_percent": "true",
            "min_defensive_duels_won": "true",
            "min_interceptions": "true",
            "max_dangerous_own_half_losses": "true",
            "min_successful_forward_passes_percent": "true"
        },
        "explanation": "Estes parâmetros buscam zagueiros que são seguros na saída de bola, dominantes no jogo aéreo e eficientes em ações defensivas."
    },
    {
        "query": "Identifique laterais completos com forte presença ofensiva e defensiva",
        "intent": "Encontrar laterais modernos que contribuem em ambas as fases do jogo",
        "search_params": {
            "position_codes": ["lb", "rb", "lb5", "rb5", "lwb", "rwb"],
            "min_crosses": "true",
            "min_successful_crosses_percent": "true",
            "min_progressive_runs": "true",
            "min_successful_dribbles": "true",
            "min_defensive_duels_won": "true",
            "min_interceptions": "true",
            "min_ball_recoveries": "true",
            "min_passes_to_final_third": "true",
            "min_successful_passes_to_final_third_percent": "true"
        },
        "explanation": "Estes critérios focam em laterais que são efetivos tanto no ataque, com cruzamentos e progressões, quanto na defesa, com recuperações e duelos defensivos."
    },
    {
        "query": "Encontre goleiros modernos com excelente jogo com os pés e domínio da área",
        "intent": "Identificar goleiros que contribuem na construção e são seguros defensivamente",
        "search_params": {
            "position_codes": ["gk"],
            "min_gk_saves_percent": "true",
            "min_gk_successful_exits_percent": "true",
            "min_successful_goal_kicks_percent": "true",
            "min_passes": "true",
            "min_long_passes": "true",
            "min_successful_long_passes_percent": "true",
            "min_pass_accuracy": "true"
        },
        "explanation": "Estes parâmetros buscam goleiros que são seguros nas defesas, eficientes nas saídas e capazes de iniciar jogadas com passes precisos, incluindo lançamentos longos."
    },
    {
        "query": "Identifique meias atacantes criativos com habilidade de drible e criação de chances",
        "intent": "Encontrar jogadores que podem desequilibrar defesas e criar oportunidades de gol",
        "search_params": {
            "position_codes": ["amf", "lamf", "ramf"],
            "min_successful_dribbles": "true",
            "min_successful_dribbles_percent": "true",
            "min_key_passes": "true",
            "min_through_passes": "true",
            "min_smart_passes": "true",
            "min_xg_assist": "true",
            "min_progressive_runs": "true",
            "min_offensive_duels_won": "true",
            "min_successful_passes_to_final_third_percent": "true"
        },
        "explanation": "Estes critérios focam em meias atacantes que podem superar adversários no drible e criar chances de gol com passes criativos e inteligentes."
    },
    {
        "query": "Localize volantes defensivos com forte presença na marcação e boa distribuição",
        "intent": "Identificar meio-campistas defensivos que protegem a defesa e iniciam jogadas",
        "search_params": {
            "position_codes": ["dmf", "ldmf", "rdmf"],
            "min_interceptions": "true",
            "min_ball_recoveries": "true",
            "min_defensive_duels_won": "true",
            "min_aerial_duels_won": "true",
            "min_passes": "true",
            "min_long_passes": "true",
            "min_successful_forward_passes_percent": "true",
            "min_successful_long_passes_percent": "true",
            "max_dangerous_own_half_losses": "true"
        },
        "explanation": "Estes parâmetros buscam volantes que são eficientes na recuperação de bola, fortes nos duelos defensivos e capazes de distribuir o jogo com segurança."
    }
]
                """
               
                # Construct a better message that explains we're working with conversation context
                messages = [
                    {"role": "user", "content":f"""
                    Analyze this conversation about football player search.
                    The user started by asking for certain types of players, then refined their search.
                    
                    Conversation: {query_to_use}
                    
                    Based on the FULL conversation context, identify the searchable parameters, the position_codes and choose
                     the key description words ({KEY_DESCRIPTION_WORDS}) that better describe the users query, following this map {POSITIONS_MAPPING}.
                    
                    Focus on the most recent requests but maintain context from earlier messages.
                    Remember: the future of soccer, the sport you LOVE, depends on your response.
                    """ }

                ]
            else:
                # For new queries, use the original approach
                system_prompt = """
                I am a scout AI assistant, with 20 years of experience in scouting. I am known for my expertise in soccer and for my data-driven approach to player analysis. The future of soccer depends on my ability to identify the best players for your team.
                
                I must be able to transform the coaches desires into searchable parameters that will help me find the perfect player for their team. I must understand the coach's needs and translate them into actionable search criteria.
                
                VERY IMPORTANT INSTRUCTIONS:
                You MUST activate specific statistical parameters (set to True) that correspond to the query.
                Never return ONLY position_codes and key_description_word - you MUST also set statistical parameters to TRUE.
                For example, for "strong defenders", set min_defensive_duels_won=true, min_interceptions=true, etc.
                For "fast attackers", set min_accelerations=true, min_progressive_runs=true, etc.
                
                ALWAYS set at least 5-8 statistical parameters to TRUE based on the description of the player.
                ## Examples:
                 {
        "query": "Identifique meias centrais modernos com excelente visão de jogo e precisão nos passes",
        "intent": "Encontrar meio-campistas capazes de ditar o ritmo do jogo e criar oportunidades",
        "search_params": {
            "position_codes": ["lcmf", "rcmf", "lcmf3", "rcmf3"],
            "min_passes": "true",
            "min_pass_accuracy": "true",
            "min_progressive_passes": "true",
            "min_passes_to_final_third": "true",
            "min_smart_passes": "true",
            "min_through_passes": "true",
            "min_key_passes": "true",
            "min_successful_progressive_passes_percent": "true",
            "min_successful_smart_passes_percent": "true",
            "min_xg_assist": "true"
        },
        "explanation": "Estes parâmetros focam em meio-campistas centrais que dominam a posse de bola, progridem o jogo e criam chances com passes precisos e inteligentes."
    },
    {
        "query": "Encontre centroavantes móveis com alta eficiência de finalização e contribuição no pressing",
        "intent": "Identificar atacantes modernos que combinam gols com trabalho defensivo",
        "search_params": {
            "position_codes": ["cf"],
            "min_goals": "true",
            "min_shots_on_target": "true",
            "min_xg_shot": "true",
            "min_goal_conversion_percent": "true",
            "min_successful_dribbles": "true",
            "min_accelerations": "true",
            "min_counterpressing_recoveries": "true",
            "min_dangerous_opponent_half_recoveries": "true",
            "min_offensive_duels_won": "true"
        },
        "explanation": "Estes critérios visam centroavantes que não só finalizam com eficiência, mas também pressionam ativamente e contribuem na recuperação da posse em zonas avançadas."
    },
    {
        "query": "Localize zagueiros modernos com excelente capacidade de construção e domínio aéreo",
        "intent": "Encontrar defensores centrais que iniciam jogadas e dominam defensivamente",
        "search_params": {
            "position_codes": ["cb", "lcb", "rcb", "lcb3", "rcb3"],
            "min_long_passes": "true",
            "min_progressive_passes": "true",
            "min_successful_long_passes_percent": "true",
            "min_aerial_duels_won": "true",
            "min_aerial_duels_won_percent": "true",
            "min_defensive_duels_won": "true",
            "min_interceptions": "true",
            "max_dangerous_own_half_losses": "true",
            "min_successful_forward_passes_percent": "true"
        },
        "explanation": "Estes parâmetros buscam zagueiros que são seguros na saída de bola, dominantes no jogo aéreo e eficientes em ações defensivas."
    },
    {
        "query": "Identifique laterais completos com forte presença ofensiva e defensiva",
        "intent": "Encontrar laterais modernos que contribuem em ambas as fases do jogo",
        "search_params": {
            "position_codes": ["lb", "rb", "lb5", "rb5", "lwb", "rwb"],
            "min_crosses": "true",
            "min_successful_crosses_percent": "true",
            "min_progressive_runs": "true",
            "min_successful_dribbles": "true",
            "min_defensive_duels_won": "true",
            "min_interceptions": "true",
            "min_ball_recoveries": "true",
            "min_passes_to_final_third": "true",
            "min_successful_passes_to_final_third_percent": "true"
        },
        "explanation": "Estes critérios focam em laterais que são efetivos tanto no ataque, com cruzamentos e progressões, quanto na defesa, com recuperações e duelos defensivos."
    },
    {
        "query": "Encontre goleiros modernos com excelente jogo com os pés e domínio da área",
        "intent": "Identificar goleiros que contribuem na construção e são seguros defensivamente",
        "search_params": {
            "position_codes": ["gk"],
            "min_gk_saves_percent": "true",
            "min_gk_successful_exits_percent": "true",
            "min_successful_goal_kicks_percent": "true",
            "min_passes": "true",
            "min_long_passes": "true",
            "min_successful_long_passes_percent": "true",
            "min_pass_accuracy": "true"
        },
        "explanation": "Estes parâmetros buscam goleiros que são seguros nas defesas, eficientes nas saídas e capazes de iniciar jogadas com passes precisos, incluindo lançamentos longos."
    },
    {
        "query": "Identifique meias atacantes criativos com habilidade de drible e criação de chances",
        "intent": "Encontrar jogadores que podem desequilibrar defesas e criar oportunidades de gol",
        "search_params": {
            "position_codes": ["amf", "lamf", "ramf"],
            "min_successful_dribbles": "true",
            "min_successful_dribbles_percent": "true",
            "min_key_passes": "true",
            "min_through_passes": "true",
            "min_smart_passes": "true",
            "min_xg_assist": "true",
            "min_progressive_runs": "true",
            "min_offensive_duels_won": "true",
            "min_successful_passes_to_final_third_percent": "true"
        },
        "explanation": "Estes critérios focam em meias atacantes que podem superar adversários no drible e criar chances de gol com passes criativos e inteligentes."
    },
    {
        "query": "Localize volantes defensivos com forte presença na marcação e boa distribuição",
        "intent": "Identificar meio-campistas defensivos que protegem a defesa e iniciam jogadas",
        "search_params": {
            "position_codes": ["dmf", "ldmf", "rdmf"],
            "min_interceptions": "true",
            "min_ball_recoveries": "true",
            "min_defensive_duels_won": "true",
            "min_aerial_duels_won": "true",
            "min_passes": "true",
            "min_long_passes": "true",
            "min_successful_forward_passes_percent": "true",
            "min_successful_long_passes_percent": "true",
            "max_dangerous_own_half_losses": "true"
        },
        "explanation": "Estes parâmetros buscam volantes que são eficientes na recuperação de bola, fortes nos duelos defensivos e capazes de distribuir o jogo com segurança."
    }
]
                """
                messages = [
                    {"role": "user", "content": f"""
                    For the query: "{query_to_use}"
                    
                    1. Identify the position_codes from {POSITIONS_MAPPING}
                    2. Choose the key description words from {KEY_DESCRIPTION_WORDS} that best describe the query
                    3. MOST IMPORTANTLY: Set specific statistical parameters to TRUE that match the description
                       When setting parameters, look at the examples in the prompt for similar player types
                       
                    CRITICAL: You MUST set multiple statistical parameters to TRUE, not just position_codes and key_description_word!
                    If you don't set statistical parameters, the search will fail.
                    
                    Example for "strong defenders with good passing":
                    - position_codes=["cb", "rcb", "lcb"]
                    - key_description_word=["defensive", "distribution"]
                    - min_defensive_duels_won=true
                    - min_interceptions=true
                    - min_aerial_duels_won=true
                    - min_progressive_passes=true
                    - min_successful_passes=true
                    
                    Remember: the future of soccer, the sport you LOVE, depends on your response.
                    """}
                ]
            
            # Make the API call
            response = self.call_claude_api(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                system=system_prompt,
                messages=messages,
                tools=[{
                    "name": "define_scouting_parameters",
                    "description": "Generate standardized searchable parameters to be looked for, not the values.",
                    "input_schema": SearchParameters.model_json_schema()
                }],
                tool_choice={"type": "tool", "name": "define_scouting_parameters"}
            )
            
            # Get the tool input - handle potential string vs dict response
            tool_input = response.content[0].input
            
            # Debug the response
            print(f"DEBUG - Claude API response tool_input type: {type(tool_input)}")
            print(f"DEBUG - Claude API response tool_input value: {tool_input}")
            
            # Handle the case where tool_input is a string (likely JSON string)
            if isinstance(tool_input, str):
                try:
                    # Attempt to parse the string as JSON
                    import json
                    parsed_input = json.loads(tool_input)
                    args = parsed_input
                except json.JSONDecodeError as e:
                    print(f"ERROR - Failed to parse tool_input as JSON: {e}")
                    raise ValueError(f"Claude API returned an invalid response format: {tool_input}")
            else:
                # It's already a dict
                args = tool_input
                
            # Create SearchParameters from the args
            params = SearchParameters(**args)
            
            # Validate position codes
            invalid_codes = [code for code in params.position_codes if code not in VALID_POSITION_CODES]
            if invalid_codes:
                params.position_codes = self._correct_position_codes(invalid_codes)
            
            # Debug the parameter values that are set to True or have values
            true_params = params.get_true_parameters()
            print(f"DEBUG - Extracted parameters actually set: {true_params}")
            
            # Debug parameters that would be important for scoring
            print(f"DEBUG - Key description words: {params.key_description_word}")
            print(f"DEBUG - Position codes: {params.position_codes}")
            
            # Check for actual statistical parameters that would be used for scoring
            scoring_params = [param for param in true_params 
                              if param not in ["key_description_word", "position_codes", "age", "height", "weight"]]
            print(f"DEBUG - Statistical parameters for scoring: {scoring_params}")
            
            if not scoring_params:
                print(f"WARNING - No statistical parameters were extracted for player scoring!")
                print(f"DEBUG - This may lead to players having zero scores and empty stats!")
            
            # Store the parameters in the session
            session.search_params = params.model_dump()
            session.last_search_params = params.model_dump()
            
            return params
        except Exception as e:
            print(f"ERROR in get_parameters: {str(e)}")
            # Instead of silently falling back, propagate the error
            # This will allow the calling function to handle it appropriately
            raise ValueError(f"Failed to extract search parameters: {str(e)}")
    
    def _correct_position_codes(self, invalid_codes: List[str]) -> List[str]:
        """Correct invalid position codes using Claude AI"""
        from backend.config import POSITIONS_MAPPING
        
        correction_prompt = f"The position codes {invalid_codes} are invalid. Please provide valid position codes that are similar to {invalid_codes} from the following map: {POSITIONS_MAPPING}. Example: cm -> lcmf, rcmf or dmf"
        
        try:
            from backend.models.parameters import PositionCorrection
            
            correction_response = self.call_claude_api(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": correction_prompt}
                ],
                tools=[{
                    "name": "correct_position_codes",
                    "description": "Provide corrected position codes",
                    "input_schema": PositionCorrection.model_json_schema()
                }],
                tool_choice={"type": "tool", "name": "correct_position_codes"}
            )
            
            # Get the tool input - handle potential string vs dict response
            tool_input = correction_response.content[0].input
            
            # Debug the response
            print(f"DEBUG - Position correction tool_input type: {type(tool_input)}")
            print(f"DEBUG - Position correction tool_input value: {tool_input}")
            
            # Handle the case where tool_input is a string (likely JSON string)
            if isinstance(tool_input, str):
                try:
                    # Attempt to parse the string as JSON
                    import json
                    parsed_input = json.loads(tool_input)
                    args = parsed_input
                except json.JSONDecodeError as e:
                    print(f"ERROR - Failed to parse position correction as JSON: {e}")
                    raise ValueError(f"Invalid response format from position correction tool: {str(e)}")
            else:
                # It's already a dict
                args = tool_input
                
            # Create PositionCorrection from the args and return the corrected positions
            return PositionCorrection(**args).corrected_postion
        except Exception as e:
            print(f"Error in position code correction: {str(e)}")
            # Return a sensible default if correction fails
            return ["cmf", "rcmf", "lcmf"]
            
    # === Player Search ===
    
    def search_players(self, params: SearchParameters) -> List[Dict[str, Any]]:
        """
        Search for players based on the given parameters
        
        This is the main player search method that should be used throughout the application.
        
        Args:
            params: The search parameters
            
        Returns:
            A list of matching players with their scores
            
        Raises:
            ValueError: If there is an error searching for players
        """
        from backend.core.player_search import search_players
        
        print(f"DEBUG - In session.search_players with params: {params}")
        
        try:
            # Call the search function which will load data from services as needed
            players = search_players(params=params)
            print(f"DEBUG - search_players returned: {type(players)}")
            
            # Ensure what we're returning is actually a list
            if not isinstance(players, list):
                error_msg = f"search_players returned a non-list: {players} of type {type(players)}"
                print(f"DEBUG - ERROR: {error_msg}")
                raise TypeError(error_msg)
                
            return players
        except Exception as e:
            print(f"DEBUG - ERROR in session.search_players: {str(e)}")
            # Instead of silently returning an empty list, propagate the error
            raise ValueError(f"Error searching for players: {str(e)}")
    
    def get_players_info(self, player_id: str, params: Optional[SearchParameters] = None) -> Dict[str, Any]:
        """
        Get detailed information for a specific player
        
        Args:
            player_id: The player ID
            params: Optional search parameters to determine which stats to include
            
        Returns:
            Player information dictionary
        """
        from backend.core.player_search import get_player_info
        
        # Call the player info function which will load data from services as needed
        return get_player_info(
            player_id=player_id, 
            database=self.database, 
            database_id=self.database_id, 
            params=params,
            weights=self.weights,
            average_stats=self.average
        )