import os
import re
from collections import namedtuple
from subprocess import check_call, DEVNULL, call, check_output, Popen, PIPE

from lxml import etree

from support import git
from support import maven

EXPERIMENT_POM = "experiment-pom.xml"
ExecutionParams = namedtuple("ExecutionParams", "log_file, args, name, reports_dir")
ExecutionModes = namedtuple("ExecutionModes", "ST, L0")

MODES = ExecutionModes(ST=ExecutionParams(log_file="test-log-default.txt", args=None, name="Standard",
                                          reports_dir="surefire-reports"),
                       L0=ExecutionParams(log_file="test-log-sequential.txt", args=["-P", "L0"], name="L0",
                                          reports_dir="surefire-L0-reports"))


def run(subject_path, clean=False):
    os.chdir(subject_path)
    if clean:
        call(["mvn", "clean"], stderr=DEVNULL, stdout=DEVNULL)

    prepare_subject()
    for settings in [MODES.ST, MODES.L0]:
        run_tests(profile=settings, clean=clean)

        # collect data from execution
        elapsed_time = collect_time_cost_data(settings.log_file)
        execution_data = collect_process_execution_data(settings.log_file)
        surefire_statistics = maven.collect_surefire_data(settings.reports_dir).statistics

        # TODO define output format
        # TODO Inspect surefire collected data to detect inconsistencies
        print(elapsed_time, execution_data, surefire_statistics)

        # results = experiment(name=subject_row["name"], path=subject_path, override=args.force)
        # if results:
        #     all_results.append(results)

        #             with open(output_file, "a") as f:
        #                 f.write(",".join([str(getattr(r, attr)) for attr in Result._fields]))
        #                 f.write("\n")
    print(maven.collect_parallel_settings_prevalence())
    print(git.which_revision())


def prepare_subject():
    """
    Resolves project dependencies, compile source files, and create a modified pom file
    :return: None
    """
    subject_name = os.path.basename(os.path.abspath(os.curdir))
    print("Preparing \"{}\"".format(subject_name))
    if not maven.is_valid_project():
        raise Exception("Subject is not a Maven project")
    _add_parallel_profiles()
    check_call(maven.resolve_dependencies_task("-f", EXPERIMENT_POM), stdout=DEVNULL, stderr=DEVNULL)
    print(" - Dependencies solved")
    if not maven.has_compiled():
        check_call(maven.build_task("-o", "-DskipTests", "-Dmaven.javadoc.skip=true", "-f", EXPERIMENT_POM),
                   timeout=30 * 60, stdout=DEVNULL, stderr=DEVNULL)
    print(" - Sources compiled")


def run_tests(profile=MODES.ST, clean=False):
    if clean and os.path.exists(profile.log_file):
        os.remove(profile.log_file)
    if len(maven.surefire_files_from(profile.reports_dir)) > 0 and os.path.exists(profile.log_file):
        print("Skipped test execution on {} mode (test reports found)".format(profile.name))
        return

    with open(profile.log_file, "w") as log_file:
        maven_args = maven.test_task("-o", "-Dmaven.javadoc.skip=true", "-f", EXPERIMENT_POM)
        if profile.args:
            maven_args.extend(profile.args)
        time_args = ["/usr/bin/time", "-f", "%U,%S,%e", "-o", _performance_log_from(profile.log_file)]
        time_args.extend(maven_args)
        exit_status = call(time_args, stdout=log_file, stderr=DEVNULL, timeout=60 * 60 * 3)  # timeout = 3 hours

        print("{} on {} mode".format("Tests executed" if exit_status == 0 else "Tests failed", profile.name))


def collect_process_execution_data(log_file):
    log_file = _performance_log_from(log_file)
    tail = check_output(["tail", "-n", "1", log_file])
    values = [float(v) for v in tail.decode().split(",")]
    return values[0], values[1], values[2]


def collect_time_cost_data(log_file):
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


def _add_parallel_profiles():
    """
    Auxiliary function for internal use.
    Creates a new pom file with execution profiles.
    :return: None
    """
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

    with open(EXPERIMENT_POM, "w") as pom:
        pom.write(etree.tostring(root, pretty_print=True).decode())

    print(" - Created \"{}\" file with parallel profiles".format(EXPERIMENT_POM))


def _performance_log_from(test_log):
    return test_log.replace("test", "performance")
