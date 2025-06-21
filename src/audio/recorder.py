import sounddevice as sd
import soundfile as sf
import os
import time
import numpy as np

class AudioRecorder:
    """
    Handles audio recording from the microphone using sounddevice and soundfile.
    NOTE: Direct microphone access and real-time streaming in a web environment
    like Streamlit is complex. This class is designed for local CLI execution.
    For web apps, client-side JavaScript (Web Audio API) is typically used
    to record and send audio.
    """
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        print("AudioRecorder initialized using sounddevice and soundfile.")

    def start_recording(self, duration=5):
        """
        Starts recording audio for a specified duration.
        Args:
            duration (int): Duration in seconds to record.
        Returns:
            str: Path to the saved audio file, or None if recording failed.
        """
        self.is_recording = True
        print(f"Recording started for {duration} seconds (press Ctrl+C to stop early)...")

        try:
            # Record audio
            # sounddevice.rec returns a NumPy array of recorded samples
            # dtype='float32' is standard for soundfile
            recording = sd.rec(int(self.sample_rate * duration),
                               samplerate=self.sample_rate,
                               channels=self.channels,
                               dtype='float32')
            sd.wait() # Wait until recording is finished

            print("Recording stopped.")

            # Save the recorded audio to a temporary file
            output_dir = "data/audio/input"
            os.makedirs(output_dir, exist_ok=True)
            timestamp = int(time.time())
            file_path = os.path.join(output_dir, f"input_audio_{timestamp}.wav")

            sf.write(file_path, recording, self.sample_rate)
            print(f"Audio saved to: {file_path}")
            return file_path

        except sd.PortAudioError as e:
            print(f"PortAudio Error during recording: {e}")
            print("Please ensure your microphone is properly connected and drivers are installed.")
            print("You might need to install PortAudio (e.g., 'brew install portaudio' on macOS, 'sudo apt-get install portaudio19-dev' on Ubuntu).")
            return None
        except Exception as e:
            print(f"Error during recording: {e}")
            self.is_recording = False
            return None

    def stop_recording(self):
        """Stops the current recording (mostly relevant if recording indefinitely, not duration-based)."""
        sd.stop() # Stops any ongoing sounddevice recording
        self.is_recording = False
        print("Recording flagged to stop.")

    def close(self):
        """Clean up resources. sounddevice manages its own PortAudio resources."""
        print("AudioRecorder closed.")

# Example usage
if __name__ == "__main__":
    recorder = AudioRecorder()
    audio_file = recorder.start_recording(duration=5) # Records for 5 seconds
    if audio_file:
        print(f"Recorded audio file: {audio_file}")
        # To verify, you could play it back (requires AudioPlayer and soundfile)
        # from src.audio.player import AudioPlayer
        # player = AudioPlayer()
        # player.play_audio_file(audio_file)
        # player.close()
        # os.remove(audio_file) # Clean up
    else:
        print("No audio file recorded.")
    recorder.close()
