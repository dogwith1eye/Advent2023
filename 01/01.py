import pandas as pd
import numpy as np
import pathlib

DAY = "01"


def main():
    input = get_input_path()
    df = pd.read_csv(input, index_col=None, header=None, names=["Code"])

    df["Digits"] = df.apply(find_digits, axis=1)
    df["Sum"] = df.apply(combine_head_tail, axis=1)
    write_csv(df, "output.csv")

    total = df[f"Sum"].sum()
    print(total)


def find_digits(row):
    code = row["Code"]
    digits = [int(c) for c in code if c.isdigit()]
    return digits


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
