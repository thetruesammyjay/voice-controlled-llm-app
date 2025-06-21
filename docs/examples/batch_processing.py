import os
import sys
import time

# Add the 'src' directory to the Python path if running directly from examples/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from voice_llm import VoiceLLM
from utils.logger import setup_logging
from utils.config import config
from audio.recorder import AudioRecorder # For creating dummy audio files

def create_dummy_audio_file(file_path: str, duration_sec: int = 2) -> str:
    """Helper to create a silent dummy audio file for testing."""
    try:
        import soundfile as sf
        import numpy as np
        samplerate = 16000
        silent_data = np.zeros(int(samplerate * duration_sec), dtype='float32')
        sf.write(file_path, silent_data, samplerate)
        print(f"Created silent dummy audio file: {file_path}")
        return file_path
    except ImportError:
        print("Warning: soundfile and numpy not installed. Cannot create dummy audio.")
        return ""
    except Exception as e:
        print(f"Error creating dummy audio file: {e}")
        return ""

def run_batch_text_processing():
    """
    Processes a list of text inputs in a batch.
    """
    print("\n--- Starting Batch Text Processing Example ---")
    llm_app = None
    try:
        setup_logging(log_file="batch_text_processing.log")
        llm_app = VoiceLLM()
        
        texts_to_process = [
            "What is the biggest planet in our solar system?",
            "Tell me about the history of artificial intelligence.",
            "Can you write a short poem about a rainy day?",
            "What are the benefits of exercise?",
            "Summarize the plot of Romeo and Juliet."
        ]

        for i, text in enumerate(texts_to_process):
            print(f"\nProcessing Text {i+1}: \"{text}\"")
            ai_response_text, audio_path = llm_app.process_text_input(text)
            print(f"AI Response: \"{ai_response_text}\"")
            if audio_path:
                print(f"AI Response Audio: {audio_path}")
                # Optionally play each audio response
                # llm_app.audio_player.play_audio_file(audio_path)
            else:
                print("No AI Response Audio generated.")
            print("-" * 50)
            time.sleep(1) # Small delay to avoid hitting rate limits if running fast

    except Exception as e:
        print(f"An error occurred during batch text processing: {e}")
        if config.DEBUG:
            import traceback
            traceback.print_exc()
    finally:
        if llm_app:
            llm_app.close()
        print("Batch text processing example finished.")

def run_batch_audio_processing():
    """
    Simulates processing a batch of pre-recorded audio files.
    """
    print("\n--- Starting Batch Audio Processing Example (Simulated) ---")
    llm_app = None
    dummy_audio_files = []
    try:
        setup_logging(log_file="batch_audio_processing.log")
        llm_app = VoiceLLM()

        # Create dummy audio files for demonstration
        audio_dir = "data/audio/batch_input"
        os.makedirs(audio_dir, exist_ok=True)
        
        for i in range(3):
            dummy_file = os.path.join(audio_dir, f"batch_audio_{i+1}.wav")
            if create_dummy_audio_file(dummy_file):
                dummy_audio_files.append(dummy_file)
            time.sleep(0.5) # Prevent same timestamp for filenames

        if not dummy_audio_files:
            print("No dummy audio files created. Skipping batch audio processing.")
            return

        for i, audio_file_path in enumerate(dummy_audio_files):
            print(f"\nProcessing Audio File {i+1}: {os.path.basename(audio_file_path)}")
            # In a real scenario, this would be an actual audio recording/upload
            user_transcription, ai_response_text, response_audio_path = llm_app.process_audio_upload(audio_file_path)
            
            print(f"User Transcribed: \"{user_transcription}\"")
            print(f"AI Response Text: \"{ai_response_text}\"")
            if response_audio_path:
                print(f"AI Response Audio: {response_audio_path}")
                # Optionally play each audio response
                # llm_app.audio_player.play_audio_file(response_audio_path)
            else:
                print("No AI Response Audio generated.")
            print("-" * 50)
            time.sleep(1) # Small delay

    except Exception as e:
        print(f"An error occurred during batch audio processing: {e}")
        if config.DEBUG:
            import traceback
            traceback.print_exc()
    finally:
        if llm_app:
            llm_app.close()
        # Clean up dummy audio files and directory
        for f in dummy_audio_files:
            if os.path.exists(f):
                os.remove(f)
        if 'audio_dir' in locals() and os.path.exists(audio_dir) and not os.listdir(audio_dir):
            os.rmdir(audio_dir)
        print("Batch audio processing example finished.")

if __name__ == "__main__":
    # Uncomment the function you want to run:
    run_batch_text_processing()
    # run_batch_audio_processing() # Requires soundfile and numpy for dummy audio creation
