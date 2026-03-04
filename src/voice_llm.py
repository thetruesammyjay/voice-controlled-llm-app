"""
Core VoiceLLM class that orchestrates the multimodal conversation pipeline:
Audio recording -> Speech-to-text -> LLM processing -> Text-to-speech -> Audio playback.

Maintains conversation state and handles configuration.
"""

from __future__ import annotations

import os
import time

from src.utils.config import config
from src.utils.exceptions import TranscriptionError, SynthesisError, ChatCompletionError
from src.api.openai_client import OpenAIClient
from src.llm.chains import get_conversation_chain
from src.llm.memory import save_conversation
from src.audio.recorder import AudioRecorder
from src.audio.player import AudioPlayer


class VoiceLLM:
    """
    Orchestrates the multimodal conversation pipeline.

    Uses ``get_conversation_chain()`` from ``src.llm.chains`` to avoid
    duplicating LLM / memory / prompt initialisation logic.
    """

    def __init__(self) -> None:
        print("Initializing VoiceLLM...")
        self.config = config
        self.openai_client = OpenAIClient()

        # Use the shared factory instead of re-creating LLM/memory/prompt here
        self.conversation_chain = get_conversation_chain(verbose=self.config.DEBUG)

        # Audio components (for CLI usage primarily)
        self.audio_recorder = AudioRecorder()
        self.audio_player = AudioPlayer()

        # Setup directories for audio files
        os.makedirs("data/audio/input", exist_ok=True)
        os.makedirs("data/audio/output", exist_ok=True)

        print("VoiceLLM initialization complete.")

    # ── Internal pipeline steps ───────────────────────────────

    def _transcribe_speech(self, audio_file_path: str) -> str:
        """
        Converts audio to text via the OpenAI Whisper API.

        Args:
            audio_file_path: Path to the recorded audio file.

        Returns:
            Transcribed text.

        Raises:
            TranscriptionError: If transcription fails.
        """
        print(f"--> Transcribing speech from: {audio_file_path}")
        return self.openai_client.transcribe_audio(audio_file_path)

    def _generate_response(self, user_input: str) -> str:
        """
        Generates an LLM response using LangChain.

        Args:
            user_input: The transcribed text from the user.

        Returns:
            The generated text response from the LLM.
        """
        print(f"--> Generating LLM response for input: '{user_input[:50]}...'")
        try:
            response: str = self.conversation_chain.predict(input=user_input)
            return response
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I apologize, but I encountered an error trying to generate a response."

    def _synthesize_speech(self, text: str) -> str:
        """
        Converts text to speech and saves it to a file.

        Args:
            text: The text to synthesize.

        Returns:
            Path to the generated audio file.
        """
        output_file_path: str = os.path.join(
            "data/audio/output", f"response_{int(time.time())}.mp3"
        )
        print(f"--> Synthesizing speech for: '{text[:50]}...' to {output_file_path}")
        return self.openai_client.synthesize_speech(text, output_file_path)

    def _play_audio_response(self, audio_file_path: str) -> None:
        """Plays the synthesized audio response."""
        if audio_file_path and os.path.exists(audio_file_path):
            print(f"--> Playing audio response from: {audio_file_path}")
            self.audio_player.play_audio_file(audio_file_path)
        else:
            print("--> No audio file to play or file not found.")

    # ── Public interface ──────────────────────────────────────

    def start_conversation(self, duration: int = 5) -> None:
        """
        Starts a voice conversation loop in CLI mode.

        Args:
            duration: Duration in seconds for each audio recording.
        """
        print("\n--- Starting Voice Conversation (CLI Mode) ---")
        print("Press Ctrl+C to exit.")
        while True:
            try:
                recorded_file_path = self.audio_recorder.start_recording(duration=duration)
                if not recorded_file_path:
                    print("Recording failed or interrupted. Retrying...")
                    continue

                # Speech-to-Text
                try:
                    user_input = self._transcribe_speech(recorded_file_path)
                except TranscriptionError:
                    print("Transcription failed. Please try again.")
                    continue

                print(f"You: {user_input}")

                # LLM Response
                ai_response_text = self._generate_response(user_input)
                print(f"AI: {ai_response_text}")

                # Text-to-Speech
                try:
                    response_audio_file_path = self._synthesize_speech(ai_response_text)
                    self._play_audio_response(response_audio_file_path)
                except SynthesisError:
                    print("Speech synthesis failed; response is text-only.")

            except KeyboardInterrupt:
                print("\nExiting conversation.")
                break
            except Exception as e:
                print(f"An unexpected error occurred in the conversation loop: {e}")
                time.sleep(1)

    def process_text_input(self, text_input: str) -> tuple[str, str]:
        """
        Processes a text input, generates a response, and synthesizes speech.

        Args:
            text_input: The user's text input.

        Returns:
            A tuple of (AI response text, path to generated audio file).
        """
        print(f"Processing text input: '{text_input[:50]}...'")
        ai_response_text = self._generate_response(text_input)
        response_audio_file_path = self._synthesize_speech(ai_response_text)
        return ai_response_text, response_audio_file_path

    def process_audio_upload(self, audio_file_path: str) -> tuple[str, str, str]:
        """
        Processes an uploaded audio file.

        Args:
            audio_file_path: Path to the uploaded audio file.

        Returns:
            A tuple of (transcribed user input, AI response text,
            path to generated audio file).
        """
        print(f"Processing uploaded audio: {audio_file_path}")
        user_input = self._transcribe_speech(audio_file_path)
        if not user_input:
            user_input = "Could not transcribe uploaded audio."

        ai_response_text = self._generate_response(user_input)
        response_audio_file_path = self._synthesize_speech(ai_response_text)
        return user_input, ai_response_text, response_audio_file_path

    def save_current_conversation(self) -> str:
        """Persists the current conversation to a JSON file."""
        return save_conversation(self.conversation_chain.memory)

    def close(self) -> None:
        """Clean up resources before exiting."""
        print("Closing VoiceLLM resources...")
        self.audio_recorder.close()
        self.audio_player.close()
        print("VoiceLLM resources closed.")


if __name__ == "__main__":
    llm_app = VoiceLLM()
    try:
        llm_app.start_conversation(duration=5)
    finally:
        llm_app.close()
