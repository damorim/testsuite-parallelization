#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import os
import json
import urllib.request
from subprocess import call, Popen, PIPE

from ghwrappers.search import RepositoryQuery


def run(queryable):
    # FIXME: Consider handling pagination
    with urllib.request.urlopen(queryable.query()) as response:
        return json.loads(response.read().decode())


def run_tests_from(project):
    working_dir = os.path.abspath(os.curdir)
    os.chdir(project)

    # FIXME: consider detecting build system instead of assuming Maven
    p = Popen(["mvn", "clean", "test"], stderr=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate()

    print("Return code:", p.returncode)
    if not p.returncode:
        stdout = stdout.decode()
        with open("stdout-log.txt", "w") as log:
            log.write(stdout)
    else:
        stderr = stderr.decode()
        with open("stderr-log.txt", "w") as log:
            log.write(stderr)

    os.chdir(working_dir)


if not os.path.exists("subjects"):
    os.mkdir("subjects")

os.chdir("subjects")

data = run(RepositoryQuery().lang("java").stars(">=100"))
print("Total items from criteria:", data["total_count"])
counter = 1
for item in data["items"]:
    proj_name = item["name"]
    git_url = item["html_url"]

    if not os.path.exists(proj_name):
        call(["git", "clone", git_url])

    print("{curr}/{total} - Trying to run tests from {name}".format(name=proj_name,
                                                                    total=len(data["items"]),
                                                                    curr=counter))
    run_tests_from(proj_name)
    counter += 1

