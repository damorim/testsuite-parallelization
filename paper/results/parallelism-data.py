#!/usr/bin/env python3
import csv

RAW_DATA = "parallel-settings-recursive.csv"

data = []
values = ["L1", "L2", "L3"]
with open(RAW_DATA, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
        for v in values:
            for i in range(int(row[v])):
                data.append(v)


with open("parallelism-data.csv", "w") as f:
    f.write("label\n")
    for v in data:
        f.write("%s\n" % v)

