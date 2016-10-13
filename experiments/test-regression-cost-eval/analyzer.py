#!/usr/bin/python3
import csv
import os

import helpers
from constants import SUBJECT_DIR, SUBJECTS_CSV_FILE
from constants import TIMECOST_CSV_FILE, COLUMN_SEP


def check(subject):
    subject_dir = os.path.join(SUBJECT_DIR, subject)
    if not os.path.exists(subject_dir):
        return

    os.chdir(subject_dir)
    builder = helpers.detect_build_system()
    try:
        compiled = builder.compile()
        tested = False if not compiled else builder.test()
        elapsed_time = builder.test_elapsed_time()
    except Exception as err:
        print(err)
        compiled = "N/A"
        tested = "N/A"
        elapsed_time = "N/A"

    csv_line = []
    csv_line.append(subject)
    csv_line.append(str(builder))
    csv_line.append(str(compiled))
    csv_line.append(str(tested))
    csv_line.append(elapsed_time)
    with open(TIMECOST_CSV_FILE, "a") as timecost:
        timecost.write(COLUMN_SEP.join(csv_line))
        timecost.write("\n")


if __name__ == "__main__":
    # Limit execution
    max_rows = None

    with open(TIMECOST_CSV_FILE, "w") as timecost:
        timecost.write(COLUMN_SEP.join(["SUBJECT", "BUILDER", "COMPILED",
                                        "TESTS_PASS", "ELAPSED_TIME"]))
        timecost.write("\n")

    with open(SUBJECTS_CSV_FILE, newline="") as subjects:
        reader = csv.DictReader(subjects)
        cur_row = 1
        for row in reader:
            if max_rows and cur_row > max_rows:
                break
            project = row["SUBJECT"]
            if not row["BUILDER"] == "N/A":
                print("Checking", project)
                check(project)
                cur_row += 1

