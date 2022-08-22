import os

folders = ["v1/test_original", "v1/test_zero_voc_sys", "v1/test_zero_voc_sys_v2"]

folder_id = input("Folder ID: ").zfill(4)

first_folder_path = f"{folders[0]}/id{folder_id}"

files = sorted(os.listdir(first_folder_path), reverse=True)

lines = []
for f in files:
    lines.append("window\n")
    for folder in folders:
        lines.append(f"file \"{folder}/id{folder_id}/{f}\"\n")

with open("audacity_files.lof", "w") as f:
    f.writelines(lines)
    f.close()

os.system("audacity audacity_files.lof")
