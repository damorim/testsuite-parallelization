#!/usr/bin/python3
import argparse
import csv
import datetime
import os
import random

from support.core import Result, experiment

BASE_DIR = os.path.abspath(os.curdir)
SUBJECTS_HOME = os.path.join(BASE_DIR, "subjects")


def load_subjects_from(csv_file, sample_size=None):
    """
    Loads subjects successfully compiled from a csv file with columns COMPILED and SUBJECTS
    :param sample_size: [optional parameter] an integer representing N elements to return
    randomly selected with fixed seed
    :param csv_file: path to a csv file with columns COMPILED and SUBJECTS
    :return: a list of subjects successfully compiled
    """
    if not os.path.exists(csv_file):
        raise Exception("invalid input file path: \"{}\"".format(csv_file))

    loaded_subjects = []
    with open(csv_file, newline="") as content:
        csv_reader = csv.DictReader(content)
        for csv_row in csv_reader:
            if csv_row["COMPILED"] == "true":
                loaded_subjects.append(csv_row["SUBJECT"])

    if sample_size:
        random.seed(1234)
        return random.sample(population=loaded_subjects, k=sample_size)

    return loaded_subjects


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to analyze (columns required: COMPILED and SUBJECT)")
    parser.add_argument("-f", "--force", help="override existing output files (if any)", action="store_true")
    parser.add_argument("-d", "--dir", help="changes the default output directory")
    parser.add_argument("-n", "--sample-size", help="sample size, in case of running only a subset of the input",
                        type=int)
    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.dir if args.dir else os.curdir)

    output_file_path = os.path.join(output_dir, "dataset-{}".format(datetime.date.today()))
    if os.path.exists("{}.csv".format(output_file_path)):
        counter = 1
        while os.path.exists("{}.{}.csv".format(output_file_path, counter)):
            counter += 1
        output_file_path = "{}.{}".format(output_file_path, counter)

    output_file = os.path.abspath("{}.csv".format(output_file_path))
    n_args = args.sample_size
    print("Input file: {}\nOutput file: {}\nOverride: {}\nSample size: {}"
          "\n".format(input_file, output_file, args.force, n_args if n_args else "ALL"))

    # Check if SUBJECTS_HOME exist (REQUIRED)
    if not os.path.exists(SUBJECTS_HOME):
        print("Required directory missing: \"{}\"\nDid you execute \"downloader.py\" first?".format(SUBJECTS_HOME))
        exit(1)

    subjects = load_subjects_from(input_file, sample_size=n_args)

    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write(",".join(Result._fields))
            f.write("\n")

    for subject in subjects:
        subject_path = os.path.join(SUBJECTS_HOME, subject)
        results = experiment(subject_path, override=args.force)
        if results:
            for r in results:
                print(" -", r)
                with open(output_file, "a") as f:
                    f.write(",".join([str(getattr(r, attr)) for attr in Result._fields]))
                    f.write("\n")
