import pandas as pd
import pathlib
import numpy as np
from io import StringIO

DAY = "13"
PART = "02"
INPUT = "input.txt"


def main():
    input = get_input_path()
    dfs = read_patterns(input)
    # for idx, df in enumerate(dfs):
    #     write_file(df, f"output-{idx}.csv")
    rs = [find_reflection(df) for df in dfs]
    if PART == "02":
        rs = [fix_find_reflection(df, rs[idx]) for idx, df in enumerate(dfs)]
    for idx, r in enumerate(rs):
        if r[0] is None:
            print(f"{idx}:x:{r[1]}")
        else:
            print(f"{idx}:y:{r[0]}")
    ts = [r[1] + 1 if r[0] is None else (r[0] + 1) * 100 for r in rs]
    total = sum(ts)
    print(total)


def read_patterns(input):
    dfs = []
    with open(input) as data:
        bio = StringIO()
        for line in data:
            if line == "\n":
                bio.seek(0)
                df = pd.read_csv(bio, index_col=None, header=None, names=["Input"])
                df = df["Input"].apply(lambda x: pd.Series(list(x)))
                dfs.append(df)
                bio = StringIO()
            else:
                bio.write(line)
    return dfs


def find_reflection(df, r=(None, None)):
    def is_reflection(idx, series):
        hs = series.head(idx + 1)
        hs = hs.iloc[::-1]
        ts = series.tail(series.size - idx - 1)
        if ts.size == 0:
            return False
        if hs.size < ts.size:
            ts = ts.head(hs.size)
            return np.array_equal(hs.values, ts.values)
        else:
            hs = hs.head(ts.size)
            return np.array_equal(hs.values, ts.values)

    # print(df)
    idxs = range(0, len(df) - 1)
    for x, col in [(x, df[x]) for x in df.columns]:
        idxs = [idx for idx in idxs if is_reflection(idx, col)]
        # print(f"y:{x}:{idxs}")
        if len(idxs) == 0:
            break
        if len(idxs) == 1 and idxs[0] == r[0]:
            break

    if len(idxs) == 1:
        if idxs[0] != r[0]:
            return (idxs[0], None)
    if len(idxs) == 2:
        if idxs[0] != r[0]:
            return (idxs[0], None)
        else:
            return (idxs[1], None)

    idxs = range(0, df.columns.size - 1)
    for y, row in df.iterrows():
        idxs = [idx for idx in idxs if is_reflection(idx, row)]
        # print(f"x:{y}:{idxs}")
        if len(idxs) == 0:
            break
        if len(idxs) == 1 and idxs[0] == r[1]:
            break

    if len(idxs) == 1:
        if idxs[0] != r[1]:
            return (None, idxs[0])
    if len(idxs) == 2:
        if idxs[0] == r[1]:
            return (None, idxs[1])
        if idxs[1] == r[1]:
            return (None, idxs[0])

    return (None, None)


def fix_find_reflection(df, r):
    for v, x, y in [(df[x][y], x, y) for y in range(0, len(df)) for x in df.columns]:
        dfr = df.copy(deep=True)
        # print(f"x:{x}:y{y}")
        if v == "#":
            dfr[x][y] = "."
        else:
            dfr[x][y] = "#"
        fr = find_reflection(dfr, r)
        if fr[0] is not None or fr[1] is not None:
            return fr


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
