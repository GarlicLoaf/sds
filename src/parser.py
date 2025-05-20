import json
from pathlib import Path

INPUT_PATH = Path("./input/")


def read_lines(content):
    json = {}
    for i, line in enumerate(content):
        line = line.strip()
        match line[0]:
            case "-":
                # standard output
                json["line_" + str(i)] = {"type": 0, "text": line[2:]}
            case "!":
                # branch
                if not json:
                    json["line_" + str(i)] = {
                        "type": 1,
                        "text": line[2:],
                        "content": read_lines(content[i:]),
                    }
                else:
                    return json
            case ">":
                # decision
                json["line_" + str(i)] = {"type": 2, "text": line[2:]}
    return json


def main():
    for file_path in INPUT_PATH.glob("*.sds"):
        json_dict = {}
        with open(file_path, "r") as file:
            contents = file.readlines()
        json_dict = read_lines(contents)
        print(json_dict)


if __name__ == "__main__":
    main()
