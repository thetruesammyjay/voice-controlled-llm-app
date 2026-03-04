"""
Provides utility functions for audio file processing.

NOTE: For full functionality, pydub often requires ffmpeg or libav to be
installed and accessible in your system's PATH.
"""

from __future__ import annotations

import os

from pydub import AudioSegment


class AudioProcessor:
    """Utility class for audio file format conversion and processing."""

    def __init__(self) -> None:
        print("AudioProcessor initialized. (Requires pydub and optionally ffmpeg/libav)")

    def convert_to_wav(self, input_file_path: str, output_file_path: str) -> str:
        """
        Converts an audio file to WAV format.

        Args:
            input_file_path: Path to the input audio file.
            output_file_path: Desired path for the output WAV file.

        Returns:
            Path to the converted WAV file, or an empty string on failure.
        """
        if not os.path.exists(input_file_path):
            print(f"Error: Input audio file not found at {input_file_path}")
            return ""

        try:
            print(f"Converting '{input_file_path}' to WAV format...")
            audio: AudioSegment = AudioSegment.from_file(input_file_path)
            audio.export(output_file_path, format="wav")
            print(f"Successfully converted to WAV: {output_file_path}")
            return output_file_path
        except Exception as e:
            print(f"Error converting audio to WAV: {e}")
            return ""

    def apply_noise_reduction(self, input_file_path: str, output_file_path: str) -> str:
        """
        Placeholder for a noise reduction function.

        Real noise reduction would involve more advanced audio processing
        libraries or machine learning models.

        Args:
            input_file_path: Path to the input audio file.
            output_file_path: Desired path for the output noise-reduced audio file.

        Returns:
            Path to the processed audio file, or an empty string on failure.
        """
        if not os.path.exists(input_file_path):
            print(f"Error: Input audio file for noise reduction not found at {input_file_path}")
            return ""

        print(f"Applying (simulated) noise reduction to: {input_file_path}")
        try:
            audio: AudioSegment = AudioSegment.from_file(input_file_path)
            audio.export(output_file_path, format=input_file_path.split(".")[-1])
            print(f"Noise reduction (simulated) complete. Output: {output_file_path}")
            return output_file_path
        except Exception as e:
            print(f"Error during simulated noise reduction: {e}")
            return ""


# Example usage
if __name__ == "__main__":
    print("--- Running AudioProcessor Example ---")
    processor = AudioProcessor()

    input_dir = "data/audio/input"
    output_dir = "data/audio/processed"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    dummy_mp3_path = os.path.join(input_dir, "test_input.mp3")
    dummy_wav_output_path = os.path.join(output_dir, "test_output.wav")
    noise_reduced_output_path = os.path.join(output_dir, "test_noise_reduced.mp3")

    try:
        silent_audio = AudioSegment.silent(duration=2000, frame_rate=16000)
        silent_audio.export(dummy_mp3_path, format="mp3")
        print(f"Created dummy MP3 for processing: {dummy_mp3_path}")
    except Exception as e:
        print(f"Could not create dummy MP3 (ensure 'pydub' and 'ffmpeg' are installed): {e}")
        dummy_mp3_path = None

    if dummy_mp3_path and os.path.exists(dummy_mp3_path):
        converted_file = processor.convert_to_wav(dummy_mp3_path, dummy_wav_output_path)
        if converted_file:
            print(f"Converted file: {converted_file}")

        processed_file = processor.apply_noise_reduction(dummy_mp3_path, noise_reduced_output_path)
        if processed_file:
            print(f"Noise-reduced (simulated) file: {processed_file}")
    else:
        print("\nSkipping AudioProcessor tests as dummy input file is not available.")

    print("\n--- AudioProcessor Example Finished ---")
