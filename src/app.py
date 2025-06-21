import streamlit as st
import os
import io
import base64
import time # For unique file names

# Local imports
from src.voice_llm import VoiceLLM
from src.utils.config import config

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Voice-Controlled LLM",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
# Initialize VoiceLLM only once per session
if 'voice_llm_instance' not in st.session_state:
    try:
        st.session_state.voice_llm_instance = VoiceLLM()
        st.session_state.conversation_history = []
        st.session_state.is_ready = True
        print("VoiceLLM instance created for Streamlit session.")
    except ValueError as ve:
        st.error(f"Configuration Error: {ve}. Please ensure your OPENAI_API_KEY is set in the .env file.")
        st.session_state.is_ready = False
        print(f"VoiceLLM initialization failed: {ve}")
    except Exception as e:
        st.error(f"An unexpected error occurred during VoiceLLM initialization: {e}")
        st.session_state.is_ready = False
        print(f"VoiceLLM initialization failed: {e}")

# Check if LLM is ready before proceeding
if not st.session_state.is_ready:
    st.stop() # Stop execution if initialization failed


# --- Helper Functions ---
def display_message(role, content, audio_file_path=None):
    """Displays a message in the chat interface."""
    with st.chat_message(role):
        st.write(content)
        if audio_file_path and os.path.exists(audio_file_path):
            st.audio(audio_file_path, format="audio/mp3", start_time=0)
            # You might want to delete the audio file after playing, or periodically
            # os.remove(audio_file_path)

def handle_text_input(user_text):
    """Processes text input from the user."""
    if user_text:
        st.session_state.conversation_history.append({"role": "user", "content": user_text})
        display_message("user", user_text)

        with st.spinner("Thinking..."):
            ai_response_text, audio_path = st.session_state.voice_llm_instance.process_text_input(user_text)
            st.session_state.conversation_history.append({"role": "assistant", "content": ai_response_text, "audio": audio_path})
            display_message("assistant", ai_response_text, audio_path)

def handle_audio_upload(uploaded_file):
    """Processes an uploaded audio file."""
    if uploaded_file:
        # Save the uploaded file temporarily
        file_extension = uploaded_file.name.split('.')[-1]
        temp_audio_dir = "data/audio/input" # Use input directory for uploaded audio
        os.makedirs(temp_audio_dir, exist_ok=True)
        temp_audio_path = os.path.join(temp_audio_dir, f"uploaded_audio_{int(time.time())}.{file_extension}")

        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.conversation_history.append({"role": "user", "content": f"🎙️ Audio input ({uploaded_file.name})"})
        display_message("user", f"Audio received from user: {uploaded_file.name}")

        with st.spinner("Transcribing and Responding..."):
            user_transcription, ai_response_text, audio_path = st.session_state.voice_llm_instance.process_audio_upload(temp_audio_path)
            
            # Update history with actual transcription
            st.session_state.conversation_history[-1]["content"] = f"You (via audio): {user_transcription}"
            
            # Display transcribed user input
            with st.chat_message("user"):
                st.write(f"You (transcribed): {user_transcription}")


            st.session_state.conversation_history.append({"role": "assistant", "content": ai_response_text, "audio": audio_path})
            display_message("assistant", ai_response_text, audio_path)
        
        # Clean up the temporary uploaded file
        os.remove(temp_audio_path)


# --- Streamlit UI ---
st.title("🗣️ Voice-Controlled LLM Chat")
st.markdown(
    """
    This application allows you to converse with an LLM using text or audio.
    """
)

# Display previous messages from history
for message in st.session_state.conversation_history:
    display_message(message["role"], message["content"], message.get("audio"))

# Text Input Section
st.markdown("---")
st.subheader("Type your message:")
user_text_input = st.chat_input("Say something...", on_submit=lambda: handle_text_input(st.session_state.user_input_key), key="user_input_key")

# Audio Upload Section (for simulating voice input in Streamlit)
st.subheader("Or upload an audio file:")
uploaded_audio = st.file_uploader("Upload an audio file (e.g., .mp3, .wav)", type=["mp3", "wav", "ogg"])
if uploaded_audio:
    handle_audio_upload(uploaded_audio)

st.markdown("---")
st.caption("Note: Real-time microphone recording and playback in Streamlit require advanced browser APIs or custom components. This app uses file upload for audio input and plays back generated audio.")

# Optional: Add a button to clear conversation history
if st.sidebar.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.session_state.voice_llm_instance.memory.clear() # Clear LangChain memory
    st.rerun()

st.sidebar.markdown("### Settings")
st.sidebar.write(f"**Model:** {config.MODEL_NAME}")
st.sidebar.write(f"**Temperature:** {config.TEMPERATURE}")
st.sidebar.write(f"**Max Tokens:** {config.MAX_TOKENS}")
st.sidebar.write(f"**TTS Voice:** {config.TTS_VOICE}")

# Add a placeholder for CLI command to run Streamlit
st.sidebar.markdown("""
---
**To run this web interface:**
`streamlit run src/app.py`
""")

