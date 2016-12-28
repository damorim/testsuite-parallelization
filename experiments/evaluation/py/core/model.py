import csv
import os
from collections import namedtuple
from datetime import datetime
from time import time

# Results from the execution of a subject with a specific ExecutionParam
ExecutionResults = namedtuple("ExecutionResults", "reports, process_execution, elapsed_time")

# Experiment results consist in all results from each ExecutionParam
ExperimentResults = namedtuple("ExperimentResults", "execution_data")

# Parameters of experiment execution for a subject
ExecutionParams = namedtuple("ExecutionParams", "log_file, args, name, reports_dir")

ParallelPrevalenceData = namedtuple("ParallelPrevalenceData", "frequency, files")

StandardParams = ExecutionParams(reports_dir="surefire-ST-reports",
                                 log_file="test-log-default.txt",
                                 args=None, name="Standard")

L0Params = ExecutionParams(reports_dir="surefire-L0-reports",
                           log_file="test-log-sequential.txt",
                           args=["-P", "L0"], name="L0")


class NotMavenProjectException(Exception):
    def __init__(self):
        super("Subject is not a Maven project")


class OutputRegister(object):
    ERROR_CSV_LOG = os.path.abspath("experiment-errors.csv")
    ERROR_LOG_HEADER = ("when", "name", "url", "rev", "cause")

    LogFileParams = namedtuple("LogFileParams", "name_template, cols")
    SUBJECTS_CSV = LogFileParams(name_template="verified-subjects-{}.csv",
                                 cols=["name", "url", "rev"])

    EXECUTION_CSV = LogFileParams(name_template="dataset-execution-{}.csv",
                                  cols=["mode", "name", "elapsed_time", "r_time", "r_skipped", "r_tests", "r_failures",
                                        "t_user", "t_sys", "t_wall"])

    def __init__(self, output_dir=os.curdir):
        # Timestamp used across all output files
        self.__ts = datetime.fromtimestamp(time()).strftime('%y%m%d%H%M')
        self.__output_dir = output_dir

        # FIXME: Commented to skip this output
        # self.__subjects_csv = self.__f(OutputRegister.SUBJECTS_CSV)

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
                row["t_user"] = exec_result.process_execution[0]
                row["t_sys"] = exec_result.process_execution[1]
                row["t_wall"] = exec_result.process_execution[2]

                # reports data
                row["r_time"] = exec_result.reports['time']
                row["r_skipped"] = exec_result.reports['skipped']
                row["r_tests"] = exec_result.reports['tests']
                row["r_failures"] = exec_result.reports['failures']

                writer.writerow(row)

    def subject(self, name, url, revision):
        # FIXME: Comment to skip this output
        # with open(self.__subjects_csv, "a", newline="") as f:
        #     writer = csv.DictWriter(f, fieldnames=OutputRegister.SUBJECTS_CSV.cols)
        #     writer.writerow({"name": name, "url": url, "rev": revision})
        pass

    @classmethod
    def error(cls, when, name, url, revision, cause):
        with open(cls.ERROR_CSV_LOG, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cls.ERROR_LOG_HEADER)
            writer.writerow({"name": name, "url": url, "when": when, "cause": cause, "rev": revision})
