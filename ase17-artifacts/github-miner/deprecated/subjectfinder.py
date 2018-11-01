#!/usr/bin/env python3
'''
Searches for subjects on GitHub based in a criteria

Author: Jeanderson Candido <http://jeandersonbc.github.io>
'''
import argparse
import csv
import json
import time

from getpass import getpass
from urllib.request import urlopen
from urllib.error import HTTPError


URL_TEMPLATE = "https://api.github.com/search/repositories?" \
               "q={query}&sort=stars&page={page}&per_page=100"


def build_query(q):
    return "+".join(["{key}:{val}".format(key=k, val=v) for k, v in q.items()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="CSV file with subjects to download")
    args = parser.parse_args()

    query = build_query({"mvn%20in": "readme", "stars": ">=100", "language": "java", "pushed": ">=2016"})
    entries = []
    page_num = 1 
    try:
        while True:
            print("Processing page", page_num)
            url = URL_TEMPLATE.format(query=query, page=page_num)
            with urlopen(url) as response:
                data = json.loads(response.read().decode())
                items = data["items"]

            entries.extend(items)
            print("Current entries:", len(entries))
            page_num += 1

            time.sleep(5)

    except HTTPError as err:
        print(err)
        print("Total pages:", page_num)

    fields = ["html_url", "full_name", "revision"]
    with open(args.output, "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        for entry in entries:
            entry["full_name"] = entry["full_name"].replace("/", "_")
            writer.writerow({k:v for k, v in entry.items() if k in fields})

