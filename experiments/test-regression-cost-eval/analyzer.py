#!/usr/bin/python3
import os

from support import builders
from support.constants import COLUMN_SEP
from support.constants import SUBJECT_DIR


# def timed_exec(command, time_limit=None):
#     time_commands = ["/usr/bin/time", "-v"]
#     time_commands.extend(command)
#
#     p = Popen(time_commands, stdout=PIPE, stderr=PIPE)
#     print("PID:", p.pid)
#
#     if not time_limit:
#         stdout_raw, stderr_raw = p.communicate()
#     else:
#         try:
#             stdout_raw, stderr_raw = p.communicate(timeout=time_limit)
#         except TimeoutExpired:
#             p.kill()
#             stdout_raw, stderr_raw = p.communicate()
#
#     with open("compile-log", "w") as log:
#         log.write(stdout_raw.decode())
#         if stderr_raw:
#             log.write("----SDTERR----\n")
#             log.write(stderr_raw.decode())


def inspect(subject):
    subject_dir = os.path.join(SUBJECT_DIR, subject)
    if not os.path.exists(subject_dir):
        return
    os.chdir(subject_dir)

    data = {"builder_name": "N/A", "#tests": "N/A", "compiled": False, "tests_pass": False}
    builder = builders.detect_system()
    if builder:
        data["builder_name"] = builder.name

        # STEP 1: COMPILE SUBJECT
        data["compiled"] = builder.compile()

        # STEP 2: TEST SUBJECT AND COLLECT DATA
        data["tests_pass"] = builder.test(data)

        # %e: Elapsed time (in seconds)
        # %P: CPU usage
        # FIXME: How to deal when the project has multiple threads?
        # time_args = ["%e", "%P"]
        # test_command = ["time", "-f", COLUMN_SEP.join(time_args)]
        # test_command = []
        # test_command.extend(builder.test())
        # pid = Popen(test_command, stderr=PIPE)
        # out, err = pid.communicate()
        # stream_lines = err.splitlines()
        # print(stream_lines[len(stream_lines) - 1])

    return COLUMN_SEP.join([subject, data["builder_name"], str(data["compiled"]), str(data["tests_pass"]),
                            data["#tests"]])

# FIXME
# def main():
#     # Limit execution
#     max_rows = None
#
#     with open(TIMECOST_CSV_FILE, "w") as timecost:
#         timecost.write(COLUMN_SEP.join(["SUBJECT", "BUILDER", "COMPILED",
#                                         "TESTS_PASS", "ELAPSED_TIME"]))
#         timecost.write("\n")
#
#     with open(SUBJECTS_CSV_FILE, newline="") as subjects:
#         reader = csv.DictReader(subjects)
#         cur_row = 1
#         for row in reader:
#             if max_rows and cur_row > max_rows:
#                 break
#             project = row["SUBJECT"]
#             if not row["BUILDER"] == "N/A":
#                 print("Checking", project)
#                 # csv_line = check(project)
#                 # with open(TIMECOST_CSV_FILE, "a") as timecost:
#                 #     timecost.write(COLUMN_SEP.join(csv_line))
#                 #     timecost.write("\n")
#                 cur_row += 1


if __name__ == "__main__":
    print(inspect("retrofit"))
