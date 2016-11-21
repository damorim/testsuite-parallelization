#!/usr/bin/python3
import argparse
import csv
import os
import re
from subprocess import call, DEVNULL, PIPE, Popen

from lxml import etree

from support import maven

BASE_DIR = os.path.abspath(os.curdir)
SUBJECTS_HOME = os.path.join(BASE_DIR, "subjects")


def _run_test_profile(test_log, profile_args=None, pom_file="pom.xml", override=False):
    if not os.path.exists(test_log) or override:
        with open(test_log, "w") as log_file:
            maven_args = maven.test_task("-o", "-Dmaven.javadoc.skip=true", "-f", pom_file)
            if profile_args:
                maven_args.extend(profile_args)
            time_args = ["/usr/bin/time", "-f", "%U,%S,%e", "-o", _performance_log_from(test_log)]
            time_args.extend(maven_args)
            call(time_args, stdout=log_file, stderr=DEVNULL)


def _add_parallel_profiles(output_pom):
    tree = etree.parse("pom.xml")
    namespace = {'ns': 'http://maven.apache.org/POM/4.0.0'}
    root = tree.getroot()
    profiles_node = root.find("{%s}profiles" % namespace['ns'])
    if profiles_node is None:
        profiles_node = etree.SubElement(root, "profiles")

    profiles_to_add_raw = [maven.PROFILE_L0_RAW]
    for profile_raw in profiles_to_add_raw:
        profile_node = etree.XML(profile_raw)
        profiles_node.append(profile_node)

    with open(output_pom, "w") as pom:
        pom.write(etree.tostring(root, pretty_print=True).decode())


def _performance_log_from(test_log):
    return test_log.replace("test", "performance")


def _compute_tests_executed(fields=("tests", "skipped", "failure")):
    statistics = maven.collect_surefire_data().statistics
    return {field: statistics[field] for field in fields}


def _compute_process_cpuness(log_file):
    log_file = _performance_log_from(log_file)
    with open(log_file) as log:
        line = log.readline()
    values = [float(v) for v in line.split(",")]
    return (values[0] + values[1]) / values[2]


def _compute_time_cost(log_file):
    cat = Popen(["cat", log_file], stdout=PIPE)
    grep = Popen(["grep", "Total time:"], stdin=cat.stdout, stdout=PIPE)
    cat.stdout.close()
    out, err = grep.communicate()

    # normalize reported time
    reported_time = re.sub(r".*: ", "", out.decode().replace("s", "").strip())
    if "min" in reported_time:
        reported_time = reported_time.replace("min", "").split(":")
        reported_time = (60 * int(reported_time[0])) + int(reported_time[1])
        # FIXME test subjects with reported time > 60min

    return round(float(reported_time))


def experiment(path, override=False):
    """
    Runs the experiment for a Maven subject from the given path
    :param path: the path to the subject
    :param override: flag indicating whether existing data should be overridden
    :return: None
    """
    subject_name = os.path.basename(path)

    # REQUIRED FILES
    test_log_seq = "test-log-sequential.txt"
    test_log_default = "test-log-default.txt"
    modified_pom = "experiment-pom.xml"

    print("Analyzing subject: \"{}\"".format(subject_name))
    compiled = maven.has_compiled(path)
    os.chdir(path)

    exit_status = 0
    if not compiled:
        exit_status = call(maven.build_task("-DskipTests", "-Dmaven.javadoc.skip=true"),
                           stdout=DEVNULL, stderr=DEVNULL)
    if not exit_status:
        if not os.path.exists(modified_pom) or override:
            _add_parallel_profiles(modified_pom)
            print("Created \"{}\" file with parallel profiles".format(modified_pom))

        call(maven.resolve_dependencies_task("-f", modified_pom), stdout=DEVNULL, stderr=DEVNULL)
        print("Dependencies solved for offline execution")

        _run_test_profile(test_log_default, override=override)
        _run_test_profile(test_log_seq, pom_file=modified_pom, profile_args=["-P", "L0"], override=override)
        print("Tests executed")

        # Read-only methods: no execution is required as long as the raw data exists
        try:
            elapsed_times = {log: _compute_time_cost(log) for log in (test_log_default, test_log_seq)}
            tests_executed = _compute_tests_executed()
            cpuness = _compute_process_cpuness(test_log_seq)
        except Exception as err:
            print(err)
            return subject_name

        return subject_name, elapsed_times, tests_executed, cpuness


def load_subjects_from(csv_file):
    """
    Loads subjects successfully compiled from a csv file with columns COMPILED and SUBJECTS
    :param csv_file: path to a csv file with columns COMPILED and SUBJECTS
    :return: a list of subjects successfully compiled
    """
    if not os.path.exists(csv_file):
        raise Exception("invalid input file path: \"{}\"".format(csv_file))

    loaded_subjects = []
    with open(csv_file, newline="") as content:
        reader = csv.DictReader(content)
        for row in reader:
            if row["COMPILED"] == "true":
                loaded_subjects.append(row["SUBJECT"])

    return loaded_subjects


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="csv file with subjects to analyze (columns required: COMPILED and SUBJECT)")
    parser.add_argument("-o", "--output", help="csv file to output raw data")
    parser.add_argument("-f", "--force", help="override existing output files (if any)", action="store_true")
    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    output_file = os.path.abspath(args.output if args.output else "raw-data.csv")
    print("Input file: {}\nOutput file: {}\nOverride: {}\n".format(input_file, output_file, args.force))

    # Check if SUBJECTS_HOME exist (REQUIRED)
    if not os.path.exists(SUBJECTS_HOME):
        print("Required directory missing: \"{}\"\nDid you execute \"downloader.py\" first?".format(SUBJECTS_HOME))
        exit(1)

    with open(output_file, "w") as f:
        f.write("output log:\n")

    subjects = load_subjects_from(input_file)
    for subject in subjects:
        subject_path = os.path.join(SUBJECTS_HOME, subject)

        if not os.path.exists(subject_path):
            print("Missing subject \"{}\". Skipping...".format(subject))
            continue
        if not maven.is_valid_project(subject_path):
            print("Subject \"{}\" is not a Maven project. Skipping...".format(subject))
            continue

        results = experiment(subject_path, override=args.force)
        print(results, "\n")
        with open(output_file, "a") as f:
            f.write(" ".join([str(r) for r in results]))
            f.write("\n")
