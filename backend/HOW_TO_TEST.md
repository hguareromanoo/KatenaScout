# Testing the KatenaScout Orchestrator Implementation

Follow these steps to test the new conversation orchestration implementation:

## 1. Start the Backend Server

```bash
cd /Users/henriqueromano/KatenaScout-1/backend
chmod +x run_enhanced.sh
./run_enhanced.sh
```

This will start the Flask server on port 5001.

## 2. Run the Test Script

In a separate terminal, run:

```bash
cd /Users/henriqueromano/KatenaScout-1/backend
python3 test_orchestrator.py
```

This will test all the new orchestrator features:
- Enhanced search with intent recognition
- Follow-up suggestions
- Player comparison
- Stats explanation
- Context-aware follow-up queries

## 3. Advanced Testing with curl

You can also test individual endpoints with curl:

**Enhanced Search:**
```bash
curl -X POST http://localhost:5001/enhanced_search \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-session", "query":"Find me technical midfielders with good passing", "language":"english"}'
```

**Player Comparison:**
```bash
curl -X POST http://localhost:5001/player_comparison \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-session", "player_ids":["Player1", "Player2"], "language":"english"}'
```

**Stats Explanation:**
```bash
curl -X POST http://localhost:5001/explain_stats \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-session", "stats":["xG", "progressive passes"], "language":"english"}'
```

**Follow-up Suggestions:**
```bash
curl -X GET http://localhost:5001/follow_up_suggestions/test-session
```

## 4. Front-end Testing

To fully test the implementation with the front-end, you'll need to update the React components to use the new endpoints. For now, focus on testing the backend functionality to ensure the orchestrator is working correctly.

## Next Steps

After testing, consider these next steps:

1. Update the frontend to use the new endpoints for richer functionality
2. Add visualizations for player comparisons
3. Expand the intent recognition to cover more use cases
4. Enhance the entity extraction for more complex queries