#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from shutil import rmtree
from sys import argv

from utils import *

THRESHOLD = 5

def find_parallel_failures(test_path, reports_dir, log_mvn):
    results = {}
    failing_tests = []

    log_mvn = os.path.join(os.path.abspath(os.curdir), log_mvn + "-mvnlog.txt")
    log_mvn = open(log_mvn, "a")

    curdir = os.path.abspath(os.curdir)
    os.chdir(test_path)

    reruns = 0
    runs = 0
    has_exausted = False
    while (reruns < THRESHOLD):
        call(['mvn', 'test'], stderr=log_mvn, stdout=log_mvn)
        reports = reports_from(reports_dir)

        # Assume this execution has exausted (ie no new failing tests discovered)
        has_exausted =  True
        for xmlFile in reports:
            xmlFileName = os.path.join(reports_dir, xmlFile)
            e = xml.etree.ElementTree.parse(xmlFileName).getroot()
            for atype in e.findall('testcase'):
                label = result_label(atype)
                key = atype.get('classname') + '#' + atype.get('name')

                # Check if this is a failing test
                if label == FAIL_LABEL and not key in failing_tests:
                    failing_tests.append(key)
                    has_exausted = False
                    reruns = 0

                if key in results:
                    results[key].append(label);
                else:
                    results[key] = [label]

        runs += 1
        if has_exausted:
            reruns += 1

    log_mvn.close()
    os.chdir(curdir)

    print "Parallel Flaky Tests"
    for test in failing_tests:
        print " -",test,results[test]

    statistics = compute_statistcs(results)
    print "[Runs]:", runs, "Threshold:" reruns
    print "[Statistics] All: {total}, Skipped: {skips}, Runs: {runs}, " \
          "Failed (any): {fails}, ".format(**statistics)

    return failing_tests


def check_failures_individually(test_path, reports_dir, output_log, failures):
    output = {}

    output_log = os.path.join(os.path.abspath(os.curdir), output_log + "-mvnlog.txt")
    output_log = open(output_log, "a")

    curdir = os.path.abspath(os.curdir)
    os.chdir(test_path)

    for test_case in failures:
        output[test_case] = []
        rmtree(reports_dir)
        for f in range(THRESHOLD):
            call(['mvn', '-Dtest=' + test_case, 'test'], stderr=output_log, stdout=output_log)

            xmlfile = report_from(reports_dir)
            xmlfilename = os.path.join(reports_dir, xmlfile)
            e = xml.etree.ElementTree.parse(xmlfilename).getroot()

            testcases = e.findall('testcase')
            assert len(testcases) == 1, "Should have only 1 testcase since a test is executed individually"
            atype = testcases[0]

            label = result_label(atype)
            key = atype.get('classname') + '#' + atype.get('name')
            assert key == test_case, "key: {0}, tc: {1}".format(key, test_case)
            output[key].append(label)

            # prune if this execution has failed
            if label == 'f': break

    output_log.close()
    os.chdir(curdir)

    print "Sequential Flaky Tests"
    for test,r in output.items():
        if 'F' in r:
            print " -",test,r

    statistics = compute_statistcs(output)
    assert statistics['skips'] == 0, "Should not have skipped tests here"
    print "[Statistics] Failed Tests (parallel execution): {total}, " \
          "Passed (individually): {passes}".format(**statistics)


if __name__ == "__main__":
    test_path = argv[1]
    log_mvn = argv[2]

    test_path = os.path.abspath(test_path)
    reports_dir = os.path.join(test_path, "target", "surefire-reports")

    failures = find_parallel_failures(test_path, reports_dir, log_mvn)
    check_failures_individually(test_path, reports_dir, log_mvn, failures)

