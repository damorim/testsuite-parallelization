# Helper classes
#
# Author: Jeanderson Candido
#
import os
from subprocess import Popen, PIPE, TimeoutExpired

class Builder:
    """ A dummy builder. """
    def compile(self):
        return False
    def test(self):
        return False
    def test_elapsed_time(self):
        return "0s"


class Maven(Builder):
    def compile(self):
        p = Popen(["mvn", "clean", "install", "-DskipTests",
                   "-Dmaven.javadoc.skip=true"], stdout=PIPE, stderr=PIPE)
        print("Compiling. PID =", p.pid)
        try:
            stdout_raw, stderr_raw = p.communicate(timeout=60*10)
        except TimeoutExpired:
            p.kill()
            stdout_raw, stderr_raw = p.communicate()

        with open("compile-log", "w") as log:
            log.write(stdout_raw.decode())
            if stderr_raw:
                log.write("----SDTERR----\n")
                log.write(stderr_raw.decode())

        return False if p.returncode else True

    def test(self):
        p = Popen(["mvn", "test", "-Dmaven.javadoc.skip=true"],
                   stdout=PIPE, stderr=PIPE)
        print("Testing. PID =", p.pid)
        stdout_raw, stderr_raw = p.communicate()
        with open("test-log", "w") as log:
            log.write(stdout_raw.decode())
            if stderr_raw:
                log.write("----SDTERR----\n")
                log.write(stderr_raw.decode())

        return False if p.returncode else True

    def __str__(self):
        return "Maven"


class Gradle(Builder):
    def compile(self):
        p = Popen(["./gradlew", "build", "-x", "test" "javadoc"],
                   stdout=PIPE, stderr=PIPE)
        print("Compiling. PID =", p.pid)
        try:
            stdout_raw, stderr_raw = p.communicate(timeout=60*10)
        except TimeoutExpired:
            p.kill()
            stdout_raw, stderr_raw = p.communicate()

        with open("compile-log", "w") as log:
            log.write(stdout_raw.decode())
            if stderr_raw:
                log.write("----SDTERR----\n")
                log.write(stderr_raw.decode())

        return False if p.returncode else True

    def test(self):
        p = Popen(["./gradlew", "test", "-x", "javadoc"],
                   stdout=PIPE, stderr=PIPE)
        print("Testing. PID =", p.pid)
        stdout_raw, stderr_raw = p.communicate()
        with open("test-log", "w") as log:
            log.write(stdout_raw.decode())
            if stderr_raw:
                log.write("----SDTERR----\n")
                log.write(stderr_raw.decode())

        return False if p.returncode else True

    def __str__(self):
        return "Gradle"


class Ant(Builder):
    def __str__(self):
        return "Ant"


def detect_build_system():
    """
    Detects the build system in the current directory.

    The verification is based if a specific path exists. Notice that
    if the project has support to multiple build systems, it gives
    preferences in the following order: Maven > Ant > Gradle

    If this routine can't determine the build system, an exception
    is raised.
    """
    if os.path.exists("pom.xml"):
        return Maven()
    elif os.path.exists("build.xml"):
        return Ant()
    elif os.path.exists("gradlew"):
        return Gradle()

    raise Exception("Could not determine build system")

