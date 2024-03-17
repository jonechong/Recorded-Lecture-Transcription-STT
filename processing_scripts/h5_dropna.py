# This script drops any datapoints where any of the 4 features (MFCCs, Spectrogram, ZCR or Spectral Centroid) are missing.
import h5py
from tqdm import tqdm


def clean_datasets_missing_features(hdf5_path, required_features):
    """
    Removes datasets from the HDF5 file if they are missing any of the required features.

    Parameters:
    - hdf5_path (str): Path to the HDF5 file.
    - required_features (list of str): List of feature names that must be present.
    """
    with h5py.File(hdf5_path, "a") as file:
        keys_to_delete = []  # Track keys of the groups to delete.

        # Iterate through each group in the HDF5 file.
        for key in tqdm(file.keys(), desc="Checking datasets"):
            group = file[key]
            # Check if any required feature is missing in the current group.
            if any(feature not in group for feature in required_features):
                keys_to_delete.append(key)

        # Delete the groups missing any required features.
        for key in keys_to_delete:
            del file[key]
            print(f"Deleted dataset {key} due to missing features.")


# Define the path to your HDF5 file and the list of required features.
hdf5_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\STT\Recorded-Lecture-Transcription-STT\processed_dataset.h5"
required_features = ["mfccs", "zcr", "spectral_centroid", "melspectrogram"]

# Execute the cleaning process.
clean_datasets_missing_features(hdf5_path, required_features)
