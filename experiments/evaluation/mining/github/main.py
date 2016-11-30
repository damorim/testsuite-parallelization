#!/usr/bin/env python3
import argparse
import json
import urllib.request
from urllib.error import HTTPError

from search import RepositoryQuery


def generate_subject_list(subject_csv):
    with open(subject_csv, "w") as f:
        f.write("name,url\n")

    criteria = {"language": "java", "stars": ">=100", "pushed": ">=2016-01-01", "mvn%20in": "readme"}
    current_page = 0
    page_size = 100
    query_url = None
    try:
        while True:
            current_page += 1
            query_url = RepositoryQuery(criteria).at(current_page).size(page_size).query()
            with urllib.request.urlopen(query_url) as response:
                data = json.loads(response.read().decode())
                for item in data["items"]:
                    project_name = item["name"]
                    git_url = item["html_url"]
                    with open(subject_csv, "a") as f:
                        f.write(",".join([project_name, git_url]))
                        f.write("\n")

    except HTTPError as err:
        print(err)
        if err.code == 400:
            print(query_url)
        elif err.code == 403:
            print("GitHub API Query has exhausted")
        print("Total pages:", current_page)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="output csv file")
    args = parser.parse_args()

    generate_subject_list(args.output)
