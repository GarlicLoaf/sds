import json
from pathlib import Path

INPUT_PATH = Path("./input/")
OUTPUT_PATH = Path("./output/")


def read_lines(content, read_idx):
    json = {}
    last_exclamation = None
    choice = 0
    line_counter = 0

    while read_idx < len(content):
        line = content[read_idx].strip()
        if line.startswith("-"):
            # standard output
            json["line_" + str(line_counter)] = {"type": 0, "text": line[2:]}
            read_idx += 1
            line_counter += 1
        elif line.startswith("!"):
            # branch
            choice = 0
            last_exclamation = line_counter
            json["line_" + str(line_counter)] = {
                "type": 1,
                "text": line[2:],
                "answers": [],
                "branches": {},
            }
            read_idx += 1
            line_counter += 1
        elif line.startswith(">"):
            # decision
            json["line_" + str(last_exclamation)]["answers"].append(line[2:-2])
            branch_json, new_read_idx = read_lines(content, read_idx + 1)
            json["line_" + str(last_exclamation)]["branches"][str(choice)] = branch_json
            choice += 1
            read_idx = new_read_idx
        else:
            return json, read_idx + 1
    return json, read_idx


def main():
    for file_path in INPUT_PATH.glob("*.sds"):
        json_dict = None
        with open(file_path, "r") as file:
            contents = file.readlines()
        json_dict, _ = read_lines(contents, 0)

        output_file = OUTPUT_PATH / (file_path.stem + ".json")

        with open(output_file, "w", encoding="utf-8") as out_file:
            json.dump(json_dict, out_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
