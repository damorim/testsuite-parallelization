#!/usr/bin/python3
import argparse
import csv
import os

from support import performance, utils

BASE_DIR = os.path.abspath(os.curdir)
SUBJECTS_HOME = os.path.join(BASE_DIR, "subjects")


def load_subjects_from(csv_file):
    if not os.path.exists(csv_file):
        raise Exception("invalid input file path: \"{}\"".format(csv_file))

    loaded_subjects = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["COMPILED"] == "true":
                loaded_subjects.append(row["SUBJECT"])

    return loaded_subjects


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to analyze (columns required: COMPILED and SUBJECT)")
    parser.add_argument("-o", "--output", help="csv file to output raw data")
    parser.add_argument("-f", "--force", help="override existing output files (if any)", action="store_true")
    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    output_file = os.path.abspath(args.output if args.output else "raw-data.csv")
    override = args.force
    print("Input file: {}\nOutput file: {}\nOverride: {}\n".format(input_file, output_file, override))

    # Check if SUBJECTS_HOME exist (REQUIRED)
    if not os.path.exists(SUBJECTS_HOME):
        print("Required directory missing: \"{}\"\nDid you execute \"downloader.py\" first?".format(SUBJECTS_HOME))
        exit(1)

    subjects = load_subjects_from(input_file)

    with open(output_file, "w") as output:
        output.write("subject,elapsed_t,tests,balance,cpu_usage,iowait,cpu_idle\n")

    for subject in subjects:
        subject_path = os.path.join(SUBJECTS_HOME, subject)

        if not os.path.exists(subject_path):
            print("Missing subject \"{}\". Skipping...".format(subject))
            continue

        os.chdir(subject_path)
        performance.evaluate(override=override)

        report_data = utils.check_test_reports()
        if report_data:
            try:
                t = utils.check_time_cost()
                tests = report_data.statistics['tests']
                balance = utils.compute_time_distribution(report_data)
                kernel_data = utils.check_resources_usage()

                with open(output_file, "a") as output:
                    output.write("{},{}\n".format(",".join([subject, str(t), str(tests), str(balance)]),
                                                  ",".join(kernel_data)))

            except Exception as err:
                with open(os.path.join(BASE_DIR, "main-errors.txt"), "a") as log:
                    log.write("{} - {}\n".format(subject, err))
