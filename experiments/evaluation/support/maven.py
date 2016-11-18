import os
from collections import Counter, namedtuple

from lxml import etree
from subprocess import check_output


def build_task(*additional_args):
    args = ["mvn", "clean", "install"]
    if additional_args:
        args.extend(additional_args)
    return args


def test_task(*additional_args):
    args = ["mvn", "test"]
    if additional_args:
        args.extend(additional_args)
    return args


def resolve_dependencies_task(*additional_args):
    """
    Task arguments to ensure dependencies are resolved before running in offline mode
    :return: List of arguments to run in a system call
    """
    args = ["mvn", "dependency:go-offline"]
    if additional_args:
        args.extend(additional_args)
    return args


def is_valid_project(subject_path):
    """
    Checks if the informed path is a valid Maven project
    :param subject_path: the path to verify
    :return: true if the informed path contains a pom.xml file (false otherwise).
    """
    return os.path.exists(os.path.join(subject_path, "pom.xml"))


def has_compiled(subject_path):
    return os.path.exists(os.path.join(subject_path, "target", "classes")) and os.path.exists(
        os.path.join(subject_path, "target", "test-classes"))


def has_surefire_dir():
    return os.path.exists(os.path.abspath(os.path.join("target", "surefire-reports")))


TestCaseInfo = namedtuple("TestCase", "name, time")
ReportData = namedtuple("Data", "statistics, items")


def collect_surefire_data():
    """
    Collect data from surefire reports.
    Returns a Data tuple with statistics counter and a list of test cases data.
    """
    if not has_surefire_dir():
        return None
    output = check_output(["find", ".", "-name", "TEST-*.xml"]).decode()
    total_counter = Counter(tests=0, skipped=0, failure=0, time=0.0)
    test_cases = []
    for xml_path in output.splitlines():
        test_suite = etree.parse(xml_path).getroot()

        time_cnt = 0
        for test_case in test_suite.iter("testcase"):
            test_name = "%s.%s" % (test_case.get("classname"), test_case.get("name"))
            test_cases.append(TestCaseInfo(name=test_name, time=float(test_case.get("time"))))
            time_cnt += float(test_case.get("time"))

        failure_cnt = _get_value_from(test_suite, "failures", default_value=0, cast_type=int)
        error_cnt = _get_value_from(test_suite, "errors", default_value=0, cast_type=int)
        tests_cnt = _get_value_from(test_suite, "tests", default_value=0, cast_type=int)
        skipped_cnt = _get_value_from(test_suite, "skipped", default_value=0, cast_type=int)

        total_counter.update(Counter(tests=tests_cnt, skipped=skipped_cnt, time=time_cnt,
                                     failure=(failure_cnt + error_cnt)))

    return ReportData(items=test_cases, statistics=total_counter)


def _get_value_from(xml_node, attribute, default_value, cast_type):
    """ Auxiliary function from collect_surefire_data """
    return default_value if not xml_node.get(attribute) else cast_type(xml_node.get(attribute).replace(",", ""))
