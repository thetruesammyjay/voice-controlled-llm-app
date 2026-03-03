#!/bin/bash
# scripts/deploy.sh
#
# This script facilitates the deployment of the Voice-Controlled LLM App
# to various environments (local, Docker, or cloud platforms).
#
# Usage: ./scripts/deploy.sh [local|docker|cloud-platform|--help]

echo "--- Starting deployment of Voice-Controlled LLM App ---"

# Ensure we are not in an activated virtual environment for deployment scripts
if command -v deactivate &> /dev/null; then
    deactivate 2>/dev/null
fi

# Function to display help message
show_help() {
    echo "Usage: ./scripts/deploy.sh [local|docker|cloud-platform|--help]"
    echo ""
    echo "Deployment targets:"
    echo "  local          : Runs the Streamlit app directly in the local environment."
    echo "                   (Requires 'venv' activated and dependencies installed manually or via setup.sh)."
    echo "  docker         : Builds and runs the application using Docker."
    echo "                   (Requires Docker installed and a Dockerfile/docker-compose.yml in the root)."
    echo "  cloud-platform : Provides general guidance for cloud VM deployment."
    echo "  --help         : Show this help message."
    exit 0
}

# Check for help flag
if [ "$1" == "--help" ]; then
    show_help
fi

# Check for a deployment argument
if [ -z "$1" ]; then
    echo "Error: No deployment target specified."
    show_help
fi

DEPLOY_TARGET=$1

case "$DEPLOY_TARGET" in
    local)
        echo "Deploying to local environment (simple run)..."
        echo "Please ensure you have activated the virtual environment (source venv/bin/activate) "
        echo "and installed dependencies (pip install -r requirements.txt)."
        echo ""
        echo "Attempting to run Streamlit app for demonstration..."
        # Check if Streamlit is available in the current PATH (assumes venv activated externally)
        if ! command -v streamlit &> /dev/null; then
            echo "Error: 'streamlit' command not found. Please activate your virtual environment."
            echo "Example: source venv/bin/activate"
            exit 1
        fi
        streamlit run src/app.py
        ;;
    docker)
        echo "Deploying using Docker..."
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            echo "Error: Docker is not installed or not in your PATH."
            echo "Please install Docker Desktop (Windows/macOS) or Docker Engine (Linux)."
            exit 1
        fi

        DOCKER_COMPOSE_FILE="docker-compose.yml"
        DOCKERFILE="Dockerfile"

        if [ -f "$DOCKER_COMPOSE_FILE" ]; then
            echo "Found '$DOCKER_COMPOSE_FILE'. Using Docker Compose."
            echo "Building Docker images with Compose..."
            docker compose build
            if [ $? -ne 0 ]; then
                echo "Error: Docker Compose build failed."
                exit 1
            fi
            echo "Starting Docker containers with Compose (in detached mode)..."
            docker compose up -d
            if [ $? -ne 0 ]; then
                echo "Error: Docker Compose up failed."
                exit 1
            fi
            echo "Docker containers started. Application should be accessible (e.g., http://localhost:8501)."
            echo "To stop: 'docker compose down'"
            echo "To view logs: 'docker compose logs -f'"
        elif [ -f "$DOCKERFILE" ]; then
            echo "Found '$DOCKERFILE'. Using direct Docker commands."
            echo "Building Docker image..."
            docker build -t voice-llm-app .
            if [ $? -ne 0 ]; then
                echo "Error: Docker image build failed."
                exit 1
            fi
            echo "Running Docker container on port 8501..."
            echo "Note: You must set your OPENAI_API_KEY as an environment variable."
            echo "Example: docker run -p 8501:8501 -e OPENAI_API_KEY='your_openai_key' voice-llm-app"
            echo "This command will run in the foreground. For detached mode, add '-d'."
        else
            echo "Error: Neither '$DOCKER_COMPOSE_FILE' nor '$DOCKERFILE' found in the root directory."
            echo "Please create one for Docker deployment."
            exit 1
        fi
        ;;
    cloud-platform)
        echo "Deploying to a generic cloud platform (e.g., AWS EC2, GCP Compute Engine, Azure VM)..."
        echo "This typically involves the following manual or automated steps:"
        echo "1.  **Provision a Virtual Machine (VM):** Choose an appropriate instance type and operating system (e.g., Ubuntu, Debian)."
        echo "2.  **Install Prerequisites:** Install Python (3.8+), pip, and essential system-level audio libraries (e.g., PortAudio for sounddevice, FFmpeg for pydub)."
        echo "    For example: sudo apt-get update && sudo apt-get install -y python3 python3-pip portaudio19-dev ffmpeg libsndfile1-dev"
        echo "3.  **Copy Application Code:** Transfer your entire 'voice-controlled-llm-app' project folder to the VM."
        echo "    e.g., using scp or rsync: scp -r ./voice-controlled-llm-app user@your_vm_ip:~/app/"
        echo "4.  **Install Python Dependencies:** Navigate to your application's root directory on the VM and install dependencies within a virtual environment:"
        echo "    cd ~/app/voice-controlled-llm-app"
        echo "    python3 -m venv venv && source venv/bin/activate"
        echo "    pip install -r requirements.txt"
        echo "5.  **Configure Environment Variables:** Set your `OPENAI_API_KEY` and other necessary variables on the VM."
        echo "    Consider using a `.env` file or directly setting them as environment variables in your startup script."
        echo "6.  **Set up a Process Manager (for persistence):** Use a tool like `systemd`, `Supervisor`, or `Gunicorn` with `Nginx`/`Caddy` to run `src/app.py` continuously in the background."
        echo "    Example (basic `nohup` for quick test, not production):"
        echo "    nohup streamlit run src/app.py --server.port 80 --server.address 0.0.0.0 > streamlit.log 2>&1 &"
        echo "7.  **Configure Network Access (Firewall):** Open the necessary port (e.g., 80 or 8501 for Streamlit) in your cloud provider's firewall settings to allow public access to your application."
        echo "This process is highly dependent on your chosen cloud provider and specific setup."
        ;;
    *)
        echo "Error: Unknown deployment target '$DEPLOY_TARGET'."
        show_help
        ;;
esac

echo "--- Deployment script finished ---"
