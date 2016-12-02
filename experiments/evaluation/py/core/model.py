from collections import namedtuple

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
