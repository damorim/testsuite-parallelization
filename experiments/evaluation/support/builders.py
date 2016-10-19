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

    def test(self, data=None):
        args = ["time", "-o", "/tmp/timeinfo", "-f", "%e,%S,%U,%P"]
        args.extend(self.test_args)
        with open("/dev/null", "wb") as DEVNULL:
            p = Popen(args, stdout=PIPE, stderr=DEVNULL)
        print("PID (use pstree):", p.pid)
        out, err = p.communicate()

        output = out.decode().splitlines()
        total = 0
        for i in range(len(output)):
            line = output[i]
            if line.startswith("Results :"):
                for j in range(len(output)):
                    test_line = output[i + j]
                    if "Tests run" in test_line:
                        total += int(re.sub(",.*", "", re.sub("Tests run: ", "", test_line)))
                        break
        if data:
            data["#tests"] = total
            with open("/tmp/timeinfo") as f:
                for line in f:
                    if not line.startswith("Command"):
                        output = line.strip().split(",")
                        data["elapsed_t"] = output[0]
                        data["system_t"] = output[1]
                        data["user_t"] = output[2]
                        data["cpu_usage"] = output[3]

        return not p.returncode


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
        return None  # TODO Feel free to implement Gradle support
    elif os.path.exists("build.xml"):
        return None  # TODO Feel free to implement Ant support

    return None
