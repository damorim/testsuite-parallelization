#!/usr/bin/env python3
import csv
from sys import argv


def remove_bad_entries(entries, bad_elems):
    [entries.remove(bad) for bad in bad_elems]


def classify_subject(entry):
    timestamp = float(entry["xml_time_avg"])
    if timestamp < 60:
        entry["timecost_group"] = "short"
    elif timestamp <= 300:
        entry["timecost_group"] = "medium"
    else:
        entry["timecost_group"] = "long"


def compute_perc_fails(entry):
    value = int(entry["failures"]) / int(entry["tests"]) * 100
    entry["perc_failures"] = "%.2f" % value
    entry["below_threshold"] = "T" if value <= FAIL_THRESHOLD else "F"


def update(entries):
    [classify_subject(e) for e in entries]
    [compute_perc_fails(e) for e in entries]
    return entries


EXPECTED_RUNS = int(argv[1])
FAIL_THRESHOLD = float(argv[2])
SUBJECTS = {"Not Maven": 48}


with open("dataset-aggregated.csv", newline="") as f:
    reader = csv.DictReader(f)
    entries = [e for e in reader]

# Remove flaky subjects
flakiness = [e for e in entries if int(e["runs"]) != EXPECTED_RUNS]
remove_bad_entries(entries, flakiness)
SUBJECTS["Flaky"] = len({e["name"] for e in flakiness})

# Remove subjects that does not run tests
untestable = [e for e in entries if e["tests"] == "0"]
remove_bad_entries(entries, untestable)
SUBJECTS["Missing Dependencies"] = len(untestable)

# Remaining is testable
SUBJECTS["Testable"] = len(entries)

if len(entries):
    update(entries)

with open("dataset-subjects.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["type", "value"])
    writer.writeheader()
    if len(entries):
        excessive_fails = sum([1 for e in entries if e["below_threshold"] == "F"])
        SUBJECTS[">{}% Failures".format(FAIL_THRESHOLD)] = excessive_fails
        SUBJECTS["Testable"] = len(entries) - excessive_fails

    [writer.writerow({"type": k, "value": v}) for k, v in SUBJECTS.items() if v > 0]

csv_header = ["name", "compiled", "tested", "tests", "suites",
              "failures", "runs", "mvn_time_avg", "mvn_time_sd",
              "xml_time_avg", "xml_time_sd", "perc_failures",
              "timecost_group", "below_threshold"]

with open("dataset-sanitized.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_header)
    writer.writeheader()
    if len(entries):
        writer.writerows(entries)

