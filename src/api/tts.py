from src.api.openai_client import OpenAIClient
import os
import time

class TTS:
    """
    Handles text-to-speech generation using the OpenAI TTS API.
    """
    def __init__(self):
        self.openai_client = OpenAIClient()
        print("TTS API integration initialized.")

    def synthesize(self, text: str, output_file_path: str) -> str:
        """
        Converts text to speech and saves it to a specified file.

        Args:
            text (str): The text content to be converted to speech.
            output_file_path (str): The desired path for the output audio file (e.g., .mp3).

        Returns:
            str: The path to the generated audio file, or an empty string on failure.
        """
        print(f"TTS: Synthesizing text to speech for: '{text[:50]}...'")
        return self.openai_client.synthesize_speech(text, output_file_path)

# Example usage (for testing purposes)
if __name__ == "__main__":
    # IMPORTANT: To run this example, you need:
    # 1. A valid .env file with OPENAI_API_KEY set.
    print("--- Running TTS API Integration Example ---")
    tts_client = TTS()

    text_to_synthesize = "Hello, this is a test of the text-to-speech synthesis from the API module. Hope it sounds natural."
    
    # Define output directory and file path
    output_dir = "data/audio/output"
    os.makedirs(output_dir, exist_ok=True)
    output_audio_file = os.path.join(output_dir, f"tts_output_{int(time.time())}.mp3")

    generated_file_path = tts_client.synthesize(text_to_synthesize, output_audio_file)

    if generated_file_path:
        print(f"\nSpeech successfully synthesized and saved to: {generated_file_path}")
        print("You can play this file using an audio player or the AudioPlayer class.")
        
        # Optionally, play the generated audio using AudioPlayer
        try:
            from src.audio.player import AudioPlayer
            player = AudioPlayer()
            player.play_audio_file(generated_file_path)
            player.close()
            # os.remove(generated_file_path) # Uncomment to clean up dummy file after test
        except ImportError:
            print("Install 'sounddevice' and 'soundfile' for AudioPlayer functionality to play the generated audio.")
        except Exception as e:
            print(f"Error playing generated audio: {e}")
    else:
        print("\nFailed to synthesize speech.")

    print("\n--- TTS API Integration Example Finished ---")

