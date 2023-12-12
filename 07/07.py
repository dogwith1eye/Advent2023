import pandas as pd
import numpy as np
import pathlib
import math

DAY = "07"
cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
types = ["5K", "4K", "FH", "3K", "2P", "1P", "HC"]
jcards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def main():
    input = get_input_path()
    df = pd.read_csv(input, sep=" ", header=None, names=["Hand", "Bid"])

    df["Type"] = df.apply(lambda x: find_type(x["Hand"]), axis=1)
    df["Type Sort"] = df.apply(lambda x: types.index(x["Type"]), axis=1)
    df["Hand Tuple"] = df.apply(lambda x: tuple(list(x["Hand"])), axis=1)
    df["Hand Sort"] = df.apply(sort_hand, axis=1)
    df = df.sort_values(by=["Type Sort", "Hand Sort"], ascending=False)
    df = df.reset_index(drop=True)
    df["Rank"] = df.apply(lambda x: (x.name + 1), axis=1)
    df["Winnings"] = df.apply(lambda x: x["Bid"] * x["Rank"], axis=1)
    write_file(df, "output.csv")

    total = df["Winnings"].sum()
    print(total)

    df["JType"] = df.apply(lambda x: find_jtype(x["Hand"]), axis=1)
    df["JType Sort"] = df.apply(lambda x: types.index(x["JType"]), axis=1)
    df["JHand Sort"] = df.apply(sort_jhand, axis=1)
    df = df.sort_values(by=["JType Sort", "JHand Sort"], ascending=False)
    df = df.reset_index(drop=True)
    df["JRank"] = df.apply(lambda x: (x.name + 1), axis=1)
    df["JWinnings"] = df.apply(lambda x: x["Bid"] * x["JRank"], axis=1)

    jtotal = df["JWinnings"].sum()
    print(jtotal)


def find_jtype(hand):
    count = hand.count("J")
    hand = hand.replace("J", "")
    type = find_type(hand)
    if count == 0:
        return type
    if type == "5K":
        return type
    if type == "4K":
        return "5K"
    if type == "FH":
        return type
    if type == "3K":
        if count == 1:
            return "4K"
        return "5K"
    if type == "2P":
        return "FH"
    if type == "1P":
        if count == 1:
            return "3K"
        if count == 2:
            return "4K"
        return "5K"
    if count == 1:
        return "1P"
    if count == 2:
        return "3K"
    if count == 3:
        return "4K"
    return "5K"


def find_type(hand):
    three = False
    two = False
    for card in cards:
        count = hand.count(card)
        if count == 5:
            return "5K"
        if count == 4:
            return "4K"
        if count == 3:
            if two:
                return "FH"
            three = True
        if count == 2:
            if three:
                return "FH"
            if two:
                return "2P"
            two = True
    if three:
        return "3K"
    if two:
        return "1P"
    return "HC"


def sort_hand(row):
    hand = list(row["Hand"])
    hand = list(map(lambda x: cards.index(x), hand))
    return tuple(hand)


def sort_jhand(row):
    hand = list(row["Hand"])
    hand = list(map(lambda x: jcards.index(x), hand))
    return tuple(hand)


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
