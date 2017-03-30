#!/usr/bin/env python3
import csv

with open("data/execution-1.csv", newline = "") as f:
    reader = csv.DictReader(f)
    dataset1 = [r for r in reader]


with open("gen/selection.csv", "w") as f:
    f.write("project,group,xml_time\n")
    for p in dataset1:
        subject_type = "untestable"
        if float(p["xml_test_time"]) > 0:
            subject_type = "testable"
        f.write("{},{},{}\n".format(p["project_path"], subject_type, p["xml_test_time"]))

    # We know that 48 projects are not based on maven
    for i in range(48):
        f.write(",not maven,\n")

print("dataset size:", len(dataset1))

