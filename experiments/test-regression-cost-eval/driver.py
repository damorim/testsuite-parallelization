#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import os
import json
import urllib.request
from subprocess import call, check_output

import helpers
from ghwrappers.search import RepositoryQuery


RAW_DATA_DIR = os.path.abspath(os.curdir)

# FIXME temporary flag to limit execution
MAX_PROJECTS = 5

def run(queryable, callback=None):
    # FIXME: Consider handling pagination
    with urllib.request.urlopen(queryable.query()) as response:
        data = json.loads(response.read().decode())
        print("Total items from criteria:", data["total_count"], "\n")
        if callback:
            callback(data)


def analyze(data):
    column_sep = ", "
    csv_file = os.path.join(RAW_DATA_DIR, "subjects-data.csv")

    with open(csv_file, "w") as csv:
        csv.write(column_sep.join(["SUBJECT", "URL", "VERSION", "BUILDER",
                                   "COMPILED", "TESTED", "ELAPSED_TIME"]))
        csv.write("\n")

    item_counter = 1
    for item in data["items"]:
        if item_counter > MAX_PROJECTS:
            break

        proj_name = item["name"]
        git_url = item["html_url"]

        # Cloning if project doesn't exist
        if not os.path.exists(proj_name):
            call(["git", "clone", git_url])

        # Moving to project directory to collect data and coming back
        # to the working directory.
        working_dir = os.path.abspath(os.curdir)
        os.chdir(proj_name)

        commit_ver_raw = check_output(["git", "rev-parse", "HEAD"])
        commit_ver = commit_ver_raw.decode().strip()

        print("{id}) {subj}".format(id=item_counter, subj=proj_name))
        try:
            builder = helpers.detect_build_system()
            compiled = builder.compile()
            tested = False if not compiled else builder.test()
            elapsed_time = builder.test_elapsed_time()

        except Exception as err:
            print(err)
            builder = "N/A"
            compiled = "N/A"
            tested = "N/A"
            elapsed_time = "N/A"

        os.chdir(working_dir)

        log_info = []
        log_info.append(proj_name)
        log_info.append(git_url)
        log_info.append(commit_ver)
        log_info.append(str(builder))
        log_info.append(str(compiled))
        log_info.append(str(tested))
        log_info.append(elapsed_time)

        with open(csv_file, "a") as csv:
            csv.write(column_sep.join(log_info))
            csv.write("\n")

        item_counter += 1


if __name__ == "__main__":
    if not os.path.exists("subjects"):
        os.mkdir("subjects")

    os.chdir("subjects")

    run(RepositoryQuery().lang("java").stars(">=100"), analyze)
