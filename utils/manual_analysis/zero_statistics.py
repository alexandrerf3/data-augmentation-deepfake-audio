import os

file_name = "zero_statistics.txt"
combinations = ["zero_sys_voc", "zero_sys", "sys_treinado_zero_voc", "sys_zero_voc"]

statistics = dict()
if(os.path.exists(file_name)):
    with open(file_name, "r") as f:
        content = f.readlines()
        f.close()

    for i in range(0, len(content)+1, (len(content)+1)//len(combinations)):
        combination = content[i].split(":")[0]
        good = int(content[i+1].split(":")[1].strip())
        reasonable = int(content[i+2].split(":")[1].strip())
        bad = int(content[i+3].split(":")[1].strip())

        statistics[combination] = {
            "good": good,
            "reasonable": reasonable,
            "bad": bad
        }
else:
    for combination in combinations:
        statistics[combination] = {
            "good": 0,
            "reasonable": 0,
            "bad": 0
        }

k = 0
mapper_op = {"G": "good", "R": "reasonable", "B": "bad"}
while True:
    lines = []
    for combination in combinations:
        lines.append(f"{combination}:\n")

        op = input(f"{combination} (G/R/B): ").upper()
        statistics[combination][mapper_op[op]] += 1

        for key in mapper_op:
            lines.append(f"- {mapper_op[key]}: {statistics[combination][mapper_op[key]]}\n")

        lines[-1] = f"{lines[-1]}\n"

    lines[-1] = lines[-1].strip()
    
    k += 1
    print("="*8 + str(k) + "="*8)

    with open(file_name, "w") as f:
        f.writelines(lines)
        f.close()
