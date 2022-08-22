import argparse
import os
import random

from pathlib import Path
from librosa import get_duration

from create_csv_file import create_csv

def get_audio_path(root_folder, audio_id):
    audio_folder, audio_file_name = audio_id.split("_")

    audio_path = root_folder / audio_folder / f"{audio_file_name}.wav"

    return audio_path, audio_file_name

"""
This function discards generated audios that have a larger gap size AND gap size percentage than the
original audio of the transcript used to generate them.
- gap_size: Duration that the audio must be longer than the original to be discarded.
- gap_size_percentage: Duration (in percentage) that the audio must be longer than the original to be discarded.
"""
def discard_audios(ids, gap_size, gap_size_percentage, audios_folder, dataset_path):
    ids_copy = ids.copy()

    count = 0
    discarded_audios = [f"Total amount of audios: {len(ids)}\n", f"Gap size: {gap_size}s\n", f"Gap size (in percentage): {gap_size_percentage}%\n\n\n"]
    for _id in ids:
        generated_audio_path, audio_file_name = get_audio_path(audios_folder, _id)
        original_audio_path = dataset_path / "wav" / f"{audio_file_name}.wav"

        generated_audio_duration = get_duration(filename=generated_audio_path)
        original_audio_duration = get_duration(filename=original_audio_path)

        if((generated_audio_duration - original_audio_duration) >= gap_size and generated_audio_duration > (original_audio_duration * (gap_size_percentage / 100 + 1))):
            ids_copy.remove(_id)
            discarded_audios.append(f"--> {_id}\n")
            discarded_audios.append(f"Original audio duration: {original_audio_duration}\n")
            discarded_audios.append(f"Generated audio duration: {generated_audio_duration}\n\n")
            count += 1

    discarded_audios.append(f"{'='*25}\n")
    discarded_audios.append(f"Discarded audios: {count}\n")
    discarded_audios.append("="*25)

    with open("discarded_audios.txt", "w") as f:
        f.writelines(discarded_audios)
        f.close()

    print(f"Discarded audios: {count}")

    return ids_copy

def get_random_IDs(ids, amount):
    ids_copy = ids.copy()

    result = []
    for i in range(amount):
        choice = random.choice(ids_copy)
        result.append(choice)

        ids_copy.remove(choice)

    return ids_copy, result

def get_audio_and_transcript_files_path(ids, audios_folder, dataset_path):
    audio_files_path = []
    transcript_files_path = []
    for _id in ids:
        audio_file_path, audio_file_name = get_audio_path(audios_folder, _id)

        audio_files_path.append(audio_file_path)
        transcript_files_path.append(dataset_path / "corrected_txt" / f"{audio_file_name}.txt")

    return audio_files_path, transcript_files_path

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--audios_folder", type=Path, required=True, help= \
        "Path to the directory that contains the audio folders that will be used during training.")
    parser.add_argument("--dataset_path", type=Path, default="nptel-pure", help= \
        "Path to the directory containing your NPTEL Pure Set dataset.")        
    parser.add_argument("--amount_dev", type=int, default=500, help= \
        "Amount of files the development CSV file will have")

    args = parser.parse_args()

    dataset_path = args.dataset_path
    if(not os.path.exists(dataset_path)):
        raise Exception("Path to directory containing NPTEL Pure Set dataset does not exist")

    audios_folder = args.audios_folder
    folders = os.listdir(audios_folder)

    ids = []
    for folder in folders:
        audio_files = os.listdir(f"{audios_folder}/{folder}")

        ids.extend([f"{folder}_{audio_file.split('.')[0]}" for audio_file in audio_files])

    amount_dev = args.amount_dev
    if(len(ids) <= amount_dev):
        raise Exception("The amount of files for development is greater than or equal to the total amount of audio files")

    ids = discard_audios(ids, 5, 50, audios_folder, dataset_path)

    ids, dev = get_random_IDs(ids, amount_dev)
    dev_audio_files_path, dev_transcript_files_path = get_audio_and_transcript_files_path(dev, audios_folder, dataset_path)
    create_csv(dev_audio_files_path, dev_transcript_files_path, "dev", dataset_path)

    print(f"Amount of audio files in development CSV file: {len(dev)}")

    _, train = get_random_IDs(ids, len(ids))
    train_audio_files_path, train_transcript_files_path = get_audio_and_transcript_files_path(train, audios_folder, dataset_path)
    create_csv(train_audio_files_path, train_transcript_files_path, "train", dataset_path)

    print(f"Amount of audio files in train CSV file: {len(train)}")