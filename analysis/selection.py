#!/usr/bin/env python3
import csv

def gen_testcost_data(group, testcases, selection):
    output = "gen/testcost-{}.csv".format(group)
    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=testcases[0].keys())
        writer.writeheader()
        for row in testcases:
            if row["project"] in selection and row["project"] not in {"INRIA_spoon"}:
                try:
                    writer.writerow(row)
                except:
                    # FIXME: it shouldn't have bad CSV rows...
                    print(row)


def csv_content(path, header=None):
    with open(path, newline="") as f:
        reader = csv.DictReader(f) if not header else csv.DictReader(f, header)
        return [r for r in reader]


def classify_subject_type(p):
    return "testable" if float(p["xml_test_time"]) > 0 else "untestable"


def classify_timecost(p):
    exec_time = float(p["xml_test_time"])
    if exec_time <= 60:
        return "short"
    elif exec_time <= (5 * 60):
        return "medium"
    return "long"

    
dataset1 = csv_content("data/execution-1.csv")

# TODO merge datasets in a single dataset
dataset = dataset1

timecost_groups = {"medium": set({}), "long": set({})}
for p in dataset:
    p["selection_group"] = classify_subject_type(p)
    p["timecost_group"] = classify_timecost(p)
    if not p["timecost_group"] == "short":
        timecost_groups[p["timecost_group"]].add(p["project_path"])

with open("gen/selection.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames = dataset[0].keys())
    writer.writeheader()
    writer.writerows(dataset)

    # We know that 48 projects are not based on maven
    for i in range(48):
        writer.writerow({"selection_group": "not maven"})

print("dataset size:", len(dataset))

testcases = csv_content("data/test-cases-1.csv", ["project", "time"])
gen_testcost_data("medium", testcases, timecost_groups["medium"])
gen_testcost_data("long", testcases, timecost_groups["long"])
