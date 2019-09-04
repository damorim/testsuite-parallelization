#!/usr/bin/env python3
import csv
import os
import re
import shutil
import xml.etree.ElementTree as etree
import subprocess

from subprocess import Popen, PIPE, call


def serialize_data_for(projects):
    entries = []
    listOfCheck = []
    for project_info in projects:
        if project_info["path_classname_error"]:
            split_result = project_info["path_classname_error"].split(",")
            for r in split_result:
                name_class = r.split(".")[-1]
                string_results = "./find_pom.rb --path ./projects/%s --file %s" % (project_info["name"],name_class)
                out = subprocess.Popen([string_results], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                stdout,stderr = out.communicate()
                result_pom = stdout.split()[0].decode('ascii')
                
                if listOfCheck:
                    if not result_pom in listOfCheck:
                        entries.append({"project": project_info["name"], "class": name_class,"pom": result_pom})
                else:
                    listOfCheck.append(result_pom)
                    entries.append({"project": project_info["name"], "class": name_class,"pom": result_pom})
           
    #print(entries)
    #print(list(set(entries)))
    fname = "dataset-flakiness.csv"
    with open(fname, "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["project", "class","pom"])
        writer.writeheader()
        writer.writerows(entries)

def analyze_data_result(projects):
    check_class_error = 0
    for project_info in projects:
        if project_info["path_classname_error"]:
            check_class_error += 1
            
    if check_class_error > 0:
        serialize_data_for(projects)
    else:
        print("Project without flakiness!")


if __name__ == "__main__":
    input_csv = "dataset-rawdata-mode.csv"
    if (not os.path.exists(input_csv)):
        print("Could not find path \"%s\"\nExiting..." % input_csv)

    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        projects = [e for e in reader]

    analyze_data_result(projects)

