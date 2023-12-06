import pandas as pd
import numpy as np
import pathlib

def main():
    root = pathlib.Path().absolute()
    input = pathlib.Path(root, "01", "input.txt")
    df = pd.read_csv(input, index_col=None, header=None, names=["Code"])
    df["Digits"] = df.apply(find_digits, axis=1)
    df["Sum"] = df.apply(combine_head_tail, axis=1)
    output = pathlib.Path(root, "01", "output.csv")
    df.to_csv(output, index=False)
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

if __name__ == "__main__":
    main()