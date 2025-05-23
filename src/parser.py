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

    while line_idx < len(content):
        print(current_indent)
        line = content[line_idx]

        if line[current_indent] == ("-"):
            json["lines"][str(line_idx)] = {
                "text": line[current_indent + 2 :],
                # Assume no branch for now
                "next": ((line_idx + 1)),
            }
            pass
        elif line[current_indent] == ("!"):
            # Branch
            # First detect where this branch ends, if it ends
            temp_line_idx = line_idx
            while temp_line_idx < len(content):
                if content[temp_line_idx][current_indent] == "-":
                    current_branch_idx = temp_line_idx

                    # Update the previous lines next jump point
                    json["lines"][str(line_idx - 1)]["next"] = current_branch_idx
                    break
                temp_line_idx += 1

            current_indent += 4
        elif line[current_indent] == (">"):
            current_indent += 4
        else:
            current_indent -= 4
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
