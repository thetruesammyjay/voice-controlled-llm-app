import os
from dotenv import dotenv_values, load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Manages application configuration, loaded from environment variables.
    """
    def __init__(self):
        # Load all values from .env file
        env_vars = dotenv_values()

        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", env_vars.get("OPENAI_API_KEY"))
        self.MODEL_NAME = os.getenv("MODEL_NAME", env_vars.get("MODEL_NAME", "gpt-3.5-turbo"))
        self.WHISPER_MODEL = os.getenv("WHISPER_MODEL", env_vars.get("WHISPER_MODEL", "whisper-1"))
        self.TTS_MODEL = os.getenv("TTS_MODEL", env_vars.get("TTS_MODEL", "tts-1"))
        self.TTS_VOICE = os.getenv("TTS_VOICE", env_vars.get("TTS_VOICE", "alloy"))
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", env_vars.get("MAX_TOKENS", "150")))
        self.TEMPERATURE = float(os.getenv("TEMPERATURE", env_vars.get("TEMPERATURE", "0.7")))
        self.DEBUG = os.getenv("DEBUG", env_vars.get("DEBUG", "False")).lower() == 'true'

        self._validate_config()

    def _validate_config(self):
        """Ensures essential configuration values are present."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables or .env file.")
        # Add other critical validations as needed

# Instantiate config globally for easy access
config = Config()

if __name__ == "__main__":
    # Example usage:
    print("--- Configuration Loaded ---")
    print(f"OpenAI API Key (first 5 chars): {config.OPENAI_API_KEY[:5]}...")
    print(f"Model Name: {config.MODEL_NAME}")
    print(f"Whisper Model: {config.WHISPER_MODEL}")
    print(f"TTS Voice: {config.TTS_VOICE}")
    print(f"Max Tokens: {config.MAX_TOKENS}")
    print(f"Temperature: {config.TEMPERATURE}")
    print(f"Debug Mode: {config.DEBUG}")
