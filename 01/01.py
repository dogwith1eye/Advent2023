import pandas as pd
import numpy as np
import pathlib
import re


DAY = "01"
PART = "02"


def main():
    input = get_input_path()
    df = pd.read_csv(input, index_col=None, header=None, names=["Code"])

    if PART == "01":
        df["Digits"] = df.apply(find_digits, axis=1)
        df["Sum"] = df.apply(combine_head_tail, axis=1)
        write_csv(df, "output.csv")

        total = df[f"Sum"].sum()
        print(total)

    if PART == "02":
        df["Sum"] = df.apply(find_digits_spelled_out, axis=1)
        write_csv(df, "output.csv")

        total = df[f"Sum"].sum()
        print(total)


def find_digits(row):
    code = row["Code"]
    digits = [int(c) for c in code if c.isdigit()]
    return digits


def find_digits_spelled_out(row):
    code = row["Code"]

    def find_min_max_positions(pattern):
        p1, p2 = pattern
        p1s = [match.start() for match in re.finditer(p1, code)]
        p2s = [match.start() for match in re.finditer(p2, code)]
        ps = p1s + p2s
        if len(ps) == 0:
            return int(p1), None, None
        return int(p1), min(ps), max(ps)

    digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    dws = list(zip(digits, words))
    dws = list(map(find_min_max_positions, dws))
    mindws = list(filter(lambda x: x[1] is not None, dws))
    min_digit = min(mindws, key=lambda x: x[1])
    maxdws = list(filter(lambda x: x[2] is not None, dws))
    max_digit = max(maxdws, key=lambda x: x[2])
    return int(f"{min_digit[0]}{max_digit[0]}")


def combine_head_tail(row):
    digits = row["Digits"]
    head = digits[0]
    tail = digits[-1]
    return int(f"{head}{tail}")


def get_input_path():
    root = pathlib.Path().absolute()
    input = pathlib.Path(root, DAY, "input.txt")
    return input


def write_csv(df, name):
    root = pathlib.Path().absolute()
    path = pathlib.Path(root, DAY, name)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
