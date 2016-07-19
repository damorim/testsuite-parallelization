#!/usr/bin/python2
import os

import xml.etree.ElementTree as et

from datetime import datetime
from time import time

from subprocess import call
from shutil import rmtree, copy
from sys import argv
from os import path


# Input parameters
build_files_path = argv[1]
project_path = argv[2]
test_rel_path = argv[3]

# Constants
BASE_DIR = path.abspath(os.curdir)

BUILD_FILES_DIR = path.abspath(build_files_path)
PROJECT_ROOT = path.abspath(project_path)
TEST_PATH = path.join(PROJECT_ROOT, test_rel_path)
PROJECT_NAME = path.basename(PROJECT_ROOT)


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


def iterative_run(BOUND, reports_dir, log_file_path):
    print "\nIterative rerun [BOUND: {0}]".format(BOUND)
    elapsedtime = 0
    failures = set({})
    for rep in range(BOUND):
        elapsedtime =+ system_call(['mvn','-Dmaven.javadoc.skip','test'], log_file_path)
        report = collect_test_results(reports_dir)
        print "#{0}:".format(rep + 1), report
        failures = failures.union(report.fail)

    print "Total Fails:", len(failures)

    individual_fails = set({})
    for tc in failures:
        for i in range(BOUND):
            rmtree(reports_dir)
            elapsedtime += system_call(['mvn', '-Dmaven.javadoc.skip', '-Dtest=' + tc,
                                        'test'], log_file_path)
            report = collect_test_results(reports_dir)
            if len(report.fail):
                individual_fails.add(tc)
                break

    print "Elapsed time:", elapsedtime
    print "Total:", len(failures), "Success:", len(failures) - len(individual_fails), \
          "Fail:", len(individual_fails)


def mvnrerun(BOUND, reports_dir, log_file_path):
    print "\nMaven RERUN [BOUND: {0}]".format(BOUND)
    elapsedtime = system_call(['mvn', '-Dsurefire.rerunFailingTestsCount=' + str(BOUND),
                            '-Dmaven.javadoc.skip','test'], log_file_path)

    print "Elapsed time:", elapsedtime
    report = collect_test_results(reports_dir)
    print report


def exhaustive_run(BOUND, reports_dir, log_file_path):
    print "\nExhaustive execution [THRESHOLD: {0}]".format(BOUND)
    elapsedtime = 0
    failures = set({})

    runs = 0
    i = 1
    while runs < BOUND:
        elapsedtime =+ system_call(['mvn','-Dmaven.javadoc.skip','test'], log_file_path)

        exhausted = True
        report = collect_test_results(reports_dir)
        old_size = len(failures)
        failures = failures.union(report.fail)
        if len(failures) > old_size:
            exhausted = False

        print "#{0}: {1},".format(i, exhausted), report

        runs = 0 if not exhausted else (runs + 1) 
        i += 1

    print "Total Fails:", len(failures)

    individual_fails = set({})
    for tc in failures:
        for i in range(BOUND):
            rmtree(reports_dir)
            elapsedtime += system_call(['mvn', '-Dmaven.javadoc.skip', '-Dtest=' + tc,
                                        'test'], log_file_path)
            report = collect_test_results(reports_dir)
            if len(report.fail):
                individual_fails.add(tc)
                break

    print "Elapsed time:", elapsedtime
    print "Total:", len(failures), "Success:", len(failures) - len(individual_fails), \
          "Fail:", len(individual_fails)


def flakiness_experiment():
    print "Checking flakiness"

    reports_dir = path.join(TEST_PATH, 'target', 'surefire-reports')
    ignore = ['seq.xml']

    buildfiles = [ f for f in os.listdir(BUILD_FILES_DIR) ]
    for buildfile in buildfiles:
        if buildfile not in ignore:
            buildfile_path = path.join(BUILD_FILES_DIR, buildfile)
            os.remove(path.join(TEST_PATH, 'pom.xml'))
            copy(buildfile_path, TEST_PATH)
            os.rename(path.join(TEST_PATH, buildfile),
                    path.join(TEST_PATH, 'pom.xml'))
            version = buildfile.replace(".xml", "")

            print "Testing version", version

            rmtree(reports_dir)
            BOUND = 5

            # FIXME
            #log_file_path = log_file_path_prefix + "flakiness-mvnrerun.txtbb"
            #mvnrerun(BOUND, reports_dir, log_file_path)

            #log_file_path = log_file_path_prefix + "flakiness-rerun.txt"
            #rmtree(reports_dir)
            #iterative_run(BOUND, reports_dir, log_file_path)

            #log_file_path = log_file_path_prefix + "flakiness-exhaustive.txt"
            #rmtree(reports_dir)
            #exhaustive_run(BOUND, reports_dir, log_file_path)


def compare_elapsed_time():
    print "Comparing elapsed times\n"
    times = {}

    ts = datetime.fromtimestamp(time()).strftime('%m%d%H%M')
    logname = '{0}-elapsedtime-{1}.txt'.format(PROJECT_NAME, ts)
    log_path = path.join(BASE_DIR, logname)

    buildfiles = [ f for f in os.listdir(BUILD_FILES_DIR) ]
    for buildfile in buildfiles:
        buildfile_path = path.join(BUILD_FILES_DIR, buildfile)
        os.remove(path.join(TEST_PATH, 'pom.xml'))
        copy(buildfile_path, TEST_PATH)
        os.rename(path.join(TEST_PATH, buildfile),
                  path.join(TEST_PATH, 'pom.xml'))
        version = buildfile.replace(".xml", "")

        print "\t- Testing version", version,
        elapsedtime = system_call(['mvn', '-X', '-Dsurefire.timeout=1800',
                                   '-Dmaven.javadoc.skip', 'test'], log_path)
        times[version] = elapsedtime
        print "...Finished!"

    print "\nSeq, ParClasses, ParMethods, ParBoth, ForkSeq, ForkPar"
    print "{seq}, {parallel-classes}, {parallel-methods}, {parallel-both}, " \
          "{fork-only}, {fork-parallel}".format(**times)

    speedup = lambda ts: "%.2fx" %(times['seq'] / ts)
    labels = ['parallel-classes', 'parallel-methods', 'parallel-both',
              'fork-only', 'fork-parallel']

    output = PROJECT_NAME + " & <TESTCASES> & "
    if (times['seq'] < 59):
        output += "%ds" %(times['seq'])
    else:
        output += "%dm:%ds" %(times['seq'] // 60, times['seq'] % 60)

    for label in labels:
        output += " & " + speedup(times[label])

    print output
    log_file_path = path.join(BASE_DIR, PROJECT_NAME + "-speedup.txt")
    with open(log_file_path, 'a') as log:
        log.write(output)
        log.write('\n')

# MAIN
print "Compiling project"
os.chdir(PROJECT_ROOT)
system_call(['mvn','clean','install','-DskipTests','-Dmaven.javadoc.skip'])

os.chdir(TEST_PATH)

compare_elapsed_time()
#flakiness_experiment()
