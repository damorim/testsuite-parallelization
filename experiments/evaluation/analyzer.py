#!/usr/bin/python3
import csv
import os

from support import builders
from support.constants import COLUMN_SEP, TIMECOST_CSV_FILE, SUBJECTS_CSV_FILE
from support.constants import SUBJECT_DIR


def inspect(subject):
    subject_dir = os.path.join(SUBJECT_DIR, subject)
    if not os.path.exists(subject_dir):
        return
    os.chdir(subject_dir)

    data = {"builder_name": "N/A", "compiled": False, "tests_pass": False, "#tests": "N/A",
            "elapsed_t": "N/A", "system_t": "N/A", "user_t": "N/A", "cpu_usage": "N/A"}

    builder = builders.detect_system()
    if builder:
        data["builder_name"] = builder.name
        if builder.compile():
            data["compiled"] = True
            # FIXME: How to deal when the project has multiple threads?
            # One option would be dividing by # of CPUs
            data["tests_pass"] = builder.test(data)

    return [subject, data["builder_name"], str(data["compiled"]), str(data["tests_pass"]), str(data["#tests"]),
            data["elapsed_t"], data["system_t"], data["user_t"], data["cpu_usage"]]


def register_data_from(project):
    csv_line = inspect(project)
    with open(TIMECOST_CSV_FILE, "a") as timecost:
        timecost.write(COLUMN_SEP.join(csv_line))
        timecost.write("\n")

def main():
    # Execution configuration
    max_rows = None
    init_row = None
    skip_subjects = ['neo4j', 'jetty.project', 'hive', 'pinot', 'hazelcast', 'hbase', 'hadoop'] #FIXME ignoring just to get output faster

    if not init_row:
        with open(TIMECOST_CSV_FILE, "w") as timecost:
            timecost.write(COLUMN_SEP.join(["SUBJECT", "BUILDER", "COMPILED", "TESTS_PASS", "TESTS", "ELAPSED_T",
                                            "SYSTEM_T", "USER_T", "CPU_USAGE"]))
            timecost.write("\n")

    with open(SUBJECTS_CSV_FILE, newline="") as subjects:
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
            if not project in skip_subjects:
                print("Checking", project)
                register_data_from(project)
                row_counter += 1

    # FIXME REMOVE ME (temporary code)
    print("Running skipped subjects....")
    for p in skip_subjects:
        print("Checking", p)
        register_data_from(p)

if __name__ == "__main__":
    main()