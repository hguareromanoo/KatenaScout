#!/bin/bash

# Activate virtual environment if it exists
if [ -d "../venv" ]; then
    source ../venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the Flask application
export FLASK_APP=enhanced_chat.py
export FLASK_ENV=development 
python -m flask run --host=0.0.0.0 --port=5001
