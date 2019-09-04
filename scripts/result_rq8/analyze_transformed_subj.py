#!/usr/bin/env python3
import csv
import os
import re
import shutil
import xml.etree.ElementTree as etree
import subprocess

from subprocess import Popen, PIPE, call


def analyze_data_result(projects):
    for project_info in projects:
        pom_str = project_info["pom"]
        split_str = pom_str.split("/")
        index_elem = split_str.index("projects")
        split_str[index_elem] = "project_transformed"
        result_path = "/".join(split_str)
        call("./transform_seq.rb --path \"%s\"" % result_path, shell=True)
        print("Generated modified pom.xml of the subject")
            

if __name__ == "__main__":
    input_csv = "dataset-flakiness.csv"
    if (not os.path.exists(input_csv)):
        print("Could not find path \"%s\"\nExiting..." % input_csv)

    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        projects = [e for e in reader]

    analyze_data_result(projects)

