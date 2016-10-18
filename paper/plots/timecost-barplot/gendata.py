#!/usr/bin/python3
import csv
import os

from sys import argv

if __name__ == "__main__":
    raw_data_path = argv[1]
    if not os.path.exists(raw_data_path):
        print("Path \"{}\" does not exist!".format(raw_data_path))
        exit(1)

    elapsed_time_groups = []
    with open(raw_data_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["COMPILED"] == "True":
                seconds = float(row["ELAPSED_T"])
                
                # Group 1: t < 1m
                if seconds < 60:
                    elapsed_time_groups.append("A")
                # Group 2: 1m <= t < 5m
                elif seconds < 5*60:
                    elapsed_time_groups.append("B")
                # Group 3: 5m <= t < 10m
                elif seconds < 600:
                    elapsed_time_groups.append("C")
                # Group 4: 10 <= t
                else:
                    elapsed_time_groups.append("D")


    with open("timecost-groups.csv", "w") as f:
        for g in elapsed_time_groups:
            f.write(g)
            f.write("\n")

