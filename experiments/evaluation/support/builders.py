# Helper classes
#
# Author: Jeanderson Candido
#
import os
import re
from subprocess import call, Popen, PIPE, TimeoutExpired


class AbstractBuilder:
    def __init__(self):
        self.name = None
        self.compile_args = None
        self.test_args = None

    def compile(self):
        """ Returns True if finished successfully """
        with open("/dev/null", "wb") as DEVNULL:
            try:
                result = not call(self.compile_args, stdout=DEVNULL, timeout=900)
            except TimeoutExpired:
                result = False
        return result

    def test(self):
        pass


class Maven(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.name = "Maven"
        self.compile_args = ["mvn", "clean", "install", "-DskipTests", "-Dmaven.javadoc.skip=true"]
        self.test_args = ["mvn", "test", "-Dmaven.javadoc.skip=true"]

    def test(self, inspect_data=None):
        flag = "ANALYZERTIMMESTAMP,"
        os.environ["TIMEFORMAT"] = flag + "%R,%S,%U,%P"
        args = ["bash", "-c", "time " + " ".join(self.test_args)]

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


class Ant(AbstractBuilder):
    # TODO Feel free to implement Ant support
    def __init__(self):
        super().__init__()
        self.name = "Ant"

    def compile(self):
        pass


class Gradle(AbstractBuilder):
    # TODO Feel free to implement Gradle support
    def __init__(self):
        super().__init__()
        self.name = "Gradle"

    def compile(self):
        pass


def detect_system():
    """
    Detects the build system in the current directory and returns the related Builder object.

    The verification is based if a specific path exists.
    Notice that if the project has support to multiple build systems, it gives
    preferences in the following order: Maven > Gradle > Ant

    None is returned if not able to detect the build manager system.
    """
    if os.path.exists("pom.xml"):
        return Maven()
    elif os.path.exists("gradlew"):
        return Gradle()
    elif os.path.exists("build.xml"):
        return Ant()

    return None
