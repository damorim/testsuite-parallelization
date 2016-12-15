#!/usr/bin/env python3
import argparse
import csv
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("subjects", help="Subject's directory")
parser.add_argument("--min", help="limits the subjects according to the elapsed time", type=float)
parser.add_argument("--max", help="limits the subjects according to the elapsed time", type=float)
args = parser.parse_args()

subjects_home = os.path.abspath(args.subjects)
base_dir = os.path.abspath(os.curdir)
min_limit = 0 if not args.min else args.min
max_limit = args.max


def filter_relevant_paths(paths):
    keywords = ["forkCount", "forkMode", "parallel"]
    relevant_paths = set()
    for file in paths:
        if subprocess.call(["grep", "\|".join(keywords), file], stdout=subprocess.DEVNULL) == 0:
            relevant_paths.add(file)
    return relevant_paths


def main():
    counter = 0
    found = 0
    relevant_files_counter = 0
    files_counter = 0
    with open(args.input, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if float(row["elapsed_time"]) >= min_limit:
                if not max_limit or float(row["elapsed_time"]) < max_limit:
                    os.chdir(os.path.join(subjects_home, row["name"]))
                    xml_paths = subprocess.check_output(["find", ".", "-path", "*/pom.xml"]).decode().splitlines()
                    paths = filter_relevant_paths(xml_paths)
                    if paths:
                        print("{} ({}/{} relevant files)".format(row["name"], len(paths), len(xml_paths)))
                        for p in paths:
                            print(" - {}".format(p))

                        relevant_files_counter += len(paths)
                        files_counter += len(xml_paths)
                        found += 1
                    counter += 1

    print("--------------------")
    print("{} subjects verified".format(counter))
    print("{} subjects found".format(found))
    print("%.2f%%" % (found / counter * 100))

    print("{} files to found".format(files_counter))
    print("{} files to inspect".format(relevant_files_counter))
    print("%.2f%%" % (relevant_files_counter / files_counter * 100))


if __name__ == "__main__":
    main()
