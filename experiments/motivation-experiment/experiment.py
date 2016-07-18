#!/usr/bin/python2
import os

import xml.etree.ElementTree as et

from datetime import datetime
from time import time

from subprocess import call
from shutil import rmtree
from sys import argv
from os import path

class TestReport:
    def __init__(self):
        self.success = set({})
        self.fail = set({})
        self.ignored = set({})
        self.flaky = set({})
        self.total = 0

    def __repr__(self):
        repr = "Total: {0}, Ignored: {1}, Runs: {2}, Success: {3}, Flaky: {4}, Fail: {5}"
        return repr.format(self.total, len(self.ignored), self.total - len(self.ignored), \
                           len(self.success), len(self.flaky), len(self.fail))

    def addpass(self, tc):
        self.total += 1
        self.success.add(tc)
        assert self.total == (len(self.success) + len(self.fail) \
                              + len(self.ignored) + len(self.flaky))

    def addskip(self, tc):
        self.total += 1
        self.ignored.add(tc)
        assert self.total == (len(self.success) + len(self.fail) \
                              + len(self.ignored) + len(self.flaky))

    def addfail(self, tc):
        self.total += 1
        self.fail.add(tc)
        assert self.total == (len(self.success) + len(self.fail) \
                              + len(self.ignored) + len(self.flaky))
    def addflaky(self, tc):
        self.total += 1
        self.flaky.add(tc)
        assert self.total == (len(self.success) + len(self.fail) \
                              + len(self.ignored) + len(self.flaky))


def collect_test_results(directory):
    report = TestReport()
    xmlfiles = [ f for f in os.listdir(directory) if f.startswith('TEST') and f.endswith('.xml') ]
    hasChild = lambda n,t: n.find(t) is not None
    for xmlfile in xmlfiles:
        root = et.parse(os.path.join(reports_dir, xmlfile)).getroot()
        for tc in root.findall('testcase'):
            tcname = "{0}#{1}".format(tc.get('classname'), tc.get('name'))
            if not len(list(tc)):
                report.addpass(tcname)
            elif hasChild(tc, 'skipped'):
                report.addskip(tcname)
            elif hasChild(tc, 'flakyError') or hasChild(tc, 'flakyFailure'):
                report.addflaky(tcname)
            else:
                report.addfail(tcname)
    return report


def system_call(cmds, logpath=os.devnull):
    with open(logpath, 'a') as log:
        starttime = time()
        call(cmds, stdout=log, stderr=log)
        elapsedtime = time() - starttime
        return elapsedtime


# Input parameters
version = argv[1]
project_path = argv[2]
test_rel_path = argv[3]

# Constants
base_dir = path.abspath(os.curdir)
project_root = path.abspath(project_path)
test_path = path.join(project_root, test_rel_path)
project_name = path.basename(project_root)

print_msg = "Setup:\nVersion: {0}\nProject Path: {1}\nTest Path:{2}"
print print_msg.format(version, project_root, test_path)

# Checking elapsed time
log_prefix = "{0}-{1}-".format(project_name, version)
os.chdir(test_path)
elapsedtime = system_call(['mvn', '-Dmaven.javadoc.skip', 'test'])
print "Test Elapsed time:", elapsedtime

# Logging time
log_file_path = os.path.join(base_dir, log_prefix + "time.txt")
with open(log_file_path, "a") as timelog:
    timelog.write(str(elapsedtime) + "\n")

timestamp = datetime.fromtimestamp(time()).strftime("%m%d%H%M")
log_prefix = "{0}-{1}-{2}-".format(project_name, version, timestamp)

# FLAKINESS EXPERIMENT
BOUND = 5
reports_dir = path.join(test_path, 'target', 'surefire-reports')

# Maven rerun
print "\nMaven RERUN [BOUND: {0}]".format(BOUND)
rmtree(reports_dir)
log_file_path = os.path.join(base_dir, log_prefix + "flakiness-mvnrerun.txt")
elapsedtime = system_call(['mvn', '-Dsurefire.rerunFailingTestsCount=' + str(BOUND),
                           '-Dmaven.javadoc.skip','test'], log_file_path)

print "Elapsed time:", elapsedtime
report = collect_test_results(reports_dir)
print report

## Iterative rerun
#print "\nIterative rerun [BOUND: {0}]".format(BOUND)
#rmtree(reports_dir)
#log_file_path = os.path.join(base_dir, log_prefix + "flakiness-rerun.txt")
#elapsedtime = 0
#failures = set({})
#for rep in range(BOUND):
#    elapsedtime =+ system_call(['mvn','-Dmaven.javadoc.skip','test'], log_file_path)
#    report = collect_test_results(reports_dir)
#    print "#{0}:".format(rep + 1), report
#    failures = failures.union(report.fail)
#
#print "Total Fails:", len(failures)
#
#individual_fails = set({})
#for tc in failures:
#    for i in range(BOUND):
#        rmtree(reports_dir)
#        elapsedtime += system_call(['mvn', '-Dmaven.javadoc.skip', '-Dtest=' + tc,
#                                    'test'], log_file_path)
#        report = collect_test_results(reports_dir)
#        if len(report.fail):
#            individual_fails.add(tc)
#            break
#
#print "Elapsed time:", elapsedtime
#print "Total:", len(failures), "Success:", len(failures) - len(individual_fails), \
#      "Fail:", len(individual_fails)
#
## Exhaustive execution
#print "\nExhaustive execution [THRESHOLD: {0}]".format(BOUND)
#rmtree(reports_dir)
#log_file_path = os.path.join(base_dir, log_prefix + "flakiness-exhaustive.txt")
#elapsedtime = 0
#failures = set({})
#
#runs = 0
#i = 1
#while runs < BOUND:
#    elapsedtime =+ system_call(['mvn','-Dmaven.javadoc.skip','test'], log_file_path)
#
#    exhausted = True
#    report = collect_test_results(reports_dir)
#    old_size = len(failures)
#    failures = failures.union(report.fail)
#    if len(failures) > old_size:
#        exhausted = False
#
#    print "#{0}: {1},".format(i, exhausted), report
#
#    if exhausted:
#        runs += 1
#    else:
#        runs = 0
#
#    i += 1
#
#print "Total Fails:", len(failures)
#
#individual_fails = set({})
#for tc in failures:
#    for i in range(BOUND):
#        rmtree(reports_dir)
#        elapsedtime += system_call(['mvn', '-Dmaven.javadoc.skip', '-Dtest=' + tc,
#                                    'test'], log_file_path)
#        report = collect_test_results(reports_dir)
#        if len(report.fail):
#            individual_fails.add(tc)
#            break
#
#print "Elapsed time:", elapsedtime
#print "Total:", len(failures), "Success:", len(failures) - len(individual_fails), \
#      "Fail:", len(individual_fails)
