#!/usr/bin/python3
import argparse
import csv
import os
from datetime import datetime
from time import time

from core import git
from core import experiment


def main():
    error_log = os.path.abspath("experiment-errors.csv")

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to analyze")
    parser.add_argument("subjects-home", help="subjects home")
    parser.add_argument("-f", "--force", help="force to cleanup test reports", action="store_true")
    parser.add_argument("-d", "--output-dir", help="changes the default output directory")
    parser.add_argument("-n", "--limit", help="execute only the first n subjects from the input file", type=int)

    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    subjects_home = os.path.abspath(args.subjects_home)
    output_dir = os.path.abspath(args.output_dir if args.output_dir else os.curdir)
    timestamp = datetime.fromtimestamp(time()).strftime('%y%m%d%H%M')
    output_file = os.path.abspath(os.path.join(output_dir, "dataset-{}.csv".format(timestamp)))
    limit = args.limit

    print("Input file: {}\nOutput file: {}\nExecution: {} subjects"
          .format(input_file, output_file, limit if limit else "All"))

    if not os.path.exists(subjects_home):
        print("Subjects' home created")
        os.mkdir(subjects_home)

    # Load subjects with errors to ignore them
    ignored = set({})
    if os.path.exists(error_log):
        with open(error_log, newline="") as f:
            reader = csv.DictReader(f, fieldnames=["timestamp", "name", "url", "reason"])
            for r in reader:
                ignored.add(r["name"])

    with open(input_file, newline="") as f:
        reader = csv.DictReader(f)
        counter = 1
        for subject_row in reader:
            if subject_row["name"] in ignored:
                continue
            if limit and counter > limit:
                print("\nLimit reached ({} subjects)".format(limit))
                break
            print("\nsubject #{}".format(counter))
            try:
                git.clone(url=subject_row["url"], directory=subjects_home)
                subject_path = os.path.join(subjects_home, subject_row["name"])
                experiment.run(subject_path, clean=args.force)
            except Exception as err:
                print(err)
                with open(error_log, "a") as log:
                    log.write(",".join([datetime.now().isoformat(), subject_row["name"],
                                        subject_row["url"], err.__str__()]))
                    log.write("\n")

            counter += 1


if __name__ == "__main__":
    main()
