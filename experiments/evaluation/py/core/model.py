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

    LogFileParams = namedtuple("LogFileParams", "name_template, cols")
    SUBJECTS_CSV = LogFileParams(name_template="verified-subjects-{}.csv",
                                 cols=["name", "url", "rev"])

    PARALLEL_CSV = LogFileParams(name_template="dataset-parprev-{}.csv",
                                 cols=["name", "files", "L0", "L1", "L2", "L3", "FL0", "FL1", "Unknown"])

    EXECUTION_CSV = LogFileParams(name_template="dataset-execution-{}.csv",
                                  cols=["mode", "name", "elapsed_time", "r_time", "r_skipped", "r_tests", "r_failures",
                                        "t_user", "t_sys", "t_wall"])

    def __init__(self, output_dir=os.curdir):
        # Timestamp used across all output files
        self.__ts = datetime.fromtimestamp(time()).strftime('%y%m%d%H%M')
        self.__output_dir = output_dir
        self.__subjects_csv = self.__f(OutputRegister.SUBJECTS_CSV)
        self.__parallel_csv = self.__f(OutputRegister.PARALLEL_CSV)
        self.__exec_csv = self.__f(OutputRegister.EXECUTION_CSV)

    def __f(self, params):
        file_path = os.path.join(self.__output_dir, params.name_template.format(self.__ts))
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=params.cols)
            writer.writeheader()
        return file_path

    def results(self, name, data):
        with open(self.__exec_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=OutputRegister.EXECUTION_CSV.cols)

            row = {}
            for mode, exec_result in data.execution_data.items():
                row["name"] = name
                row["mode"] = mode
                row["elapsed_time"] = exec_result.elapsed_time

                # as defined in "time" when executing _run_tests
                row["t_user"] = "TODO"
                row["t_sys"] = "TODO"
                row["t_wall"] = "TODO"

                # reports data
                row["r_time"] = 0
                row["r_skipped"] = 0
                row["r_tests"] = 0
                row["r_failures"] = 0

                writer.writerow(row)

        with open(self.__parallel_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=OutputRegister.PARALLEL_CSV.cols)
            row = {"name": name, "files": data.parallel_data.files}
            row.update(data.parallel_data.frequency)
            writer.writerow(row)

    def subject(self, name, url, revision):
        with open(self.__subjects_csv, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=OutputRegister.SUBJECTS_CSV.cols)
            writer.writerow({"name": name, "url": url, "rev": revision})

    @classmethod
    def error(cls, when, name, url, revision, cause):
        with open(cls.ERROR_CSV_LOG, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cls.ERROR_LOG_HEADER)
            writer.writerow({"name": name, "url": url, "when": when, "cause": cause, "rev": revision})
