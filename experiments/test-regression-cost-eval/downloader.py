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
from constants import SUBJECT_DIR, SUBJECTS_CSV_FILE
from ghwrappers.search import RepositoryQuery


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

        # Moving to project directory to collect data and going back
        # to the subject directory.
        os.chdir(proj_name)

        commit_ver_raw = check_output(["git", "rev-parse", "HEAD"])
        commit_ver = commit_ver_raw.decode().strip()
        builder = helpers.detect_build_system()

        os.chdir(SUBJECT_DIR)

        csv_line = []
        csv_line.append(proj_name)
        csv_line.append(git_url)
        csv_line.append(commit_ver)
        csv_line.append(str(builder))

        with open(SUBJECTS_CSV_FILE, "a") as csv:
            csv.write(COLUMN_SEP.join(csv_line))
            csv.write("\n")


if __name__ == "__main__":
    if not os.path.exists(SUBJECT_DIR):
        os.mkdir(SUBJECT_DIR)

    os.chdir(SUBJECT_DIR)
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
            criteria = {"language": "java",
                        "stars": ">=100"}

            run(RepositoryQuery(criteria).at(current_page)
                                         .size(page_size), download)

    except HTTPError as err:
        print(err)
        print("Github API Query has exhausted")
        print("Total pages:", current_page)

