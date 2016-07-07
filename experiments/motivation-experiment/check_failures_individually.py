#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from shutil import rmtree
from sys import argv

from utils import *

if __name__ == "__main__":
    freq = 10 #fixme
    test_path = os.path.abspath(argv[1])
    logfile = open(argv[2])
    output_log = argv[3]
    output_log = os.path.join(os.path.abspath(os.curdir), output_log + "-mvnlog.txt")
    output_log = open(output_log, "w")

    reports_dir = os.path.join(test_path, "target", "surefire-reports")
    os.chdir(test_path)

    output = {}
    for line in logfile.readlines():
        if not line.startswith("[statistics]"):
            test_case = line.split(" ")[0]

            output[test_case] = []
            rmtree(reports_dir)
            for f in range(freq):
                call(['mvn', '-dtest=' + test_case, 'test'], stderr=output_log, stdout=output_log)

                xmlfile = report_from(reports_dir)
                xmlfilename = os.path.join(reports_dir, xmlfile)
                e = xml.etree.elementtree.parse(xmlfilename).getroot()

                testcases = e.findall('testcase')
                assert len(testcases) == 1, "should have only 1 testcase since a test is executed individually"
                atype = testcases[0]

                label = result_label(atype)
                key = atype.get('classname') + '#' + atype.get('name')
                assert key == test_case, "key: {0}, tc: {1}".format(key, test_case)
                output[key].append(label)

                # prune if this execution has failed
                if label == 'f': break

    output_log.close()
    statistics = compute_statistcs(output)
    assert statistics['skips'] == 0, "should not have skipped tests here"
    print "[statistics] failed tests (parallel execution): {total}, " \
          "passed (individually): {passes}".format(**statistics)
