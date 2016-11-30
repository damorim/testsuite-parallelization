#!/usr/bin/env python3
import os
import re
from collections import namedtuple
from subprocess import call, DEVNULL, check_output, Popen, PIPE, TimeoutExpired

from lxml import etree

from support import maven

Result = namedtuple("Result", "mode,name,elapsed_time,r_time,r_skipped,r_tests,r_failures,t_user,t_sys,t_wall")


def _run_test_profile(test_log, pom_file, profile_args=None, override=False):
    if not os.path.exists(test_log) or override:
        with open(test_log, "w") as log_file:
            maven_args = maven.test_task("-o", "-Dmaven.javadoc.skip=true", "-f", pom_file)
            if profile_args:
                maven_args.extend(profile_args)
            time_args = ["/usr/bin/time", "-f", "%U,%S,%e", "-o", _performance_log_from(test_log)]
            time_args.extend(maven_args)
            call(time_args, stdout=log_file, stderr=DEVNULL, timeout=60 * 60 * 3)  # timeout = 3 hours


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


def _compute_tests_executed():
    statistics = maven.collect_surefire_data().statistics
    return statistics


def _compute_process_cpuness(log_file):
    log_file = _performance_log_from(log_file)
    tail = check_output(["tail", "-n", "1", log_file])
    values = [float(v) for v in tail.decode().split(",")]
    return values[0], values[1], values[2]


def _compute_time_cost(log_file):
    cat = Popen(["cat", log_file], stdout=PIPE)
    grep = Popen(["grep", "\[INFO\] Total time:"], stdin=cat.stdout, stdout=PIPE)
    cat.stdout.close()
    out, err = grep.communicate()

    # normalize reported time
    last_reported_time = out.splitlines()[-1]
    reported_time = re.sub(r".*: ", "", last_reported_time.decode().replace("s", "").strip())
    if "min" in reported_time:
        reported_time = reported_time.replace("min", "").split(":")
        reported_time = (60 * int(reported_time[0])) + int(reported_time[1])
    elif "h" in reported_time:
        reported_time = reported_time.replace("h", "").split(":")
        reported_time = (60 * int(reported_time[0]) + int(reported_time[1])) * 60

    return reported_time


def experiment(subject_path, override=False):
    """
    Runs the experiment for a Maven subject from the given path
    :param subject_path: the path to the subject
    :param override: flag indicating whether existing data should be overridden
    :return: None
    """
    subject_name = os.path.basename(subject_path)
    if not os.path.exists(subject_path):
        print("Missing subject \"{}\". Skipping...".format(subject_name))
        return
    if not maven.is_valid_project(subject_path):
        print("Subject \"{}\" is not a Maven project. Skipping...".format(subject_name))
        return

    # REQUIRED FILES
    modified_pom = "experiment-pom.xml"

    print("Analyzing subject: \"{}\"".format(subject_name))
    compiled = maven.has_compiled(subject_path)
    os.chdir(subject_path)

    exit_status = 0
    if not compiled:
        print(" - Compiling sources")
        exit_status = call(maven.build_task("-DskipTests", "-Dmaven.javadoc.skip=true"),
                           stdout=DEVNULL, stderr=DEVNULL)
    if not exit_status:
        if not os.path.exists(modified_pom) or override:
            _add_parallel_profiles(modified_pom)
            print(" - Created \"{}\" file with parallel profiles".format(modified_pom))

        if override:
            call(maven.resolve_dependencies_task("-f", modified_pom), stdout=DEVNULL, stderr=DEVNULL)
            print(" - Dependencies solved for offline execution")

        mode_settings = {
            "ST": {
                "log-file": "test-log-default.txt",
                "pom-file": "pom.xml",
                "args": None
            },
            "L0": {
                "log-file": "test-log-sequential.txt",
                "pom-file": modified_pom,
                "args": ["-P", "L0"]
            }
        }
        results_to_return = []
        for mode, params in mode_settings.items():
            test_log_file = params["log-file"]
            pom_file = params["pom-file"]
            profile_args = params["args"]

            try:
                _run_test_profile(test_log_file, pom_file, profile_args, override)
            except TimeoutExpired as err:
                print(" -", err)
                return

            # Read-only methods: no execution is required as long as the raw data exists
            try:
                elapsed_time = _compute_time_cost(test_log_file)
                tests_executed = _compute_tests_executed()
                cpuness = _compute_process_cpuness(test_log_file)
            except Exception as err:
                print(" -", err)
                return

            results_to_return.append(Result(
                mode=mode,
                name=subject_name,
                elapsed_time=elapsed_time,
                r_time=tests_executed["time"],
                r_skipped=tests_executed["skipped"],
                r_tests=tests_executed["tests"],
                r_failures=tests_executed["failure"],
                t_user=cpuness[0],
                t_sys=cpuness[1],
                t_wall=cpuness[2]
            ))

        return results_to_return
