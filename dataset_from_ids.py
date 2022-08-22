import argparse
import os
import shutil

from pathlib import Path

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--dataset_path", type=Path, default="nptel-pure", help= \
        "Path to the directory containing your NPTEL Pure Set dataset.")
    parser.add_argument("--ids_path", type=Path, required=True, help= \
        "File path with the IDs that will be used to generate a folder with audios and texts from the dataset")
    
    args = parser.parse_args()

    if(not args.ids_path.exists()):
        raise Exception("File path with the IDs don't exists")

    with open(args.ids_path, "r") as f:
        ids = f.read().split(",")
    print(f"Total IDs that the folder will have: {len(ids)}")

    output_folder = f"dataset-{os.path.basename(os.path.normpath(args.ids_path)).split('.')[0]}"

    if(os.path.exists(output_folder)):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    os.mkdir(f"{output_folder}/data")

    for _id in ids:
        os.mkdir(f"{output_folder}/data/{_id}")
        os.mkdir(f"{output_folder}/data/{_id}/data")

        audio_file_name = f"{_id}.wav"
        text_file_name = f"{_id}.txt"

        audio_source_path = args.dataset_path / "wav" / audio_file_name
        text_source_path = args.dataset_path / "corrected_txt" / text_file_name

        audio_destination_path = f"{output_folder}/data/{_id}/data/{audio_file_name}"
        text_destination_path = f"{output_folder}/data/{_id}/data/{text_file_name}"

        shutil.copyfile(audio_source_path, audio_destination_path)
        shutil.copyfile(text_source_path, text_destination_path)

    print(f"Folder name with the audios and texts (in the LibriSpeech directory structure): {output_folder}")