"""
Handles audio playback using sounddevice and soundfile.

NOTE: Similar to recording, direct server-side audio playback in a web app
is unusual. For web apps, the audio is typically sent to the client's
browser to be played using JavaScript (Web Audio API or HTML5 <audio> tag).
This class is primarily for CLI execution.
"""

from __future__ import annotations

import os

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioPlayer:
    """Plays audio files using sounddevice and soundfile."""

    def __init__(self) -> None:
        print("AudioPlayer initialized using sounddevice and soundfile.")

    def play_audio_file(self, file_path: str) -> None:
        """
        Plays an audio file.

        Args:
            file_path: Path to the audio file.
        """
        if not os.path.exists(file_path):
            print(f"Error: Audio file not found at {file_path}")
            return

        try:
            print(f"Playing audio file: {file_path}...")
            data: np.ndarray
            samplerate: int
            data, samplerate = sf.read(file_path, dtype="float32")
            sd.play(data, samplerate)
            sd.wait()  # Wait until playback is finished
            print("Audio playback finished.")

        except sf.LibsndfileError as e:
            print(f"Soundfile Error reading audio: {e}")
            print(f"Ensure the audio file '{file_path}' is a valid and supported format (e.g., WAV, MP3).")
        except sd.PortAudioError as e:
            print(f"PortAudio Error during playback: {e}")
            print("Please ensure your audio output device is properly configured.")
            print(
                "You might need to install PortAudio (e.g., 'brew install portaudio' "
                "on macOS, 'sudo apt-get install portaudio19-dev' on Ubuntu)."
            )
        except Exception as e:
            print(f"Error during audio playback: {e}")

    def close(self) -> None:
        """Clean up resources."""
        print("AudioPlayer closed.")


# Example usage
if __name__ == "__main__":
    output_dir = "data/audio/output"
    os.makedirs(output_dir, exist_ok=True)
    dummy_wav_path = os.path.join(output_dir, "dummy_playback.wav")

    try:
        samplerate = 16000
        duration = 1
        frequency = 440
        t = np.linspace(0.0, duration, int(samplerate * duration), endpoint=False)
        data = 0.5 * np.sin(2.0 * np.pi * frequency * t)
        sf.write(dummy_wav_path, data, samplerate)
        print(f"Created dummy audio file for playback test: {dummy_wav_path}")

        player = AudioPlayer()
        player.play_audio_file(dummy_wav_path)
        player.close()
        os.remove(dummy_wav_path)
        print(f"Cleaned up {dummy_wav_path}")
    except Exception as e:
        print(f"Could not create or play dummy audio file: {e}")
