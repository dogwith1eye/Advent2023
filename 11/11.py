import pandas as pd
import numpy as np
import pathlib
from itertools import combinations
import multiprocessing as mp
from functools import partial

DAY = "11"
INPUT = "input.txt"
PART = "02"


def main():
    input = get_input_path()
    df = pd.read_csv(input, index_col=None, header=None, names=["Input"])
    df = df["Input"].apply(lambda x: pd.Series(list(x)))
    if PART == "01":
        df = expand_df(df)
        df, step, lookup = assign_number_df(df)
        write_file(df, "output.csv")
        pairs = list(combinations(range(1, step), 2))
        shortest = [find_shortest_path(lookup, pair) for pair in pairs]
        total = sum(shortest)
        print(total)
    if PART == "02":
        df = expand_df_02(df, 1000000)
        df, step, lookup = assign_number_df(df)
        write_file(df, "output.csv")
        pairs = list(combinations(range(1, step), 2))
        shortest = []
        fsp = partial(find_shortest_path_02, df, lookup)
        with mp.Pool(processes=mp.cpu_count() - 1) as pool:
            shortest = pool.map(fsp, pairs)
        total = sum(shortest)
        print(total)


def expand_df(df):
    cols = []
    for col, j in [(df[j], j) for j in df.columns]:
        if col[col.isin(["#"])].empty:
            cols.append((col, j))
    for idx, (col, j) in enumerate(cols):
        df.insert(j + idx + 1, f"{j}-copy", col)
    df.columns = range(0, len(df.columns))

    rows = []
    for i, row in df.iterrows():
        if row[row.isin(["#"])].empty:
            rows.append((row, i))
    for row, i in rows:
        df.loc[i + 0.5] = row
    df = df.sort_index().reset_index(drop=True)
    return df


def expand_df_02(df, amount):
    for col, x in [(df[x], x) for x in df.columns]:
        if col[col.isin(["#"])].empty:
            df[x] = col.map({".": (amount, 1)})
        else:
            df[x] = col.map({".": (1, 1), "#": "#"})
    for y, row in df.iterrows():
        if row[row.isin(["#"])].empty:
            df.loc[y] = row.map(
                {(1, 1): (1, 1), (1, 1): (1, amount), (amount, 1): (amount, amount)}
            )
    return df


def assign_number_df(df):
    step = 1
    locations = {}
    for val, x, y in [(df[x][y], x, y) for y in range(0, len(df)) for x in df.columns]:
        if val == "#":
            df[x][y] = step
            locations[step] = (x, y)
            step = step + 1
    return df, step, locations


def find_shortest_path(lookup, pair):
    a, b = pair
    ax, ay = lookup[a]
    bx, by = lookup[b]
    return abs(ax - bx) + abs(ay - by)


def find_shortest_path_02(df, lookup, pair):
    a, b = pair
    # print(pair)
    ax, ay = lookup[a]
    bx, by = lookup[b]
    ds = []

    def add_value(x, y, pos):
        value = df[x][y]
        if type(value) is tuple:
            ds.append(int(value[pos]))
        else:
            ds.append(1)

    def add_x_value(x, y):
        add_value(x, y, 0)

    def add_y_value(x, y):
        add_value(x, y, 1)

    xstep = 1 if bx > ax else -1
    ystep = 1 if by > ay else -1
    for x in range(ax + xstep, bx + xstep, xstep):
        add_x_value(x, ay)

    for y in range(ay, by, ystep):
        add_y_value(bx, y)

    return sum(ds)


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
