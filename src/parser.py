import json
from pathlib import Path

INPUT_PATH = Path("./input/")
OUTPUT_PATH = Path("./output/")


def read_lines(content):
    json = {"lines": {}, "metadata": {}}

    line_idx = 0
    current_indent = 0
    current_branch_idx = None
    branch_stack = []
    last_line_idx = None

    while line_idx < len(content):
        print(current_indent)
        print(content[line_idx])
        line = content[line_idx]
        stripped_line = line.lstrip()

        if stripped_line.startswith("]"):
            current_indent = len(line) - len(stripped_line)
            json["lines"][str(last_line_idx)]["next"] = current_indent
        elif line[current_indent] == ("-"):
            json["lines"][str(line_idx)] = {
                "text": line[current_indent + 2 :],
                "next": ((line_idx + 1)),
            }
            last_line_idx = line_idx
        elif line[current_indent] == ("!"):
            # Branch
            current_indent += 4
            last_line_idx = line_idx
        elif line[current_indent] == (">"):
            current_indent += 4
            last_line_idx = line_idx
        line_idx += 1
    return json


def main():
    for file_path in INPUT_PATH.glob("*.sds"):
        json_dict = None
        with open(file_path, "r") as file:
            contents = file.readlines()
        json_dict = read_lines(contents)

        output_file = OUTPUT_PATH / (file_path.stem + ".json")

        with open(output_file, "w", encoding="utf-8") as out_file:
            json.dump(json_dict, out_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
