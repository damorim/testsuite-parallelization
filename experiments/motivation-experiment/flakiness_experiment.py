#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from shutil import rmtree
from sys import argv

from utils import *

def run_tests(test_path, reports_dir, log_prefix):
    results = {}

    output_log = os.path.join(os.path.abspath(os.curdir), log_prefix + "-runlog.txt")
    output_log = open(output_log, "a")

    curdir = os.path.abspath(os.curdir)
    os.chdir(test_path)

    cmds = ['mvn', '-Dsurefire.rerunFailingTestsCount=100', 'test']
    call(cmds, stderr=output_log, stdout=output_log)

    reports = reports_from(reports_dir)
    for xmlFile in reports:
        xmlFileName = os.path.join(reports_dir, xmlFile)
        e = xml.etree.ElementTree.parse(xmlFileName).getroot()
        for atype in e.findall('testcase'):
            label = result_label(atype)
            test_name = atype.get('classname') + '#' + atype.get('name')

            if test_name in results:
                results[test_name].append(label);
            else:
                results[test_name] = [label]

    output_log.close()
    os.chdir(curdir)

    return results 


def rerun_individually(test_path, reports_dir, log_prefix, failures):
    results = {}

    output_log = os.path.join(os.path.abspath(os.curdir), log_prefix + "-rerunslog.txt")
    output_log = open(output_log, "a")

    curdir = os.path.abspath(os.curdir)
    os.chdir(test_path)

    RERUNS = 10
    for test_case in failures:
        results[test_case] = []
        for run in range(RERUNS):
            rmtree(reports_dir)

            call(['mvn', '-Dtest=' + test_case, 'test'], stderr=output_log, stdout=output_log)

            xmlfile = report_from(reports_dir)
            xmlfilename = os.path.join(reports_dir, xmlfile)
            e = xml.etree.ElementTree.parse(xmlfilename).getroot()

            testcases = e.findall('testcase')
            if not len(testcases) == 1:
                print " - Test case: %s" %test_case
                print " - Should have only 1 test case but found %d" %(len(testcases))
                print " - Resolution: Skipping this run"
                continue

            testcase_xml = testcases[0]
            label = result_label(testcase_xml)
            results[test_case].append(label)

            # prune if this execution has failed
            if label == FAIL_LABEL: break

    output_log.close()
    os.chdir(curdir)

    return results 


def failures_from(tests):
    return filter(lambda t: FAIL_LABEL in tests[t], tests.keys())


def make_report(report_name, iterable):
    if len(iterable):
        with open(report_name, 'w') as report:
            for item in iterable:
                report.write(item)
                report.write("\n")

        report.close()


if __name__ == "__main__":
    test_path = argv[1]
    log_prefix = argv[2]

    test_path = os.path.abspath(test_path)
    reports_dir = os.path.join(test_path, "target", "surefire-reports")

    # Run tests in parallel
    test_results = run_tests(test_path, reports_dir, log_prefix)
    pef_failures = failures_from(test_results)
    make_report(log_prefix + "-PEF.txt", pef_failures)

    statistics = compute_statistcs(test_results)
    print "[Statistics] All: {total}, Skipped: {skips}, Runs: {runs}, " \
          "Failed (any): {fails}, ".format(**statistics)

    if len(pef_failures):
        # Run individually failing tests
        test_results = rerun_individually(test_path, reports_dir, log_prefix, pef_failures)
        sef_failures = failures_from(test_results)
        make_report(log_prefix + "-SEF.txt", sef_failures)

        statistics = compute_statistcs(test_results)
        print "[Statistics] Failed Tests (parallel execution): {total}, " \
            "Passed (individually): {passes}".format(**statistics)

