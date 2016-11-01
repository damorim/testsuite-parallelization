import json
import urllib.request
from urllib.error import HTTPError

from mining.github.search import RepositoryQuery


def generate_subject_list():
    subject_csv = "download.csv"
    with open(subject_csv, "w") as f:
        f.write("SUBJECT,URL\n")

    criteria = {"language": "java", "stars": ">=100"}
    current_page = 0
    page_size = 100
    try:
        while True:
            current_page += 1
            query_url = RepositoryQuery(criteria).at(current_page).size(page_size).query()
            with urllib.request.urlopen(query_url) as response:
                data = json.loads(response.read().decode())
                for item in data["items"]:
                    project_name = item["name"]
                    git_url = item["html_url"]
                    csv_line = [project_name, git_url]
                    with open(subject_csv, "a") as f:
                        f.write(",".join(csv_line))
                        f.write("\n")

    except HTTPError as err:
        print(err)
        print("GitHub API Query has exhausted")
        print("Total pages:", current_page)

if __name__ == "__main__":
    generate_subject_list()
