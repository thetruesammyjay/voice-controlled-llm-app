"""
Flask Web Server for Voice-Controlled LLM App
Serves the frontend UI and provides REST API endpoints
for text chat, audio transcription, and speech synthesis.
"""

import os
import time
import logging
from flask import Flask, render_template, request, jsonify, send_file

from src.utils.config import config
from src.voice_llm import VoiceLLM

# ─── Flask App Setup ───
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
)

logger = logging.getLogger(__name__)

# ─── Global VoiceLLM Instance ───
voice_llm = None


def get_voice_llm():
    """Lazy initialization of VoiceLLM instance."""
    global voice_llm
    if voice_llm is None:
        voice_llm = VoiceLLM()
    return voice_llm


# ═══════════════════════════════════════════════════
# Page Routes
# ═══════════════════════════════════════════════════

@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template('index.html', config={
        'model_name': config.MODEL_NAME,
        'temperature': config.TEMPERATURE,
        'max_tokens': config.MAX_TOKENS,
        'tts_voice': config.TTS_VOICE,
    })


# ═══════════════════════════════════════════════════
# API Routes
# ═══════════════════════════════════════════════════

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """
    Process a text message and return an AI response with optional audio.

    Request JSON:
        { "text": "user message" }

    Response JSON:
        { "response": "AI response text", "audio_url": "/api/audio/<filename>" }
    """
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({'error': 'No text provided'}), 400

    user_text = data['text'].strip()
    if not user_text:
        return jsonify({'error': 'Empty text'}), 400

    try:
        llm = get_voice_llm()
        ai_response, audio_path = llm.process_text_input(user_text)

        audio_url = None
        if audio_path and os.path.exists(audio_path):
            audio_filename = os.path.basename(audio_path)
            audio_url = f'/api/audio/{audio_filename}'

        return jsonify({
            'response': ai_response,
            'audio_url': audio_url,
        })

    except Exception as e:
        logger.error(f"Chat processing error: {e}")
        return jsonify({'error': 'Failed to process message'}), 500


@app.route('/api/transcribe', methods=['POST'])
def api_transcribe():
    """
    Transcribe uploaded audio, generate AI response, and return everything.

    Request: multipart/form-data with 'audio' file

    Response JSON:
        {
            "transcription": "what the user said",
            "response": "AI response text",
            "audio_url": "/api/audio/<filename>"
        }
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if not audio_file.filename:
        return jsonify({'error': 'Empty audio file'}), 400

    try:
        # Save uploaded audio temporarily
        input_dir = os.path.join('data', 'audio', 'input')
        os.makedirs(input_dir, exist_ok=True)

        ext = audio_file.filename.rsplit('.', 1)[-1] if '.' in audio_file.filename else 'webm'
        temp_path = os.path.join(input_dir, f'upload_{int(time.time())}.{ext}')
        audio_file.save(temp_path)

        # Process through VoiceLLM pipeline
        llm = get_voice_llm()
        transcription, ai_response, audio_path = llm.process_audio_upload(temp_path)

        # Clean up uploaded file
        try:
            os.remove(temp_path)
        except OSError:
            pass

        audio_url = None
        if audio_path and os.path.exists(audio_path):
            audio_filename = os.path.basename(audio_path)
            audio_url = f'/api/audio/{audio_filename}'

        return jsonify({
            'transcription': transcription,
            'response': ai_response,
            'audio_url': audio_url,
        })

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return jsonify({'error': 'Failed to process audio'}), 500


@app.route('/api/audio/<filename>')
def api_audio(filename):
    """Serve a generated audio file."""
    audio_dir = os.path.join('data', 'audio', 'output')
    file_path = os.path.join(audio_dir, filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'Audio file not found'}), 404

    return send_file(file_path, mimetype='audio/mpeg')


@app.route('/api/settings', methods=['GET'])
def api_settings():
    """Return the current application settings."""
    return jsonify({
        'model': config.MODEL_NAME,
        'temperature': config.TEMPERATURE,
        'max_tokens': config.MAX_TOKENS,
        'voice': config.TTS_VOICE,
    })


@app.route('/api/clear', methods=['POST'])
def api_clear():
    """Clear the conversation memory."""
    try:
        llm = get_voice_llm()
        llm.memory.clear()
        return jsonify({'status': 'ok'})
    except Exception as e:
        logger.error(f"Clear error: {e}")
        return jsonify({'error': 'Failed to clear'}), 500


# ═══════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════

def run_web():
    """Run the Flask development server."""
    print("\n--- Starting Voice-Controlled LLM Web App ---")
    print(f"  Model: {config.MODEL_NAME}")
    print(f"  TTS Voice: {config.TTS_VOICE}")
    print(f"  Debug: {config.DEBUG}")
    print(f"  Open http://127.0.0.1:5000 in your browser")
    print("----------------------------------------------\n")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG,
    )


if __name__ == '__main__':
    run_web()
