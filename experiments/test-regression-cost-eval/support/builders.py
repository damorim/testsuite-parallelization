# Helper classes
#
# Author: Jeanderson Candido
#
import os
from subprocess import call, Popen, PIPE

import re


class AbstractBuilder:
    def __init__(self):
        self.name = None
        self.compile_args = None
        self.test_args = None

    def compile(self):
        """ Returns True if finished successfully """
        return not call(self.compile_args)

    def test(self):
        pass


class Maven(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.name = "Maven"
        self.compile_args = ["mvn", "clean", "install", "-DskipTests", "-Dmaven.javadoc.skip=true"]
        self.test_args = ["mvn", "test", "-Dmaven.javadoc.skip=true"]

    def test(self, data=None):
        p = Popen(self.test_args, stdout=PIPE)
        out, err = p.communicate()

        # Fixme collect # of tests
        output = out.decode()
        print(output)

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
