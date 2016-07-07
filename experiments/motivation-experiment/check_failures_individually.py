#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from shutil import rmtree
from sys import argv

from utils import *

if __name__ == "__main__":
    freq = 10 #FIXME
    test_path = os.path.abspath(argv[1])
    logfile = open(argv[2])
    output_log = argv[3]
    output_log = os.path.join(os.path.abspath(os.curdir), output_log + "-mvnlog.txt")
    output_log = open(output_log, "w")

    reports_dir = os.path.join(test_path, "target", "surefire-reports")
    os.chdir(test_path)

    output = {}
    for line in logfile.readlines():
        if not line.startswith("[Statistics]"):
            test_case = line.split(" ")[0]

            output[test_case] = []
            rmtree(reports_dir)
            for f in range(freq):
                call(['mvn', '-Dtest=' + test_case, 'test'], stderr=output_log, stdout=output_log)

                xmlFile = report_from(reports_dir)
                xmlFileName = os.path.join(reports_dir, xmlFile)
                e = xml.etree.ElementTree.parse(xmlFileName).getroot()

                testcases = e.findall('testcase')
                assert len(testcases) == 1, "Should have only 1 testcase since a test is executed individually"
                atype = testcases[0]

                label = result_label(atype)
                key = atype.get('classname') + '#' + atype.get('name')
                assert key == test_case, "key: {0}, tc: {1}".format(key, test_case)
                output[key].append(label)

                # Prune if this execution has failed
                if label == 'F': break

    output_log.close()
    statistics = compute_statistcs(output)
    assert statistics['skips'] == 0, "Should not have skipped tests here"
    print "[Statistics] Failed Tests (parallel execution): {total}, " \
          "Passed (individually): {passes}".format(**statistics)
