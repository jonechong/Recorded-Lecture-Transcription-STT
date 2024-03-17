import os
from mutagen.mp3 import MP3


def find_longest_audio(directory):
    longest_duration = 0
    longest_file = None

    # Iterate through all files in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                # Construct the full path to the file
                file_path = os.path.join(root, file)
                try:
                    # Load the audio file metadata
                    audio = MP3(file_path)
                    # Check if this file is the longest so far
                    if audio.info.length > longest_duration:
                        longest_duration = audio.info.length
                        longest_file = file_path
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    # Convert seconds to minutes and seconds for easier reading
    longest_duration_mins = divmod(longest_duration, 60)
    return longest_file, longest_duration_mins


# Set your directory path here
directory_path = "path/to/your/audio/files"
longest_file, longest_duration = find_longest_audio(directory_path)
print(f"The longest audio file is: {longest_file}")
print(f"Duration: {longest_duration[0]} minutes and {longest_duration[1]:.2f} seconds")
