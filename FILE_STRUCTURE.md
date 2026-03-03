voice-controlled-llm-app/
├── src/
│   ├── __init__.py
│   ├── main.py                      # Main CLI application entry point
│   ├── app.py                       # Streamlit web interface
│   ├── voice_llm.py                 # Core VoiceLLM orchestrator class
│   │
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── recorder.py              # Audio recording from microphone
│   │   ├── player.py                # Audio playback functionality
│   │   └── processor.py             # Audio format conversion & processing
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── chains.py                # LangChain conversation chains
│   │   ├── prompts.py               # Prompt templates and management
│   │   └── memory.py                # Conversation memory & context
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── openai_client.py         # OpenAI API client wrapper
│   │   ├── whisper.py               # Whisper speech-to-text integration
│   │   └── tts.py                   # Text-to-speech API integration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py                # Configuration and settings management
│       ├── logger.py                # Logging configuration
│       └── helpers.py               # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_voice_llm.py           # Core functionality tests
│   ├── test_audio.py               # Audio recording/playback tests
│   ├── test_llm.py                 # LangChain integration tests
│   └── test_api.py                 # API integration tests
│
├── data/
│   ├── audio/                      # Temporary audio files
│   │   ├── input/                  # Recorded audio files
│   │   └── output/                 # Generated speech files
│   ├── logs/                       # Application logs
│   └── conversations/              # Saved conversation history
│
├── config/
│   ├── prompts/                    # Prompt template files
│   │   ├── default.txt
│   │   ├── creative.txt
│   │   └── technical.txt
│   └── models.yaml                 # Model configuration settings
│
├── scripts/
│   ├── setup.sh                    # Environment setup script
│   ├── test.sh                     # Test runner script
│   └── deploy.sh                   # Deployment script
│
├── docs/
│   ├── api.md                      # API documentation
│   ├── architecture.md             # System architecture
│   └── examples/                   # Usage examples
│       ├── basic_usage.py
│       ├── custom_chains.py
│       └── batch_processing.py
│
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── setup.py                        # Package setup configuration
├── Dockerfile                      # Docker container configuration
├── docker-compose.yml              # Docker compose for development
├── pytest.ini                     # Pytest configuration
├── .flake8                        # Code linting configuration
├── .black                         # Code formatting configuration
├── LICENSE                        # MIT License file
└── README.md                      # Project documentation