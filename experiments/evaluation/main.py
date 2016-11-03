#!/usr/bin/python3
import os

from support import performance, utils

BASE_DIR = os.path.abspath(os.curdir)
SUBJECTS_HOME = os.path.join(BASE_DIR, "subjects")

# TODO populate this list from csv file
subjects = ["retrofit"]

print("subject,elapsed_t,tests,balance,cpu_usage")  # TODO define an output format
for subject in subjects:
    subject_path = os.path.join(SUBJECTS_HOME, subject)
    os.chdir(subject_path)

    performance.evaluate()

    t = utils.check_time_cost()
    report_data = utils.check_test_reports()
    if report_data:
        tests = report_data.statistics['tests']
        balance = utils.compute_time_distribution(report_data)
        cpu_usage = utils.check_cpu_usage()

        # TODO define an output format
        print(",".join([subject, str(t), str(tests), str(balance), str(cpu_usage)]))