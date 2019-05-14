#!/usr/bin/env python3
import csv, os
from subprocess import call


output_dir = "downloads"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


input_csv = os.path.join("csv", "interesting.csv")
with open(input_csv, newline="") as out:
    reader = csv.DictReader(out)
    entries = [e for e in reader]


clone_cmd = "git clone https://github.com/{} --recursive {}"
reset_cmd = "git reset --hard {}"


cnt = 0 # XXX download subset only
ordered_entries = sorted(entries, key=lambda e: int(e["size"]), reverse=True)
for e in ordered_entries:
    dirname = e["full_name"].replace("/", "_")
    target = os.path.join(output_dir, dirname)
    curdir = os.path.abspath(os.path.curdir)

    rev = e["rev"]
    if not os.path.exists(target):
        call(clone_cmd.format(e["full_name"], target), shell=True)
        os.chdir(target)
        call(reset_cmd.format(rev), shell=True)
    
    print(curdir)
    #os.chdir(target)
    #call(reset_cmd.format(rev), shell=True)
    os.chdir(curdir)

    # XXX download subset only
    cnt += 1
    if (cnt >= 957):
        break

