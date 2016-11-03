#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import os
from subprocess import Popen, DEVNULL, PIPE

import time

from support import utils


# TODO expected to output performance report on separated files
def evaluate(subject_path=os.curdir):
    subject_name = os.path.basename(subject_path)
    if not os.path.isdir(subject_path):
        raise Exception("Project: {}\nInvalid path: {}".format(subject_name, subject_path))

    os.chdir(subject_path)
    if os.path.exists("test-output.txt"):
        # No need to regenerate raw data if report files exist
        # TODO: add report file from performance
        return

    builder = utils.detect_builder()
    if builder:
        # TODO Use performance analyzer
        #
        #      Consider using a tool (e.g sar, mpstat...) to run in background
        #      and output the data in a file, so we can use the data later, if necessary
        #
        initial_t = time.time()
        p = Popen(builder.test, stderr=DEVNULL, stdout=PIPE)
        output_stream, error_stream = p.communicate()
        elapsed_t = time.time() - initial_t
        with open("test-output.txt", "w") as f:
            for line in output_stream.splitlines(keepends=True):
                f.write(line.decode())
            f.write("TIME-COST={}".format(round(elapsed_t)))


if __name__ == "__main__":
    print("Running test...")
    base_dir = os.path.abspath("..")
    try:
        evaluate(subject_path=os.path.join(base_dir, "subjects/okhttp"))
        evaluate(subject_path=os.path.join(base_dir, "subjects/guava"))
        print("Subjects successfully tested")
    except Exception as err:
        assert False, "Should not have raised exception for valid subject\n{}".format(err)
