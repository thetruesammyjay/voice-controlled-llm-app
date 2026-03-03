"""
Tests for the Flask web server (src/web.py).
Uses Flask's test client to test API endpoints.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


@pytest.fixture
def mock_voice_llm():
    """Mock VoiceLLM to avoid needing OpenAI API key."""
    with patch("src.web.VoiceLLM") as mock_cls:
        mock_instance = MagicMock()
        mock_cls.return_value = mock_instance
        mock_instance.process_text_input.return_value = ("AI response", None)
        mock_instance.process_audio_upload.return_value = ("transcribed text", "AI audio response", None)
        yield mock_instance


@pytest.fixture
def mock_config():
    """Mock config to avoid needing .env file."""
    with patch("src.web.config") as mock_cfg:
        mock_cfg.OPENAI_API_KEY = "test-key"
        mock_cfg.MODEL_NAME = "gpt-3.5-turbo"
        mock_cfg.TEMPERATURE = 0.7
        mock_cfg.MAX_TOKENS = 150
        mock_cfg.TTS_VOICE = "alloy"
        mock_cfg.DEBUG = False
        yield mock_cfg


@pytest.fixture
def client(mock_config, mock_voice_llm):
    """Create Flask test client."""
    # Need to patch config before importing app
    with patch("src.utils.config.config", mock_config):
        from src.web import app
        app.config["TESTING"] = True
        with app.test_client() as client:
            # Reset the global voice_llm
            import src.web as web_module
            web_module.voice_llm = None
            yield client


# ═══════════════════════════════════════════════════
# Page Route Tests
# ═══════════════════════════════════════════════════

class TestPageRoutes:
    """Tests for HTML page routes."""

    def test_index_returns_200(self, client):
        """Test index page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_contains_title(self, client):
        """Test index page has the app title."""
        response = client.get("/")
        assert b"Voice-Controlled LLM" in response.data


# ═══════════════════════════════════════════════════
# Chat API Tests
# ═══════════════════════════════════════════════════

class TestChatAPI:
    """Tests for /api/chat endpoint."""

    def test_chat_success(self, client, mock_voice_llm):
        """Test successful text chat returns JSON response."""
        mock_voice_llm.process_text_input.return_value = ("Hello!", None)

        response = client.post("/api/chat",
                                data=json.dumps({"text": "Hi"}),
                                content_type="application/json")

        assert response.status_code == 200
        data = response.get_json()
        assert data["response"] == "Hello!"

    def test_chat_no_body(self, client):
        """Test chat with no request body returns 400."""
        response = client.post("/api/chat",
                                content_type="application/json")

        assert response.status_code == 400

    def test_chat_empty_text(self, client):
        """Test chat with empty text returns 400."""
        response = client.post("/api/chat",
                                data=json.dumps({"text": "   "}),
                                content_type="application/json")

        assert response.status_code == 400

    def test_chat_missing_text_field(self, client):
        """Test chat without 'text' field returns 400."""
        response = client.post("/api/chat",
                                data=json.dumps({"message": "Hi"}),
                                content_type="application/json")

        assert response.status_code == 400

    def test_chat_with_audio_url(self, client, mock_voice_llm):
        """Test chat response includes audio URL when audio is generated."""
        mock_voice_llm.process_text_input.return_value = ("Response", "data/audio/output/test.mp3")

        with patch("src.web.os.path.exists", return_value=True):
            response = client.post("/api/chat",
                                    data=json.dumps({"text": "Hello"}),
                                    content_type="application/json")

        data = response.get_json()
        assert data["audio_url"] == "/api/audio/test.mp3"


# ═══════════════════════════════════════════════════
# Transcribe API Tests
# ═══════════════════════════════════════════════════

class TestTranscribeAPI:
    """Tests for /api/transcribe endpoint."""

    def test_transcribe_no_file(self, client):
        """Test transcribe with no audio file returns 400."""
        response = client.post("/api/transcribe")
        assert response.status_code == 400

    def test_transcribe_success(self, client, mock_voice_llm):
        """Test successful audio transcription."""
        mock_voice_llm.process_audio_upload.return_value = (
            "Hello world", "AI response", None
        )

        data = {"audio": (BytesIO(b"fake audio data"), "recording.webm")}
        response = client.post("/api/transcribe",
                                data=data,
                                content_type="multipart/form-data")

        assert response.status_code == 200
        result = response.get_json()
        assert result["transcription"] == "Hello world"
        assert result["response"] == "AI response"


# ═══════════════════════════════════════════════════
# Settings API Tests
# ═══════════════════════════════════════════════════

class TestSettingsAPI:
    """Tests for /api/settings endpoint."""

    def test_settings_returns_config(self, client, mock_config):
        """Test settings endpoint returns current configuration."""
        response = client.get("/api/settings")

        assert response.status_code == 200
        data = response.get_json()
        assert data["model"] == "gpt-3.5-turbo"
        assert data["temperature"] == 0.7
        assert data["max_tokens"] == 150
        assert data["voice"] == "alloy"


# ═══════════════════════════════════════════════════
# Clear API Tests
# ═══════════════════════════════════════════════════

class TestClearAPI:
    """Tests for /api/clear endpoint."""

    def test_clear_success(self, client, mock_voice_llm):
        """Test clearing conversation memory."""
        response = client.post("/api/clear")

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"


# ═══════════════════════════════════════════════════
# Audio Serving Tests
# ═══════════════════════════════════════════════════

class TestAudioServing:
    """Tests for /api/audio/<filename> endpoint."""

    def test_audio_file_not_found(self, client):
        """Test serving nonexistent audio file returns 404."""
        response = client.get("/api/audio/nonexistent.mp3")
        assert response.status_code == 404
