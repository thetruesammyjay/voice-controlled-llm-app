import os
import sys
import time

# Add the 'src' directory to the Python path if running directly from examples/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from voice_llm import VoiceLLM
from utils.logger import setup_logging
from utils.config import config
from llm.chains import get_conversation_chain # Import to demonstrate direct chain creation if needed
from llm.prompts import get_creative_chat_prompt, get_technical_qa_prompt # Import specific prompts

def run_custom_chain_example():
    """
    Demonstrates using VoiceLLM to switch between different conversational personas
    by reconfiguring its internal LangChain.
    """
    print("\n--- Starting Custom Chains Example ---")
    llm_app = None
    try:
        setup_logging(log_file="custom_chains.log")
        
        llm_app = VoiceLLM()
        print("VoiceLLM initialized. Demonstrating different chain types.")

        # --- Test 1: Default Chain (already set up in VoiceLLM's init) ---
        print("\n--- Using Default Chain ---")
        user_input_default = "Tell me something interesting about the history of computers."
        print(f"User (Default): \"{user_input_default}\"")
        ai_response_text, audio_path = llm_app.process_text_input(user_input_default)
        print(f"AI (Default): \"{ai_response_text}\"")
        if audio_path: llm_app.audio_player.play_audio_file(audio_path)
        time.sleep(2)

        # --- Test 2: Creative Chain ---
        print("\n--- Switching to Creative Chain ---")
        # To change the chain type, we re-initialize the conversation_chain
        # in the VoiceLLM instance, typically with a new prompt and fresh memory.
        # For simplicity, we'll get a new chain directly and assign it.
        # In a real app, you might expose a method in VoiceLLM to switch personas.
        
        # We'll create a new chain instance directly for demonstration purposes
        # This clears the previous conversation memory for this new creative interaction
        llm_app.conversation_chain = get_conversation_chain(
            llm_model=llm_app.llm,
            memory_instance=llm_app.memory, # Reusing the memory instance, but it's cleared when assigned to a new chain
            chain_type="creative"
        )
        # Clear memory if you want a fresh start for the new chain type
        llm_app.memory.clear()

        user_input_creative = "Imagine a world where animals can talk. What's the first thing they would complain about?"
        print(f"User (Creative): \"{user_input_creative}\"")
        ai_response_text, audio_path = llm_app.process_text_input(user_input_creative)
        print(f"AI (Creative): \"{ai_response_text}\"")
        if audio_path: llm_app.audio_player.play_audio_file(audio_path)
        time.sleep(2)

        # --- Test 3: Technical Chain ---
        print("\n--- Switching to Technical Chain ---")
        llm_app.conversation_chain = get_conversation_chain(
            llm_model=llm_app.llm,
            memory_instance=llm_app.memory,
            chain_type="technical"
        )
        llm_app.memory.clear()

        user_input_technical = "Explain the difference between TCP and UDP protocols in networking."
        print(f"User (Technical): \"{user_input_technical}\"")
        ai_response_text, audio_path = llm_app.process_text_input(user_input_technical)
        print(f"AI (Technical): \"{ai_response_text}\"")
        if audio_path: llm_app.audio_player.play_audio_file(audio_path)
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred during custom chains example: {e}")
        if config.DEBUG:
            import traceback
            traceback.print_exc()
    finally:
        if llm_app:
            llm_app.close()
        print("Custom chains example finished.")

if __name__ == "__main__":
    run_custom_chain_example()
