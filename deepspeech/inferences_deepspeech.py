import argparse
import time
import numpy as np
import os
import wave
import subprocess
import shlex
import jiwer

from tqdm import tqdm
from deepspeech import Model
from pathlib import Path

def convert_sample_rate(audio_path, desired_sample_rate):
    sox_cmd = f"sox '{audio_path}' --type raw --bits 16 --channels 1 --rate {desired_sample_rate} --encoding signed-integer --endian little --compression 0.0 --no-dither - "

    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"SoX returned non-zero status: {e.stderr}")
    except OSError as e:
        raise OSError(e.errno, f"SoX not found, use {desired_sample_rate}hz files or install it: {e.strerror}")

    return np.frombuffer(output, np.int16)

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--model", required=True, help="Path to the model")
    parser.add_argument("--scorer", required=True, help="Path to the external scorer file")
    parser.add_argument("--test_csv", type=Path, required=True, help= \
        "Path to test CSV file that will be used in inference")
    
    args = parser.parse_args()

    if(not os.path.exists(args.test_csv)):
        raise Exception("Path to CSV file don't exists")

    print(f"Loading model from path {args.model}")

    model_load_start = time.time()
    ds = Model(args.model)
    model_load_end = time.time()

    print(f"Loaded model in {model_load_end - model_load_start:.3}s.")

    print(f"Loading scorer from path {args.scorer}")

    scorer_load_start = time.time()
    ds.enableExternalScorer(args.scorer)
    scorer_load_end = time.time()

    print(f"Loaded scorer in {scorer_load_end - scorer_load_start:.3}s.")

    desired_sample_rate = ds.sampleRate()

    with open(args.test_csv, "r") as f:
        tests = f.readlines()[1:]

    pbar = tqdm(total=len(tests))

    ground_truths = []
    deepspeech_outputs = []
    for test in tests:
        audio_file_path, _, transcript = test.split(",")

        wr_audio = wave.open(audio_file_path, "rb")

        sample_rate = wr_audio.getframerate()
        if(sample_rate != desired_sample_rate):
            print(f"Warning: original sample rate ({sample_rate}) is different than {desired_sample_rate}hz." \
                " Resampling might produce erratic speech recognition.")
            
            audio = convert_sample_rate(audio_file_path, desired_sample_rate)
        else:
            audio = np.frombuffer(wr_audio.readframes(wr_audio.getnframes()), np.int16)

        audio_length = wr_audio.getnframes() * (1/sample_rate)
        wr_audio.close()

        print(f"Running inference for audio: {os.path.basename(os.path.normpath(audio_file_path))}")

        inference_start = time.time()
        deepspeech_outputs.append(ds.stt(audio))
        inference_end = time.time()

        print(f"Inference took {inference_end - inference_start:.3}s for {audio_length:.3}s audio file.")

        ground_truths.append(transcript.strip())

        pbar.update()

    pbar.close()

    wer = jiwer.wer(ground_truths, deepspeech_outputs)
    cer = jiwer.cer(ground_truths, deepspeech_outputs)

    print(f"WER: {wer:.3f}")
    print(f"CER: {cer:.3f}")