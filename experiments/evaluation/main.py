#!/usr/bin/python3
import argparse
import csv
import os
from subprocess import call, DEVNULL, PIPE, Popen

import re

from support import maven

BASE_DIR = os.path.abspath(os.curdir)
SUBJECTS_HOME = os.path.join(BASE_DIR, "subjects")


def measure_test_cost(override=False):
    # RQ1
    call(maven.resolve_dependencies_task(), stdout=DEVNULL, stderr=DEVNULL)
    test_log_default = "test-log-default.txt"
    test_log_sequential = "test-log-sequential.txt"
    if not os.path.exists(test_log_default) or override:
        with open(test_log_default, "w") as log_file:
            call(maven.test_task("-o", "-Dmaven.javadoc.skip=true"),
                 stdout=log_file, stderr=DEVNULL)
    if not os.path.exists(test_log_sequential) or override:
        with open(test_log_sequential, "w") as log_file:
            call(maven.test_task("-o", "-Dmaven.javadoc.skip=true", "-P", "tests-seq"),
                 stdout=log_file, stderr=DEVNULL)
    timestamps = {test_log_default: None, test_log_sequential: None}
    for log in timestamps.keys():
        cat = Popen(["cat", log], stdout=PIPE)
        grep = Popen(["grep", "Total time:"], stdin=cat.stdout, stdout=PIPE)
        cat.stdout.close()
        out, err = grep.communicate()

        # normalize reported time
        reported_time = re.sub(r".*: ", "", out.decode().replace("s", "").strip())
        if "min" in reported_time:
            reported_time = reported_time.replace("min", "").split(":")
            reported_time = (60 * int(reported_time[0])) + int(reported_time[1])
            # FIXME test subjects with reported time > 60min

        timestamps[log] = round(float(reported_time))

    return timestamps


def experiment(subject_path, override=False):
    """
    Runs the experiment for a Maven subject from the given path
    :param subject_path: the path to the subject
    :param override: flag indicating whether existing data should be overridden
    :return: None
    """
    subject_name = os.path.basename(subject_path)
    if not os.path.exists(subject_path):
        print("Missing subject \"{}\". Skipping...".format(subject_name))
        return

    if not maven.is_valid_project(subject_path):
        print("Subject \"{}\" is not a Maven project. Skipping...".format(subject_name))
        return

    print("Analyzing subject: \"{}\"".format(subject_name))

    os.chdir(subject_path)
    exit_status = call(maven.build_task("-DskipTests", "-Dmaven.javadoc.skip=true"),
                       stdout=DEVNULL, stderr=DEVNULL)
    if not exit_status:
        timestamps = measure_test_cost(override=override)
        print(subject_name, timestamps)


def load_subjects_from(csv_file):
    """
    Loads subjects successfully compiled from a csv file with columns COMPILED and SUBJECTS
    :param csv_file: path to a csv file with columns COMPILED and SUBJECTS
    :return: a list of subjects successfully compiled
    """
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
    print("Input file: {}\nOutput file: {}\nOverride: {}\n".format(input_file, output_file, args.force))

    # Check if SUBJECTS_HOME exist (REQUIRED)
    if not os.path.exists(SUBJECTS_HOME):
        print("Required directory missing: \"{}\"\nDid you execute \"downloader.py\" first?".format(SUBJECTS_HOME))
        exit(1)

    subjects = load_subjects_from(input_file)
    for subject in subjects:
        experiment(os.path.join(SUBJECTS_HOME, subject), override=args.force)
