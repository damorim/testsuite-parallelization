#!/usr/bin/env python3
'''
Downloads projects given their URL address.

Author: Jeanderson Candido <http://jeandersonbc.github.io>
'''
import argparse
import csv
import os
import shutil

from subprocess import call, DEVNULL


def is_maven(path):
    return os.path.exists(os.path.join(path, "pom.xml"))


def download(info, download_dir):
    project_name = info["full_name"]
    project_url = info["html_url"]
    revision = info["revision"]
    download_path = os.path.join(download_dir, project_name)
    if os.path.exists(download_path):
        print("Subject {} already downloaded".format(project_name))
        return

    os.chdir(download_dir)
    call(["git", "clone", project_url, project_name], stdout=DEVNULL, stderr=DEVNULL)
    print("Cloned project \"{}\"".format(project_name))
    if revision:
        os.chdir(download_path)
        call(["git", "reset", "--hard", revision], stdout=DEVNULL, stderr=DEVNULL)
        os.chdir(download_dir)

    if not is_maven(project_name):
        print("{} is not a Maven project".format(project_name))
        shutil.rmtree(project_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="CSV file with subjects to download")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise Exception("File path not valid!")

    output_dir = os.path.join(os.path.abspath(os.curdir), "downloads")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("Created directory output directory")

    with open(args.input, newline="") as f:
        reader = csv.DictReader(f)
        [download(r, output_dir) for r in reader]
