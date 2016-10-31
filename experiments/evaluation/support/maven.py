# Helper classes
#
# Author: Jeanderson Candido
#
import os
import re
from collections import namedtuple, Counter
from subprocess import call, Popen, PIPE, TimeoutExpired, check_output
from xml.etree import ElementTree

TestCase = namedtuple("TestCase", "name, time")
SurefireData = namedtuple("Data", "statistics, items")


def build():
    with open(os.devnull, "wb") as DEVNULL:
        compile_command = ["mvn", "clean", "install", "-DskipTests", "-Dmaven.javadoc.skip=true"]
        try:
            result = not call(compile_command, stdout=DEVNULL, timeout=900)
        except TimeoutExpired:
            result = False
    return result


def test(inspect_data=None):
    flag = "ANALYZERTIMMESTAMP,"
    test_command = ["mvn", "test", "-Dmaven.javadoc.skip=true"]

    os.environ["TIMEFORMAT"] = flag + "%R,%S,%U,%P"
    args = ["bash", "-c", "time " + " ".join(test_command)]

    p = Popen(args, stdout=PIPE, stderr=PIPE)
    print("Running tests - PID (use pstree):", p.pid)
    out, err = p.communicate()
    if inspect_data:
        output = out.decode()
        pattern = re.compile(r"Results :\n\nTests run: .*", re.MULTILINE)
        for m in re.finditer(pattern, output):
            result = re.findall("\d+", m.group(0))
            inspect_data.tests += int(result[0])
            inspect_data.skipped += int(result[3])

        error = err.decode()
        for m in re.finditer(r"{}.*".format(flag), error):
            values = (m.group(0).split(","))
            inspect_data.elapsed_t = float(values[1])
            inspect_data.system_t = float(values[2])
            inspect_data.user_t = float(values[3])
            inspect_data.cpu_usage = float(values[4])

    return not p.returncode


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
            test_cases.append(TestCase(name=test_name, time=float(test_case.get("time"))))

    return SurefireData(items=test_cases, statistics=total_counter)


def is_maven_project():
    """ Returns true if the current dir has a pom.xml file. """
    return os.path.exists("pom.xml")


def get_value_from(xml_node, attribute, default_value, cast_type):
    """ Auxiliary function from collect_surefire_data """
    return default_value if not xml_node.get(attribute) else cast_type(xml_node.get(attribute).replace(",", ""))
