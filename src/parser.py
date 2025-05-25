import json
import re
from pathlib import Path
import time

INPUT_PATH = Path("./input/")
OUTPUT_PATH = Path("./output/")


def parse_variables(content):
    pattern = re.compile(r"\$(\w+)\s*=\s*(.+)")
    var_dict = {}
    line_idx = 0

    while not content[line_idx].startswith("]"):
        line = content[line_idx].strip()

        match = pattern.match(line)
        if match:
            key = match.group(1)
            val = match.group(2)

            if val.startswith('"') and val.endswith('"'):
                var_dict[key] = val[1:-1]
            else:
                var_dict[key] = int(val)
        line_idx += 1

    return content[line_idx + 1 :], var_dict


def parse_modules(content):
    modules = {}
    for i, line in enumerate(content):
        line = line.strip()

        if line.startswith("#"):
            modules[line[2:]] = i - 2

    return modules


def parse_dialogue(content, vars, modules):
    json = {"lines": {}, "metadata": {}}
    current_line = 0
    last_branch = []
    branch_depth = 0

    while not content[current_line].startswith("FIN"):
        line = content[current_line].strip()

        try:
            match line[0]:
                case "-":
                    json["lines"][str(current_line)] = {
                        "text": line[2:],
                        "next": current_line + 1,
                    }
                case "!":
                    last_branch.append(current_line)
                    branch_depth += 1
                    json["lines"][str(current_line)] = {
                        "text": line[2:-2],
                        "options": [],
                    }
                case ">":
                    if last_branch:
                        json["lines"][str(last_branch[-1])]["options"].append(
                            current_line
                        )
                        json["lines"][str(current_line)] = {
                            "text": line[2:],
                            "next": current_line + 1,
                        }
                    else:
                        print("No branch initializer found when there should be one!")
                case "=":
                    next_line = int(modules[line[3:]])
                    json["lines"][str(current_line - 1)]["next"] = next_line + 1
                case "]":
                    branch_depth -= 1
            current_line += 1
        except:
            current_line += 1

        last_branch = last_branch[:branch_depth]
        print(current_line - 1, content[current_line - 1])

    json["lines"][str(current_line - 1)]["next"] = -1
    return json


def main():
    start_time = time.time()
    for file_path in INPUT_PATH.glob("*.sds"):
        with open(file_path, "r") as file:
            content = file.readlines()

        variable_dict, file_dialogue = None, None
        if content[0].startswith("def"):
            file_dialogue, variable_dict = parse_variables(content[1:])

        modules = parse_modules(file_dialogue)

        json_dict = parse_dialogue(file_dialogue[2:], variable_dict, modules)

        output_file = OUTPUT_PATH / (file_path.stem + ".json")
        with open(output_file, "w", encoding="utf-8") as out_file:
            json.dump(json_dict, out_file, indent=4, ensure_ascii=False)
    end_time = time.time()
    print(f"Parsed the dialogues in : {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
