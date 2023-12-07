import pandas as pd
import numpy as np
import pathlib
import math

DAY = "04"


def main():
    input = get_input_path()
    df = pd.read_csv(
        input,
        sep=":|\|",
        index_col=None,
        header=None,
        names=["Card", "Winning Numbers", "My Numbers"],
    )
    df["Card"] = df["Card"].str.replace("Card ", "")
    df["Card"] = df["Card"].astype("int")
    df["My Winning Numbers"] = df.apply(find_my_winning_numbers, axis=1)
    df["Points"] = [double(1, len(w)) for w in df["My Winning Numbers"]]
    df["Copies"] = [
        copies(c, len(w)) for c, w in zip(df["Card"], df["My Winning Numbers"])
    ]
    write_file(df, "output.csv")
    total = df["Points"].sum()

    df_copy = df.copy()

    cards = df["Card"].unique()
    for card in cards:
        print(f"card: {card}")
        df_card = df_copy[df_copy["Card"] == card]
        print(f"copies: {len(df_card)}")

        cards_to_copy = df_card["Copies"].iloc[0]
        print(f"new copies: {len(df_card) * len(cards_to_copy)}")

        df_copy_row = df[df["Card"].isin(cards_to_copy)]
        df_copy_row_repeat = pd.DataFrame(
            np.repeat(df_copy_row.values, len(df_card), axis=0)
        )
        df_copy_row_repeat.columns = df.columns

        df_copy = pd.concat([df_copy, df_copy_row_repeat])
        print(f"total: {len(df_copy)}")

    print(f"final total: {len(df_copy)}")


def double(num, n):
    if n == 0:
        return 0
    for x in range(n - 1):
        num = num + num
    return num


def copies(card, n):
    if n == 0:
        return []
    return [x + card + 1 for x in range(n)]


def find_my_winning_numbers(row):
    ws = row["Winning Numbers"].split(" ")
    ms = row["My Numbers"].split(" ")
    mws = list(filter(lambda x: x.isdigit() and x in ws, ms))
    return mws


def get_input_path():
    root = pathlib.Path().absolute()
    input = pathlib.Path(root, DAY, "input.txt")
    return input


def write_file(df, name):
    root = pathlib.Path().absolute()
    path = pathlib.Path(root, DAY, name)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
