#!/usr/bin/env python3
import csv
import os
import xml.etree.ElementTree as etree


def parse_tc_timestamps(xml_files):
    timestamps = []
    for f in xml_files:
        root = etree.parse(f).getroot()
        for tc in root.findall("testcase"):
            try:
                timestamps.append(tc.get("time").replace(",", ""))
            except (ValueError, TypeError) as e:
                print(e)
                print(f)

    return timestamps


def extract_data(info, basedir):
    project_path = os.path.join(basedir, info["name"])
    latest_run = os.listdir(project_path)[-1]
    latest_run_path = os.path.join(project_path, latest_run)
    xml_files = [os.path.join(latest_run_path, f) for f in os.listdir(latest_run_path) if f.endswith(".xml")]
    timestamps = parse_tc_timestamps(xml_files)

    return [{"project": info["name"], "time": t} for t in timestamps]


def serialize_data_for(projects, timecost_group):
    entries = []
    for project_info in projects:
        if project_info["timecost_group"] == timecost_group:
            entries.extend(extract_data(info=project_info, basedir=logs_dir))

    fname = "dataset-testcases-{t}.csv"
    with open(fname.format(t=timecost_group), "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["project", "time"])
        writer.writeheader()
        writer.writerows(entries)


def isvalid(e):
    return e["timecost_group"] != "short" and e["below_threshold"] == "T"


if __name__ == "__main__":
    logs_dir = os.path.abspath("rawdata")
    input_csv = "dataset-sanitized.csv"
    if (not os.path.exists(logs_dir)) or (not os.path.exists(input_csv)):
        print("Could not find path \"%s\"\nExiting..." % logs_dir)

    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        projects = [e for e in reader if isvalid(e)]

    serialize_data_for(projects, "long")
    serialize_data_for(projects, "medium")

