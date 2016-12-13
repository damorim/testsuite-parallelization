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


def inspect(paths):
    for file in paths:
        for t in ["forkCount", "forkMode", "parallel"]:
            if subprocess.call(["grep", t, file], stdout=subprocess.DEVNULL) == 0:
                return row["name"]

counter = 0
found = 0
with open(args.input, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if float(row["elapsed_time"]) >= min_limit:
            os.chdir(os.path.join(subjects_home, row["name"]))
            xml_paths = subprocess.check_output(["find", ".", "-path", "*/pom.xml"]).decode().splitlines()
            subj = inspect(xml_paths)
            if subj:
                print(subj)
                found += 1
            counter += 1

print("--------------------")
print("{} subjects verified".format(counter))
print("{} subjects found".format(found))
print("%.2f%%" % (found / counter * 100))
