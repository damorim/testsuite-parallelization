import os
import re
import shutil
from collections import Counter
from subprocess import check_call, DEVNULL, call, check_output, Popen, PIPE

from lxml import etree

from core import maven
from core import model

EXPERIMENT_POM = "experiment-pom.xml"


def run(subject_path=os.curdir, clean=False):
    os.chdir(subject_path)
    _prepare_subject()

    results = {}

    for settings in [model.StandardParams]:
        print("Testing in {} mode".format(settings.name))
        _run_tests(profile=settings, clean=clean)

        # collect data from execution
        surefire_statistics = maven.collect_surefire_data(settings.reports_dir).statistics
        execution_data = _collect_process_execution_data(settings.log_file)
        time_cost = _collect_time_cost_data(settings.log_file)

        # aggregating results
        results[settings.name] = model.ExecutionResults(process_execution=execution_data,
                                                        reports=surefire_statistics,
                                                        elapsed_time=time_cost)

    return model.ExperimentResults(execution_data=results)


def _verify_collected_data():
    # ensure all report folders are equals for the executed modes in results
    ref_mode = model.StandardParams
    ref_reports = os.listdir(ref_mode.reports_dir)
    for curr_mode in [model.L0Params]:
        if not (ref_reports == os.listdir(curr_mode.reports_dir)):
            raise Exception(" - Reports from {} and {} modes diverge".format(ref_mode.name, curr_mode.name))
            # TODO ensure tests field are the same as well...


def _prepare_subject():
    """
    Resolves project dependencies, compile source files, and create a modified pom file
    :return: None
    """
    if not maven.is_valid_project():
        raise model.NotMavenProjectException()
    # _add_parallel_profiles()
    # print(" - Created \"{}\" file with parallel profiles".format(EXPERIMENT_POM))
    if not maven.has_compiled():
        check_call(maven.build_task("-DskipTests", "-Dmaven.javadoc.skip=true", "-f", EXPERIMENT_POM),
                   timeout=30 * 60, stdout=DEVNULL, stderr=DEVNULL)
    print(" - Sources compiled")
    check_call(maven.resolve_dependencies_task("-f", EXPERIMENT_POM), stdout=DEVNULL, stderr=DEVNULL)
    print(" - Dependencies solved")


def _run_tests(profile, clean=False):
    if clean:
        _cleanup(profile)

    if not os.path.exists(profile.reports_dir):
        os.mkdir(profile.reports_dir)

    if os.listdir(profile.reports_dir) and os.path.exists(profile.log_file):
        print(" - Skipping execution (test reports and log file found)")
        return

    with open(profile.log_file, "w") as log_file:
        maven_args = maven.test_task("-o", "-Dmaven.javadoc.skip=true", "-f", EXPERIMENT_POM)
        if profile.args:
            maven_args.extend(profile.args)
        time_args = ["/usr/bin/time", "-f", "%U,%S,%e", "-o", _performance_log_from(profile.log_file)]
        time_args.extend(maven_args)
        exit_status = call(time_args, stdout=log_file, stderr=DEVNULL, timeout=60 * 60 * 3)  # timeout = 3 hours
        print(" - {} on {} mode".format("Tests executed" if exit_status == 0 else "Tests failed", profile.name))

        _collect_test_reports(destiny=profile.reports_dir)
        print(" - Test reports collected")


def _collect_test_reports(destiny):
    paths = maven.surefire_reports()
    if len(paths) == 0:
        raise Exception(" - Couldn't find *ANY* surefire report")
    for p in paths:
        file_name = os.path.basename(p)
        shutil.move(p, os.path.join(destiny, file_name))


def _collect_process_execution_data(log_file):
    log_file = _performance_log_from(log_file)
    tail = check_output(["tail", "-n", "1", log_file])
    values = [float(v) for v in tail.decode().split(",")]
    return values[0], values[1], values[2]


def _collect_time_cost_data(log_file):
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


def _cleanup(profile):
    if os.path.exists(profile.log_file):
        os.remove(profile.log_file)
    if os.path.exists(_performance_log_from(profile.log_file)):
        os.remove(_performance_log_from(profile.log_file))
    if os.path.exists(profile.reports_dir):
        shutil.rmtree(profile.reports_dir)


def _performance_log_from(test_log):
    return test_log.replace("test", "performance")


# FIXME: not used
def _collect_parallel_settings_data(recursive=True):
    find_command = ["find", "."]
    if not recursive:
        find_command.extend(["-maxdepth", "1"])
    find_command.extend(["-name", "pom.xml"])

    # get all pom.xml paths
    output = check_output(find_command)

    # for each pom file, inspect it!
    settings_frequency = Counter(L0=0, L1=0, L2=0, L3=0, FL0=0, FL1=0, Unknown=0)
    files = 0
    for xml_path in output.decode().splitlines():
        files += 1
        frequency = maven.inspect_parallel_settings(xml_path)
        settings_frequency.update(frequency)

    return model.ParallelPrevalenceData(frequency=settings_frequency, files=files)
