from src.api.openai_client import OpenAIClient
import os

class Whisper:
    """
    Handles speech-to-text processing using the OpenAI Whisper API.
    """
    def __init__(self):
        self.openai_client = OpenAIClient()
        print("Whisper API integration initialized.")

    def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribes speech from an audio file into text.

        Args:
            audio_file_path (str): The file path of the audio to transcribe.

        Returns:
            str: The transcribed text.
        """
        print(f"Whisper: Transcribing audio file: {audio_file_path}")
        return self.openai_client.transcribe_audio(audio_file_path)

# Example usage (for testing purposes)
if __name__ == "__main__":
    # IMPORTANT: To run this example, you need:
    # 1. A valid .env file with OPENAI_API_KEY set.
    # 2. A dummy audio file for transcription.
    #    You can create one using the AudioRecorder example in src/audio/recorder.py
    #    or a small existing .wav/.mp3 file.

    print("--- Running Whisper API Integration Example ---")
    whisper_client = Whisper()

    # Create a dummy audio file path for demonstration
    dummy_audio_file = "data/audio/input/sample_input_for_whisper.wav"
    # In a real scenario, this file would be recorded by AudioRecorder or uploaded.
    # For this example, we'll just check if it exists and simulate.
    if not os.path.exists("data/audio/input"):
        os.makedirs("data/audio/input")
    if not os.path.exists(dummy_audio_file):
        print(f"Please create a dummy audio file at '{dummy_audio_file}' for testing.")
        print("You can use the `src/audio/recorder.py` example to create one.")
        print("Example: python src/audio/recorder.py to record a 5-second audio, then rename it.")
        # Attempt to create a silent dummy file if soundfile is available
        try:
            import soundfile as sf
            import numpy as np
            samplerate = 16000
            duration = 1  # seconds of silence
            silent_data = np.zeros(int(samplerate * duration), dtype='float32')
            sf.write(dummy_audio_file, silent_data, samplerate)
            print(f"Created a silent dummy file: {dummy_audio_file}")
        except ImportError:
            print("To create a dummy file automatically, please install 'soundfile' and 'numpy'.")
        except Exception as e:
            print(f"Failed to create dummy audio file: {e}")

    if os.path.exists(dummy_audio_file):
        transcribed_text = whisper_client.transcribe(dummy_audio_file)
        print(f"\nTranscribed Text: \"{transcribed_text}\"")
        # os.remove(dummy_audio_file) # Uncomment to clean up dummy file after test
    else:
        print("\nSkipping transcription test as no dummy audio file is available.")

    print("\n--- Whisper API Integration Example Finished ---")

