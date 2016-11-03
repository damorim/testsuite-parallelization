# FIXME DEPRECATED MODULE
#
# Helper classes
#
# Author: Jeanderson Candido
#
import os
import re
from subprocess import call, Popen, PIPE, TimeoutExpired


# FIXME DEPRECATED FUNCTION
def build():
    with open(os.devnull, "wb") as DEVNULL:
        compile_command = ["mvn", "clean", "install", "-DskipTests", "-Dmaven.javadoc.skip=true"]
        try:
            result = not call(compile_command, stdout=DEVNULL, timeout=900)
        except TimeoutExpired:
            result = False
    return result


# FIXME DEPRECATED FUNCTION
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


# FIXME DEPRECATED FUNCTION
def is_maven_project():
    """ Returns true if the current dir has a pom.xml file. """
    return os.path.exists("pom.xml")
