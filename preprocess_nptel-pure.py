import argparse
import os
import random

from pathlib import Path
from tqdm import tqdm

def create_portions(ids, number_of_portions, portions_size):
    portions = [[] for _ in range(number_of_portions)]
    ids_copy = ids.copy()

    for i in range(number_of_portions - 1):
        for _ in range(portions_size[i]):
            choice = random.choice(ids_copy)
            portions[i].append(choice)

            ids_copy.remove(choice)
    
    portions[number_of_portions - 1] = list(set(ids_copy))

    return portions

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--dataset_path", type=Path, default="nptel-pure", help= \
        "Path to the directory containing your NPTEL Pure Set dataset.")
    parser.add_argument("--portions", type=int, default=2, help= \
        "Number of portions")
    parser.add_argument("--portions_size", type=list, nargs="+", default=[500, 500], help= \
        "Portion sizes, respectively")
    
    args = parser.parse_args()

    portions_size = args.portions_size
    if(portions_size != [500, 500]):
        portions_size = [int("".join(portion_size)) for portion_size in portions_size]

    if(args.portions != len(portions_size)):
        raise Exception("The amount of portions sizes is not equal to the number of portions")

    dataset_path = args.dataset_path

    folder_names = os.listdir(dataset_path)
    file_types = [os.listdir(dataset_path.joinpath(folder_name))[0].split(".")[1] for folder_name in folder_names]
    folders = dict(zip(folder_names, file_types))

    files = os.listdir(dataset_path.joinpath(folder_names[0]))
    names = [fil.split(".")[0] for fil in files]

    deleted_audios = []
    ids = []
    names_set = set(names)
    for i in tqdm(range(len(names))):
        _id = f"id{str(i+1).zfill(4)}"

        if(not f"{_id}" in names_set):
            for folder_name in folder_names:
                os.rename(
                    dataset_path.joinpath(folder_name, f"{names[i]}.{folders[folder_name]}"),
                    dataset_path.joinpath(folder_name, f"{_id}.{folders[folder_name]}"))

        with open(str(dataset_path / "corrected_txt" / f"{_id}.txt"), "r") as f:
            transcript = f.read()
        
        if(transcript == ""):
            for folder_name in folder_names:
                os.remove(dataset_path / folder_name / f"{_id}.{folders[folder_name]}")

            deleted_audios.append(_id)
        else:
            wav_path = dataset_path.joinpath("wav", f"{_id}.{folders['wav']}")
            post_filter = "anlmdn=s=0.0001:p=0.01:m=15,dynaudnorm=p=0.5:s=5,highpass=f=100"
            os.system(f"ffmpeg-normalize {wav_path} -lrt 20 -pof '{post_filter}' -o {wav_path} -f -ar 16000")

            ids.append(_id)

    if((len(ids) + len(deleted_audios)) != sum(portions_size)):
        raise Exception("The sum of the amounts of the portions is not equal to the amount of speech files")

    print(f"Amount of deleted audios: {len(deleted_audios)}")
    print(f"Deleted audios: {' '.join(deleted_audios)}")

    portions = create_portions(ids, args.portions, portions_size)

    for i in range(len(portions)):
        with open(f"{i+1}_{len(portions[i])}-ids.txt", "w") as f:
            f.write(",".join(portions[i]))