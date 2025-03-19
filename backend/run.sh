#!/bin/bash

# KatenaScout Unified Backend Start Script

# Make sure we're in the backend directory
cd "$(dirname "$0")"

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Set Python path to include the parent directory for consistent imports
PROJECT_ROOT=$(dirname "$(pwd)")
export PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH

echo "Starting KatenaScout Backend..."
echo "PYTHONPATH: $PYTHONPATH"

# Start the Flask app - use the same file as FLASK_APP
python3 app.py