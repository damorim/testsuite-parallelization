#!/usr/bin/python3
import csv
import os

from support import performance, utils

BASE_DIR = os.path.abspath(os.curdir)
SUBJECTS_HOME = os.path.join(BASE_DIR, "subjects")

INPUT_FILE = os.path.join(BASE_DIR, "subjects.csv")

subjects = []
with open(INPUT_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["COMPILED"] == "true":
            subjects.append(row["SUBJECT"])

print("subject,elapsed_t,tests,balance,cpu_usage,iowait,cpu_idle")  # TODO define an output format
for subject in subjects:
    subject_path = os.path.join(SUBJECTS_HOME, subject)
    os.chdir(subject_path)

    performance.evaluate()

    t = utils.check_time_cost()
    report_data = utils.check_test_reports()
    if report_data:
        try:
            tests = report_data.statistics['tests']
            balance = utils.compute_time_distribution(report_data)
            kernel_data = utils.check_resources_usage()

            # TODO define an output format
            print("{},{}".format(",".join([subject, str(t), str(tests), str(balance)]), ",".join(kernel_data)))
        except Exception as err:
            with open(os.path.join(BASE_DIR, "main-errors.txt"), "a") as log:
                log.write("{} - {}\n".format(subject, err))
