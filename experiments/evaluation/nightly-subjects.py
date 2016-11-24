#!/usr/bin/env python3
import csv
from collections import namedtuple

Subj = namedtuple("Subj", "name, et")


def main(data_file="./data/rawdata.csv", subjects_csv="./data/rawdata.csv"):
    blacklist = {"jsoup", "jstorm", "mapdb", "neo4j", "nutz", "presto", "spark", "hbase", "pinot"}
    with open(data_file, newline="") as content:
        reader = csv.DictReader(content)
        subjects = [Subj(name=r["name"], et=float(r["elapsed_time"])) for r in reader
                    if r["mode"] == "ST" and float(r["elapsed_time"]) >= 300]

    ordered_subjects = sorted(subjects, key=lambda s: s.et, reverse=True)
    nightly_subjects = set({})
    cost = 0
    threshold = (3600 * 8)
    for subj in ordered_subjects:
        if (subj.et * 2) + cost <= threshold and subj.name not in blacklist:
            cost += subj.et * 2
            nightly_subjects.add(subj.name)

    with open(subjects_csv, newline="") as content:
        reader = csv.DictReader(content)
        header = reader.fieldnames
        rows = [r for r in reader if r["SUBJECT"] in nightly_subjects]

    print(cost / 3600)
    print(nightly_subjects)

    with open("nightly-subjects.csv", "w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
