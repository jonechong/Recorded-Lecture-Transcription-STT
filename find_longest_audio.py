import os
from pydub import AudioSegment


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
                    # Load the audio file
                    audio = AudioSegment.from_file(file_path)
                    # Check if this file is the longest so far
                    if len(audio) > longest_duration:
                        longest_duration = len(audio)
                        longest_file = file_path
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    # Convert milliseconds to minutes and seconds for easier reading
    longest_duration_mins = divmod(longest_duration // 1000, 60)
    return longest_file, longest_duration_mins


# Set your directory path here
directory_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\Voice dataset\cv-corpus-4\clips"
longest_file, longest_duration = find_longest_audio(directory_path)
print(f"The longest audio file is: {longest_file}")
print(f"Duration: {longest_duration[0]} minutes and {longest_duration[1]} seconds")
