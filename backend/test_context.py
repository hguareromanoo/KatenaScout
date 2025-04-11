import asyncio
from core.session import UnifiedSession
from models.parameters import SearchParameters

async def run_test():
    print("Initializing session manager...")
    # Need to ensure all necessary files are loaded relative to backend dir
    session_manager = UnifiedSession()
    print("Session manager initialized.")

    session_id = "test-context-session-123"
    language = "english"

    # --- Turn 1: Initial Search ---
    print("\n--- Turn 1: Initial Search ---")
    query1 = "Find me fast wingers"
    print(f"User Query: {query1}")

    # Simulate adding user message to session (app.py does this)
    session = session_manager.get_session(session_id, language)
    session.messages.append({"role": "user", "content": query1})
    session.is_follow_up = False # Mark as new search

    print("Calling get_parameters for initial query...")
    try:
        params1 = session_manager.get_parameters(session_id, query1)
        print("\nExtracted Parameters (Turn 1):")
        print(params1.model_dump_json(indent=2))
        # Simulate adding assistant response (not strictly needed for test)
        session.messages.append({"role": "assistant", "content": "Okay, I found some fast wingers."})
    except Exception as e:
        print(f"Error during Turn 1 get_parameters: {e}")
        return # Stop test if initial extraction fails

    # --- Turn 2: Follow-up Search ---
    print("\n--- Turn 2: Follow-up Search ---")
    query2 = "show me ones under 20"
    print(f"User Query: {query2}")

    # Simulate adding user message and setting follow-up flag (app.py does this)
    session = session_manager.get_session(session_id, language) # Get session again
    session.messages.append({"role": "user", "content": query2})
    session.is_follow_up = True # Mark as follow-up

    print("Calling get_parameters for follow-up query...")
    try:
        params2 = session_manager.get_parameters(session_id, query2)
        print("\nExtracted Parameters (Turn 2 - Follow-up):")
        print(params2.model_dump_json(indent=2))

        # Check if context was maintained (e.g., position codes and age)
        # Adjust the age check since params2.age is likely an integer (max age)
        if params2.position_codes and ("lw" in params2.position_codes or "lwf" in params2.position_codes) and params2.age == 20:
             print("\nSUCCESS: Context (wingers) and new criteria (age < 20) seem to be combined correctly.")
        else:
             print("\nWARNING: Parameters might not reflect combined context. Check manually.")
             print(f"  Expected positions like 'lw', 'rw', got: {params2.position_codes}")
             print(f"  Expected age max 20, got: {params2.age}")

    except Exception as e:
        print(f"Error during Turn 2 get_parameters: {e}")

if __name__ == "__main__":
    # Use asyncio.run() if your environment supports it directly
    # For broader compatibility, especially in scripts, manage the loop explicitly
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_test())
    except RuntimeError as e:
        if "Cannot run the event loop while another loop is running" in str(e):
            # If running in an environment like Jupyter that already has a loop
            asyncio.run(run_test())
        else:
            raise
