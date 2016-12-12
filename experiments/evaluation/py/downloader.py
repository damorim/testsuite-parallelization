#!/usr/bin/env python3
#
# Author: Jeanderson Candido
import argparse
import csv
import os

from core import git


def main():
    args = setup_arguments().parse_args()

    output_dir = os.path.abspath(args.output)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    input_file = os.path.abspath(args.input)
    with open(input_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            os.chdir(output_dir)
            git.clone(row["url"], output_dir)

            subject_path = os.path.join(output_dir, row["name"])
            os.chdir(subject_path)
            git.reset("--hard", row["rev"])


def setup_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to download")
    parser.add_argument("output", help="output directory")
    return parser


if __name__ == "__main__":
    main()
