import json
import re
from pathlib import Path

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
                var_dict[key] = val
            else:
                var_dict[key] = int(val)
        line_idx += 1

    return content[line_idx + 1 :], var_dict


def parse_modules(content):
    modules = {}
    for i, line in enumerate(content):
        line = line.strip()

        if line.startswith("#"):
            modules[line[2:]] = i + 1

    return modules


def main():
    for file_path in INPUT_PATH.glob("*.sds"):
        with open(file_path, "r") as file:
            content = file.readlines()

        variable_dict, file_dialogue = None, None
        if content[0].startswith("def"):
            file_dialogue, variable_dict = parse_variables(content[1:])

        modules = parse_modules(file_dialogue)

        print(variable_dict)
        print(modules)
        # output_file = OUTPUT_PATH / (file_path.stem + ".json")

        # with open(output_file, "w", encoding="utf-8") as out_file:
        #     json.dump(json_dict, out_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
