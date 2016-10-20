#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import csv
import json
import os
import urllib.request
from subprocess import call, check_output
from urllib.error import HTTPError

from ghwrappers.search import RepositoryQuery
from support.constants import SUBJECT_DIR, SUBJECTS_CSV_FILE, COLUMN_SEP, SUBJECTS_CSV_HEADER_FIELDS, BASE_DIR


def download_from_github():
    with open(SUBJECTS_CSV_FILE, "w") as f:
        f.write(COLUMN_SEP.join(SUBJECTS_CSV_HEADER_FIELDS))
        f.write("\n")

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

            query_url = RepositoryQuery(criteria).at(current_page).size(page_size).query()
            with urllib.request.urlopen(query_url) as response:
                data = json.loads(response.read().decode())
                for item in data["items"]:
                    project_name = item["name"]
                    git_url = item["html_url"]

                    # Cloning if project doesn't exist and ensuring we are avoiding duplicated projects
                    if not os.path.exists(project_name):
                        call(["git", "clone", "--depth", "1", git_url])

                        # Moving to project directory to collect data and going back
                        # to the subject directory.
                        os.chdir(project_name)

                        commit_ver_raw = check_output(["git", "rev-parse", "HEAD"])
                        commit_ver = commit_ver_raw.decode().strip()

                        os.chdir(SUBJECT_DIR)

                        csv_line = [project_name, git_url, commit_ver]
                        with open(SUBJECTS_CSV_FILE, "a") as f:
                            f.write(COLUMN_SEP.join(csv_line))
                            f.write("\n")

    except HTTPError as err:
        print(err)
        print("GitHub API Query has exhausted")
        print("Total pages:", current_page)


def download_from_file(file_path):
    file_abs_path = os.path.join(BASE_DIR, file_path)
    if not os.path.exists(file_abs_path):
        raise Exception("Invalid path:", file_abs_path)

    with open(file_abs_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row["URL"]
            rev = row["VERSION"]
            project_name = row["SUBJECT"]

            if not os.path.exists(project_name):
                print("Fetching project", project_name)
                os.chdir(SUBJECT_DIR)
                call(["git", "clone", url])

                os.chdir(project_name)
                call(["git", "reset", "--hard", rev])


if __name__ == "__main__":
    if not os.path.exists(SUBJECT_DIR):
        os.mkdir(SUBJECT_DIR)

    os.chdir(SUBJECT_DIR)

    # Download either from the existing file or from GitHub. Downloading from GitHub generates a new subject list
    download_from_file("subjects.csv")
    # download_from_github()
