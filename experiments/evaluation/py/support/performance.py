#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import os
import time
from subprocess import Popen, DEVNULL, PIPE

from support import utils


def evaluate(subject_path=os.curdir, output_dir=os.curdir, override=False):
    subject_name = os.path.basename(subject_path)
    if not os.path.isdir(subject_path):
        raise Exception("Project: {}\nInvalid path: {}".format(subject_name, subject_path))

    builder_log_txt = os.path.join(output_dir, utils.BUILDER_LOG_TXT)
    performance_log_txt = os.path.join(output_dir, utils.PERFORMANCE_LOG_TXT)

    os.chdir(subject_path)
    builder = utils.detect_builder()
    if not builder:
        return

    if (not override) and builder.has_test_reports() \
            and os.path.exists(builder_log_txt) \
            and os.path.exists(performance_log_txt):
        return

    print("Running performance analysis")
    ctrl_c_signal = 2
    initial_t = time.time()

    analyzer_process = Popen(["sar", "-u", "-P", "ALL", "1"], stdout=PIPE)
    p = Popen(builder.test, stderr=DEVNULL, stdout=PIPE)
    test_out, test_err = p.communicate()

    analyzer_process.send_signal(ctrl_c_signal)
    elapsed_t = time.time() - initial_t

    analyzer_out, analyzer_err = analyzer_process.communicate()

    with open(performance_log_txt, "w") as f:
        for line in analyzer_out.splitlines(keepends=True):
            f.write(line.decode())

    with open(builder_log_txt, "w") as f:
        for line in test_out.splitlines(keepends=True):
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
