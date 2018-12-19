#!/usr/bin/env python3
import csv, re, os, shutil
from sys import argv


input_csv = os.path.join("csv", "maven-projects.csv")
download_dir = "downloads"
with open(input_csv, newline="") as out:
    reader = csv.DictReader(out)
    entries = {re.sub("/", "_", entry["full_name"]) for entry in reader}

counter = 0
part_counter = 0
for entry in os.listdir(download_dir):

    dirname = "eval-part{}".format(part_counter)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    if entry in entries:
        print("Moving {} to {}".format(entry, dirname))
        origin = os.path.join(download_dir, entry)
        destiny = os.path.join(dirname, entry)
        shutil.move(origin, destiny)

        counter += 1

        if (counter >= 50):
            counter = 0
            part_counter += 1

