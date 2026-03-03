"""
Tests for the audio module (recorder, player, processor).
Uses mocking to avoid requiring actual audio hardware.
"""

import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock, mock_open

from src.audio.recorder import AudioRecorder
from src.audio.player import AudioPlayer
from src.audio.processor import AudioProcessor


# ═══════════════════════════════════════════════════
# AudioRecorder Tests
# ═══════════════════════════════════════════════════

class TestAudioRecorder:
    """Tests for AudioRecorder class."""

    def test_init_defaults(self):
        """Test AudioRecorder initializes with correct default values."""
        recorder = AudioRecorder()
        assert recorder.sample_rate == 16000
        assert recorder.channels == 1
        assert recorder.is_recording is False

    def test_init_custom_params(self):
        """Test AudioRecorder with custom sample rate and channels."""
        recorder = AudioRecorder(sample_rate=44100, channels=2)
        assert recorder.sample_rate == 44100
        assert recorder.channels == 2

    @patch("src.audio.recorder.sd")
    @patch("src.audio.recorder.sf")
    @patch("src.audio.recorder.os.makedirs")
    def test_start_recording_success(self, mock_makedirs, mock_sf, mock_sd):
        """Test successful audio recording returns a file path."""
        # Mock sounddevice recording
        mock_recording = np.zeros((16000 * 5, 1), dtype="float32")
        mock_sd.rec.return_value = mock_recording

        recorder = AudioRecorder()
        result = recorder.start_recording(duration=5)

        assert result is not None
        assert result.endswith(".wav")
        assert "data/audio/input" in result
        mock_sd.rec.assert_called_once()
        mock_sd.wait.assert_called_once()
        mock_sf.write.assert_called_once()

    @patch("src.audio.recorder.sd")
    def test_start_recording_portaudio_error(self, mock_sd):
        """Test recording gracefully handles PortAudio errors."""
        import sounddevice as sd
        mock_sd.rec.side_effect = sd.PortAudioError("No device")
        mock_sd.PortAudioError = sd.PortAudioError

        recorder = AudioRecorder()
        result = recorder.start_recording(duration=3)

        assert result is None

    @patch("src.audio.recorder.sd")
    def test_start_recording_generic_error(self, mock_sd):
        """Test recording handles unexpected exceptions."""
        mock_sd.rec.side_effect = RuntimeError("Unexpected error")

        recorder = AudioRecorder()
        result = recorder.start_recording(duration=3)

        assert result is None
        assert recorder.is_recording is False

    @patch("src.audio.recorder.sd")
    def test_stop_recording(self, mock_sd):
        """Test stop_recording calls sd.stop and resets flag."""
        recorder = AudioRecorder()
        recorder.is_recording = True

        recorder.stop_recording()

        mock_sd.stop.assert_called_once()
        assert recorder.is_recording is False

    def test_close(self):
        """Test close runs without error."""
        recorder = AudioRecorder()
        recorder.close()  # Should not raise


# ═══════════════════════════════════════════════════
# AudioPlayer Tests
# ═══════════════════════════════════════════════════

class TestAudioPlayer:
    """Tests for AudioPlayer class."""

    def test_init(self):
        """Test AudioPlayer initializes without error."""
        player = AudioPlayer()
        assert player is not None

    @patch("src.audio.player.sd")
    @patch("src.audio.player.sf")
    def test_play_audio_file_success(self, mock_sf, mock_sd):
        """Test successful audio playback."""
        mock_data = np.zeros(16000, dtype="float32")
        mock_sf.read.return_value = (mock_data, 16000)

        with patch("src.audio.player.os.path.exists", return_value=True):
            player = AudioPlayer()
            player.play_audio_file("test_audio.wav")

        mock_sf.read.assert_called_once_with("test_audio.wav", dtype="float32")
        mock_sd.play.assert_called_once_with(mock_data, 16000)
        mock_sd.wait.assert_called_once()

    def test_play_audio_file_not_found(self):
        """Test playback with nonexistent file does not raise."""
        player = AudioPlayer()
        # Should print error but not raise
        player.play_audio_file("nonexistent_file.wav")

    @patch("src.audio.player.sd")
    @patch("src.audio.player.sf")
    def test_play_audio_file_soundfile_error(self, mock_sf, mock_sd):
        """Test playback handles soundfile errors gracefully."""
        import soundfile as sf
        mock_sf.read.side_effect = sf.LibsndfileError(1)
        mock_sf.LibsndfileError = sf.LibsndfileError

        with patch("src.audio.player.os.path.exists", return_value=True):
            player = AudioPlayer()
            player.play_audio_file("corrupt_file.wav")
            # Should not raise

    def test_close(self):
        """Test close runs without error."""
        player = AudioPlayer()
        player.close()  # Should not raise


# ═══════════════════════════════════════════════════
# AudioProcessor Tests
# ═══════════════════════════════════════════════════

class TestAudioProcessor:
    """Tests for AudioProcessor class."""

    def test_init(self):
        """Test AudioProcessor initializes without error."""
        processor = AudioProcessor()
        assert processor is not None

    @patch("src.audio.processor.AudioSegment")
    def test_convert_to_wav_success(self, mock_audio_segment):
        """Test successful WAV conversion."""
        mock_audio = MagicMock()
        mock_audio_segment.from_file.return_value = mock_audio

        with patch("src.audio.processor.os.path.exists", return_value=True):
            processor = AudioProcessor()
            result = processor.convert_to_wav("input.mp3", "output.wav")

        assert result == "output.wav"
        mock_audio_segment.from_file.assert_called_once_with("input.mp3")
        mock_audio.export.assert_called_once_with("output.wav", format="wav")

    def test_convert_to_wav_file_not_found(self):
        """Test conversion with nonexistent input file."""
        processor = AudioProcessor()
        result = processor.convert_to_wav("nonexistent.mp3", "output.wav")
        assert result == ""

    @patch("src.audio.processor.AudioSegment")
    def test_convert_to_wav_error(self, mock_audio_segment):
        """Test conversion handles errors gracefully."""
        mock_audio_segment.from_file.side_effect = Exception("Conversion failed")

        with patch("src.audio.processor.os.path.exists", return_value=True):
            processor = AudioProcessor()
            result = processor.convert_to_wav("input.mp3", "output.wav")

        assert result == ""

    @patch("src.audio.processor.AudioSegment")
    def test_apply_noise_reduction_success(self, mock_audio_segment):
        """Test noise reduction placeholder works."""
        mock_audio = MagicMock()
        mock_audio_segment.from_file.return_value = mock_audio

        with patch("src.audio.processor.os.path.exists", return_value=True):
            processor = AudioProcessor()
            result = processor.apply_noise_reduction("input.wav", "output.wav")

        assert result == "output.wav"

    def test_apply_noise_reduction_file_not_found(self):
        """Test noise reduction with nonexistent input file."""
        processor = AudioProcessor()
        result = processor.apply_noise_reduction("nonexistent.wav", "output.wav")
        assert result == ""
