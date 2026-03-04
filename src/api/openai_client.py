"""
Unified client for interacting with OpenAI APIs (GPT, Whisper, TTS).
Includes automatic retry logic for transient failures using tenacity.
"""

import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.utils.config import config
from src.utils.exceptions import (
    TranscriptionError,
    ChatCompletionError,
    SynthesisError,
    AudioFileNotFoundError,
)


class OpenAIClient:
    """
    Unified client for interacting with OpenAI APIs (GPT, Whisper, TTS).
    Uses tenacity for automatic retries on transient API errors.
    """

    def __init__(self) -> None:
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.whisper_model: str = config.WHISPER_MODEL
        self.tts_model: str = config.TTS_MODEL
        self.tts_voice: str = config.TTS_VOICE

    # ── Whisper (Speech-to-Text) ──────────────────────────────

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _call_whisper_api(self, audio_file_path: str) -> str:
        """Low-level Whisper API call with automatic retry."""
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=self.whisper_model,
                file=audio_file,
                response_format="text",
            )
        return transcript.text if hasattr(transcript, "text") else transcript

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Converts speech from an audio file to text using OpenAI Whisper API.

        Args:
            audio_file_path: Path to the audio file.

        Returns:
            Transcribed text.

        Raises:
            AudioFileNotFoundError: If the audio file does not exist.
            TranscriptionError: If the Whisper API call fails.
        """
        if not os.path.exists(audio_file_path):
            print(f"Error: Audio file not found at {audio_file_path}")
            raise AudioFileNotFoundError(f"Audio file not found at {audio_file_path}")

        try:
            print(f"Transcribing audio from {audio_file_path} using Whisper model: {self.whisper_model}...")
            return self._call_whisper_api(audio_file_path)
        except Exception as e:
            print(f"Error during audio transcription: {e}")
            raise TranscriptionError(f"Could not transcribe audio: {e}") from e

    # ── GPT (Chat Completion) ─────────────────────────────────

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _call_chat_api(self, messages: list, model: str, temperature: float, max_tokens: int) -> str:
        """Low-level Chat Completion API call with automatic retry."""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def get_chat_completion(self, messages: list, model: str, temperature: float, max_tokens: int) -> str:
        """
        Generates a chat completion using OpenAI GPT models.

        Args:
            messages: List of message dictionaries [{role: "user", content: "..."}].
            model: The GPT model to use (e.g., "gpt-3.5-turbo").
            temperature: Controls creativity (0.0-1.0).
            max_tokens: Maximum number of tokens in the response.

        Returns:
            Generated text response.

        Raises:
            ChatCompletionError: If the Chat Completion API call fails.
        """
        try:
            print(f"Generating chat completion using model: {model}...")
            return self._call_chat_api(messages, model, temperature, max_tokens)
        except Exception as e:
            print(f"Error during chat completion: {e}")
            raise ChatCompletionError(f"Could not generate response: {e}") from e

    # ── TTS (Text-to-Speech) ──────────────────────────────────

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _call_tts_api(self, text: str, output_file_path: str) -> str:
        """Low-level TTS API call with automatic retry."""
        response = self.client.audio.speech.create(
            model=self.tts_model,
            voice=self.tts_voice,
            input=text,
        )
        response.stream_to_file(output_file_path)
        return output_file_path

    def synthesize_speech(self, text: str, output_file_path: str) -> str:
        """
        Converts text to natural-sounding audio using OpenAI TTS API.

        Args:
            text: The text to synthesize.
            output_file_path: The path to save the generated audio file.

        Returns:
            Path to the generated audio file.

        Raises:
            SynthesisError: If the TTS API call fails.
        """
        try:
            print(f"Synthesizing speech for text: '{text[:50]}...' using TTS model: {self.tts_model}, voice: {self.tts_voice}...")
            return self._call_tts_api(text, output_file_path)
        except Exception as e:
            print(f"Error during speech synthesis: {e}")
            raise SynthesisError(f"Could not synthesize speech: {e}") from e


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
