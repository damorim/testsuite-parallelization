#!/usr/bin/python3
import csv
import os

from sys import argv


def classify_group(raw_time):
    seconds = float(raw_time)
    # Group 1: t < 1m
    if seconds < 60:
        return "Short"
    # Group 2: 1m <= t < 5m
    elif seconds < 5*60:
        return "Norm"
    # Group 3: 5m <= t < 10m
    elif seconds < 600:
        return "Long"
    # Group 4: 10 <= t
    return "Very Long"


def convert_time(raw_time):
    seconds = float(raw_time)
    if seconds < 60:
        return "%ds" % seconds
    return "%dm%ds" % (seconds // 60, seconds % 60)


if __name__ == "__main__":
    raw_data_path = argv[1]
    output_file = argv[2]
    if not os.path.exists(raw_data_path):
        print("Path \"{}\" does not exist!".format(raw_data_path))
        exit(1)

    with open(raw_data_path, newline='') as f:
        reader = csv.DictReader(f)
        with open(output_file, "w") as out:
            out.write("subject,tests,elapsed_t,group,elapsed_t_debug")
            out.write("\n")
            for row in reader:
                if not row["tests"] == "0":
                    tests = int(row["tests"]) - int(row["skipped"])
                    group = classify_group(row["elapsed_t"])
                    elapsed_t_debug = convert_time(row["elapsed_t"])

                    columns = [row["subject"], str(tests), row["elapsed_t"],
                               group, elapsed_t_debug]
                    out.write(",".join(columns))
                    out.write("\n")

