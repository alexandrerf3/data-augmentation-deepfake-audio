import argparse
import os

from pathlib import Path

def format_transcript(transcript):
    transcript = transcript.lower()
    transcript = transcript.replace("\t", " ")

    new_transcript = ""
    for i in range(len(transcript)):
        if(transcript[i] == "1"):
            if((i-1) >= 0 and transcript[i-1] != " "):
                new_transcript += " "
            
            new_transcript += "one"

            if((i+1) < len(transcript) and transcript[i+1] != " "):
                new_transcript += " "
        elif(transcript[i] == "2"):
            if((i-1) >= 0 and transcript[i-1] != " "):
                new_transcript += " "
            
            new_transcript += "two"

            if((i+1) < len(transcript) and transcript[i+1] != " "):
                new_transcript += " "
        else:
            new_transcript += transcript[i]
    
    return new_transcript

def create_csv(audio_files_path, transcript_files_path, file_name, dataset_path):
    if(len(audio_files_path) != len(transcript_files_path)):
        raise Exception("The amount of audio files path must be equal to the amount of transcript files path, keeping the same order.")

    csv = "wav_filename,wav_filesize,transcript"
    for i in range(len(audio_files_path)):
        audio_size_in_bytes = os.path.getsize(audio_files_path[i])

        with open(str(transcript_files_path[i]), "r") as tf:
            transcript = tf.read()

        transcript = format_transcript(transcript)
        
        csv += f"\n{audio_files_path[i]},{audio_size_in_bytes},{transcript}"

    with open(f"{file_name}.csv", "w") as f_csv:
        f_csv.write(csv)
        f_csv.close()

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--ids_path", type=Path, required=True, help= \
        "File path with the IDs that will be used to generate the CSV file")
    parser.add_argument("--file_name", type=str, required=True, help= \
        "Name of the CSV file that will be created")
    parser.add_argument("--dataset_path", type=Path, default="nptel-pure", help= \
        "Path to the directory containing your NPTEL Pure Set dataset.")

    args = parser.parse_args()

    dataset_path = args.dataset_path
    if(not os.path.exists(dataset_path)):
        raise Exception("Path to directory containing NPTEL Pure Set dataset does not exist")

    if(not os.path.exists(args.ids_path)):
        raise Exception("File path with the IDs don't exists")

    with open(args.ids_path, "r") as f:
        ids = f.read().split(",")

    audio_files_path = []
    transcript_files_path = []
    for _id in ids:
        audio_files_path.append(dataset_path / "wav" / f"{_id}.wav")
        transcript_files_path.append(dataset_path / "corrected_txt" / f"{_id}.txt")
    
    create_csv(audio_files_path, transcript_files_path, args.file_name, dataset_path)