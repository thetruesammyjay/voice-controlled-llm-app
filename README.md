# Voice-Controlled LLM App

A multimodal AI application that enables voice-to-voice conversations with large language models using speech-to-text input, intelligent text generation, and audio response capabilities.

## Features

- **Speech-to-Text**: Convert voice input to text using OpenAI Whisper API
- **Intelligent Response**: Generate contextual responses using LangChain and OpenAI GPT models
- **Text-to-Speech**: Convert AI responses back to natural-sounding audio
- **Conversation Memory**: Maintain context across multiple exchanges
- **Real-time Processing**: Seamless voice interaction with minimal latency
- **Configurable Models**: Easy switching between different OpenAI models

## Tech Stack

- **LangChain**: LLM orchestration and chaining
- **OpenAI API**: GPT models for text generation
- **Whisper API**: Speech-to-text conversion
- **Python**: Core application logic
- **Streamlit**: Web interface (optional)
- **PyAudio**: Audio recording and playback
- **dotenv**: Environment variable management

## Prerequisites

- Python 3.8+
- OpenAI API key
- Microphone access
- Audio output capability

## Installation

1. **Clone the repository**
   ```bash
   git clone voice-controlled-llm-app
   cd voice-controlled-llm-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

## Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-3.5-turbo
WHISPER_MODEL=whisper-1
TTS_MODEL=tts-1
TTS_VOICE=alloy
MAX_TOKENS=150
TEMPERATURE=0.7
```

## Usage

### Command Line Interface
```bash
python src/main.py
```

### Web Interface (Streamlit)
```bash
streamlit run src/app.py
```

### Basic Usage Example
```python
from src.voice_llm import VoiceLLM

# Initialize the voice LLM
voice_llm = VoiceLLM()

# Start voice conversation
voice_llm.start_conversation()
```

## Project Structure

```
voice-controlled-llm-app/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── app.py               # Streamlit web interface
│   ├── voice_llm.py         # Core VoiceLLM class
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── recorder.py      # Audio recording functionality
│   │   ├── player.py        # Audio playback functionality
│   │   └── processor.py     # Audio processing utilities
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── chains.py        # LangChain configurations
│   │   ├── prompts.py       # Prompt templates
│   │   └── memory.py        # Conversation memory management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── openai_client.py # OpenAI API client
│   │   ├── whisper.py       # Whisper API integration
│   │   └── tts.py           # Text-to-speech integration
│   └── utils/
│       ├── __init__.py
│       ├── config.py        # Configuration management
│       ├── logger.py        # Logging setup
│       └── helpers.py       # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_voice_llm.py
│   ├── test_audio.py
│   └── test_api.py
├── data/
│   ├── audio/               # Temporary audio files
│   └── logs/                # Application logs
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── setup.py
```

## API Integration

### OpenAI Whisper (Speech-to-Text)
```python
# Convert audio to text
transcript = whisper_client.transcribe(audio_file)
```

### LangChain + OpenAI (Text Generation)
```python
# Generate response using LangChain
response = llm_chain.run(user_input)
```

### OpenAI TTS (Text-to-Speech)
```python
# Convert text to speech
audio = tts_client.synthesize(response_text)
```

## Key Components

### VoiceLLM Class
The main orchestrator that handles the complete voice-to-voice pipeline:
- Audio recording and preprocessing
- Speech-to-text conversion
- LLM response generation
- Text-to-speech synthesis
- Audio playback

### Audio Module
- **Recorder**: Captures audio from microphone
- **Player**: Plays generated audio responses
- **Processor**: Handles audio format conversion and noise reduction

### LLM Module
- **Chains**: LangChain configurations for different conversation types
- **Prompts**: Template management for various interaction patterns
- **Memory**: Conversation context and history management

### API Module
- **OpenAI Client**: Unified interface for all OpenAI services
- **Whisper**: Speech-to-text processing
- **TTS**: Text-to-speech generation

## Configuration Options

### Model Settings
- `MODEL_NAME`: GPT model to use (gpt-3.5-turbo, gpt-4, etc.)
- `MAX_TOKENS`: Maximum response length
- `TEMPERATURE`: Response creativity (0.0-1.0)

### Audio Settings
- `SAMPLE_RATE`: Audio recording sample rate
- `CHUNK_SIZE`: Audio processing chunk size
- `RECORDING_TIMEOUT`: Maximum recording duration

### Voice Settings
- `TTS_VOICE`: Voice for text-to-speech (alloy, echo, fable, etc.)
- `TTS_SPEED`: Speech rate (0.25-4.0)

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
flake8 src/
```

### Adding New Features
1. Create feature branch
2. Implement functionality
3. Add tests
4. Update documentation
5. Submit pull request

## Troubleshooting

### Common Issues

**Audio Not Recording**
- Check microphone permissions
- Verify PyAudio installation
- Test audio device availability

**API Errors**
- Verify OpenAI API key
- Check API rate limits
- Ensure sufficient credits

**Performance Issues**
- Adjust chunk sizes
- Optimize model parameters
- Consider local audio processing

### Debugging
Enable debug mode by setting `DEBUG=True` in `.env` file.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for Whisper and GPT models
- LangChain for LLM orchestration
- Contributors and community feedback

## Support

For support, please open an issue in the GitHub repository or contact the development team.
