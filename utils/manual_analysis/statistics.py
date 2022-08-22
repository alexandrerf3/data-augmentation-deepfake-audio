import os

file_name = "statistics.txt"
combinations = ["padrão", "sys_voc_treinado", "sys_treinado", "sys_treinado_zero_voc", "sys_zero_voc"]

statistics = dict()
if(os.path.exists(file_name)):
    with open(file_name, "r") as f:
        content = f.readlines()
        f.close()

    for i in range(0, len(content)+1, (len(content)+1)//len(combinations)):
        combination = content[i].split(":")[0]
        good_long = int(content[i+2].split(":")[1].strip())
        good_default = int(content[i+3].split(":")[1].strip())
        reasonable_long = int(content[i+5].split(":")[1].strip())
        reasonable_default = int(content[i+6].split(":")[1].strip())
        bad_long = int(content[i+8].split(":")[1].strip())
        bad_default = int(content[i+9].split(":")[1].strip())

        statistics[combination] = {
            "good": {"long": good_long, "default": good_default},
            "reasonable": {"long": reasonable_long, "default": reasonable_default},
            "bad": {"long": bad_long, "default": bad_default}
        }
else:
    for combination in combinations:
        statistics[combination] = {
            "good": {"long": 0, "default": 0},
            "reasonable": {"long": 0, "default": 0},
            "bad": {"long": 0, "default": 0}
        }

k = 0
mapper_op = {"G": "good", "R": "reasonable", "B": "bad"}
mapper_size = {"L": "long", "D": "default"}
while True:
    lines = []
    for combination in combinations:
        lines.append(f"{combination}:\n")

        op = input(f"{combination} (G/R/B): ").upper()
        op_size = input(f"L/D: ").upper()
        statistics[combination][mapper_op[op]][mapper_size[op_size]] += 1

        for key in mapper_op:
            lines.append(f"- {mapper_op[key]}: {sum(statistics[combination][mapper_op[key]].values())}\n")

            for key_size in mapper_size:
                lines.append(f"- * {mapper_size[key_size]}: {statistics[combination][mapper_op[key]][mapper_size[key_size]]}\n")
        
        lines[-1] = f"{lines[-1]}\n"

    lines[-1] = lines[-1].strip()
    
    k += 1
    print("="*8 + str(k) + "="*8)

    with open(file_name, "w") as f:
        f.writelines(lines)
        f.close()
