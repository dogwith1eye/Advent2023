import pandas as pd
import numpy as np
import pathlib

DAY = "02"


def main():
    input = get_input_path()
    df = pd.read_csv(
        input,
        sep=";|:",
        index_col=None,
        header=None,
        names=["Game", "1", "2", "3", "4", "5", "6"],
    )
    df["Game"] = df["Game"].str.replace("Game ", "")
    df["Game"] = df["Game"].astype("int")
    df = df.melt(id_vars=["Game"], var_name="Set", value_name="Result")
    df = df[df["Result"].notna()]
    df["RGB"] = df.apply(find_rgb, axis=1)
    df["Red"] = df.apply(lambda row: row["RGB"][0], axis=1)
    df["Green"] = df.apply(lambda row: row["RGB"][1], axis=1)
    df["Blue"] = df.apply(lambda row: row["RGB"][2], axis=1)
    df["Valid"] = df.apply(is_valid, axis=1)
    write_csv(df, "output.csv")
    totals = df.groupby("Game", as_index=False).agg(
        {
            "RGB": "count",
            "Red": "max",
            "Green": "max",
            "Blue": "max",
            "Valid": "sum",
        }
    )
    totals["Game Valid"] = totals.apply(lambda row: row["RGB"] == row["Valid"], axis=1)
    totals["Power"] = totals.apply(find_power, axis=1)
    write_csv(totals, "totals.csv")
    total = totals.loc[totals["Game Valid"]]["Game"].sum()
    print(total)
    power = totals["Power"].sum()
    print(power)


def find_rgb(row):
    result = row["Result"]
    red = 0
    green = 0
    blue = 0
    for r in result.split(","):
        amount, color = r.strip().split(" ")
        if color == "red":
            red = int(amount)
        elif color == "green":
            green = int(amount)
        elif color == "blue":
            blue = int(amount)
    return [red, green, blue]


def is_valid(row):
    rgb = row["RGB"]
    red, green, blue = rgb
    if red > 12:
        return False
    if green > 13:
        return False
    if blue > 14:
        return False
    return True


def find_power(row):
    red = row["Red"]
    green = row["Green"]
    blue = row["Blue"]
    return red * green * blue


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
