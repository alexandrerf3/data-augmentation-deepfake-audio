import argparse
import os
import random

from pathlib import Path
from voice_cloning_inferences import process_audios

def raffle(limit, ids):
    result = dict()
    for _id in ids:
        result[_id] = []

        ids_copy = ids.copy()
        ids_copy.remove(_id)
        for _ in range(limit):
            choice = random.choice(ids_copy)
            result[_id].append(choice)

            ids_copy.remove(choice)

    return result

def get_text_from_id(folder_path, file_id, file_type):
    with open(folder_path.joinpath(f"{file_id}.{file_type}"), "r") as file:
        data = file.read().rstrip()
    
    return data

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--ids_path", type=Path, required=True, help= \
        "File path with the IDs that will be used in generating new audios")
    parser.add_argument("--dataset_path", type=Path, default="nptel-pure", help= \
        "Path to the directory containing your NPTEL Pure Set dataset.")
    parser.add_argument("--limit", type=int, default=200, help= \
        "Limit of Repeats")
    parser.add_argument("--pure_folder_name", type=str, default="corrected_txt", help= \
        "Folder name with manually annotated transcripts")
    parser.add_argument("--audios_folder_name", type=str, default="wav", help= \
        "Folder name with the wav audio files")
    
    args = parser.parse_args()

    if(not os.path.exists(args.ids_path)):
        raise Exception("File path with the IDs don't exists")
    
    with open(args.ids_path, "r") as f:
        ids = f.read().split(",")

    chosen_IDs = raffle(args.limit, ids)

    dataset_path = args.dataset_path

    folder_names = os.listdir(dataset_path)
    file_types = [os.listdir(dataset_path.joinpath(folder_name))[0].split(".")[1] for folder_name in folder_names]
    folders = dict(zip(folder_names, file_types))

    for _id in chosen_IDs:
        for i in range(len(chosen_IDs[_id])):
            chosen_IDs[_id][i] = (get_text_from_id(
                dataset_path.joinpath(args.pure_folder_name),
                chosen_IDs[_id][i],
                folders[args.pure_folder_name]
            ), chosen_IDs[_id][i])

    process_audios(chosen_IDs, dataset_path.joinpath(args.audios_folder_name))