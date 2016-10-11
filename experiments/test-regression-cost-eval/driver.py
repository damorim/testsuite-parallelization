#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import os
import json
import urllib.request
from subprocess import call, Popen, CalledProcessError, PIPE

from ghwrappers.search import RepositoryQuery


def run(queryable):
    # FIXME: Consider handling pagination
    with urllib.request.urlopen(queryable.query()) as response:
        return json.loads(response.read().decode())


def run_tests_from(project):
    print("Trying to run tests from {name}".format(name=project))
    working_dir = os.path.abspath(os.curdir)
    os.chdir(project)

    # FIXME: consider detecting build system instead of assuming Maven
    p = Popen(["mvn", "clean", "test"], stderr=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate()

    stderr = stderr.decode()
    stdout = stdout.decode()
    with open("stderr-log.txt", "w") as log:
        log.write(stderr)
    with open("stdout-log.txt", "w") as log:
        log.write(stdout)

    os.chdir(working_dir)


if not os.path.exists("subjects"):
    os.mkdir("subjects")

os.chdir("subjects")

data = run(RepositoryQuery().lang("java").stars(">=100"))
print("Total items from criteria:", data["total_count"])
for item in data["items"]:
    proj_name = item["name"]
    git_url = item["html_url"]

    if not os.path.exists(proj_name):
        call(["git", "clone", git_url])

    run_tests_from(proj_name)

