import os
from mutagen.mp3 import MP3
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def analyze_audio_lengths(directory):
    lengths = []
    # Prepare a list of all MP3 files
    mp3_files = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(directory)
        for file in files if file.endswith(".mp3")
    ]

    # Use tqdm to wrap around the loop for a progress bar
    for file_path in tqdm(mp3_files, desc="Analyzing audio files"):
        try:
            # Load the audio file metadata
            audio = MP3(file_path)
            # Append the length of the audio file in seconds
            lengths.append(audio.info.length)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    return lengths

def plot_length_distribution(lengths):
    # Filter lengths to include only those less than 150 seconds
    filtered_lengths = [length for length in lengths if length <= 150]
    
    # Plot the distribution of audio lengths
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_lengths, bins=100, color="blue", alpha=0.7, edgecolor="black")
    plt.title("Distribution of Audio File Lengths (<= 150s)")
    plt.xlabel("Length in Seconds")
    plt.ylabel("Number of Files")
    plt.grid(True)
    plt.show()

def print_percentiles(lengths):
    # Filter lengths to include only those less than 150 seconds
    filtered_lengths = [length for length in lengths if length <= 150]
    
    # Print selected percentiles to understand the distribution
    percentiles = [50, 75, 85, 90, 95]
    for p in percentiles:
        value = np.percentile(filtered_lengths, p)
        print(f"{p}th percentile: {value:.2f} seconds")

# Set your directory path here
directory_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\Voice dataset\cv-corpus-4\clips"
lengths = analyze_audio_lengths(directory_path)

# Filter and plot the distribution of lengths for clips <= 150s
plot_length_distribution(lengths)

# Print percentiles for clips <= 150s
print_percentiles(lengths)
