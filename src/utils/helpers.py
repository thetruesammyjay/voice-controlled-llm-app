import os
import datetime

def generate_timestamped_filename(prefix: str = "file", extension: str = "tmp") -> str:
    """
    Generates a unique filename using a timestamp.

    Args:
        prefix (str): A prefix for the filename (e.g., "audio_rec").
        extension (str): The file extension (e.g., "wav", "mp3").

    Returns:
        str: A timestamped filename.
    """
    timestamp = int(datetime.datetime.now().timestamp() * 1000) # Millisecond precision
    return f"{prefix}_{timestamp}.{extension}"

def ensure_directory_exists(path: str):
    """
    Ensures that a given directory path exists. If it doesn't, it creates it.

    Args:
        path (str): The directory path to check and create.
    """
    try:
        os.makedirs(path, exist_ok=True)
        # print(f"Ensured directory exists: {path}") # Uncomment for verbose
    except OSError as e:
        print(f"Error creating directory {path}: {e}")

# Example usage
if __name__ == "__main__":
    print("--- Running Helpers Example ---")

    # Test timestamped filename generation
    filename = generate_timestamped_filename("recording", "wav")
    print(f"Generated filename: {filename}")

    filename_mp3 = generate_timestamped_filename(extension="mp3")
    print(f"Generated default filename: {filename_mp3}")

    # Test directory creation
    test_dir = "temp_test_dir_12345"
    ensure_directory_exists(test_dir)
    print(f"Checked/created directory: {test_dir}")
    if os.path.exists(test_dir):
        print("Directory exists.")
        os.rmdir(test_dir) # Clean up
        print(f"Cleaned up {test_dir}")
    else:
        print("Directory does not exist (error?).")

    # Test with nested directory
    nested_test_dir = os.path.join("temp_parent", "temp_child", "temp_grandchild")
    ensure_directory_exists(nested_test_dir)
    print(f"Checked/created nested directory: {nested_test_dir}")
    if os.path.exists(nested_test_dir):
        print("Nested directory exists.")
        # Clean up parent directory
        import shutil
        shutil.rmtree("temp_parent")
        print(f"Cleaned up temp_parent and its contents.")

    print("--- Helpers Example Finished ---")
