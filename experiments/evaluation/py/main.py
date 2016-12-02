#!/usr/bin/python3
import argparse
import csv
import os
from datetime import datetime

from core import experiment
from core import git
from core import model


def main():
    args = setup_arguments().parse_args()

    input_file = os.path.abspath(args.input)
    subjects_home = os.path.abspath(args.subjects)
    output_dir = os.path.abspath(args.output_dir if args.output_dir else os.curdir)
    limit = args.limit
    print("Input file: {}\nExecution: {} subjects".format(input_file, limit if limit else "All"))

    if not os.path.exists(subjects_home):
        print("Subjects' home created")
        os.mkdir(subjects_home)

    ignored = load_ignored_subjects()
    register = model.OutputRegister(output_dir)

    with open(input_file, newline="") as f:
        reader = csv.DictReader(f)
        counter = 1

        # Main loop
        for subject_row in reader:

            # special cases
            if ignored and subject_row["name"] in ignored:
                continue
            if limit and counter > limit:
                print("\nLimit reached ({} subjects)".format(limit))
                break

            print("\nsubject #{}".format(counter))
            rev = "unknown"
            try:
                # Subject setup
                git.clone(url=subject_row["url"], directory=subjects_home)
                subject_path = os.path.join(subjects_home, subject_row["name"])
                os.chdir(subject_path)
                try:
                    rev = subject_row["rev"]
                    git.reset("--hard", rev)
                except KeyError:
                    pass

                rev = git.which_revision()

                print("Running experiment on \"{}\" rev \"{}\"".format(subject_row["name"], rev))
                results = experiment.run(clean=args.force)
                register.results(name=subject_row["name"], data=results)
                register.subject(name=subject_row["name"], url=subject_row["url"], revision=rev)

            except Exception as err:
                print(err)
                register.error(when=datetime.now().isoformat(), name=subject_row["name"],
                               url=subject_row["url"], revision=rev, cause=err.__str__())
            counter += 1

    print("\nALL SUBJECTS PROCESSED\nCheck directory \"{}\" for output files".format(output_dir))


def setup_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to analyze")
    parser.add_argument("subjects", help="subjects home")
    parser.add_argument("-f", "--force", help="force to cleanup test reports", action="store_true")
    parser.add_argument("-d", "--output-dir", help="changes the default output directory")
    parser.add_argument("-n", "--limit", help="execute only the first n subjects from the input file", type=int)
    return parser


def load_ignored_subjects():
    """
    Populates a set with subject names from the error log.
    :return: None if the error log is empty or a set of subject names
    """
    ignored = None
    if os.path.exists(model.OutputRegister.ERROR_CSV_LOG):
        with open(model.OutputRegister.ERROR_CSV_LOG, newline="") as f:
            reader = csv.DictReader(f, fieldnames=model.OutputRegister.ERROR_LOG_HEADER)
            ignored = {r["name"] for r in reader}
    return ignored


if __name__ == "__main__":
    main()
