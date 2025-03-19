"""
Claude API Integration for KatenaScout

This module provides a standardized interface for interacting with the Claude API.
"""

import os
import time
import requests
from typing import List, Dict, Any, Optional
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout

def get_anthropic_api_key() -> str:
    """Get the Anthropic API key from environment variables or keys file"""
    try:
        # Try to import from env_keys
        from env_keys import get_anthropic_api_key as get_key
        key = get_key()
        if key:
            return key
    except (ImportError, AttributeError):
        pass
    
    # Fallback to environment variable
    return os.environ.get("ANTHROPIC_API_KEY", "")


class ClaudeAPIResponse:
    """Response object that mimics the structure of the Anthropic client library response"""
    class Content:
        def __init__(self, content_data: Dict[str, Any]):
            self.type = content_data.get("type")
            self.text = content_data.get("text", "")
            self.input = content_data.get("input", {})
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.model = data.get("model")
        self.content = [self.Content(item) for item in data.get("content", [])]


def call_claude_api_with_retry(
    api_key: str, 
    model: str = "claude-3-5-sonnet-20240624",  # Updated to use sonnet
    max_tokens: int = 1000, 
    system: Optional[str] = None, 
    messages: Optional[List[Dict[str, Any]]] = None, 
    tools: Optional[List[Dict[str, Any]]] = None, 
    tool_choice: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    initial_backoff: float = 1.0,
    backoff_factor: float = 2.0
) -> ClaudeAPIResponse:
    """
    Make a direct HTTP request to the Claude API with retry logic
    
    Args:
        api_key: Anthropic API key
        model: The Claude model to use (e.g. "claude-3-5-sonnet-20241022")
        max_tokens: Maximum number of tokens to generate
        system: Optional system prompt
        messages: List of message objects with role and content
        tools: Optional list of tool objects
        tool_choice: Optional tool choice object
        max_retries: Maximum number of retry attempts
        initial_backoff: Initial backoff time in seconds
        backoff_factor: Multiplier for subsequent backoff times
        
    Returns:
        ClaudeAPIResponse object mimicking the structure of the Anthropic client library response
    """
    # API URL
    url = "https://api.anthropic.com/v1/messages"
    
    # Set headers
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "anthropic-beta": "messages-2023-12-15"  # Add beta header for newer API features
    }
    
    # Build request body
    request_body = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages or []
    }
    
    # Add system prompt if provided
    if system:
        request_body["system"] = system
    
    # Add tools if provided
    if tools:
        request_body["tools"] = tools
    
    # Add tool_choice if provided
    if tool_choice:
        request_body["tool_choice"] = tool_choice
    
    # Get friendly debug name for the API call
    tool_name = tool_choice.get("name") if isinstance(tool_choice, dict) else "None"
    
    # Initialize retry variables
    current_retry = 0
    current_backoff = initial_backoff
    last_exception = None
    
    # Retry loop
    while current_retry <= max_retries:
        try:
            # Log the request attempt
            log_prefix = f"[Attempt {current_retry + 1}/{max_retries + 1}]"
            print(f"{log_prefix} Calling Claude API with model {model}, tool: {tool_name}")
            print(f"{log_prefix} Request body: {request_body}")
            
            # Make the request
            response = requests.post(url, headers=headers, json=request_body, timeout=30)
            
            # Log response for debugging
            if response.status_code != 200:
                print(f"{log_prefix} Error response: {response.text}")
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            print(f"{log_prefix} Claude API response status: {response.status_code}")
            
            # Return response in the expected format
            return ClaudeAPIResponse(data)
        
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            last_exception = e
            current_retry += 1
            
            if current_retry <= max_retries:
                # Log the error and retry info
                print(f"{log_prefix} Error calling Claude API: {str(e)}")
                print(f"{log_prefix} Retrying in {current_backoff} seconds...")
                
                # Wait before retrying
                time.sleep(current_backoff)
                
                # Increase backoff for next retry
                current_backoff *= backoff_factor
            else:
                # We've exhausted all retries
                print(f"Error calling Claude API after {max_retries} retries: {str(e)}")
                break
        
        except Exception as e:
            # For non-connection related exceptions, don't retry
            last_exception = e
            print(f"Unexpected error calling Claude API: {str(e)}")
            break
    
    # All retries failed or unexpected error occurred, return fallback response
    fallback_data = {
        "id": "error",
        "model": model,
        "content": []
    }
    
    # Include error info in the fallback
    error_message = f"Error after {current_retry} attempts: {str(last_exception)}"
    
    # For intent classification fallback
    if tools and tool_choice and tool_choice.get("name") == "classify_intent":
        fallback_data["content"].append({
            "type": "tool_use",
            "text": "Fallback intent classification",
            "input": {
                "intent": "casual_conversation",
                "confidence": 0.9
            }
        })
    elif tools and tool_choice and tool_choice.get("name") == "define_scouting_parameters":
        fallback_data["content"].append({
            "type": "tool_use",
            "text": "Fallback search parameters",
            "input": {
                "key_description_word": ["passing"],
                "position_codes": ["cmf"],
                "age": 25,
                "height": 180,
                "weight": 75
            }
        })
    else:
        # Generic text response fallback
        fallback_data["content"].append({
            "type": "text",
            "text": f"I apologize, but I'm having trouble processing your request right now. {error_message}. Please try again later."
        })
    
    return ClaudeAPIResponse(fallback_data)


# Keep the original function as a simple wrapper for backward compatibility
def call_claude_api(
    api_key: str, 
    model: str, 
    max_tokens: int, 
    system: Optional[str] = None, 
    messages: Optional[List[Dict[str, Any]]] = None, 
    tools: Optional[List[Dict[str, Any]]] = None, 
    tool_choice: Optional[Dict[str, Any]] = None
) -> ClaudeAPIResponse:
    """
    Make a direct HTTP request to the Claude API (with retry logic)
    
    This function is a wrapper around call_claude_api_with_retry for backward compatibility.
    
    Args:
        api_key: Anthropic API key
        model: The Claude model to use (e.g. "claude-3-5-sonnet-20241022")
        max_tokens: Maximum number of tokens to generate
        system: Optional system prompt
        messages: List of message objects with role and content
        tools: Optional list of tool objects
        tool_choice: Optional tool choice object
        
    Returns:
        ClaudeAPIResponse object mimicking the structure of the Anthropic client library response
    """
    return call_claude_api_with_retry(
        api_key=api_key,
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice
    )