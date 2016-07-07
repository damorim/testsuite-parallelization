#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from sys import argv

from utils import *

if __name__ == "__main__":
    freq = 30 #FIXME
    test_path = argv[1]
    log_mvn = argv[2]
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
    statistics = compute_statistcs(results)
    print "[Statistics] All: {total}, Skipped: {skips}, Runs: {runs}, Failed (any): {fails}, ".format(**statistics)
