import pandas as pd
import numpy as np
import pathlib

def main():
    root = pathlib.Path().absolute()
    input = pathlib.Path(root, "03", "input.txt")
    df = pd.read_csv(input, index_col=None, header=None, names=["Input"])
    df = df['Input'].apply(lambda x: pd.Series(list(x)))

    symbols = pd.Series([item for col in df for item in df[col]]).unique()
    symbols = [c for c in symbols if not c.isdigit() and not c == '.']
    print(symbols)

    rowcount,colcount = df.shape

    ns = []
    for irow, j in df.iterrows():
        rns = []
        digit = ''
        for icol in range(0, colcount):
            v = df.loc[irow][icol]
            if v.isdigit():
                digit = f"{digit}{v}"
            if len(digit) > 0:
                end_of_digit = (icol == colcount - 1) or (not df.iloc[irow][icol].isdigit())
                if end_of_digit:
                    if add_digit(symbols, digit, irow, rowcount, icol, colcount, df):
                        points = [(irow, col) for col in range(icol - len(digit), icol)]
                        value = (int(digit), points)
                        rns.append(value)
                    digit = ''
        ns.append(rns)
    print(ns)
    ns = flatten(ns)
    nvals = list(map(lambda x: x[0], ns))
    total = pd.Series(nvals).sum()
    print(total)

    gears = []
    for irow, j in df.iterrows():
        rgears = []
        for icol in range(0, colcount):
            v = df.loc[irow][icol]
            if v == "*":
                 (g1, g2) = find_gears(ns, irow, rowcount, icol, colcount, df)
                 if g1 is not None and g2 is not None:
                     rgears.append(int(g1) * int(g2))
                   
        gears.append(rgears)
    gears = flatten(gears)
    gear_total = pd.Series(gears).sum()
    print(gear_total)

def add_digit(symbols, digit, irow, rowcount, icol, colcount, df):
    dlen = len(digit)
    last_col = icol if icol == colcount - 1 else icol + 1
    first_col = 0 if icol - dlen == 0 else icol - dlen - 1
    
    rows = [irow]
    if irow > 0:
        rows.append(irow-1)
    if irow < rowcount - 1:
        rows.append(irow+1)
        
    for pcol in range(first_col,last_col):
        for prow in rows:
            if df.iloc[prow][pcol] in symbols:
                return True
            
    return False

def find_gears(ns, irow, rowcount, icol, colcount, df):
    points = [(row, col) for row in range(irow -1, irow + 2) for col in range(icol - 1, icol + 2)]
    def check(x):
        for g in x[1]:
            if g in points:
                return True
        return False
    
    gears = list(filter(lambda x: check(x), ns))
    if len(gears) == 2:       
        return gears[0][0], gears[1][0]
    return None, None
    
def flatten(list):
    return [item for sublist in list for item in sublist]

def write_file(df, name):
    root = pathlib.Path().absolute()
    path = pathlib.Path(root, "03", name)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    main()