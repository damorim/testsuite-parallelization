#!/usr/bin/env python3
'''
This script is related to the RQ7. It compares test execution with
several different parallel settings.
@author: Jeanderson Candido <http://jeandersonbc.github.io>
'''
import csv
import os
import re
import shutil

from subprocess import Popen, PIPE, call


SUBJECTS_DIR = os.path.abspath(os.path.join("projects", "downloads"))
EXPERIMENT_DIR = os.path.abspath("./flakiness-speedup-experiment-2")
RAWDATA_DIR = os.path.abspath("./flakiness-speedup-rawdata-2")
SUBJECTS_NUM = 50


def minversion(dependency, reference):
    semantic_fields = lambda e:[int(v) for v in e.split(".")]
    try:
        ver = semantic_fields(dependency.split(":")[-2])
        print("Version subject:")
        print(ver)

        reffields = semantic_fields(reference)
        print("Version reference:")
        print(reffields)
        for i in range(len(reffields)):
            print("range:")
            print(i)
            if reffields[i] > ver[i]:
                return False

    except ValueError:
        return False

    return True


def criteria(entry):
    condition = entry["timecost_group"] != "short" \
                and entry["compiled"] == entry["tested"] == "SUCCESS" \
                and entry["perc_failures"] == "0"

    if not condition:
        print("Subject without condition ", entry["name"])
        return False

    print("Checking", entry["name"])
    project_path = os.path.join(SUBJECTS_DIR, entry["name"])
    if not os.path.exists(project_path):
        print("Project Path not found! ", entry["name"])
        return False

    p1 = Popen("cd \"%s\" && mvn dependency:list" % project_path, shell=True, stdout=PIPE)
    stdout, stderr = p1.communicate()
    p1.wait()
    if p1.returncode == 1:
        rawdeps = stdout.decode().split("\n")
        dependencies = [re.sub(".* ", "", d) for d in rawdeps if "junit:jar:" in d]
        for d in dependencies:
            if ("testng" in d) or ("junit" in d and not minversion(d, "4.7")):
                print("Old version JUnit in Error show dependency!")
                return False
        #print("Error show dependency! ", entry["name"])
        #return False
    rawdeps = stdout.decode().split("\n")
    dependencies = [re.sub(".* ", "", d) for d in rawdeps if "junit:jar:" in d]
    for d in dependencies:
        if ("testng" in d) or ("junit" in d and not minversion(d, "4.7")):
            print("Old version JUnit")
            return False

    return True


def prepare(subject):
    print("Preparing subject", subject["name"])
    project_path = os.path.join(SUBJECTS_DIR, subject["name"])
    if not os.path.exists(EXPERIMENT_DIR):
        os.mkdir(EXPERIMENT_DIR)

    modes = ["C0", "C1", "C2", "C3", "FC0", "FC1"]
    #modes = ["C0"]
    #modes = ["C1", "C2", "C3", "FC0", "FC1"]

    for mode in modes:
        target_path = os.path.join(EXPERIMENT_DIR, "%s_%s" % (subject["name"], mode))
        if not os.path.exists(target_path):
            call("cp -r \"%s\" \"%s\"" % (project_path, target_path), shell=True)

        call("./transform.rb --path \"%s\"" % target_path, shell=True)
        print("Generated modified subject", mode)


if __name__ == "__main__":  

    runs_time = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    with open("dataset-sanitized.csv", newline="") as f:
        reader = csv.DictReader(f)
        entries = [e for e in reader]

    entries = sorted(entries, key=lambda e: float(e["mvn_time_avg"]), reverse=True)

    subjects = []
    verifications = 0
    for entry in entries:
        subjects.append(entry)
        #if len(subjects) >= SUBJECTS_NUM:
        #    break
    #    if criteria(entry):
    #        print("Added", entry["name"])
    #        subjects.append(entry)

    #    verifications += 1
    #print("Verified: %d\nCollected: %d\n" % (verifications, len(subjects)))

    if os.path.exists(EXPERIMENT_DIR):
        print("Deleting old files...")
        shutil.rmtree(EXPERIMENT_DIR)

    [prepare(subject) for subject in subjects]

    if not os.path.exists(RAWDATA_DIR):
        os.mkdir(RAWDATA_DIR)
    
    for run in runs_time:
        with open('analysis-results.csv', 'w', newline='') as fout:
            csvout = csv.DictWriter(fout, fieldnames=["total_runs"])
            csvout.writeheader()
            csvout.writerows([{'total_runs': run}])

        call("./compile-test.sh 20m \"%s\" \"%s\"" % (EXPERIMENT_DIR, RAWDATA_DIR), shell=True)

