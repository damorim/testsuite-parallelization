import os
import re
from collections import Counter, namedtuple

from subprocess import check_output
from xml.etree import ElementTree

TestCaseInfo = namedtuple("TestCase", "name, time")
ReportData = namedtuple("Data", "statistics, items")


class Builder:
    def __init__(self, name, args, test, test_report_inspector=None):
        self.name = name
        self.args = args
        self.test = test
        self.test_report_inspector = test_report_inspector


def detect_builder():
    if os.path.exists("pom.xml"):
        return Builder(name="Maven", args=["mvn", "clean", "install", "-DskipTests", "-Dmaven.javadoc.skip=true"],
                       test=["mvn", "test", "-Dmaven.javadoc.skip=true"],
                       test_report_inspector=collect_surefire_data)

    elif os.path.exists("gradlew"):
        return Builder(name="Gradle", args=["./gradlew", "clean", "build", "-X", "test"],
                       test=["./gradlew", "test"])

    elif os.path.exists("build.xml"):
        return Builder(name="Ant", args=["ant", "compile"], test=["ant", "test"])

    return None


def collect_surefire_data():
    """
    Collect data from surefire reports.
    Returns a Data tuple with statistics counter and a list of test cases data.
    """
    output = check_output(["find", ".", "-name", "TEST-*.xml"]).decode()
    total_counter = Counter(tests=0, skipped=0, failure=0, time=0.0)
    test_cases = []

    for xml_path in output.splitlines():
        test_suite = ElementTree.parse(xml_path).getroot()

        failure_cnt = get_value_from(test_suite, "failures", default_value=0, cast_type=int)
        error_cnt = get_value_from(test_suite, "errors", default_value=0, cast_type=int)
        tests_cnt = get_value_from(test_suite, "tests", default_value=0, cast_type=int)
        skipped_cnt = get_value_from(test_suite, "skipped", default_value=0, cast_type=int)
        time_cnt = get_value_from(test_suite, "time", default_value=0.0, cast_type=float)

        total_counter.update(Counter(tests=tests_cnt, skipped=skipped_cnt, time=time_cnt,
                                     failure=(failure_cnt + error_cnt)))

        for test_case in test_suite.iter("testcase"):
            test_name = "%s.%s" % (test_case.get("classname"), test_case.get("name"))
            test_cases.append(TestCaseInfo(name=test_name, time=float(test_case.get("time"))))

    return ReportData(items=test_cases, statistics=total_counter)


def get_value_from(xml_node, attribute, default_value, cast_type):
    """ Auxiliary function from collect_surefire_data """
    return default_value if not xml_node.get(attribute) else cast_type(xml_node.get(attribute).replace(",", ""))


def compute_time_distribution(data):
    test_cases = sorted(data.items, key=lambda t: t.time)
    total_time = data.statistics['time']

    counter = Counter(tests=0, time=0)
    threshold = total_time * 0.9
    for tc in test_cases:
        if counter['time'] + tc.time > threshold:
            break
        counter.update(Counter(tests=1, time=tc.time))

    return round((counter['tests'] / len(test_cases)) * 100, 2)


def check_time_cost(subject_path=os.curdir):
    with open(os.path.join(subject_path, "test-output.txt")) as builder_output:
        for line in builder_output:
            if line.startswith("TIME-COST="):
                elapsed_time_raw = re.sub(r"TIME-COST=", "", line.strip())
                return int(elapsed_time_raw)


def check_test_reports(subject_path=os.curdir):
    subject_name = os.path.basename(subject_path)
    if not os.path.isdir(subject_path):
        raise Exception("Project: {}\nInvalid path: {}".format(subject_name, subject_path))

    os.chdir(subject_path)
    builder = detect_builder()
    if builder and builder.test_report_inspector:
        return builder.test_report_inspector()


def check_cpu_usage():
    # TODO implement function to read data from 'performance.evaluate' output file and return %CPU
    return 0
