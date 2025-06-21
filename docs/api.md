# API Documentation

This document outlines the key API integrations and their usage within the Voice-Controlled LLM App. The application primarily interfaces with OpenAI's services for speech-to-text, text generation, and text-to-speech.

All external API interactions are encapsulated within the `src/api` module for clarity and ease of management.

## 1. OpenAI Client (`src/api/openai_client.py`)

This class serves as a unified wrapper for interacting with various OpenAI services. It centralizes API key management and provides methods for the core functionalities.

### Key Methods:

#### `transcribe_audio(audio_file_path: str) -> str`

- **Description:** Converts an audio file (e.g., WAV, MP3) into text using the OpenAI Whisper API.
- **Parameters:**
  - `audio_file_path` (str): The full path to the audio file to be transcribed.
- **Returns:**
  - `str`: The transcribed text from the audio. Returns an error message string if transcription fails.
- **Usage:**

```python
from src.api.openai_client import OpenAIClient
client = OpenAIClient()
transcript = client.transcribe_audio("path/to/your/audio.wav")
print(transcript)
```

#### `get_chat_completion(messages: list, model: str, temperature: float, max_tokens: int) -> str`

- **Description:** Generates a text response from a Large Language Model (LLM) using OpenAI's GPT models.
- **Parameters:**
  - `messages` (list): A list of message dictionaries, following the OpenAI chat completion format (e.g., `[{role: "user", content: "..."}]`).
  - `model` (str): The name of the GPT model to use (e.g., "gpt-3.5-turbo", "gpt-4").
  - `temperature` (float): A value between 0.0 and 1.0 that controls the randomness of the output. Higher values make the output more creative.
  - `max_tokens` (int): The maximum number of tokens (words/sub-words) to generate in the response.
- **Returns:**
  - `str`: The generated text content from the LLM. Returns an error message string if generation fails.
- **Usage:**

```python
from src.api.openai_client import OpenAIClient
client = OpenAIClient()
messages = [{"role": "user", "content": "Tell me a joke."}]
response = client.get_chat_completion(messages, "gpt-3.5-turbo", 0.7, 100)
print(response)
```

#### `synthesize_speech(text: str, output_file_path: str) -> str`

- **Description:** Converts a given text string into natural-sounding audio using the OpenAI Text-to-Speech (TTS) API and saves it to a file.
- **Parameters:**
  - `text` (str): The text content to be synthesized into speech.
  - `output_file_path` (str): The full path where the generated audio file (e.g., MP3) will be saved.
- **Returns:**
  - `str`: The path to the saved audio file. Returns an empty string if synthesis fails.
- **Usage:**

```python
from src.api.openai_client import OpenAIClient
client = OpenAIClient()
audio_file = client.synthesize_speech("Hello, how are you?", "output.mp3")
if audio_file:
    print(f"Audio saved to: {audio_file}")
```

## 2. Whisper API Integration (`src/api/whisper.py`)

This module provides a simplified interface specifically for speech-to-text functionality, internally utilizing the `OpenAIClient`.

### Key Methods:

#### `transcribe(audio_file_path: str) -> str`

- **Description:** Directly calls the `OpenAIClient`'s transcription method.
- **Parameters:**
  - `audio_file_path` (str): Path to the audio file.
- **Returns:**
  - `str`: Transcribed text.
- **Usage:**

```python
from src.api.whisper import Whisper
whisper_service = Whisper()
transcript = whisper_service.transcribe("path/to/recorded_voice.wav")
print(transcript)
```

## 3. TTS API Integration (`src/api/tts.py`)

This module provides a simplified interface specifically for text-to-speech functionality, internally utilizing the `OpenAIClient`.

### Key Methods:

#### `synthesize(text: str, output_file_path: str) -> str`

- **Description:** Directly calls the `OpenAIClient`'s speech synthesis method.
- **Parameters:**
  - `text` (str): The text to synthesize.
  - `output_file_path` (str): The path to save the generated audio file.
- **Returns:**
  - `str`: Path to the generated audio file, or empty string on error.
- **Usage:**

```python
from src.api.tts import TTS
tts_service = TTS()
audio_output = tts_service.synthesize("Here is the AI's response.", "response_audio.mp3")
if audio_output:
    print(f"Synthesized speech to: {audio_output}")
```