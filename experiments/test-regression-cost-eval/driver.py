#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import os
import json
import urllib.request
from subprocess import call, check_output
from urllib.error import HTTPError

import helpers
from ghwrappers.search import RepositoryQuery

RAW_DATA_DIR = os.path.abspath(os.curdir)
TIMECOST_CSV_FILE = os.path.join(RAW_DATA_DIR, "timecost.csv")
COLUMN_SEP = ", "


def run(queryable, callback=None):
    """
    This routine executes the given query and send the output data
    to a callback function (if any).
    """
    url = queryable.query()
    print(url)
    with urllib.request.urlopen(queryable.query()) as response:
        data = json.loads(response.read().decode())
        if callback:
            callback(data)


def analyze(data):
    """
    Callback function
    """
    for item in data["items"]:
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

        print("Subject:", proj_name)
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

        with open(TIMECOST_CSV_FILE, "a") as csv:
            csv.write(COLUMN_SEP.join(log_info))
            csv.write("\n")


if __name__ == "__main__":
    if not os.path.exists("subjects"):
        os.mkdir("subjects")

    os.chdir("subjects")
    with open(TIMECOST_CSV_FILE, "w") as csv:
        csv.write(COLUMN_SEP.join(["SUBJECT", "URL", "VERSION", "BUILDER",
                                   "COMPILED", "TESTS_PASSED", "ELAPSED_TIME"]))
        csv.write("\n")

    max_pages = 1
    current_page = 0
    page_size = 5
    try:
        while True:
            current_page += 1
            if max_pages and current_page > max_pages:
                break
            print("Processing page", current_page)
            run(RepositoryQuery().lang("java")
                                 .stars(">=100")
                                 .at(current_page)
                                 .size(page_size), analyze)

    except HTTPError as err:
        print(err)
        print("Github API Query has exhausted")
        print("Total pages:", current_page)

