#!/usr/bin/env python3
import csv
from sys import argv


def writetocsv(data, name):
    if len(data) == 0:
        return
    with open(name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sorted(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


entries = []

for input_csv in argv[1:]:
    with open(input_csv, newline="") as out:
        reader = csv.DictReader(out)
        [entries.append(entry) for entry in reader]

total = len(entries)

unable_to_compile = [e for e in entries if int(e["compile_exit_code"]) != 0]
entries = [e for e in entries if int(e["compile_exit_code"]) == 0]
tests_not_found = [e for e in entries if int(e["tests"]) == 0]
entries = [e for e in entries if int(e["tests"]) > 0]

has_failures = [e for e in entries if int(e["test_exit_code"]) != 0]
no_failures = [e for e in entries if int(e["test_exit_code"]) == 0]

print("Total entries:", total)
print("Unable to compile:", len(unable_to_compile))
print("Tests not found:", len(tests_not_found))
print("Has failures:",len(has_failures))
print("No failures:",len(no_failures))

assert total == len(unable_to_compile) + len(tests_not_found) + len(has_failures) + len(no_failures)

writetocsv(no_failures, "nofailures.csv")
writetocsv(has_failures, "hasfailures.csv")
writetocsv(tests_not_found, "notests.csv")
writetocsv(unable_to_compile, "cantcompile.csv")

