1. User Message → Conversation Manager → Function Dispatcher → Response Generator

  # Core models
  class ConversationMemory(BaseModel):
      session_id: str
      messages: List[Dict] = Field(default_factory=list)
      entities: Dict[str, Any] = Field(default_factory=dict)  # Players, teams mentioned
      current_intent: Optional[str] = None
      recent_function_calls: List[str] = Field(default_factory=list)

  class Intent(BaseModel):
      name: str = Field(..., description="Intent name")
      confidence: float = (ge=0,fe=1)

  # 1. First, handle incoming messages
  def process_user_message(session_id: str, message: str, language: str = "english"):
      # Get or create session
      memory = get_conversation_memory(session_id, language)

      # Add user message to memory
      memory.messages.append({"role": "user", "content": message})

      # Process with orchestrator
      return conversation_orchestrator(memory, message)

  # 2. Conversation orchestrator decides what to do next
  def conversation_orchestrator(memory: ConversationMemory, message: str):
      # Identify user intent with LLM
      intent = identify_intent(memory, message)
      memory.current_intent = intent.name

      # Extract relevant entities based on intent
      entities = extract_entities(memory, message, intent)
      memory.entities.update(entities)

      # Dispatch to appropriate function
      if intent.name == "player_search":
          response = handle_player_search(memory, message)
      elif intent.name == "player_comparison":
          response = handle_player_comparison(memory, message)
      elif intent.name == "explain_stats":
          response = handle_stats_explanation(memory, message)
      elif intent.name == "casual_conversation":
          response = handle_casual_chat(memory, message)
      else:
          response = handle_fallback(memory, message)

      # Generate appropriate response
      return format_response(memory, response)

  # 3. Intent recognition with Claude
  def identify_intent(memory: ConversationMemory, message: str) -> Intent:
      messages = create_context_from_memory(memory)
      messages.append({"role": "user", "content": message})

      response = call_claude_api(
          model="claude-3-5-sonnet-20241022",
          max_tokens=1024,
          system="Identify the user's intent from these options: player_search, player_comparison, explain_stats, casual_conversation, or other.",
          messages=messages,
          tools=[{
              "name": "classify_intent",
              "description": "Classify the user's intent",
              "input_schema": Intent.model_json_schema()
          }],
          tool_choice={"type": "tool", "name": "classify_intent"}
      )

      return Intent(**response.content[0].input)

  # 4. Handle player search (your current core functionality, enhanced)
  def handle_player_search(memory: ConversationMemory, message: str):
      # Extract search parameters using your existing function
      params = get_parameters(memory.session_id, message)

      # Search for players with your existing function
      players = search_players(params)

      # Update memory with players found
      memory.entities["recent_players"] = [p["name"] for p in players]

      return {
          "type": "search_results",
          "players": players,
          "params": params.model_dump(),
          "follow_up_suggestions": generate_follow_up_suggestions(memory, players)
      }

  # 5. Generate personalized response with Claude
  def format_response(memory: ConversationMemory, response_data):
      # Format response based on type
      response_type = response_data.get("type", "text")

      if response_type == "search_results":
          # Use Claude to generate natural language response
          system_prompt = get_language_specific_prompt(memory)

          # Create conversational response
          response = call_claude_api(
              model="claude-3-5-sonnet-20241022",
              max_tokens=2048,
              system=system_prompt,
              messages=[
                  {"role": "user", "content": f"User's intent: {memory.current_intent}"},
                  {"role": "user", "content": f"Recent conversation: {memory.messages[-5:]}"},
                  {"role": "user", "content": f"Data to respond with: {json.dumps(response_data)}"}
              ]
          )

          # Add response to memory
          memory.messages.append({"role": "assistant", "content": response.content[0].text})

          return response.content[0].text

  This structure preserves your existing search capability while adding:
  1. Intent classification to handle more types of interactions
  2. Entity tracking to maintain conversation context
  3. Tailored response generation based on interaction type
  4. Follow-up suggestions to guide the conversation