"""
Handles audio recording from the microphone using sounddevice and soundfile.

NOTE: Direct microphone access and real-time streaming in a web environment
like Streamlit is complex. This class is designed for local CLI execution.
For web apps, client-side JavaScript (Web Audio API) is typically used
to record and send audio.
"""

from __future__ import annotations

import os
import time
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf


class AudioRecorder:
    """Records audio from the microphone using sounddevice and soundfile."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1) -> None:
        self.sample_rate: int = sample_rate
        self.channels: int = channels
        self.is_recording: bool = False
        print("AudioRecorder initialized using sounddevice and soundfile.")

    def start_recording(self, duration: int = 5) -> Optional[str]:
        """
        Starts recording audio for a specified duration.

        Args:
            duration: Duration in seconds to record.

        Returns:
            Path to the saved audio file, or ``None`` if recording failed.
        """
        self.is_recording = True
        print(f"Recording started for {duration} seconds (press Ctrl+C to stop early)...")

        try:
            recording: np.ndarray = sd.rec(
                int(self.sample_rate * duration),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
            )
            sd.wait()  # Wait until recording is finished

            print("Recording stopped.")

            output_dir: str = "data/audio/input"
            os.makedirs(output_dir, exist_ok=True)
            timestamp: int = int(time.time())
            file_path: str = os.path.join(output_dir, f"input_audio_{timestamp}.wav")

            sf.write(file_path, recording, self.sample_rate)
            print(f"Audio saved to: {file_path}")
            return file_path

        except sd.PortAudioError as e:
            print(f"PortAudio Error during recording: {e}")
            print("Please ensure your microphone is properly connected and drivers are installed.")
            print(
                "You might need to install PortAudio (e.g., 'brew install portaudio' "
                "on macOS, 'sudo apt-get install portaudio19-dev' on Ubuntu)."
            )
            return None
        except Exception as e:
            print(f"Error during recording: {e}")
            self.is_recording = False
            return None

    def stop_recording(self) -> None:
        """Stops the current recording."""
        sd.stop()
        self.is_recording = False
        print("Recording flagged to stop.")

    def close(self) -> None:
        """Clean up resources."""
        print("AudioRecorder closed.")


# Example usage
if __name__ == "__main__":
    recorder = AudioRecorder()
    audio_file = recorder.start_recording(duration=5)
    if audio_file:
        print(f"Recorded audio file: {audio_file}")
    else:
        print("No audio file recorded.")
    recorder.close()
