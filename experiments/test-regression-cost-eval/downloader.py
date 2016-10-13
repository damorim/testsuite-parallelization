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
SUBJECTS_CSV_FILE = os.path.join(RAW_DATA_DIR, "subjects.csv")
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


def download(data):
    """
    Callback function
    """
    for item in data["items"]:
        proj_name = item["name"]
        git_url = item["html_url"]

        # Cloning if project doesn't exist
        if not os.path.exists(proj_name):
            call(["git", "clone", "--depth", "1", git_url])

        # Moving to project directory to collect data and coming back
        # to the working directory.
        working_dir = os.path.abspath(os.curdir)
        os.chdir(proj_name)

        commit_ver_raw = check_output(["git", "rev-parse", "HEAD"])
        commit_ver = commit_ver_raw.decode().strip()
        builder = helpers.detect_build_system()

# TODO: Lines commented because we want to build the subject
#       list first with each respective commit version.
#
#            compiled = builder.compile()
#            tested = False if not compiled else builder.test()
#            elapsed_time = builder.test_elapsed_time()
#
#            compiled = "N/A"
#            tested = "N/A"
#            elapsed_time = "N/A"

        os.chdir(working_dir)

        csv_line = []
        csv_line.append(proj_name)
        csv_line.append(git_url)
        csv_line.append(commit_ver)
        csv_line.append(str(builder))
#        csv_line.append(str(compiled))
#        csv_line.append(str(tested))
#        csv_line.append(elapsed_time)

        with open(SUBJECTS_CSV_FILE, "a") as csv:
            csv.write(COLUMN_SEP.join(csv_line))
            csv.write("\n")


if __name__ == "__main__":
    if not os.path.exists("subjects"):
        os.mkdir("subjects")

    os.chdir("subjects")
    with open(SUBJECTS_CSV_FILE, "w") as csv:
        csv.write(COLUMN_SEP.join(["SUBJECT", "URL", "VERSION", "BUILDER"]))
        csv.write("\n")

    max_pages = None
    current_page = 0
    page_size = 100
    try:
        while True:
            current_page += 1
            if max_pages and current_page > max_pages:
                break
            print("Processing page", current_page)
            criteria = {"language": "java", "stars": ">=100"}
            run(RepositoryQuery(criteria).at(current_page)
                                         .size(page_size), download)

    except HTTPError as err:
        print(err)
        print("Github API Query has exhausted")
        print("Total pages:", current_page)

