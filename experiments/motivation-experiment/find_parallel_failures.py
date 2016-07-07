#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from sys import argv

from utils import *

freq = 10 #FIXME

def find_parallel_failures(test_path, reports_dir, log_mvn):
    results = {}

    log_mvn = os.path.join(os.path.abspath(os.curdir), log_mvn + "-mvnlog.txt")
    log_mvn = open(log_mvn, "w")

    curdir = os.path.abspath(os.curdir)
    os.chdir(test_path)

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
    os.chdir(curdir)

    failing_tests = []
    for test,r in results.items():
        if 'F' in r:
            failing_tests.append(test)
            print test,r

    statistics = compute_statistcs(results)
    print "[Statistics] All: {total}, Skipped: {skips}, Runs: {runs}, Failed (any): {fails}, ".format(**statistics)

    return failing_tests

def check_failures_individually(test_path, reports_dir, output_log):
    # TODO: Should merge this with the other script
    pass

if __name__ == "__main__":
    test_path = argv[1]
    log_mvn = argv[2]

    test_path = os.path.abspath(test_path)
    reports_dir = os.path.join(test_path, "target", "surefire-reports")

    failures = find_parallel_failures(test_path, reports_dir, log_mvn)
    check_failures_individually(test_path, reports_dir, failures)

