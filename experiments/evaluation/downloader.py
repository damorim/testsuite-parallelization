#!/usr/bin/python3
#
# Author: Jeanderson Candido
#
import csv
import os
import re
from collections import Counter
from subprocess import call, check_output, Popen, PIPE

from support.utils import detect_builder

BASE_DIR = os.path.abspath(os.curdir)
SUBJECT_DIR = os.path.join(BASE_DIR, "subjects")


def download_from_file(file_abs_path):
    if not os.path.exists(file_abs_path):
        raise Exception("Invalid path:", file_abs_path)

    with open(file_abs_path) as f:
        reader = csv.DictReader(f)

    for row in reader:
        url = row["URL"]
        project_name = row["SUBJECT"]
        try:
            revision = row["REVISION"]
        except KeyError:
            revision = None

        project_path = os.path.join(SUBJECT_DIR, project_name)
        if not os.path.exists(project_path):
            print("Fetching project", project_name)
            os.chdir(SUBJECT_DIR)
            call(["git", "clone", url])
            if revision:
                call(["git", "reset", "--hard", revision])


def verify_subjects_from(output_file):
    output_file = os.path.abspath(output_file)
    with open(output_file, "w") as out:
        out.write("SUBJECT,URL,REV,BUILDER,COMPILED\n")

    builder_counter = Counter()
    compiled_counter = Counter()
    progress_counter = 1

    # FIXME consider reading from download.csv instead of listing the directory
    for subject in sorted(os.listdir(SUBJECT_DIR)):
        subject_path = os.path.join(SUBJECT_DIR, subject)
        if os.path.isdir(subject_path):
            print("Progress: {}# - {}".format(progress_counter, subject))
            os.chdir(subject_path)

            git_remote_output = check_output(["git", "remote", "-v"]).decode()
            sanitized_output = re.sub(r"\s", " ", git_remote_output)
            url = sanitized_output.split(" ")[1]

            revision = check_output(["git", "rev-parse", "HEAD"]).decode().strip()
            builder = detect_builder()
            if not builder:
                compiled = "n/a"
                builder_name = "unknown"
            else:
                builder_name = builder.name
                try:
                    fifteen_min = 15 * 60
                    p = Popen(builder.args, stderr=PIPE, stdout=PIPE)
                    p.communicate(timeout=fifteen_min)
                    exit_status = p.returncode
                except Exception as err:
                    with open(os.path.join(BASE_DIR, "downloader-errors.txt"), "a") as log:
                        log.write("{} - {}\n".format(subject, err))
                    exit_status = 1
                compiled = "false" if exit_status else "true"

            compiled_counter.update([compiled])
            builder_counter.update([builder_name])

            print("  Builder{}\n  Compiled{}\n".format(builder_counter, compiled_counter))
            progress_counter += 1

            output_entry = [subject, url, revision, builder_name, compiled]
            with open(output_file, "a") as out:
                out.write(",".join(output_entry))
                out.write("\n")


if __name__ == "__main__":
    if not os.path.exists(SUBJECT_DIR):
        os.mkdir(SUBJECT_DIR)

    # download_from_file(file_abs_path="./mining/github/download.csv")
    verify_subjects_from(output_file="subjects.csv")
