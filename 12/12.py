import pandas as pd
import pathlib
import numpy as np
from itertools import product, groupby
import multiprocessing as mp

DAY = "12"
INPUT = "input.txt"


def main():
    input = get_input_path()
    df = pd.read_csv(
        input, sep=" ", index_col=None, header=None, names=["Input", "Count"]
    )
    df = parallelize_dataframe(df, parallelize_function)
    write_file(df, "output.csv")
    total = df["Arrangements"].sum()
    print(total)


def find_arrangements(row):
    ars = 0
    count = [int(c) for c in row["Count"].split(",")]
    xs = list(row["Input"])
    qs = [i for i, x in enumerate(xs) if x == "?"]
    ls = ["#", "."]
    ls = list(product(ls, repeat=len(qs)))
    for l in ls:
        ys = xs.copy()
        for idx, q in enumerate(qs):
            ys[q] = l[idx]

        s = "".join(ys)
        groups = groupby(s)
        rs = [(sum(1 for _ in group)) for label, group in groups if label == "#"]
        if rs == count:
            ars = ars + 1
    return ars


def parallelize_function(df):
    df["Arrangements"] = df.apply(find_arrangements, axis=1)
    return df


def parallelize_dataframe(df, func):
    num_processes = mp.cpu_count()
    df_split = np.array_split(df, num_processes)
    with mp.Pool(num_processes) as p:
        df = pd.concat(p.map(func, df_split))
    return df


def get_input_path():
    root = pathlib.Path().absolute()
    input = pathlib.Path(root, DAY, INPUT)
    return input


def write_file(df, name):
    root = pathlib.Path().absolute()
    path = pathlib.Path(root, DAY, name)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    main()
