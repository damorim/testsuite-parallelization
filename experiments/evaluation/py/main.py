#!/usr/bin/python3
import argparse
import csv
import os
from datetime import datetime
from time import time

from support import git
from support.core import RESULT_FIELDS

SUBJECTS_HOME = os.path.abspath("subjects")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to analyze")
    parser.add_argument("-f", "--force", help="override existing output files (if any)", action="store_true")
    parser.add_argument("-d", "--output-dir", help="changes the default output directory")
    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output_dir if args.output_dir else os.curdir)
    timestamp = datetime.fromtimestamp(time()).strftime('%y%m%d%H%M')
    output_file = os.path.abspath(os.path.join(output_dir, "dataset-{}.csv".format(timestamp)))

    print("Input file: {}\nOutput file: {}\nOverride: {}\n".format(input_file, output_file, args.force))

    if not os.path.exists(SUBJECTS_HOME):
        print("Subjects' home created")
        os.mkdir(SUBJECTS_HOME)
    with open(output_file, "w") as f:
        f.write(RESULT_FIELDS)
        f.write("\n")

    with open(input_file, newline="") as f:
        reader = csv.DictReader(f)
        for subject_row in reader:
            git.clone(url=subject_row["url"], clone_home=SUBJECTS_HOME)

            # TODO process this subject right now!

            # for subject in subjects:
            #     subject_path = os.path.join(SUBJECTS_HOME, subject)
            #     results = experiment(subject_path, override=args.force)
            #     if results:
            #         for r in results:
            #             print(" -", r)
            #             with open(output_file, "a") as f:
            #                 f.write(",".join([str(getattr(r, attr)) for attr in Result._fields]))
            #                 f.write("\n")
