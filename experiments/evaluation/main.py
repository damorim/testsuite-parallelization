#!/usr/bin/python3
import csv
import os

import analysis

BASE_DIR = os.path.abspath(os.curdir)
INPUT_CSV = os.path.join(BASE_DIR, "subjects.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "rawdata.csv")


def main():
    # Execution configuration
    max_rows = None
    init_row = None

    # FIXME ignoring just to get output faster
    skip_subjects = ['neo4j', 'jetty.project', 'hive', 'pinot', 'hazelcast', 'hbase', 'hadoop']

    if not init_row:
        with open(OUTPUT_CSV, "w") as time_cost:
            time_cost.write(",".join("%s" % attrib for attrib in analysis.ExecutionData.header()))
            time_cost.write("\n")

    with open(INPUT_CSV, newline="") as subjects:
        reader = csv.DictReader(subjects)

        row_counter = 1
        cur_row = 2
        for row in reader:
            if init_row and cur_row < init_row:
                cur_row += 1
                continue

            if max_rows and row_counter > max_rows:
                break

            project = row["SUBJECT"]
            if project not in skip_subjects:
                print("Checking", project)
                data = analysis.main(project)
                with open(OUTPUT_CSV, "a") as time_cost:
                    time_cost.write(",".join("%s" % str(value) for value in data.values()))
                    time_cost.write("\n")
                row_counter += 1

    # FIXME REMOVE ME (temporary code)
    print("Running skipped subjects....")
    for p in skip_subjects:
        print("Checking", p)
        data = analysis.main(p)
        with open(OUTPUT_CSV, "a") as time_cost:
            time_cost.write(",".join("%s" % str(value) for value in data.values()))
            time_cost.write("\n")


if __name__ == "__main__":
    os.chdir(os.path.join(BASE_DIR, "subjects"))
    main()
