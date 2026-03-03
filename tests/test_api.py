"""
Tests for the API module (OpenAI client, Whisper, TTS).
Uses mocking to avoid making real API calls.
"""

import os
import pytest
from unittest.mock import patch, MagicMock, mock_open

from src.api.openai_client import OpenAIClient
from src.api.whisper import Whisper
from src.api.tts import TTS


# ═══════════════════════════════════════════════════
# OpenAIClient Tests
# ═══════════════════════════════════════════════════

class TestOpenAIClient:
    """Tests for OpenAIClient class."""

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_init(self, mock_openai_cls, mock_config):
        """Test OpenAIClient initializes with config values."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        client = OpenAIClient()

        assert client.whisper_model == "whisper-1"
        assert client.tts_model == "tts-1"
        assert client.tts_voice == "alloy"
        mock_openai_cls.assert_called_once_with(api_key="test-key")

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_transcribe_audio_success(self, mock_openai_cls, mock_config):
        """Test successful audio transcription."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        mock_client_instance = MagicMock()
        mock_openai_cls.return_value = mock_client_instance
        mock_client_instance.audio.transcriptions.create.return_value = "Hello world"

        client = OpenAIClient()

        with patch("builtins.open", mock_open(read_data=b"audio data")):
            with patch("src.api.openai_client.os.path.exists", return_value=True):
                result = client.transcribe_audio("test.wav")

        assert result == "Hello world"

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_transcribe_audio_file_not_found(self, mock_openai_cls, mock_config):
        """Test transcription with nonexistent file."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        client = OpenAIClient()
        result = client.transcribe_audio("nonexistent.wav")

        assert result == "Audio file not found."

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_transcribe_audio_api_error(self, mock_openai_cls, mock_config):
        """Test transcription handles API errors gracefully."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        mock_client_instance = MagicMock()
        mock_openai_cls.return_value = mock_client_instance
        mock_client_instance.audio.transcriptions.create.side_effect = Exception("API Error")

        client = OpenAIClient()

        with patch("builtins.open", mock_open(read_data=b"audio data")):
            with patch("src.api.openai_client.os.path.exists", return_value=True):
                result = client.transcribe_audio("test.wav")

        assert result == "Could not transcribe audio."

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_get_chat_completion_success(self, mock_openai_cls, mock_config):
        """Test successful chat completion."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        mock_client_instance = MagicMock()
        mock_openai_cls.return_value = mock_client_instance

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello! I'm fine."
        mock_client_instance.chat.completions.create.return_value = mock_response

        client = OpenAIClient()
        messages = [{"role": "user", "content": "Hi"}]
        result = client.get_chat_completion(messages, "gpt-3.5-turbo", 0.7, 150)

        assert result == "Hello! I'm fine."

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_get_chat_completion_error(self, mock_openai_cls, mock_config):
        """Test chat completion handles errors."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        mock_client_instance = MagicMock()
        mock_openai_cls.return_value = mock_client_instance
        mock_client_instance.chat.completions.create.side_effect = Exception("Rate limit")

        client = OpenAIClient()
        result = client.get_chat_completion([], "gpt-3.5-turbo", 0.7, 150)

        assert result == "Could not generate response."

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_synthesize_speech_success(self, mock_openai_cls, mock_config):
        """Test successful speech synthesis."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        mock_client_instance = MagicMock()
        mock_openai_cls.return_value = mock_client_instance

        mock_response = MagicMock()
        mock_client_instance.audio.speech.create.return_value = mock_response

        client = OpenAIClient()
        result = client.synthesize_speech("Hello", "output.mp3")

        assert result == "output.mp3"
        mock_response.stream_to_file.assert_called_once_with("output.mp3")

    @patch("src.api.openai_client.config")
    @patch("src.api.openai_client.OpenAI")
    def test_synthesize_speech_error(self, mock_openai_cls, mock_config):
        """Test speech synthesis handles errors."""
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.WHISPER_MODEL = "whisper-1"
        mock_config.TTS_MODEL = "tts-1"
        mock_config.TTS_VOICE = "alloy"

        mock_client_instance = MagicMock()
        mock_openai_cls.return_value = mock_client_instance
        mock_client_instance.audio.speech.create.side_effect = Exception("TTS Error")

        client = OpenAIClient()
        result = client.synthesize_speech("Hello", "output.mp3")

        assert result == ""


# ═══════════════════════════════════════════════════
# Whisper Wrapper Tests
# ═══════════════════════════════════════════════════

class TestWhisper:
    """Tests for Whisper wrapper class."""

    @patch("src.api.whisper.OpenAIClient")
    def test_transcribe_delegates_to_client(self, mock_client_cls):
        """Test that Whisper.transcribe delegates to OpenAIClient."""
        mock_instance = MagicMock()
        mock_client_cls.return_value = mock_instance
        mock_instance.transcribe_audio.return_value = "transcribed text"

        whisper = Whisper()
        result = whisper.transcribe("audio.wav")

        assert result == "transcribed text"
        mock_instance.transcribe_audio.assert_called_once_with("audio.wav")


# ═══════════════════════════════════════════════════
# TTS Wrapper Tests
# ═══════════════════════════════════════════════════

class TestTTS:
    """Tests for TTS wrapper class."""

    @patch("src.api.tts.OpenAIClient")
    def test_synthesize_delegates_to_client(self, mock_client_cls):
        """Test that TTS.synthesize delegates to OpenAIClient."""
        mock_instance = MagicMock()
        mock_client_cls.return_value = mock_instance
        mock_instance.synthesize_speech.return_value = "output.mp3"

        tts = TTS()
        result = tts.synthesize("Hello", "output.mp3")

        assert result == "output.mp3"
        mock_instance.synthesize_speech.assert_called_once_with("Hello", "output.mp3")
