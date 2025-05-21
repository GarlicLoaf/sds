import json
from pathlib import Path

INPUT_PATH = Path("./input/")
OUTPUT_PATH = Path("./output/")


def read_lines(content, read_idx):
    json = {"lines": []}
    last_exclamation = None
    choice = 0

    while read_idx < len(content):
        line = content[read_idx].strip()

        if line.startswith("-"):
            # standard output
            json["lines"].append({"type": 0, "text": line[2:]})
            read_idx += 1

        elif line.startswith("!"):
            # branch
            choice = 0
            last_exclamation = len(json["lines"])
            json["lines"].append(
                {
                    "type": 1,
                    "text": line[2:],
                    "answers": [],
                    "branches": [],
                }
            )
            read_idx += 1

        elif line.startswith(">"):
            # decision
            json["lines"][last_exclamation]["answers"].append(line[2:-2])

            branch_json, new_read_idx = read_lines(content, read_idx + 1)
            json["lines"][last_exclamation]["branches"].append(branch_json["lines"])

            choice += 1
            read_idx = new_read_idx

        else:
            read_idx += 1
            return json, read_idx
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
