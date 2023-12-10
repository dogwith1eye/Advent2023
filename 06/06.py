import pandas as pd
import numpy as np
import pathlib
import math

DAY = "06"


def main():
    input = get_input_path()
    df = pd.read_csv(
        input, sep=":", index_col=None, header=None, names=["Label", "Result"]
    )
    df["Result Array"] = df.apply(find_arrays, axis=1)
    write_file(df, "output.csv")
    print_result(df)

    df["Result Int"] = df.apply(find_int, axis=1)
    write_file(df, "output.csv")
    print_result_2(df)


def find_int(row):
    r = row["Result"].replace(" ", "")
    r = [int(r)]
    return r


def print_result(df):
    pairs = list(zip(df.iloc[0]["Result Array"], df.iloc[1]["Result Array"]))
    print(pairs)
    rs = list(map(lambda x: find_records(x), pairs))
    r = np.prod(rs)
    print(r)


def print_result_2(df):
    pairs = list(zip(df.iloc[0]["Result Int"], df.iloc[1]["Result Int"]))
    print(pairs)
    rs = list(map(lambda x: find_records_fast(x), pairs))
    print(rs)


def find_arrays(row):
    rs = row["Result"].split(" ")
    rs = list(filter(lambda x: len(x) > 0, rs))
    rs = np.array([int(i) for i in rs])
    return rs


def find_records(pair):
    time, rdistance = pair
    ps = []
    for speed in range(1, time + 1):
        travel = time - speed
        tdistance = travel * speed
        ps.append((speed, tdistance))
    rs = list(filter(lambda x: x[1] > rdistance, ps))
    return len(rs)


def find_records_fast(pair):
    time, rdistance = pair

    def find_first_record(start, stop, step):
        for speed in range(start, stop, step):
            travel = time - speed
            tdistance = travel * speed
            if tdistance > rdistance:
                return (speed - step, speed)

    def find_record(start, stop, step):
        include = 1 if step > 0 else -1
        while True:
            start, stop = find_first_record(start, stop + include, step)
            if step == include:
                break
            else:
                step = int(step / 10)
                print(start, stop, step)
        return stop

    min = find_record(1, time, 1000000)
    print(min)
    max = find_record(time, 1, -1000000)
    print(max)
    return max - min + 1


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
