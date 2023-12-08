import pandas as pd
import numpy as np
import pathlib
import math

DAY = "05"


def main():
    input = get_input_path()
    seeds_df = pd.read_csv(
        input,
        sep=": ",
        header=None,
        nrows=1,
        names=["Title", "Text"],
    )
    seeds_df["Seeds"] = seeds_df["Text"].str.split(" ")
    write_file(seeds_df, "output_seeds.csv")
    seeds = [int(i) for i in seeds_df["Seeds"][0]]
    seeds_range = [z for z in zip(*[iter(seeds)] * 2)]

    # range start, the source range start, and the range length.
    df = pd.read_csv(
        input,
        sep=" ",
        header=None,
        names=["Destination", "Source", "Length"],
        skiprows=2,
    )
    write_file(df, "output.csv")
    table_names = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    groups = df["Destination"].isin(table_names).cumsum()
    tables = {g.iloc[0, 0]: g.iloc[1:] for k, g in df.groupby(groups)}

    data = get_data_for_seeds(tables, seeds)
    totals = get_totals_for_seeds(data)
    write_file(totals, "output.csv")
    print_totals(totals)


def get_data_for_seeds(tables, seeds):
    print(len(seeds))
    data = []
    for seed in seeds:
        print(seed)
        input = seed
        for k, v in tables.items():
            print("table:", k)
            v = v.astype("int64")
            v["Source End"] = v.apply(lambda row: row["Source"] + row["Length"], axis=1)
            write_file(v, f"output-{k}.csv")
            v = v[(input >= v["Source"]) & (input < v["Source End"])]
            print(len(v))
            if len(v) == 0:
                output = input
                data.append([seed, input, k, input])
            else:
                output = v.iloc[0]["Destination"] + (input - v.iloc[0]["Source"])
                data.append([seed, input, k, output])
            input = output
    return data


def get_totals_for_seeds(data):
    totals = pd.DataFrame(data, columns=["Seed", "Input", "Table", "Output"])
    return totals


def print_totals(totals):
    totals = totals[totals["Table"] == "humidity-to-location"]
    min = totals["Output"].min()
    print(min)


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
