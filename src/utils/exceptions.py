"""
Custom exception classes for the Voice-Controlled LLM Application.

These replace magic string error returns with proper typed exceptions
that can be caught and handled at appropriate abstraction boundaries.
"""


class VoiceLLMError(Exception):
    """Base exception for all Voice-Controlled LLM errors."""
    pass


class TranscriptionError(VoiceLLMError):
    """Raised when audio-to-text transcription fails."""
    pass


class SynthesisError(VoiceLLMError):
    """Raised when text-to-speech synthesis fails."""
    pass


class ChatCompletionError(VoiceLLMError):
    """Raised when the LLM chat completion fails."""
    pass


class AudioProcessingError(VoiceLLMError):
    """Raised when audio recording, playback, or conversion fails."""
    pass


class AudioFileNotFoundError(AudioProcessingError):
    """Raised when an expected audio file is not found on disk."""
    pass
