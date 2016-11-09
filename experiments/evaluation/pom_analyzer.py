#!/usr/bin/env python3
import argparse
import csv
import os
import subprocess
from collections import Counter
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError


def is_surefire_node(node):
    return len([n for n in node if n.text == "maven-surefire-plugin"])


def inspect_pom_file(xml_path):
    namespace = {"ns": "http://maven.apache.org/POM/4.0.0"}
    frequency = Counter(L0=0, L1=0, L2=0, L3=0, UNKNOWN=0)
    try:
        root = ElementTree.parse(xml_path).getroot()
    except ParseError as err:
        print(xml_path, err)
        return frequency

    surefire_nodes = [c for c in root.iter('{%s}plugin' % namespace['ns']) if is_surefire_node(c)]
    for node in surefire_nodes:
        config_node = node.find("{%s}configuration" % namespace['ns'])
        if config_node is not None:
            parallel_setting_node = config_node.find("{%s}parallel" % namespace['ns'])
            if parallel_setting_node is not None:
                if parallel_setting_node.text == "classes":
                    frequency["L2"] += 1
                elif parallel_setting_node.text == "none":
                    frequency["L0"] += 1
                elif parallel_setting_node.text == "methods":
                    frequency["L1"] += 1
                elif parallel_setting_node.text in ["classesAndMethods", "both", "all"]:
                    frequency["L3"] += 1
                else:
                    frequency["UNKNOWN"] += 1
        else:
            frequency["L0"] += 1

    return frequency


def find_prevalence(subject_path=os.curdir, recursive=False):
    os.chdir(subject_path)

    find_command = ["find", "."]
    if not recursive:
        find_command.extend(["-maxdepth", "1"])
    find_command.extend(["-name", "pom.xml"])

    # get all pom.xml paths
    output = subprocess.check_output(find_command)

    # for each pom file, inspect it!
    settings_frequency = Counter(L0=0, L1=0, L2=0, L3=0, UNKNOWN=0)
    files = 0
    for xml_path in output.decode().splitlines():
        files += 1
        frequency = inspect_pom_file(xml_path)
        settings_frequency.update(frequency)
    return settings_frequency, files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to analyze (columns required: SUBJECT and BUILDER)")
    parser.add_argument("output", help="csv file to output data")
    parser.add_argument("-r", "--recursive", help="runs the prevalence recursively", action="store_true")
    args = parser.parse_args()

    input_csv = os.path.abspath(args.input)
    output_file = os.path.abspath(args.output)

    subjects = []
    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["BUILDER"] == "Maven":
                subjects.append(row["SUBJECT"])

    with open(output_file, "w") as f:
        f.write("subject,files,L0,L1,L2,L3,UNKNOWN\n")

    SUBJECTS_HOME = os.path.abspath("subjects")
    for i in range(len(subjects)):
        subject = subjects[i]
        target = os.path.join(SUBJECTS_HOME, subject)
        if os.path.exists(target):
            (counter, files_cnt) = find_prevalence(subject_path=target, recursive=args.recursive)
            if sum([counter[t] for t in counter.keys()]):
                with open(output_file, "a") as f:
                    f.write("{},{},{},{},{},{},{}\n".format(subject, files_cnt,
                                                            counter['L0'], counter['L1'],
                                                            counter['L2'], counter['L3'],
                                                            counter['UNKNOWN']))
