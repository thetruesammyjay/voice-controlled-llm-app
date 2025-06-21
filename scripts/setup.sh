#!/bin/bash
# scripts/setup.sh
#
# This script automates the setup of the Python virtual environment
# and installs all necessary dependencies for the Voice-Controlled LLM App.
#
# Usage: ./scripts/setup.sh

echo "--- Setting up Voice-Controlled LLM App environment ---"

# 1. Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment 'venv'..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment. Ensure Python 3.8+ is installed."
        exit 1
    fi
else
    echo "Virtual environment 'venv' already exists."
fi

# 2. Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi
echo "Virtual environment activated."

# 3. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Warning: Failed to upgrade pip. Continuing with installation."
fi

# 4. Install core dependencies from requirements.txt
echo "Installing core dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install core dependencies. Check requirements.txt and network connection."
    echo "Remember to install system-level dependencies for audio (e.g., PortAudio for sounddevice)."
    exit 1
fi
echo "Core dependencies installed."

# 5. Install development dependencies from requirements-dev.txt (if it exists)
if [ -f "requirements-dev.txt" ]; then
    echo "Installing development dependencies from requirements-dev.txt..."
    pip install -r requirements-dev.txt
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to install development dependencies. Continuing."
    fi
else
    echo "requirements-dev.txt not found. Skipping development dependency installation."
fi
echo "Development setup complete."

echo "--- Environment setup finished successfully! ---"
echo "To run the CLI app: python src/main.py --mode cli"
echo "To run the Streamlit app: streamlit run src/app.py"
echo "To deactivate the virtual environment, simply type 'deactivate'."

