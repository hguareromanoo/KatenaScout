#!/bin/bash

# This is a wrapper script that delegates to run.sh
# It exists for backward compatibility

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Add a log message for clarity
echo "Starting KatenaScout with enhanced conversational abilities..."

# Call the actual run script
exec "$DIR/run.sh"