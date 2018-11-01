#!/usr/bin/env python3
import csv
import re


def compare(reference, other):
    if reference["tests"] != other["tests"]:
        return ["x", "x"]
    speedup = float(reference["mvn_test_time"]) / float(other["mvn_test_time"])
    flakiness = float(other["failures"]) / float(reference["tests"]) * 100
    return ["%sx" % format_value(speedup), "%s%%" % format_value(flakiness)]


def format_value(value):
    return "0" if not value else "%.2f" % value


def inminutes(raw_time):
    return "%.1fm" % (float(raw_time) / 60)


def entries(reference, data):
    return [entry for entry in data if reference in entry["name"]]


if __name__ == "__main__":
    with open("dataset-rq7.csv", newline="") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    names = {re.sub(r"_F*C[0-3]", "", d["name"]) for d in data}
    indexes = {}
    for entry in data:
        indexes[entry["name"]] = entry

    rows = []
    for n in names:
        C0 = indexes["%s_C0" % (n)]

        row = [n, inminutes(C0["mvn_test_time"]), C0["tests"]]
        for mode in ["C1", "C2", "C3", "FC0", "FC1"]:
            other = indexes["%s_%s" % (n, mode)]
            [row.append(differences) for differences in compare(C0, other)]

        rows.append(row)

    [print(" & ".join(p)) for p in sorted(rows, key=lambda v: float(re.sub("m", "", v[1])), reverse=True)]
