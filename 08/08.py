import pandas as pd
import pathlib
import numpy as np

DAY = "08"
PART = "03"


def main():
    input = get_input_path()
    dfi = pd.read_csv(
        input,
        header=None,
        nrows=1,
        names=["Instructions"],
    )
    instructions = dfi.iloc[0]["Instructions"]

    # range start, the source range start, and the range length.
    dfn = pd.read_csv(
        input,
        sep=" = ",
        header=None,
        names=["Node", "Next"],
        skiprows=2,
        engine="python",
    )
    dfn["Next"] = dfn.apply(
        lambda row: row["Next"]
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .split(),
        axis=1,
    )
    dfn = dfn.set_index("Node")
    write_file(dfn, "output.csv")

    if PART == "01":
        node = "AAA"
        step = 1
        idx = 0
        while True:
            ins = instructions[idx : idx + 1]
            node = find_node(node, ins)
            if node == "ZZZ":
                break
            step = step + 1
            idx = 0 if idx == len(instructions) - 1 else idx + 1
        print(step)

    def find_node(node, ins):
        next = dfn.loc[node, "Next"]
        return next[1] if ins == "R" else next[0]

    if PART == "02":
        nodes = list(filter(lambda x: x.endswith("A"), dfn.index))
        step = 1
        idx = 0
        while True:
            ins = instructions[idx : idx + 1]
            nodes = [find_node(n, ins) for n in nodes]
            if all(list(map(lambda x: x.endswith("Z"), nodes))):
                break
            step = step + 1
            if step % 100000 == 0:
                print(f"{step}:{nodes}")
            idx = 0 if idx == len(instructions) - 1 else idx + 1
        print(step)

    def find_node_repeat(node):
        step = 1
        idx = 0
        while True:
            ins = instructions[idx : idx + 1]
            next = dfn.loc[node, "Next"]
            node = next[1] if ins == "R" else next[0]
            if node.endswith("Z"):
                return step
            step = step + 1
            idx = 0 if idx == len(instructions) - 1 else idx + 1

    if PART == "03":
        nodes = list(filter(lambda x: x.endswith("A"), dfn.index))
        results = [find_node_repeat(n) for n in nodes]
        x = np.lcm.reduce(results, dtype=object)
        print(type(x))
        print(x)


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
