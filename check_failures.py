#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call
from shutil import rmtree
from sys import argv

def result_label(atype):
    label = 'F'
    if (atype.find('failure') == None) and (atype.find('error') == None):
        label = 'P'
    return label

def report_from(path_dir):
    xmlFiles = []
    for root, dir, files in os.walk(path_dir):
        xmlFiles = [fi for fi in files if fi.startswith('TEST') and fi.endswith('.xml')]
    assert len(xmlFiles) == 1
    return xmlFiles[0]

if __name__ == "__main__":
    freq = int(argv[1])
    test_path = os.path.abspath(argv[2])
    logfile = open(argv[3])
    output_log = argv[4]
    output_log = os.path.join(os.path.abspath(os.curdir), output_log + "-check_failures.txt")
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
                for atype in e.findall('testcase'):
                    label = result_label(atype)
                    key = atype.get('classname') + '#' + atype.get('name')
                    assert key == test_case, "key: {0}, tc: {1}".format(key, test_case)
                    output[key].append(label);

    output_log.close()

    total = len(output)
    fails = 0
    for k,v in output.items():
        if 'F' in v:
            fails += 1
            print k, v
    print "[Statistics] Failed in parallel: {0}, Failed individually: {1}".format(total, fails)
