#!/usr/bin/env python3
import argparse
import csv
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("subjects")
parser.add_argument("threshold", help="limits the subjects according to the elapsed time", type=float)
args = parser.parse_args()

subjects_home = os.path.abspath(args.subjects)
base_dir = os.path.abspath(os.curdir)


def inspect(paths):
    for file in paths:
        for t in ["forkCount", "forkMode", "parallel"]:
            if subprocess.call(["grep", t, file], stdout=subprocess.DEVNULL) == 0:
                print(row["name"])
                return


with open(args.input, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if float(row["elapsed_time"]) > args.threshold:
            os.chdir(os.path.join(subjects_home, row["name"]))
            xml_paths = subprocess.check_output(["find", ".", "-path", "*/pom.xml"]).decode().splitlines()
            inspect(xml_paths)
