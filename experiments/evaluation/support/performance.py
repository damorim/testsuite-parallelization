#!/usr/bin/python3
import os
from subprocess import Popen, STDOUT, DEVNULL

from support import utils


def evaluate(subject_path):
    subject_name = os.path.basename(subject_path)
    if not os.path.isdir(subject_path):
        raise Exception("Project: {}\nInvalid path: {}".format(subject_name, subject_path))

    os.chdir(subject_path)
    builder = utils.detect_builder()
    if builder:
        # TODO Use performance analyzer
        #
        #      Consider using a tool (e.g sar, mpstat...) to run in background
        #      and output the data in a file, so we can use the data later, if necessary
        #
        p = Popen(builder.test, stderr=STDOUT, stdout=DEVNULL)
        p.communicate()

if __name__ == "__main__":
    print("Running test...")
    base_dir = os.path.abspath("..")
    try:
        evaluate(subject_path=os.path.join(base_dir, "subjects/okhttp"))
        evaluate(subject_path=os.path.join(base_dir, "subjects/guava"))
        print("Subjects successfully tested")
    except Exception as err:
        assert False, "Should not have raised exception for valid subject\n{}".format(err)
