import pandas as pd
import pathlib
import itertools

DAY = "09"


def main():
    input = get_input_path()
    df = pd.read_csv(
        input,
        sep=" ",
        header=None,
        names=range(21),
        # names=range(6),
    )
    df[["Previous", "Next"]] = df.apply(extrapolate_history, axis=1)
    write_file(df, "output.csv")
    previous = df["Previous"].sum()
    print(previous)
    next = df["Next"].sum()
    print(next)


def extrapolate_history(row):
    xss = []
    xs = list(pd.Series(row).array)
    xss.append(xs)
    while True:
        xs = [pair[1] - pair[0] for pair in itertools.pairwise(xs)]
        xss.append(xs)
        if all([x == 0 for x in xs]):
            break
    ys = [ls[-1] for ls in reversed(xss)]
    ns = [0]
    for y in ys[1:]:
        ns.append(ns[-1] + y)

    zs = [ls[0] for ls in reversed(xss)]
    ps = [0]
    for z in zs[1:]:
        ps.append(z - ps[-1])
    return pd.Series([ps[-1], ns[-1]])


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
