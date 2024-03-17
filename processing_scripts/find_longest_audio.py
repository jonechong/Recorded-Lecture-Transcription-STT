import os
from mutagen.mp3 import MP3
from tqdm import tqdm

def find_longest_audio(directory):
    longest_duration = 0
    longest_file = None

    # Prepare a list of all MP3 files
    mp3_files = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(directory)
        for file in files if file.endswith(".mp3")
    ]

    # Iterate through all MP3 files with a progress bar
    for file_path in tqdm(mp3_files, desc="Processing audio files"):
        try:
            # Load the audio file metadata
            audio = MP3(file_path)
            # Check if this file is the longest so far
            if audio.info.length > longest_duration:
                longest_duration = audio.info.length
                longest_file = file_path
                # Log the update of the longest file
                print(f"New longest file: {file_path} with duration: {audio.info.length} seconds")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # Convert seconds to minutes and seconds for easier reading
    longest_duration_mins = divmod(longest_duration, 60)
    return longest_file, longest_duration_mins

# Set your directory path here
directory_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\Voice dataset\cv-corpus-4\clips"
longest_file, longest_duration = find_longest_audio(directory_path)
print(f"The longest audio file is: {longest_file}")
print(f"Duration: {longest_duration[0]} minutes and {longest_duration[1]:.2f} seconds")
