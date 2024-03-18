# This script aims to split a large h5 file into a specified number of sets. The default number of parts is 10.

import h5py
import os
from tqdm import tqdm
import numpy as np

def split_hdf5_file(original_hdf5_path, parts=10):
    with h5py.File(original_hdf5_path, 'r') as original_hdf5:
        keys = list(original_hdf5.keys())
        total_keys = len(keys)
        keys_per_part = np.ceil(total_keys / parts).astype(int)

        for part in range(parts):
            start_index = part * keys_per_part
            end_index = min((part + 1) * keys_per_part, total_keys)
            part_keys = keys[start_index:end_index]

            part_file_name = f"{os.path.splitext(original_hdf5_path)[0]}_{part + 1}.h5"
            with h5py.File(part_file_name, 'w') as part_hdf5:
                for key in tqdm(part_keys, desc=f"Writing {part_file_name}"):
                    grp = original_hdf5[key]
                    dest_grp = part_hdf5.create_group(key)
                    for dataset_name in grp.keys():
                        data = grp[dataset_name][()]
                        dest_grp.create_dataset(dataset_name, data=data)
            print(f"Part {part + 1} saved as {part_file_name}")

if __name__ == "__main__":
    original_hdf5_path = r"C:\Users\jonec\Documents\SUTD\T6\AI\STT\Recorded-Lecture-Transcription-STT\reduced_mfcc_dataset.h5"
    split_hdf5_file(original_hdf5_path)
