#!/bin/bash
# scripts/test.sh
#
# This script runs all tests for the Voice-Controlled LLM App using pytest.
#
# Usage: ./scripts/test.sh

echo "--- Running tests for Voice-Controlled LLM App ---"

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment. Make sure 'venv' exists."
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Please install development dependencies: pip install -r requirements-dev.txt"
    exit 1
fi

# Run pytest on the tests directory
echo "Executing pytest..."
pytest tests/
# You can add more pytest arguments here, e.g., for verbosity or coverage:
# pytest tests/ -v --cov=src

# Check the exit status of pytest
if [ $? -eq 0 ]; then
    echo "--- All tests passed successfully! ---"
else
    echo "--- Tests failed. See output above for details. ---"
fi

# Deactivate the virtual environment
deactivate

