import argparse
from src.voice_llm import VoiceLLM
from src.utils.config import config # Import config to check debug mode

def main():
    """
    Parses command-line arguments and starts the VoiceLLM application.
    """
    parser = argparse.ArgumentParser(
        description="Voice-Controlled LLM App: Engage in voice-to-voice conversations with an AI."
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="cli",
        choices=["cli", "streamlit"], # Added streamlit as a choice for conceptual clarity
        help="Application mode: 'cli' for command-line interface, 'streamlit' for web interface (runs app.py)."
    )
    parser.add_argument(
        "--record-duration",
        type=int,
        default=5,
        help="Duration in seconds for each audio recording chunk in CLI mode."
    )

    args = parser.parse_args()

    if args.mode == "cli":
        print("\n--- Starting Voice-Controlled LLM App (CLI Mode) ---")
        llm_app = None
        try:
            llm_app = VoiceLLM()
            llm_app.start_conversation(duration=args.record_duration)
        except KeyboardInterrupt:
            print("\nApplication stopped by user (Ctrl+C).")
        except ValueError as ve:
            print(f"Configuration Error: {ve}")
            print("Please ensure your .env file is correctly configured, especially OPENAI_API_KEY.")
        except Exception as e:
            print(f"An unhandled error occurred: {e}")
            if config.DEBUG:
                import traceback
                traceback.print_exc()
        finally:
            if llm_app:
                llm_app.close()
            print("Application gracefully shut down.")
    elif args.mode == "streamlit":
        print("\n--- To run Streamlit app, please use: 'streamlit run src/app.py' ---")
        print("This main.py script does not launch the Streamlit app directly.")
        # In a real setup, you might use subprocess.Popen here,
        # but Streamlit prefers direct execution via `streamlit run`.

if __name__ == "__main__":
    main()