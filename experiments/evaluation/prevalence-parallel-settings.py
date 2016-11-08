#!/usr/bin/env python3
import csv
import os
import subprocess
from collections import Counter
from sys import argv

def find_prevalence(subject_path=os.curdir, recursive=False):
    os.chdir(subject_path)
    subject_name = os.path.basename(os.path.abspath(os.curdir))

    find_command = ["find", "."]
    if not recursive:
        find_command.extend(["-maxdepth", "1"])
    find_command.extend(["-name", "pom.xml"])

    # get all pom.xml paths
    output = subprocess.check_output(find_command)

    print(subject_name)

    # for each pom file, grep it!
    # TODO a better approach would be parsing the XML file,
    # considering namespace costraints, to know HOW the settings
    # are used...
    counter = Counter(parallel=0, forkMode=0, forkCount=0, files=0)
    for xml_path in output.decode().splitlines():
        counter["files"] += 1
        for tag in counter.keys():
            try:
                out = subprocess.check_output(["grep", "-r", "<{}>".format(tag), xml_path])
                counter[tag] += len(out.splitlines())
            except:
                pass
    return counter


SUBJECTS_CSV = argv[1]
BASE_DIR = os.path.abspath(os.curdir)
OUTPUT_FILE = os.path.join(BASE_DIR, "parallel-settings.csv")

subjects = []
with open(SUBJECTS_CSV, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["BUILDER"] == "Maven":
            subjects.append(row["SUBJECT"])

with open(OUTPUT_FILE, "w") as f:
    f.write("subject,files,parallel,forkmode,forkcount\n")

SUBJECTS_HOME = os.path.abspath("subjects")
for i in range(len(subjects)):
    subject = subjects[i]
    subject_path = os.path.join(SUBJECTS_HOME, subject)
    if os.path.exists(subject_path):
        counter = find_prevalence(subject_path=subject_path)
        print(subject, counter)
        with open(OUTPUT_FILE, "a") as f:
            f.write("{},{},{},{},{}\n".format(subject, counter['files'],
                                              counter['parallel'],
                                              counter['forkMode'],
                                              counter['forkCount']))

