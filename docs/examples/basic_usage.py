import os
import sys
import time 

# Add the 'src' directory to the Python path if running directly from examples/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from voice_llm import VoiceLLM
from utils.logger import setup_logging
from utils.config import config # Import config to check DEBUG status

def run_cli_conversation():
    """
    Demonstrates starting a voice-to-voice conversation in CLI mode.
    """
    print("\n--- Starting Basic CLI Conversation Example ---")
    llm_app = None
    try:
        # Initialize logging first
        setup_logging(log_file="basic_usage_cli.log")
        
        llm_app = VoiceLLM()
        print("VoiceLLM initialized. Speak after the 'Recording started...' prompt.")
        print("Press Ctrl+C to end the conversation.")
        llm_app.start_conversation(duration=5) # Each recording turn is 5 seconds
    except KeyboardInterrupt:
        print("\nCLI conversation ended by user.")
    except Exception as e:
        print(f"An error occurred during CLI conversation: {e}")
        if config.DEBUG:
            import traceback
            traceback.print_exc()
    finally:
        if llm_app:
            llm_app.close()
        print("CLI conversation example finished.")

def run_text_input_example():
    """
    Demonstrates processing a text input, generating a response, and synthesizing speech.
    Useful for testing the LLM and TTS pipeline without microphone interaction.
    """
    print("\n--- Starting Basic Text Input Example ---")
    llm_app = None
    try:
        # Initialize logging
        setup_logging(log_file="basic_usage_text.log")
        
        llm_app = VoiceLLM()
        
        test_phrases = [
            "Hello, how are you today?",
            "Can you tell me a short story about a brave knight?",
            "What is the capital of France?",
            "Explain the concept of quantum entanglement in simple terms."
        ]

        for i, phrase in enumerate(test_phrases):
            print(f"\nUser Input {i+1}: \"{phrase}\"")
            ai_response_text, audio_path = llm_app.process_text_input(phrase)
            print(f"AI Response Text: \"{ai_response_text}\"")
            if audio_path:
                print(f"AI Response Audio saved to: {audio_path}")
                # You can play the audio here if desired (requires audio_player instance)
                # llm_app.audio_player.play_audio_file(audio_path)
            else:
                print("No AI Response Audio generated.")
            print("-" * 50)
            if config.DEBUG:
                time.sleep(2) # Pause briefly for readability in debug mode

    except Exception as e:
        print(f"An error occurred during text input example: {e}")
        if config.DEBUG:
            import traceback
            traceback.print_exc()
    finally:
        if llm_app:
            llm_app.close()
        print("Text input example finished.")

if __name__ == "__main__":
    # You can choose which example to run
    # For a full voice-to-voice experience, run_cli_conversation()
    # For quick text-based testing, run_text_input_example()

    # Uncomment the one you want to run:
    run_cli_conversation()
    # run_text_input_example()
