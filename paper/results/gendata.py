#!/usr/bin/python3
import csv
from sys import argv


def gen_balance(row, fname):
    balance = float(row["balance"])
    intervals = [(0, 5, "0-5"),
                 (5, 10, "5-10"),
                 (10, 15, "10-15"),
                 (15, 20, "15-20"),
                 (20, 25, "20-25"),
                 (25, 30, "25-30"),
                 (30, 35, "30-35"),
                 (35, 40, "35-40"),
                 (40, 45, "40-45"),
                 (45, 50, "45-40"),
                 (50, 100, "50-100")]
    for i in intervals:
        if i[0] <= balance < i[1]:
            with open(fname, "a") as f:
                f.write(",".join([row["subject"], row["balance"], i[2]]))
                f.write("\n")


def gen_cpuness(row, fname):
    cpu_usage = float(row["cpu_usage"])
    intervals = [(0, 5, "0-5"),
                 (5, 10, "5-10"),
                 (10, 15, "10-15"),
                 (15, 20, "15-20"),
                 (20, 25, "20-25"),
                 (25, 30, "25-30"),
                 (30, 35, "30-35"),
                 (35, 40, "35-40"),
                 (40, 45, "40-45"),
                 (45, 50, "45-40"),
                 (50, 55, "50-55"),
                 (55, 60, "55-60"),
                 (60, 100, "60-100")]
    for i in intervals:
        if i[0] <= cpu_usage < i[1]:
            with open(fname, "a") as f:
                f.write(",".join([row["subject"], row["cpu_usage"], i[2]]))
                f.write("\n")

raw_data = argv[1]

with open("balance.csv", "w") as f:
    f.write(",".join(["subject", "balance", "label"]))
    f.write("\n")
with open("cpuness.csv", "w") as f:
    f.write(",".join(["subject", "cpuness", "label"]))
    f.write("\n")

with open(raw_data, newline="") as data:
    reader = csv.DictReader(data)
    for row in reader:
        if int(row["elapsed_t"]) >= 300:
            gen_balance(row, "balance.csv")
            gen_cpuness(row, "cpuness.csv")

