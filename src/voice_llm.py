import os
import time
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI # Updated import for LangChain 0.1.0+
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder

from src.utils.config import config
from src.api.openai_client import OpenAIClient
from src.llm.memory import get_conversation_memory
from src.audio.recorder import AudioRecorder
from src.audio.player import AudioPlayer

class VoiceLLM:
    """
    Core VoiceLLM class that orchestrates the multimodal conversation pipeline:
    Audio recording -> Speech-to-text -> LLM processing -> Text-to-speech -> Audio playback.
    Maintains conversation state and handles configuration.
    """
    def __init__(self):
        print("Initializing VoiceLLM...")
        self.config = config
        self.openai_client = OpenAIClient()

        # Initialize LangChain LLM and memory
        self.llm = ChatOpenAI(
            model=self.config.MODEL_NAME,
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
            openai_api_key=self.config.OPENAI_API_KEY # Ensure API key is passed
        )
        self.memory = get_conversation_memory()

        # Define the prompt template for conversation chain
        self.prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"), # Where conversation history goes
            HumanMessagePromptTemplate.from_template("{input}") # User's current input
        ])

        self.conversation_chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=self.config.DEBUG # Set verbose based on debug config
        )

        # Audio components (for CLI usage primarily)
        self.audio_recorder = AudioRecorder()
        self.audio_player = AudioPlayer()

        # Setup directories for audio files
        os.makedirs("data/audio/input", exist_ok=True)
        os.makedirs("data/audio/output", exist_ok=True)

        print("VoiceLLM initialization complete.")

    def _transcribe_speech(self, audio_file_path: str) -> str:
        """
        Internal method to convert audio to text.
        Args:
            audio_file_path (str): Path to the recorded audio file.
        Returns:
            str: Transcribed text.
        """
        print(f"--> Transcribing speech from: {audio_file_path}")
        return self.openai_client.transcribe_audio(audio_file_path)

    def _generate_response(self, user_input: str) -> str:
        """
        Internal method to generate an LLM response using LangChain.
        Args:
            user_input (str): The transcribed text from the user.
        Returns:
            str: The generated text response from the LLM.
        """
        print(f"--> Generating LLM response for input: '{user_input[:50]}...'")
        try:
            # Use the conversation chain to get a response and update memory
            response = self.conversation_chain.predict(input=user_input)
            return response
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I apologize, but I encountered an error trying to generate a response."

    def _synthesize_speech(self, text: str) -> str:
        """
        Internal method to convert text to speech and save it to a file.
        Args:
            text (str): The text to synthesize.
        Returns:
            str: Path to the generated audio file.
        """
        output_file_path = os.path.join("data/audio/output", f"response_{int(time.time())}.mp3")
        print(f"--> Synthesizing speech for: '{text[:50]}...' to {output_file_path}")
        return self.openai_client.synthesize_speech(text, output_file_path)

    def _play_audio_response(self, audio_file_path: str):
        """
        Internal method to play the synthesized audio response.
        Args:
            audio_file_path (str): Path to the audio file to play.
        """
        if audio_file_path and os.path.exists(audio_file_path):
            print(f"--> Playing audio response from: {audio_file_path}")
            self.audio_player.play_audio_file(audio_file_path)
        else:
            print("--> No audio file to play or file not found.")

    def start_conversation(self, duration: int = 5):
        """
        Starts a voice conversation loop in CLI mode.
        Continuously records user audio, processes it, and plays back responses.
        Args:
            duration (int): Duration in seconds for each audio recording.
        """
        print("\n--- Starting Voice Conversation (CLI Mode) ---")
        print("Press Ctrl+C to exit.")
        while True:
            try:
                # 1. Audio Recording
                recorded_file_path = self.audio_recorder.start_recording(duration=duration)
                if not recorded_file_path:
                    print("Recording failed or interrupted. Retrying...")
                    continue

                # 2. Speech-to-Text
                user_input = self._transcribe_speech(recorded_file_path)
                print(f"You: {user_input}")

                if not user_input or user_input.strip() == "Audio file not found." or user_input.strip() == "Could not transcribe audio.":
                    print("No clear speech detected or transcription failed. Please try again.")
                    continue

                # 3. Intelligent Response Generation
                ai_response_text = self._generate_response(user_input)
                print(f"AI: {ai_response_text}")

                # 4. Text-to-Speech
                response_audio_file_path = self._synthesize_speech(ai_response_text)

                # 5. Audio Playback
                self._play_audio_response(response_audio_file_path)

                # Clean up the input audio file after processing
                # os.remove(recorded_file_path) # Uncomment to delete recorded files

            except KeyboardInterrupt:
                print("\nExiting conversation.")
                break
            except Exception as e:
                print(f"An unexpected error occurred in the conversation loop: {e}")
                time.sleep(1) # Wait a bit before retrying

    def process_text_input(self, text_input: str) -> tuple[str, str]:
        """
        Processes a text input, generates a response, and synthesizes speech.
        Useful for web interfaces where text input might be primary or
        audio is pre-recorded/uploaded.

        Args:
            text_input (str): The user's text input.

        Returns:
            tuple[str, str]: A tuple containing (AI response text, path to generated audio file).
        """
        print(f"Processing text input: '{text_input[:50]}...'")
        ai_response_text = self._generate_response(text_input)
        response_audio_file_path = self._synthesize_speech(ai_response_text)
        return ai_response_text, response_audio_file_path

    def process_audio_upload(self, audio_file_path: str) -> tuple[str, str, str]:
        """
        Processes an uploaded audio file. Transcribes it, generates a response,
        and synthesizes speech.

        Args:
            audio_file_path (str): Path to the uploaded audio file.

        Returns:
            tuple[str, str, str]: (Transcribed user input, AI response text, path to generated audio file).
        """
        print(f"Processing uploaded audio: {audio_file_path}")
        user_input = self._transcribe_speech(audio_file_path)
        if not user_input:
            user_input = "Could not transcribe uploaded audio."

        ai_response_text = self._generate_response(user_input)
        response_audio_file_path = self._synthesize_speech(ai_response_text)
        return user_input, ai_response_text, response_audio_file_path

    def close(self):
        """Clean up resources before exiting."""
        print("Closing VoiceLLM resources...")
        self.audio_recorder.close()
        self.audio_player.close()
        # No explicit close needed for OpenAI client or LangChain, but good practice
        # to ensure any streams are closed if they were opened.
        print("VoiceLLM resources closed.")

if __name__ == "__main__":
    # Ensure a .env file is configured with OPENAI_API_KEY, etc.
    # This block will run the CLI conversation.
    llm_app = VoiceLLM()
    try:
        llm_app.start_conversation(duration=5) # Records for 5 seconds per turn
    finally:
        llm_app.close()
