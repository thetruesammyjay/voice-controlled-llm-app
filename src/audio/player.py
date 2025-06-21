import sounddevice as sd
import soundfile as sf
import os
import numpy as np

class AudioPlayer:
    """
    Handles audio playback using sounddevice and soundfile.
    NOTE: Similar to recording, direct server-side audio playback in a web app
    is unusual. For web apps, the audio is typically sent to the client's
    browser to be played using JavaScript (Web Audio API or HTML5 <audio> tag).
    This class is primarily for CLI execution.
    """
    def __init__(self):
        print("AudioPlayer initialized using sounddevice and soundfile.")

    def play_audio_file(self, file_path: str):
        """
        Plays an audio file.

        Args:
            file_path (str): Path to the audio file.
        """
        if not os.path.exists(file_path):
            print(f"Error: Audio file not found at {file_path}")
            return

        try:
            print(f"Playing audio file: {file_path}...")
            # Read file to get data and sample rate
            data, samplerate = sf.read(file_path, dtype='float32')
            sd.play(data, samplerate)
            sd.wait() # Wait until playback is finished
            print("Audio playback finished.")

        except sf.LibsndfileError as e:
            print(f"Soundfile Error reading audio: {e}")
            print(f"Ensure the audio file '{file_path}' is a valid and supported format (e.g., WAV, MP3).")
        except sd.PortAudioError as e:
            print(f"PortAudio Error during playback: {e}")
            print("Please ensure your audio output device is properly configured.")
            print("You might need to install PortAudio (e.g., 'brew install portaudio' on macOS, 'sudo apt-get install portaudio19-dev' on Ubuntu).")
        except Exception as e:
            print(f"Error during audio playback: {e}")

    def close(self):
        """Clean up resources. sounddevice manages its own PortAudio resources."""
        print("AudioPlayer closed.")

# Example usage
if __name__ == "__main__":
    # Create a dummy WAV file for testing
    output_dir = "data/audio/output"
    os.makedirs(output_dir, exist_ok=True)
    dummy_wav_path = os.path.join(output_dir, "dummy_playback.wav")

    # Generate a simple sine wave or silent audio
    try:
        samplerate = 16000
        duration = 1  # seconds
        frequency = 440 # Hz (A4 note)
        t = np.linspace(0., duration, int(samplerate * duration), endpoint=False)
        data = 0.5 * np.sin(2. * np.pi * frequency * t) # Simple sine wave
        sf.write(dummy_wav_path, data, samplerate)
        print(f"Created dummy audio file for playback test: {dummy_wav_path}")

        player = AudioPlayer()
        player.play_audio_file(dummy_wav_path)
        player.close()
        os.remove(dummy_wav_path)
        print(f"Cleaned up {dummy_wav_path}")

    except ImportError:
        print("Install 'numpy' (pip install numpy) for full AudioPlayer example functionality if not already installed.")
    except Exception as e:
        print(f"Could not create or play dummy audio file: {e}")
        print("Ensure 'soundfile' and 'sounddevice' are installed correctly and PortAudio is set up.")

