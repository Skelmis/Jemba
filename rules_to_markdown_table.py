import csv
import io
import json
import tomllib
from collections import defaultdict


def generate_legacy_table():
    with open("jemba_rules.json", "r") as f:
        data = json.load(f)

    keys = list(data.keys())
    keys.sort()
    sorted_dict = {i: data[i] for i in keys}

    output = io.StringIO()
    output.write("|Name|Rule|\n|----|----|\n")
    for k, v in sorted_dict.items():
        output.write(f"{k.title()}|{v}|\n")

    with open("jemba_rules.md", "w") as f:
        f.write(output.getvalue())


def generate_index(letters: list[str], *, width: int) -> str:
    col_count = 0
    output = io.StringIO()
    output.write("|")
    for _ in range(width):
        output.write("|")

    output.write("\n|")
    for _ in range(width):
        output.write("-|")

    output.write("\n|")
    for letter in letters:
        output.write(f"[{letter.upper()}](#{letter})|")
        col_count += 1
        if col_count >= width:
            output.write("\n|")
            col_count = 0

    return output.getvalue()


def generate_table(data: list[tuple[str, str]]) -> str:
    output = io.StringIO()
    output.write("|Name|Rule|\n|----|----|\n")
    for k, v in sorted(data, key=lambda x: x[0]):
        output.write(f"|{k.title()}|{v}|\n")

    return output.getvalue()


def generate_csv(data: dict[str, list[tuple[str, str]]]) -> None:
    with open("rules.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["Name", "Rule"])
        for value in data.values():
            for k, v in value:
                writer.writerow([k, v])


def generate_nested_tables():
    file = io.StringIO()
    # with open("jemba_rules.json", "r") as f:
    #     raw_data = json.load(f)

    with open("rules.toml", "r") as f:
        raw_data = tomllib.loads(f.read())

    flattened_raw_data = {}
    for category in raw_data.values():
        for rule in category.values():
            for k, v in rule.items():
                flattened_raw_data[k] = v

    data = defaultdict(list)
    for k, v in flattened_raw_data.items():
        data[k[0].lower()].append([k, v])

    file.write(generate_index(list(data.keys()), width=5))
    file.write("\n\n")

    for key, value in data.items():
        file.write(f"### {key.title()}\n")
        file.write(generate_table(value))
        file.write("\nBack to [top](#top)\n\n")
        file.write("---\n")

    with open("jemba_rules.md", "w") as f:
        f.write(file.getvalue())

    generate_csv(data)

    print(
        f"Wrote {len(flattened_raw_data.keys())} rules out. Jemba requires 108 for a full game."
    )


generate_nested_tables()
