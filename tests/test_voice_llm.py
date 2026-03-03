"""
Tests for the core VoiceLLM orchestrator class.
Uses mocking to avoid requiring OpenAI API key or audio hardware.
"""

import os
import pytest
from unittest.mock import patch, MagicMock, PropertyMock


# Patch config before importing VoiceLLM to avoid ValueError on missing API key
@pytest.fixture(autouse=True)
def mock_config():
    """Mock config to provide a fake API key for all tests."""
    with patch("src.utils.config.config") as mock_cfg:
        mock_cfg.OPENAI_API_KEY = "test-key-12345"
        mock_cfg.MODEL_NAME = "gpt-3.5-turbo"
        mock_cfg.WHISPER_MODEL = "whisper-1"
        mock_cfg.TTS_MODEL = "tts-1"
        mock_cfg.TTS_VOICE = "alloy"
        mock_cfg.MAX_TOKENS = 150
        mock_cfg.TEMPERATURE = 0.7
        mock_cfg.DEBUG = False
        yield mock_cfg


class TestVoiceLLM:
    """Tests for VoiceLLM orchestrator class."""

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_init_creates_all_components(self, mock_makedirs, mock_memory,
                                          mock_llm, mock_chain, mock_client,
                                          mock_recorder, mock_player):
        """Test VoiceLLM initializes all required components."""
        from src.voice_llm import VoiceLLM

        llm_app = VoiceLLM()

        assert llm_app.openai_client is not None
        assert llm_app.audio_recorder is not None
        assert llm_app.audio_player is not None
        mock_makedirs.assert_called()  # Creates audio directories
        mock_memory.assert_called_once()
        mock_llm.assert_called_once()

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_transcribe_speech(self, mock_makedirs, mock_memory,
                                mock_llm, mock_chain, mock_client_cls,
                                mock_recorder, mock_player):
        """Test internal speech transcription method."""
        from src.voice_llm import VoiceLLM

        mock_client_instance = mock_client_cls.return_value
        mock_client_instance.transcribe_audio.return_value = "Hello there"

        llm_app = VoiceLLM()
        result = llm_app._transcribe_speech("test.wav")

        assert result == "Hello there"
        mock_client_instance.transcribe_audio.assert_called_once_with("test.wav")

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_generate_response(self, mock_makedirs, mock_memory,
                                mock_llm, mock_chain_cls, mock_client,
                                mock_recorder, mock_player):
        """Test LLM response generation."""
        from src.voice_llm import VoiceLLM

        mock_chain_instance = mock_chain_cls.return_value
        mock_chain_instance.predict.return_value = "I am doing well!"

        llm_app = VoiceLLM()
        result = llm_app._generate_response("How are you?")

        assert result == "I am doing well!"

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_generate_response_error(self, mock_makedirs, mock_memory,
                                      mock_llm, mock_chain_cls, mock_client,
                                      mock_recorder, mock_player):
        """Test response generation handles errors gracefully."""
        from src.voice_llm import VoiceLLM

        mock_chain_instance = mock_chain_cls.return_value
        mock_chain_instance.predict.side_effect = Exception("LLM Error")

        llm_app = VoiceLLM()
        result = llm_app._generate_response("Test input")

        assert "error" in result.lower() or "apologize" in result.lower()

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_synthesize_speech(self, mock_makedirs, mock_memory,
                                mock_llm, mock_chain, mock_client_cls,
                                mock_recorder, mock_player):
        """Test text-to-speech synthesis."""
        from src.voice_llm import VoiceLLM

        mock_client_instance = mock_client_cls.return_value
        mock_client_instance.synthesize_speech.return_value = "data/audio/output/response.mp3"

        llm_app = VoiceLLM()
        result = llm_app._synthesize_speech("Hello world")

        assert result == "data/audio/output/response.mp3"

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_process_text_input(self, mock_makedirs, mock_memory,
                                 mock_llm, mock_chain_cls, mock_client_cls,
                                 mock_recorder, mock_player):
        """Test process_text_input returns response and audio path."""
        from src.voice_llm import VoiceLLM

        mock_chain_instance = mock_chain_cls.return_value
        mock_chain_instance.predict.return_value = "AI response"

        mock_client_instance = mock_client_cls.return_value
        mock_client_instance.synthesize_speech.return_value = "audio.mp3"

        llm_app = VoiceLLM()
        response_text, audio_path = llm_app.process_text_input("Hello")

        assert response_text == "AI response"
        assert audio_path == "audio.mp3"

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_process_audio_upload(self, mock_makedirs, mock_memory,
                                   mock_llm, mock_chain_cls, mock_client_cls,
                                   mock_recorder, mock_player):
        """Test process_audio_upload returns transcription, response, and audio."""
        from src.voice_llm import VoiceLLM

        mock_client_instance = mock_client_cls.return_value
        mock_client_instance.transcribe_audio.return_value = "User said hello"
        mock_client_instance.synthesize_speech.return_value = "response.mp3"

        mock_chain_instance = mock_chain_cls.return_value
        mock_chain_instance.predict.return_value = "AI says hi"

        llm_app = VoiceLLM()
        transcription, response, audio = llm_app.process_audio_upload("upload.wav")

        assert transcription == "User said hello"
        assert response == "AI says hi"
        assert audio == "response.mp3"

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_process_audio_upload_transcription_fails(self, mock_makedirs, mock_memory,
                                                       mock_llm, mock_chain_cls,
                                                       mock_client_cls, mock_recorder,
                                                       mock_player):
        """Test audio upload handles transcription failure."""
        from src.voice_llm import VoiceLLM

        mock_client_instance = mock_client_cls.return_value
        mock_client_instance.transcribe_audio.return_value = ""  # Empty = failed
        mock_client_instance.synthesize_speech.return_value = "response.mp3"

        mock_chain_instance = mock_chain_cls.return_value
        mock_chain_instance.predict.return_value = "Fallback response"

        llm_app = VoiceLLM()
        transcription, response, audio = llm_app.process_audio_upload("upload.wav")

        assert "Could not transcribe" in transcription

    @patch("src.voice_llm.AudioPlayer")
    @patch("src.voice_llm.AudioRecorder")
    @patch("src.voice_llm.OpenAIClient")
    @patch("src.voice_llm.ConversationChain")
    @patch("src.voice_llm.ChatOpenAI")
    @patch("src.voice_llm.get_conversation_memory")
    @patch("src.voice_llm.os.makedirs")
    def test_close(self, mock_makedirs, mock_memory,
                    mock_llm, mock_chain, mock_client,
                    mock_recorder_cls, mock_player_cls):
        """Test close cleans up recorder and player."""
        from src.voice_llm import VoiceLLM

        llm_app = VoiceLLM()
        llm_app.close()

        mock_recorder_cls.return_value.close.assert_called_once()
        mock_player_cls.return_value.close.assert_called_once()
