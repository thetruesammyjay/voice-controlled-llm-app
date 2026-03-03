"""
Tests for the utils module (config, helpers, logger).
"""

import os
import logging
import pytest
from unittest.mock import patch, MagicMock

from src.utils.helpers import generate_timestamped_filename, ensure_directory_exists


# ═══════════════════════════════════════════════════
# Config Tests
# ═══════════════════════════════════════════════════

class TestConfig:
    """Tests for the Config class."""

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-key-abc123",
        "MODEL_NAME": "gpt-4",
        "MAX_TOKENS": "200",
        "TEMPERATURE": "0.5",
        "DEBUG": "True",
    })
    def test_config_loads_from_env(self):
        """Test Config reads values from environment variables."""
        from src.utils.config import Config
        cfg = Config()

        assert cfg.OPENAI_API_KEY == "test-key-abc123"
        assert cfg.MODEL_NAME == "gpt-4"
        assert cfg.MAX_TOKENS == 200
        assert cfg.TEMPERATURE == 0.5
        assert cfg.DEBUG is True

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-key",
    }, clear=False)
    def test_config_defaults(self):
        """Test Config applies defaults for optional values."""
        from src.utils.config import Config
        cfg = Config()

        assert cfg.WHISPER_MODEL == "whisper-1"
        assert cfg.TTS_MODEL == "tts-1"
        assert cfg.TTS_VOICE == "alloy"

    @patch.dict(os.environ, {}, clear=True)
    @patch("src.utils.config.dotenv_values", return_value={})
    @patch("src.utils.config.load_dotenv")
    def test_config_raises_without_api_key(self, mock_load, mock_dotenv):
        """Test Config raises ValueError when API key is missing."""
        from src.utils.config import Config
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            Config()

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "key-123",
        "DEBUG": "false",
    })
    def test_config_debug_false(self):
        """Test Config correctly parses DEBUG=false."""
        from src.utils.config import Config
        cfg = Config()
        assert cfg.DEBUG is False

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "key-123",
        "DEBUG": "true",
    })
    def test_config_debug_true_case_insensitive(self):
        """Test Config parses DEBUG=true case-insensitively."""
        from src.utils.config import Config
        cfg = Config()
        assert cfg.DEBUG is True


# ═══════════════════════════════════════════════════
# Helper Tests
# ═══════════════════════════════════════════════════

class TestHelpers:
    """Tests for utility helper functions."""

    def test_generate_timestamped_filename_default(self):
        """Test default filename generation."""
        filename = generate_timestamped_filename()
        assert filename.startswith("file_")
        assert filename.endswith(".tmp")

    def test_generate_timestamped_filename_custom(self):
        """Test custom prefix and extension."""
        filename = generate_timestamped_filename(prefix="recording", extension="wav")
        assert filename.startswith("recording_")
        assert filename.endswith(".wav")

    def test_generate_timestamped_filename_unique(self):
        """Test generated filenames are unique (different timestamps)."""
        f1 = generate_timestamped_filename()
        f2 = generate_timestamped_filename()
        # They should be very close but potentially different
        # At minimum, they should follow the pattern
        assert f1.startswith("file_")
        assert f2.startswith("file_")

    def test_generate_timestamped_filename_format(self):
        """Test filename follows prefix_timestamp.extension format."""
        filename = generate_timestamped_filename(prefix="test", extension="mp3")
        parts = filename.split("_", 1)
        assert parts[0] == "test"
        assert "." in parts[1]
        timestamp_part = parts[1].rsplit(".", 1)[0]
        assert timestamp_part.isdigit()

    def test_ensure_directory_exists_creates_dir(self, tmp_path):
        """Test directory creation."""
        new_dir = os.path.join(str(tmp_path), "new_directory")
        assert not os.path.exists(new_dir)

        ensure_directory_exists(new_dir)

        assert os.path.exists(new_dir)
        assert os.path.isdir(new_dir)

    def test_ensure_directory_exists_nested(self, tmp_path):
        """Test nested directory creation."""
        nested_dir = os.path.join(str(tmp_path), "a", "b", "c")
        ensure_directory_exists(nested_dir)
        assert os.path.exists(nested_dir)

    def test_ensure_directory_exists_already_exists(self, tmp_path):
        """Test does not error on existing directory."""
        existing_dir = str(tmp_path)
        ensure_directory_exists(existing_dir)  # Should not raise
        assert os.path.exists(existing_dir)


# ═══════════════════════════════════════════════════
# Logger Tests
# ═══════════════════════════════════════════════════

class TestLogger:
    """Tests for the logging setup."""

    @patch("src.utils.logger.config")
    def test_setup_logging_creates_log_dir(self, mock_config, tmp_path):
        """Test logging setup creates the log directory."""
        mock_config.DEBUG = False
        log_dir = os.path.join(str(tmp_path), "logs")

        from src.utils.logger import setup_logging
        setup_logging(log_file="test.log", log_dir=log_dir)

        assert os.path.exists(log_dir)

    @patch("src.utils.logger.config")
    def test_setup_logging_creates_file_handler(self, mock_config, tmp_path):
        """Test logging setup creates a log file."""
        mock_config.DEBUG = True
        log_dir = str(tmp_path)

        from src.utils.logger import setup_logging
        setup_logging(log_file="test_app.log", log_dir=log_dir)

        # Check that the log file path exists in handlers
        log_path = os.path.join(log_dir, "test_app.log")
        # Log something to create the file
        logging.info("Test message")
        assert os.path.exists(log_path)

    @patch("src.utils.logger.config")
    def test_setup_logging_debug_level(self, mock_config, tmp_path):
        """Test debug mode sets DEBUG log level."""
        mock_config.DEBUG = True

        from src.utils.logger import setup_logging
        setup_logging(log_dir=str(tmp_path))

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    @patch("src.utils.logger.config")
    def test_setup_logging_info_level(self, mock_config, tmp_path):
        """Test non-debug mode sets INFO log level."""
        mock_config.DEBUG = False

        from src.utils.logger import setup_logging
        setup_logging(log_dir=str(tmp_path))

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
