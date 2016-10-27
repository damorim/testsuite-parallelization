#!/usr/bin/python3
import csv
import os

from support import builders
from support.constants import COLUMN_SEP, RAW_DATA_CSV_FILE, SUBJECTS_CSV_FILE
from support.constants import SUBJECT_DIR


class ExecutionData:
    def __init__(self, subject="N/A"):
        self.subject = subject
        self.builder_name = "N/A"
        self.compiled = False
        self.tests_pass = False
        self.tests = 0
        self.skipped = 0
        self.elapsed_t = 0
        self.system_t = 0
        self.user_t = 0
        self.cpu_usage = 0

    def values(self):
        return [self.subject, self.builder_name, self.compiled, self.tests_pass, self.tests, self.skipped,
                self.elapsed_t, self.system_t, self.user_t, self.cpu_usage]

    @staticmethod
    def header():
        return ["subject", "builder_name", "compiled", "tests_pass", "tests", "skipped",
                "elapsed_t", "system_t", "user_t", "cpu_usage"]


def inspect(subject):
    subject_dir = os.path.join(SUBJECT_DIR, subject)
    if not os.path.exists(subject_dir):
        print("Missing path:", subject_dir)
        return
    os.chdir(subject_dir)

    execution_data = ExecutionData(subject)
    builder = builders.detect_system()
    if builder:
        execution_data.builder_name = builder.name
        if builder.compile():
            execution_data.compiled = True
            execution_data.tests_pass = builder.test(execution_data)

    return execution_data


def register_data_from(project):
    data = inspect(project)
    with open(RAW_DATA_CSV_FILE, "a") as time_cost:
        time_cost.write(COLUMN_SEP.join("%s" % str(value) for value in data.values()))
        time_cost.write("\n")


def main():
    # Execution configuration
    max_rows = None
    init_row = None

    # FIXME ignoring just to get output faster
    skip_subjects = ['neo4j', 'jetty.project', 'hive', 'pinot', 'hazelcast', 'hbase', 'hadoop']

    if not init_row:
        with open(RAW_DATA_CSV_FILE, "w") as time_cost:
            time_cost.write(COLUMN_SEP.join("%s" % attrib for attrib in ExecutionData.header()))
            time_cost.write("\n")

    with open(SUBJECTS_CSV_FILE, newline="") as subjects:
        reader = csv.DictReader(subjects)

        row_counter = 1
        cur_row = 2
        for row in reader:
            if init_row and cur_row < init_row:
                cur_row += 1
                continue

            if max_rows and row_counter > max_rows:
                break

            project = row["SUBJECT"]
            if project not in skip_subjects:
                print("Checking", project)
                register_data_from(project)
                row_counter += 1

    # FIXME REMOVE ME (temporary code)
    print("Running skipped subjects....")
    for p in skip_subjects:
        print("Checking", p)
        register_data_from(p)


if __name__ == "__main__":
    # main()
    print(inspect("retrofit").values())
