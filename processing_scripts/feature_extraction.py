import librosa
import os
import h5py
import numpy as np
import pandas as pd
from tqdm import tqdm

# Rename paths accordingly

## Creation of Labels

####################################################################
# import re
# import inflect

# # Define the path to the folder containing your TSV files
# folder_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\Voice dataset\cv-corpus-4"

# # List of the TSV files you want to combine
# tsv_files = [
#     "dev.tsv",
#     "invalidated.tsv",
#     "other.tsv",
#     "test.tsv",
#     "train.tsv",
#     "validated.tsv",
# ]

# # Initialize an empty DataFrame to hold the combined data
# combined_df = pd.DataFrame()

# # Iterate over each file and append its contents to the combined DataFrame
# for file_name in tsv_files:
#     file_path = os.path.join(folder_path, file_name)
#     temp_df = pd.read_csv(file_path, sep="\t")
#     combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

# # Drop unnecessary columns
# combined_df.drop(
#     ["client_id", "up_votes", "down_votes", "age", "gender", "accent"],
#     axis=1,
#     inplace=True,
# )

# # Initialize the inflect engine
# p = inflect.engine()


# def normalize_text(text):
#     # Check if the input is not a string (e.g., NaN or None)
#     if not isinstance(text, str):
#         return ""  # or some placeholder text, e.g., "missing_sentence"

#     # Convert numbers to words
#     text = re.sub(r"\b\d+\b", lambda x: p.number_to_words(x.group()), text)

#     # Convert to lowercase
#     text = text.lower()

#     # Keep only spaces, lowercase letters, and numbers in word form
#     text = re.sub(r"[^a-z ]", "", text)

#     return text


# # Apply normalization including the check for non-string types
# combined_df["sentence"] = combined_df["sentence"].apply(normalize_text)

# # Proceed with saving the normalized labels as before
# combined_csv_path = os.path.join(folder_path, "labels.csv")


#####################################################################

## Feature Extraction


#####################################################################
def load_labels(label_file_path):
    labels_df = pd.read_csv(label_file_path)
    # Ensure that the 'path' column is the index and 'sentence' is the value
    labels_dict = pd.Series(labels_df.sentence.values, index=labels_df.path).to_dict()
    return labels_dict


def process_audio_file(
    filename, folder_path, hdf5_file, labels_dict, sampling_rate, hop_length, n_mfcc
):
    if not isinstance(labels_dict.get(filename, None), str):
        return False

    file_path = os.path.join(folder_path, filename)
    signal, _ = None, None

    # Reference or create the group for the file
    grp = (
        hdf5_file.get(filename)
        if filename in hdf5_file
        else hdf5_file.create_group(filename)
    )

    # Determine if we need to load the audio file by checking if any feature is missing
    need_to_load_signal = any(
        feature not in grp
        for feature in ["mfccs", "zcr", "spectral_centroid", "melspectrogram"]
    )

    if need_to_load_signal:
        try:
            signal, _ = librosa.load(file_path, sr=sampling_rate)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return False

    # Process and store each feature if it's not already in the group
    if "mfccs" not in grp:
        try:
            mfccs = librosa.feature.mfcc(
                y=signal, sr=sampling_rate, n_mfcc=n_mfcc, hop_length=hop_length
            )
            grp.create_dataset("mfccs", data=mfccs)
        except Exception as e:
            print(f"Error computing MFCCs for {filename}: {e}")

    if "zcr" not in grp:
        try:
            zcr = librosa.feature.zero_crossing_rate(y=signal, hop_length=hop_length)
            grp.create_dataset("zcr", data=zcr)
        except Exception as e:
            print(f"Error computing ZCR for {filename}: {e}")

    if "spectral_centroid" not in grp:
        try:
            spectral_centroid = librosa.feature.spectral_centroid(
                y=signal, sr=sampling_rate, hop_length=hop_length
            )
            grp.create_dataset("spectral_centroid", data=spectral_centroid)
        except Exception as e:
            print(f"Error computing Spectral Centroid for {filename}: {e}")

    if "melspectrogram" not in grp:
        try:
            melspectrogram = librosa.feature.melspectrogram(
                y=signal,
                sr=sampling_rate,
                n_fft=2048,
                hop_length=hop_length,
                n_mels=128,
            )
            melspectrogram_db = librosa.power_to_db(melspectrogram, ref=np.max)
            grp.create_dataset("melspectrogram", data=melspectrogram_db)
        except Exception as e:
            print(f"Error computing mel-spectrogram for {filename}: {e}")

    # Store the label if it's not already there
    if "label" not in grp:
        label_data = labels_dict[filename].encode("utf-8")
        grp.create_dataset("label", data=label_data)

    return True


def process_files(
    folder_path, hdf5_path, labels_dict, sampling_rate=16000, hop_length=512, n_mfcc=13
):
    processed_files = 0
    updated_files = 0  # Keep track of files updated with missing features
    skipped_files = 0

    with h5py.File(hdf5_path, "a") as hdf5_file:
        for filename in tqdm(os.listdir(folder_path), desc="Processing files"):
            if filename.endswith(".mp3"):
                success = process_audio_file(
                    filename,
                    folder_path,
                    hdf5_file,
                    labels_dict,
                    sampling_rate,
                    hop_length,
                    n_mfcc,
                )
                if success:
                    if filename in hdf5_file:
                        updated_files += 1
                    else:
                        processed_files += 1
                else:
                    skipped_files += 1

    print(f"Processed {processed_files} new files.")
    print(f"Updated {updated_files} files with missing features.")
    print(f"Skipped {skipped_files} files.")


# change source and destination names accordingly
if __name__ == "__main__":
    folder_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\Voice dataset\cv-corpus-4\clips"
    hdf5_path = "processed_dataset.h5"
    label_file_path = (
        r"C:\Users\jonec\Documents\SUTD\T6\AI\Voice dataset\cv-corpus-4\labels.csv"
    )
    labels_dict = load_labels(label_file_path)

    process_files(folder_path, hdf5_path, labels_dict)
