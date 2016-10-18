#!/usr/bin/python3
import csv
import os

from sys import argv

if __name__ == "__main__":
    raw_data_path = argv[1]
    if not os.path.exists(raw_data_path):
        print("Path \"{}\" does not exist!".format(raw_data_path))
        exit(1)

    with open(raw_data_path, newline='') as f:
        reader = csv.DictReader(f)
        with open("timetests-data.csv", "w") as out:
            out.write("SUBJECT,TESTS,ELAPSED_T")
            out.write("\n")
            for row in reader:
                if not (row["TESTS"] == "N/A" or row["TESTS"] == "0"):
                    columns = [row["SUBJECT"], row["TESTS"], row["ELAPSED_T"]]
                    out.write(",".join(columns))
                    out.write("\n")

