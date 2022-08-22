import os
import subprocess

from pathlib import Path
from librosa import get_duration

path = Path("../datasets/nptel-pure")
audios_folder_path = path / "wav"

audios = os.listdir(audios_folder_path)

total_duration = 0
for audio in audios:
    total_duration += get_duration(filename=(audios_folder_path / audio))

print(f"Número de trechos: {len(audios)}")
print(f"Duração média dos trechos: {total_duration / len(audios):.2f}s")
print(f"Total de minutos: {int(total_duration / 60)}mins")
print(f"Tamanho do conjunto: {subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')}")