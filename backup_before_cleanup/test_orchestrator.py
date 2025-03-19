#!/usr/bin/env python3
"""
Test script for the KatenaScout orchestrator implementation.
Run this after implementing the orchestrator to verify functionality.
"""

import json
import os
import sys
import requests
from typing import Dict, Any, List

# Configuration
BASE_URL = "http://localhost:5001"
TEST_SESSION_ID = "test-orchestrator-session"


def test_enhanced_search():
    """Test the enhanced search endpoint with orchestrator."""
    print("Testing enhanced search with orchestrator...")
    
    url = f"{BASE_URL}/enhanced_search"
    payload = {
        "session_id": TEST_SESSION_ID,
        "query": "Find me attacking midfielders who are good at scoring goals",
        "is_follow_up": False,
        "language": "english"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("  ✓ Search endpoint returned success")
        
        if data.get("players"):
            print(f"  ✓ Found {len(data['players'])} players")
        else:
            print("  ✗ No players found")
        
        if data.get("follow_up_suggestions"):
            print(f"  ✓ Generated {len(data['follow_up_suggestions'])} follow-up suggestions")
        else:
            print("  ✗ No follow-up suggestions generated")
            
        return data.get("players", [])
    else:
        print(f"  ✗ Search request failed: {response.status_code}")
        print(f"  Error: {response.text}")
        return []


def test_follow_up_suggestions():
    """Test the follow-up suggestions endpoint."""
    print("\nTesting follow-up suggestions...")
    
    url = f"{BASE_URL}/follow_up_suggestions/{TEST_SESSION_ID}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("  ✓ Follow-up suggestions endpoint returned success")
        
        if data.get("suggestions"):
            print(f"  ✓ Generated {len(data['suggestions'])} suggestions:")
            for suggestion in data.get("suggestions", []):
                print(f"    - {suggestion}")
        else:
            print("  ✗ No suggestions generated")
    else:
        print(f"  ✗ Follow-up suggestions request failed: {response.status_code}")
        print(f"  Error: {response.text}")


def test_player_comparison(players: List[Dict[str, Any]]):
    """Test the player comparison endpoint."""
    print("\nTesting player comparison...")
    
    if len(players) < 2:
        print("  ✗ Not enough players to compare. Using hardcoded player IDs.")
        # Use hardcoded player IDs for testing
        url = f"{BASE_URL}/player_comparison"
        payload = {
            "session_id": TEST_SESSION_ID,
            "player_ids": ["4913", "65325"],  # Use actual player IDs from database
            "language": "english"
        }
        print("  Using hardcoded player IDs for testing")
    else:
        url = f"{BASE_URL}/player_comparison"
        payload = {
            "session_id": TEST_SESSION_ID,
            "player_ids": [players[0].get("wyId", players[0].get("name")), 
                          players[1].get("wyId", players[1].get("name"))],
            "language": "english"
        }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("  ✓ Player comparison endpoint returned success")
        
        if data.get("comparison"):
            print("  ✓ Generated comparison text")
            print("  ✓ Comparison aspects: " + ", ".join(data.get("comparison_aspects", [])))
        else:
            print("  ✗ No comparison generated")
    else:
        print(f"  ✗ Player comparison request failed: {response.status_code}")
        print(f"  Error: {response.text}")


def test_explain_stats():
    """Test the explain stats endpoint."""
    print("\nTesting stats explanation...")
    
    url = f"{BASE_URL}/explain_stats"
    payload = {
        "session_id": TEST_SESSION_ID,
        "stats": ["xG", "progressive passes", "ball recoveries"],
        "language": "english"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("  ✓ Explain stats endpoint returned success")
        
        if data.get("explanations"):
            print(f"  ✓ Generated {len(data['explanations'])} explanations:")
            for stat, explanation in data.get("explanations", {}).items():
                print(f"    - {stat}: {explanation[:50]}...")
        else:
            print("  ✗ No explanations generated")
    else:
        print(f"  ✗ Explain stats request failed: {response.status_code}")
        print(f"  Error: {response.text}")


def test_follow_up_query():
    """Test a follow-up query to check context preservation."""
    print("\nTesting follow-up query with context...")
    
    url = f"{BASE_URL}/enhanced_search"
    payload = {
        "session_id": TEST_SESSION_ID,
        "query": "What about ones with better defensive skills?",
        "is_follow_up": True,
        "language": "english"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("  ✓ Follow-up query endpoint returned success")
        
        if data.get("players"):
            print(f"  ✓ Found {len(data['players'])} players in follow-up")
        else:
            print("  ✗ No players found in follow-up")
    else:
        print(f"  ✗ Follow-up query request failed: {response.status_code}")
        print(f"  Error: {response.text}")


def main():
    """Run all tests."""
    print("=== KatenaScout Orchestrator Tests ===\n")
    
    # Test the health endpoint to make sure the server is running
    health_response = requests.get(f"{BASE_URL}/health")
    if health_response.status_code != 200:
        print("Error: Backend server not running. Please start the server first.")
        sys.exit(1)
    
    # Run the tests
    players = test_enhanced_search()
    test_follow_up_suggestions()
    test_player_comparison(players)
    test_explain_stats()
    test_follow_up_query()
    
    print("\n=== All tests completed ===")


if __name__ == "__main__":
    main()