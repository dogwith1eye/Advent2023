import pandas as pd
import pathlib
import math

DAY = "10"

PIPES = ["|", "-", "L", "J", "7", "F", "S"]


def main():
    input = get_input_path()
    df = pd.read_csv(input, index_col=None, header=None, names=["Input"])
    df = df["Input"].apply(lambda x: pd.Series(list(x)))
    start = find_start_pos(df)
    pipes = find_pipes(df, start)
    max_step = math.ceil(len(pipes) / 2)
    print(max_step)


def find_start_pos(df):
    for i, j, k in [(df[j][k], j, k) for k in range(0, len(df)) for j in df.columns]:
        if i == "S":
            return j, k
    return 0, 0


def find_pipes(df, start):
    next = find_pipe_for_pos(df, ("S", start, (start[0], start[1] + 1)))
    if next == None:
        next = find_pipe_for_pos(df, ("S", start, (start[0], start[1] - 1)))
    if next == None:
        next = find_pipe_for_pos(df, ("S", start, (start[0] + 1, start[1])))
    if next == None:
        next = find_pipe_for_pos(df, ("S", start, (start[0] - 1, start[1])))
    pipes = [next]
    while True:
        next = find_pipe_for_pos(df, next)
        if next[0] == "S":
            break
        pipes.append(next)
    return pipes


def find_pipe_for_pos(df, pos):
    name, prev, cur = pos
    direction = find_direction(prev, cur)
    value = df[cur[0]][cur[1]]
    pipes = [x for x in PIPES if x == value]
    if len(pipes) > 0:
        pipe = pipes[0]
        if pipe == "|":
            if direction == "N":
                return (pipe, cur, (cur[0], cur[1] - 1))
            if direction == "S":
                return (pipe, cur, (cur[0], cur[1] + 1))
        if pipe == "-":
            if direction == "E":
                return (pipe, cur, (cur[0] + 1, cur[1]))
            if direction == "W":
                return (pipe, cur, (cur[0] - 1, cur[1]))
        if pipe == "F":
            if direction == "N":
                return (pipe, cur, (cur[0] + 1, cur[1]))
            if direction == "W":
                return (pipe, cur, (cur[0], cur[1] + 1))
        if pipe == "7":
            if direction == "N":
                return (pipe, cur, (cur[0] - 1, cur[1]))
            if direction == "E":
                return (pipe, cur, (cur[0], cur[1] + 1))
        if pipe == "J":
            if direction == "S":
                return (pipe, cur, (cur[0] - 1, cur[1]))
            if direction == "E":
                return (pipe, cur, (cur[0], cur[1] - 1))
        if pipe == "L":
            if direction == "S":
                return (pipe, cur, (cur[0] + 1, cur[1]))
            if direction == "W":
                return (pipe, cur, (cur[0], cur[1] - 1))
        if pipe == "S":
            return (pipe, cur, None)
        return None


def find_direction(prev, cur):
    if cur[1] > prev[1]:
        return "S"
    if prev[1] > cur[1]:
        return "N"
    if cur[0] > prev[0]:
        return "E"
    return "W"


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
