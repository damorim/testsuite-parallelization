from collections import namedtuple

ExecutionResults = namedtuple("ResultsResults", "reports, process_execution, elapsed_time")
ExecutionParams = namedtuple("ExecutionParams", "log_file, args, name, reports_dir")

StandardParams = ExecutionParams(reports_dir="surefire-ST-reports",
                                 log_file="test-log-default.txt",
                                 args=None, name="Standard")

L0Params = ExecutionParams(reports_dir="surefire-L0-reports",
                           log_file="test-log-sequential.txt",
                           args=["-P", "L0"], name="L0")

MODES = (StandardParams, L0Params)
