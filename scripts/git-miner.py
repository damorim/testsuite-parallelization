# This version of the miner searches for projects based in a search criteria
# over multiple time windows.
#
# This approach is necessary to increase the number of potential subjects to
# analyze because the GitHub Search API v3 limits the query response to the
# top 1000 results. The miner overcomes this limit by querying over multiple
# time windows and returning the union of all results.
#
# Author: Jeanderson Candido <http://jeandersonbc.github.io>, Sotero Junior <srsj2@cin.ufpe.br>
import os, re

import logging

from shutil import rmtree
from subprocess import call, check_output

from utils import TimeInterval, CSVOutput, Query, verify_maven_support, Filter

from utils import msgLogger

def git_revision(project_path):
    """
    Given a directory (or any child) associated with a cloned git repository, 
    this command returns the hash (SHA) associated with that project.
    """
    if not os.path.exists(project_path):
        return ""
    basedir = os.path.abspath(os.curdir)
    os.chdir(project_path)
    try:
        revision = check_output("git rev-parse HEAD", shell=True).decode().strip()
    except:
        revision = ""
    os.chdir(basedir)
    return revision


def checkIfInteresting(full_name, branch="master", download_dir=os.curdir):
    """
    Clones a project hosted on Github based on the given project full name.

    The project full name is the suffix of the GitHub url "{user}/{repo_name}".
    For instance, in "www.github.com/foo/bar", the full name is "foo/bar".
    By default, this function considers the latests 50 commits.
    """
    dir_name = re.sub("/", "_", full_name)
    output_dir = os.path.join(download_dir, dir_name)
    if not os.path.exists(output_dir):
        # antes de fazer o clone, verifica na api do github pelo /code
        # EX.: https://api.github.com/search/code?q=forkcount+in:pom.xml+filename:pom.xml+repo:apache/flink
        # se o params +items+ for vazio, retornar nil, senão git clone os subjects
        filter_obj = Filter(full_name)
        data_result = filter_obj.fetch()
        entries = data_result["items"]

        if not entries:
            output_dir = ""

    return output_dir


def main(query_fields, output_dir):
    """
    query_field is a dictionary indicating the selection criteria for 
    github project. These fields include:
      "language": "java",  
      "archived": "false", <-- exclude old projects
      "stars": ">=100"
    
    output_dir denotes the directory where the project will be saved.
    """
    msgLogger.info("starting a new run...")

    download_dir = os.path.join(os.curdir, output_dir)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    output_header = ["full_name", "fork", "size", "stargazers_count",
                     "default_branch", "created_at", "pushed_at"]

    output = CSVOutput("interesting.csv", sorted(output_header))

    ## only covers projects in a certain interval range
    for min_date, max_date in TimeInterval("2018-12-01", delta=0):
        query_fields["pushed"] = "{}..{}".format(min_date, max_date)
        q = Query(query_fields)
        entries_counter = 1

        ## iterates through the page objects returned from the github api
        while q.has_next():
            data = q.fetch()
            entries = data["items"]
            ## iterates through projects from a page
            for entry in entries:
                project_name = entry["full_name"]
                project_path = checkIfInteresting(project_name, entry["default_branch"], download_dir)
                if project_path:
                    ## write to file interesting.csv
                    #entry["rev"] = git_revision(project_path)
                    output.write(entry)
                else:
                    msgLogger.warning("Subject {} not interesting".format(project_name))

                entries_counter += 1

if __name__ == "__main__":
    main({"language": "java", "archived": "false", "stars": ">=100"}, "downloads")

