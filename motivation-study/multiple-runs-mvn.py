#!/usr/bin/env python2
import os
import xml.etree.ElementTree

from subprocess import call, STDOUT
from sys import argv

if not (len(argv) == 4):
    print "Usage: {name} <repeats> <projdir> <testpath>".format(name=__file__)
    exit(1)

## constants
NUM_REPEATS = int(argv[1])
PROJECT_DIR = argv[2]
TEST_DIR = argv[3]

projectPath = os.path.abspath(PROJECT_DIR)

os.chdir(projectPath)
call(['mvn', '-q', '-DskipTests', 'clean'])  # MAVEN SPECIFIC COMMAND

os.chdir(TEST_DIR)
output = {}

FNULL=file(os.devnull, 'wb')
for x in range(NUM_REPEATS):
    call(['mvn', 'test'], stdout=FNULL, stderr=STDOUT)  # MAVEN SPECIFIC COMMAND

     # MAVEN SPECIFIC OUTPUT FORMAT
    reportsPathName = os.path.abspath('target/surefire-reports')
    xmlFiles = []
    for root, dir, files in os.walk(reportsPathName):
        xmlFiles = [fi for fi in files if fi.startswith('TEST') and fi.endswith('.xml')]

    # MAVEN SPECIFIC OUTPUT FORMAT
    for xmlFile in xmlFiles:
        xmlFileName = os.path.join(reportsPathName, xmlFile)
        e = xml.etree.ElementTree.parse(xmlFileName).getroot()
        for atype in e.findall('testcase'):

            label = 'F'
            if (atype.find('failure') == None) and (atype.find('error') == None):
                label = 'P'

            key = atype.get('classname') + '.' + atype.get('name')
            if key in output:
                output[key].append(label); ## should be the output (pass or fail)
            else:
                output[key] = [label]
FNULL.close()
# PRINT
print "Summary: {0} Tests run".format(len(output))
for test,results in output.items():
    if ('F' in results):
        print test, results
