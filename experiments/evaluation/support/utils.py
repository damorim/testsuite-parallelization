import os
import re
from collections import Counter

from subprocess import check_output, PIPE, Popen

BUILDER_LOG_TXT = "builder-output-log.txt"
PERFORMANCE_LOG_TXT = "test-performance-log.txt"


class Builder:
    def __init__(self, name, args, test, test_report_inspector=None, has_test_reports=None):
        self.name = name
        self.args = args
        self.test = test
        self.test_report_inspector = test_report_inspector
        self.has_test_reports = has_test_reports


def detect_builder():
    if os.path.exists("pom.xml"):
        return Builder(name="Maven", args=["mvn", "clean", "install", "-DskipTests", "-Dmaven.javadoc.skip=true"],
                       test=["mvn", "test", "-Dmaven.javadoc.skip=true"])

    elif os.path.exists("gradlew"):
        return Builder(name="Gradle", args=["./gradlew", "clean", "build", "-X", "test"],
                       test=["./gradlew", "test"])

    elif os.path.exists("build.xml"):
        return Builder(name="Ant", args=["ant", "compile"], test=["ant", "test"])

    return None


def compute_time_distribution(data):
    test_cases = sorted(data.items, key=lambda t: t.time, reverse=True)
    total_time = data.statistics['time']

    counter = Counter(tests=0, time=0)
    threshold = total_time * 0.9

    for tc in test_cases:
        if counter['time'] + tc.time > threshold:
            break
        counter.update(Counter(tests=1, time=tc.time))

    return round((counter['tests'] / len(test_cases)) * 100, 2)


def check_resources_usage(subject_path=os.curdir):
    performance_log_path = os.path.join(subject_path, PERFORMANCE_LOG_TXT)
    if os.path.exists(performance_log_path):
        output = check_output(["cat", performance_log_path])
        p = Popen(["grep", "Average"], stdin=PIPE, stdout=PIPE)
        out, err = p.communicate(input=output)

        results_avg = None
        for line in out.decode().splitlines():
            if "all" in line:
                results_avg = line
                break
        values = re.sub("\s+", " ", results_avg).strip().split(" ")

        io_wait = values[5].replace(",", ".")
        cpu_idle = values[7].replace(",", ".")
        cpu_usage = sum([float(v.replace(",", ".")) for v in values[2:5]])

        return [str(cpu_usage), io_wait, cpu_idle]

    return ["0.0", "0.0", "0.0"]
