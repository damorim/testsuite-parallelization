#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from sys import argv

def reports_from(path_dir):
    xmlFiles = []
    for root, dir, files in os.walk(path_dir):
        xmlFiles = [fi for fi in files if fi.startswith('TEST') and fi.endswith('.xml')]
    return xmlFiles

def result_label(atype):
    if not (atype.find('skipped') == None):
        return 'S'
    elif (atype.find('failure') == None) and (atype.find('error') == None):
        return 'P'
    return 'F'

if __name__ == "__main__":
    freq = int(argv[1])
    test_path = argv[2]
    log_mvn = argv[3]
    results = {}

    log_mvn = os.path.join(os.path.abspath(os.curdir), log_mvn + "-mvnlog.txt")
    log_mvn = open(log_mvn, "w")

    test_path = os.path.abspath(test_path)
    os.chdir(test_path)
    reports_dir = os.path.join(test_path, "target", "surefire-reports")

    for i in range(freq):
        call(['mvn', 'test'], stderr=log_mvn, stdout=log_mvn)
        reports = reports_from(reports_dir)
        for xmlFile in reports:
            xmlFileName = os.path.join(reports_dir, xmlFile)
            e = xml.etree.ElementTree.parse(xmlFileName).getroot()
            for atype in e.findall('testcase'):
                label = result_label(atype)
                key = atype.get('classname') + '#' + atype.get('name')
                if key in results:
                    results[key].append(label);
                else:
                    results[key] = [label]

    log_mvn.close()

    # output failed tests and frequency
    total = len(results)
    fails = 0
    skipped = 0
    for t,r in results.items():
        if 'S' in r:
            skipped += 1
        elif 'F' in r:
            fails += 1
            print t, r

    print "[Statistics] All: {0}, Skipped: {1}, Runs: {2}, Failed (any): {3}, ".format(total, skipped, (total-skipped), fails)
