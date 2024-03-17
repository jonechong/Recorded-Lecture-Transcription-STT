# This script aims to remove clips that is greatest than a certain duration, based on the params below.

import h5py
from tqdm import tqdm


def remove_long_clips(
    source_hdf5_path,
    destination_hdf5_path,
    max_duration=8.0,
    sampling_rate=16000,
    hop_length=512,
):
    with h5py.File(source_hdf5_path, "r") as source_hdf5, h5py.File(
        destination_hdf5_path, "w"
    ) as dest_hdf5:
        # Wrap source_hdf5.keys() with tqdm for progress bar
        for clip_name in tqdm(source_hdf5.keys(), desc="Filtering clips"):
            grp = source_hdf5[clip_name]
            if "mfccs" in grp:
                mfccs = grp["mfccs"]
                # Calculate the duration of the clip from the MFCC shape
                clip_duration = mfccs.shape[1] * hop_length / sampling_rate
                if clip_duration <= max_duration:
                    # Copy the group if the duration is within the limit
                    dest_grp = dest_hdf5.create_group(clip_name)
                    for dataset_name in grp.keys():
                        data = grp[dataset_name][()]
                        dest_grp.create_dataset(dataset_name, data=data)


if __name__ == "__main__":
    source_hdf5_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\STT\Recorded-Lecture-Transcription-STT\processed_dataset (mfccs only).h5"
    destination_hdf5_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\STT\Recorded-Lecture-Transcription-STT\reduced_mfcc_dataset.h5"

    # Adjust these parameters as needed
    max_duration = 8.0  # seconds
    sampling_rate = 16000  # Hz, ensure this matches your original preprocessing
    hop_length = 512  # frames, ensure this matches your original preprocessing

    remove_long_clips(
        source_hdf5_path, destination_hdf5_path, max_duration, sampling_rate, hop_length
    )

    print(
        f"Clips longer than {max_duration} seconds have been removed. Processed dataset saved to: {destination_hdf5_path}"
    )
