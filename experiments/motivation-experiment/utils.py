import os

PASS_LABEL = 'P'
IGNORE_LABEL = 'S'
FAIL_LABEL = 'F'

def result_label(atype):
    '''Returns a label for the given xml report node representing a testcase.'''
    if atype.find('skipped') is not None:
        return IGNORE_LABEL

    for tag in ['failure', 'error', 'flakyError', 'flakyFailure']:
        if atype.find(tag) is not None:
            return FAIL_LABEL

    return PASS_LABEL


def report_from(path_dir):
    '''Returns the *ONLY* TEST-<testname>.xml file name from the given path.

    Use this method if you want to ensure 'path_dir' contains only one report.
    In case more there are more xml reports, this function will abort the execution.
    Use 'reports_from' if you expect more files in 'path_dir'.
    '''
    xmlFiles = []
    for root, dir, files in os.walk(path_dir):
        xmlFiles = [fi for fi in files if fi.startswith('TEST') and fi.endswith('.xml')]
    assert len(xmlFiles) == 1, "Should have only one xml reports: {0} (found)".format(len(xmlFiles))
    return xmlFiles[0]


def reports_from(path_dir):
    '''Returns a list of all TEST-<testname>.xml file names from the given path.'''
    xmlFiles = []
    for root, dir, files in os.walk(path_dir):
        xmlFiles = [fi for fi in files if fi.startswith('TEST') and fi.endswith('.xml')]
    return xmlFiles


def compute_statistcs(results):
    statistics = {}

    statistics['total'] = len(results)
    statistics['fails'] = 0
    statistics['skips'] = 0

    for t,r in results.items():
        if 'S' in r:
            statistics['skips'] += 1
        elif 'F' in r:
            statistics['fails'] += 1

    statistics['runs'] = statistics['total'] - statistics['skips']
    statistics['passes'] = statistics['runs'] - statistics['fails']

    return statistics

if __name__ == "__main__":
    print "Usage: 'from utils import *' in a python2 script"
