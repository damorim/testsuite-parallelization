import csv
import os
from collections import namedtuple
from datetime import datetime
from time import time

# Results from the execution of a subject with a specific ExecutionParam
ExecutionResults = namedtuple("ExecutionResults", "reports, process_execution, elapsed_time")

# Experiment results consist in all results from each ExecutionParam and ParallelPrevalenceData
ExperimentResults = namedtuple("ExperimentResults", "parallel_data, execution_data")

# Parameters of experiment execution for a subject
ExecutionParams = namedtuple("ExecutionParams", "log_file, args, name, reports_dir")

ParallelPrevalenceData = namedtuple("ParallelPrevalenceData", "frequency, files")

StandardParams = ExecutionParams(reports_dir="surefire-ST-reports",
                                 log_file="test-log-default.txt",
                                 args=None, name="Standard")

L0Params = ExecutionParams(reports_dir="surefire-L0-reports",
                           log_file="test-log-sequential.txt",
                           args=["-P", "L0"], name="L0")


class OutputRegister(object):
    ERROR_CSV_LOG = os.path.abspath("experiment-errors.csv")
    ERROR_LOG_HEADER = ("when", "name", "url", "rev", "cause")

    def __init__(self, output_dir=os.curdir):
        # Timestamp used across all output files
        timestamp = datetime.fromtimestamp(time()).strftime('%y%m%d%H%M')
        output_dir = output_dir

        self._subjects_csv = os.path.join(output_dir, "verified-subjects-{}.csv".format(timestamp))
        with open(self._subjects_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "url", "rev"])
            writer.writeheader()

        self._parallel_prev_csv = os.path.join(output_dir, "dataset-parprev-{}.csv".format(timestamp))
        with open(self._parallel_prev_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "files", "L0", "L1", "L2", "L3", "FL0", "FL1", "Unknown"])
            writer.writeheader()

    def results(self, name, data):
        # TODO save execution data
        with open(self._parallel_prev_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "files", "L0", "L1", "L2", "L3", "FL0", "FL1", "Unknown"])
            row = {"name": name, "files": data.parallel_data.files}
            row.update(data.parallel_data.frequency)
            writer.writerow(row)

    def subject(self, name, url, revision):
        with open(self._subjects_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "url", "rev"])
            writer.writerow({"name": name, "url": url, "rev": revision})

    @classmethod
    def error(cls, when, name, url, rev, cause):
        with open(cls.ERROR_CSV_LOG, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cls.ERROR_LOG_HEADER)
            writer.writerow({"name": name, "url": url, "when": when, "cause": cause, "rev": rev})
