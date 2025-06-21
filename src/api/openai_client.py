from openai import OpenAI
from src.utils.config import config
import os

class OpenAIClient:
    """
    Unified client for interacting with OpenAI APIs (GPT, Whisper, TTS).
    """
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.whisper_model = config.WHISPER_MODEL
        self.tts_model = config.TTS_MODEL
        self.tts_voice = config.TTS_VOICE

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Converts speech from an audio file to text using OpenAI Whisper API.

        Args:
            audio_file_path (str): Path to the audio file.

        Returns:
            str: Transcribed text.
        """
        if not os.path.exists(audio_file_path):
            print(f"Error: Audio file not found at {audio_file_path}")
            return "Audio file not found."

        try:
            print(f"Transcribing audio from {audio_file_path} using Whisper model: {self.whisper_model}...")
            # For demonstration, we'll simulate a response.
            # In a real application, you would do:
            with open(audio_file_path, "rb") as audio_file:
                 transcript = self.client.audio.transcriptions.create(
                     model=self.whisper_model,
                     file=audio_file,
                     response_format="text"
                 )
            return transcript.text if hasattr(transcript, 'text') else transcript
        except Exception as e:
            print(f"Error during audio transcription: {e}")
            return "Could not transcribe audio."

    def get_chat_completion(self, messages: list, model: str, temperature: float, max_tokens: int) -> str:
        """
        Generates a chat completion using OpenAI GPT models.

        Args:
            messages (list): List of message dictionaries [{role: "user", content: "..."}].
            model (str): The GPT model to use (e.g., "gpt-3.5-turbo").
            temperature (float): Controls creativity (0.0-1.0).
            max_tokens (int): Maximum number of tokens in the response.

        Returns:
            str: Generated text response.
        """
        try:
            print(f"Generating chat completion using model: {model}...")
            # For demonstration, we'll simulate a response.
            # In a real application, you would do:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during chat completion: {e}")
            return "Could not generate response."

    def synthesize_speech(self, text: str, output_file_path: str) -> str:
        """
        Converts text to natural-sounding audio using OpenAI TTS API.

        Args:
            text (str): The text to synthesize.
            output_file_path (str): The path to save the generated audio file.

        Returns:
            str: Path to the generated audio file, or empty string on error.
        """
        try:
            print(f"Synthesizing speech for text: '{text[:50]}...' using TTS model: {self.tts_model}, voice: {self.tts_voice}...")
            # For demonstration, we'll simulate saving an empty file.
            # In a real application, you would do:
            response = self.client.audio.speech.create(
                model=self.tts_model,
                voice=self.tts_voice,
                input=text
            )
            response.stream_to_file(output_file_path)
            return output_file_path
        except Exception as e:
            print(f"Error during speech synthesis: {e}")
            return ""

# Example usage (for testing purposes, not typically run directly)
if __name__ == "__main__":
    # Ensure you have a .env file with OPENAI_API_KEY
    # Create a dummy audio file for testing transcription
    dummy_audio_path = "dummy_audio.mp3"
    with open(dummy_audio_path, "w") as f:
        f.write("This is a dummy audio file content.")

    openai_client = OpenAIClient()

    # Test transcription
    transcript = openai_client.transcribe_audio(dummy_audio_path)
    print(f"Transcription Result: {transcript}")

    # Test chat completion
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    response_text = openai_client.get_chat_completion(messages, "gpt-3.5-turbo", 0.7, 50)
    print(f"Chat Completion Result: {response_text}")

    # Test TTS
    tts_output_path = "output_speech.mp3"
    generated_audio_path = openai_client.synthesize_speech("Hello, I am fine, thank you!", tts_output_path)
    if generated_audio_path:
        print(f"Generated speech saved to: {generated_audio_path}")
        # Clean up dummy files
        os.remove(dummy_audio_path)
        os.remove(tts_output_path)
