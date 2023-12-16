import pandas as pd
import numpy as np
import pathlib
import math

DAY = "05"


def main():
    input = get_input_path()
    df = pd.read_csv(
        input, sep=": ", header=None, nrows=1, names=["Title", "Text"], engine="python"
    )
    df["Seeds"] = df["Text"].str.split(" ")
    seeds = [int(i) for i in df["Seeds"][0]]
    seeds_range = [range(z[0], z[0] + z[1]) for z in zip(*[iter(seeds)] * 2)]

    dft = pd.read_csv(
        input,
        sep=" ",
        header=None,
        names=["Destination", "Source", "Length"],
        skiprows=2,
    )
    table_names = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    groups = dft["Destination"].isin(table_names).cumsum()
    tables = {g.iloc[0, 0]: g.iloc[1:] for k, g in dft.groupby(groups)}
    for k, v in tables.items():
        v = v.astype("int64")
        tables[k] = v

    def make_seed_df():
        data = []
        for seed in seeds:
            row = [seed]
            for name in table_names:
                destination = find_destination_for_source(row[-1], name)
                row.append(destination)
            data.append(row)
        return pd.DataFrame(data, columns=["seed"] + table_names)

    def find_destination_for_source(source, mapping):
        dft = tables[mapping]
        dft = dft[
            (source >= dft["Source"]) & (source < (dft["Source"] + dft["Length"]))
        ]
        if len(dft) == 0:
            return source
        else:
            return dft.iloc[0]["Destination"] + (source - dft.iloc[0]["Source"])

    dfs = make_seed_df()
    write_file(dfs, "seeds.csv")

    location = dfs["humidity-to-location"].min()
    print(location)

    def make_seed_df_range():
        data = []
        for seed in seeds_range:
            row = [[seed]]
            for name in table_names:
                destination = find_destination_for_source_range(row[-1], name)
                row.append(destination)
            ms = [loc.start for loc in row[-1]]
            row.append(min(ms))
            data.append(row)
        return pd.DataFrame(data, columns=["seed"] + table_names + ["location"])

    def find_destination_for_source_range(source, mapping):
        dft = tables[mapping]
        dsis = []
        ddis = []
        for src in source:
            for index, row in dft.iterrows():
                ds = range(row["Source"], row["Source"] + row["Length"])
                dsi = range_intersect(src, ds)
                if dsi is not None:
                    dsis.append(dsi)
                    offset = row["Destination"] - row["Source"]
                    ddi = range(dsi.start + offset, dsi.stop + offset)
                    ddis.append(ddi)

        for src in source:
            rr = [src]
            for srci in dsis:
                rr = range_remaining(rr, srci)
                if len(rr) == 0:
                    break
            for r in rr:
                ddis.append(r)
        return ddis

    def range_intersect(r1, r2):
        return range(max(r1.start, r2.start), min(r1.stop, r2.stop)) or None

    def range_remaining(r1s, r2):
        rrs = []
        for r1 in r1s:
            if r1.start < r2.start:
                r1b = range(r1.start, min(r1.stop, r2.start))
                rrs.append(r1b)
            if r1.stop > r2.stop:
                r1a = range(max(r1.start, r2.stop), r1.stop)
                rrs.append(r1a)

        return rrs

    dfsr = make_seed_df_range()
    write_file(dfsr, "seeds_range.csv")

    location = dfsr["location"].min()
    print(location)


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
