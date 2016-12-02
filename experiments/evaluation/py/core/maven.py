import os
from collections import Counter, namedtuple
from subprocess import check_output

from lxml import etree
from lxml.etree import ParseError


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


def is_valid_project(subject_path=os.curdir):
    """
    Checks if the informed path is a valid Maven project
    :param subject_path: the path to verify
    :return: true if the informed path contains a pom.xml file (false otherwise).
    """
    return os.path.exists(os.path.join(subject_path, "pom.xml"))


def has_compiled(subject_path=os.curdir):
    output = check_output(["find", subject_path, "-path", os.path.join("*target", "classes")])
    classes = output.decode().splitlines()
    output = check_output(["find", subject_path, "-path", os.path.join("*target", "test-classes")])
    test_classes = output.decode().splitlines()
    return len(classes) > 0 and len(test_classes) > 0


# Used to assist collect_surefire_data
TestCaseInfo = namedtuple("TestCase", "name, time")
ReportData = namedtuple("Data", "statistics, items")


def collect_surefire_data(reports_dir):
    """
    Collect data from surefire reports from the given directory.
    :param reports_dir: surefire reports directory
    :return: data tuple with statistics counter and a list of test cases data.
    """
    surefire_files = os.listdir(reports_dir)
    total_counter = Counter(tests=0, skipped=0, failure=0, time=0.0)
    test_cases = []
    for file_name in surefire_files:
        test_suite = etree.parse(os.path.join(reports_dir, file_name)).getroot()

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


def surefire_reports():
    output = check_output(["find", ".", "-path", os.path.join("*target", "surefire-reports", "TEST-*.xml")])
    return output.decode().splitlines()


def collect_parallel_settings_prevalence(subject_path=os.curdir, recursive=True):
    os.chdir(subject_path)

    find_command = ["find", "."]
    if not recursive:
        find_command.extend(["-maxdepth", "1"])
    find_command.extend(["-name", "pom.xml"])

    # get all pom.xml paths
    output = check_output(find_command)

    # for each pom file, inspect it!
    settings_frequency = Counter()
    files = 0
    for xml_path in output.decode().splitlines():
        files += 1
        frequency = _inspect_pom_file(xml_path)
        settings_frequency.update(frequency)

    ParallelPrevalenceData = namedtuple("ParallelPrevalenceData", "frequency, files")
    return ParallelPrevalenceData(frequency=settings_frequency, files=files)


def _inspect_pom_file(xml_path):
    namespace = {"ns": "http://maven.apache.org/POM/4.0.0"}
    frequency = Counter()
    try:
        root = etree.parse(xml_path).getroot()
    except ParseError as err:
        print(xml_path, err)
        return frequency

    surefire_nodes = [c for c in root.iter('{%s}plugin' % namespace['ns']) if _is_surefire_node(c)]

    # If there aren't surefire nodes, default behavior is L0
    if not len(surefire_nodes):
        frequency.update(["L0"])
        return frequency

    for node in surefire_nodes:
        config_node = node.find("{%s}configuration" % namespace['ns'])
        if config_node is None:
            frequency.update(["L0"])

        else:
            parallel_setting_node = config_node.find("{%s}parallel" % namespace['ns'])
            fork_setting_node = config_node.find("{%s}forkCount" % namespace['ns'])
            if fork_setting_node is None:
                fork_setting_node = config_node.find("{%s}forkMode" % namespace['ns'])

            if fork_setting_node is not None:
                if parallel_setting_node is not None:
                    frequency.update(["FL1"])
                else:
                    frequency.update(['FL0'])

            elif parallel_setting_node is not None:
                if parallel_setting_node.text == "classes":
                    frequency.update(["L2"])
                elif parallel_setting_node.text == "none":
                    frequency.update(["L0"])
                elif parallel_setting_node.text == "methods":
                    frequency.update(["L1"])
                elif parallel_setting_node.text in ["classesAndMethods", "both", "all"]:
                    frequency.update(["L3"])
                else:
                    frequency.update(["UNKNOWN"])

    return frequency


def _is_surefire_node(node):
    return len([n for n in node if n.text == "maven-surefire-plugin"])


def _get_value_from(xml_node, attribute, default_value, cast_type):
    """ Auxiliary function from collect_surefire_data """
    return default_value if not xml_node.get(attribute) else cast_type(xml_node.get(attribute).replace(",", ""))


PROFILE_L0_RAW = """
<profile>
  <id>L0</id>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration>
          <parallel>none</parallel>
          <forkCount>1</forkCount>
          <reuseFork>true</reuseFork>
        </configuration>
      </plugin>
    </plugins>
  </build>
</profile>
"""
