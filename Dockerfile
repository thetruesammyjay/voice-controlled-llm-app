# Dockerfile
#
# This Dockerfile builds an image for your Voice-Controlled LLM App,
# specifically designed to run the Streamlit web interface.

# Use an official Python runtime as a parent image
# python:3.12-slim-buster is a good choice for smaller image size
FROM python:3.12-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install system-level dependencies required for sounddevice and pydub (ffmpeg)
# libsndfile1-dev is for soundfile (which sounddevice uses)
# ffmpeg is for pydub
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    portaudio19-dev \
    libsndfile1-dev \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install any specified Python packages listed in requirements.txt
# --no-cache-dir avoids caching wheels, making the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
# The 'src', 'config', 'data', 'docs', 'scripts' folders etc.
COPY . .

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Set environment variables for Streamlit (optional, but good practice)
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Command to run the Streamlit application
# This assumes src/app.py is your main Streamlit entry point
CMD ["streamlit", "run", "src/app.py"]

# Note: You will need to pass your OPENAI_API_KEY as an environment variable
# when running the container, e.g.:
# docker run -p 8501:8501 -e OPENAI_API_KEY="your_key" my-voice-llm-app-image
