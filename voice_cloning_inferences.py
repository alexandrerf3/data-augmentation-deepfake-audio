import torch
import os
import librosa
import numpy as np
import soundfile as sf
import sys
import shutil

from pathlib import Path

sys.path.append("Real-Time-Voice-Cloning")

from encoder import inference as encoder
from vocoder import inference as vocoder
from synthesizer.inference import Synthesizer

# Format of input:
# audios_with_texts = {filename_audio1: [(text1, id1), (text2, id2), (text3, id3)], filename_audio2: [(text1, id1), (text2, id2)]}
def process_audios(audios_with_texts, audios_folder_path):
    SEED = 37

    print(audios_folder_path)   

    if(torch.cuda.is_available()):
        device_id = torch.cuda.current_device()
        gpu_properties = torch.cuda.get_device_properties(device_id)
        ## Print some environment information (for debugging purposes)
        print("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
            "%.1fGb total memory.\n" %
            (torch.cuda.device_count(),
            device_id,
            gpu_properties.name,
            gpu_properties.major,
            gpu_properties.minor,
            gpu_properties.total_memory / 1e9))
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        print("Using CPU for inference.\n")

    torch.manual_seed(SEED)
    encoder.load_model(Path("Real-Time-Voice-Cloning/saved_models/zero_voc_sys_v2/encoder.pt"))
    synthesizer = Synthesizer(Path("Real-Time-Voice-Cloning/saved_models/zero_voc_sys_v2/synthesizer.pt"))
    vocoder.load_model(Path("Real-Time-Voice-Cloning/saved_models/zero_voc_sys_v2/vocoder.pt"))

    if(not os.path.exists("output")):
        os.mkdir("output")
    
    count = 1
    skiped = 0
    major_skips = 0
    for audio in audios_with_texts:
        print(f"\n{'='*10} {count} -- {audio} {'='*10}\n")

        try:
            audio_folder_path = f"output/{audio}"
            if(os.path.exists(audio_folder_path)):
                shutil.rmtree(audio_folder_path)
            os.mkdir(audio_folder_path)

            input_path = audios_folder_path.joinpath(f"{audio}.wav")
            original_wav, sampling_rate = librosa.load(str(input_path))
            preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)

            embed = encoder.embed_utterance(preprocessed_wav)

            samples = len(audios_with_texts[audio])
            for i in range(samples):
                try:
                    print(f"\n{i+1}/{samples} - {audios_with_texts[audio][i][1]}")

                    text = audios_with_texts[audio][i][0]
                    spec = synthesizer.synthesize_spectrograms([text], [embed])[0]

                    if(len(spec[0]) > 20):
                        generated_wav = vocoder.infer_waveform(spec)

                        # Trim excess silences to compensate for gaps in spectrograms (issue #53)
                        generated_wav = encoder.preprocess_wav(generated_wav)

                        # Salvando o arquivo no disco
                        filename = f"{audio_folder_path}/{audios_with_texts[audio][i][1]}.wav"
                        sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)
                    else:
                        skiped += 1
                except Exception as e:
                    print("="*20)
                    print(e)
                    print("="*20)

                    skiped += 1
        
            count += 1
            
            torch.cuda.empty_cache()
        except Exception as e:
            print("="*20)
            print(e)
            print("="*20)

            major_skips += 1
            skiped += len(audios_with_texts[audio])

    print(f"\n\n\n---> Skiped: {skiped}")
    print(f"---> Major skips: {major_skips}")