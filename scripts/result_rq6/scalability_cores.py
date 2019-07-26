#!/usr/bin/env python3
'''
This script is related to the RQ6. It compares time execution with
more CPU available.
@author: Sotero Junior <https://soterojunior.github.io/>

The Arguments = <PROJECT_DIR> and <NUM_CORE> are required

# Usage:   ./scalability_cores <PROJECT_DIR> <NUM_CORE> 
# Example: ./scalability_cores ./projects 17

'''

import csv
import os
import re 
import shutil
import xml.etree.ElementTree as etree

from collections import Counter
from subprocess import check_output, CalledProcessError, Popen, PIPE, call
from sys import argv


def extract_last_field(log_path, field, default="?"):
    try:
        cmd = "cat %s | grep --text \"%s\""
        out = check_output(cmd % (log_path, field), shell=True)
        out = out.decode().strip().split("\n")[-1]
        value = re.sub(".*%s" % field.strip(), "", out).strip()
    except CalledProcessError as e:
        print("Warning: unable to extract requested field \"%s\"" % field)
        print("  Possible cause: Unfinished execution")
        print("  File: \"%s\"" % log_path)
        print("  Value assigned: \"%s\"" % default)
        value = default
    except Exception as e:
        print(e)
        print(log_path)
        value = default
    return value


def normalize(timestamp):
    if "min" in timestamp:
        fields = [int(t) for t in re.sub(" .*", "", timestamp).split(":")]
        return fields[0]*60 + fields[1]
    elif "s" in timestamp:
        return float(re.sub(" .*", "", timestamp))
    elif "h" in timestamp:
        fields = [int(t) for t in re.sub(" .*", "", timestamp).split(":")]
        return (fields[0]*60 + fields[1])*60

    return timestamp


def parse_xml_reports(xml_files):
    summary = Counter(tests=0, time=0, failures=0, suites=len(xml_files))
    for f in xml_files:
        if os.path.basename(f) == "TEST-results.xml":
            continue
        try:
            root = etree.parse(f).getroot()
            # The comma replacement is required for high timestamps (eg 1,529.43)
            time_attr = float(root.get("time").replace(",", ""))
            tests_attr = int(root.get("tests"))
            failures_attr = int(root.get("failures"))
            if root.get("errors"):
                failures_attr += int(root.get("errors"))

            summary.update(tests=tests_attr, time=time_attr, failures=failures_attr)

        except (ValueError, TypeError) as e:
            print(e)
            print(f)

        except:
            # fail-fast
            import traceback
            traceback.print_exc()
            print("A problem occurred while parsing", f)
            exit(1)

    return summary


def extract_data_from(project_path):
    project_name = os.path.basename(project_path)

    log_data = []
    suite_data = []
    for subdir in os.listdir(project_path):
        subdir_path = os.path.join(project_path, subdir)

        compile_log = os.path.join(subdir_path, "compile.log")
        testing_log = os.path.join(subdir_path, "testing.log")

        compile_field = extract_last_field(compile_log, "\[INFO\] BUILD ")
        testing_field = extract_last_field(testing_log, "\[INFO\] BUILD ")

        mvn_time = "0" if testing_field == "?" else extract_last_field(testing_log, " Total time: ")
        mvn_time = normalize(mvn_time)

        xml_files = [os.path.join(subdir_path, f) for f in os.listdir(subdir_path) if f.endswith(".xml")]
        suite_statistics = parse_xml_reports(xml_files)

        log_data.append({"name": project_name,
                         "numcore": project_name[project_name.rindex('_')+1:],
                         "compiled": compile_field,
                         "tested": testing_field,
                         "time": mvn_time,
                         "tests": suite_statistics["tests"],
                         "suites": suite_statistics["suites"],
                         "failures": suite_statistics["failures"]})
    return log_data

if __name__ == "__main__":  

    RUNS_TIME = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    RAWDATA_DIR = "./rawdata_scalability"

    try:

        PROJECT_DIR = argv[1]
        NUM_CORE = argv[2]

        if not NUM_CORE.isdigit():
            print("The core argument must be Integer..\"%s\"\nExiting..." % NUM_CORE)

        if not os.path.exists(PROJECT_DIR):
            print("Could not find directory \"%s\"\nExiting..." % PROJECT_DIR)

        if not os.path.exists(RAWDATA_DIR):
            os.mkdir(RAWDATA_DIR)

        for run in RUNS_TIME:
            call("./compile-test.sh 90m \"%s\" \"%s\" \"%s\"" % (PROJECT_DIR, RAWDATA_DIR, NUM_CORE), shell=True)

        print("Generating the results...")

        ENTRIES = []
        for project in os.listdir(RAWDATA_DIR):
            project_path = os.path.join(RAWDATA_DIR, project)
            ENTRIES.extend(extract_data_from(project_path))

        HEADER = ["name", "numcore", "compiled", "tested", "time","tests", "suites", "failures"]

        RESULT_FILE = "result_scalability_%s.csv" % NUM_CORE

        with open(RESULT_FILE, "w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=HEADER)
            writer.writeheader()
            writer.writerows(ENTRIES)

        print("Process Completed!")

    except IndexError as ie:
        print("Error: params not found. Exception: {0}".format(ie))

