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

from utils import find_interesting_logger


def checkIfInteresting(full_name, branch="master"):
    """
    Checks if a project (identified by full_name) is interesting

    The project full name is the suffix of the GitHub url "{user}/{repo_name}".
    For instance, in "www.github.com/foo/bar", the full name is "foo/bar".
    """
    filter_obj = Filter(full_name)
    data_result = filter_obj.fetch()

    if not data_result["items"]:
        output_dir = ""

    return output_dir


def main(query_fields):
    """
    query_field is a dictionary indicating the selection criteria for 
    github project. These fields include:
      "language": "java",  
      "archived": "false", <-- exclude old projects
      "stars": ">=100"
    
    output_dir denotes the directory where the project will be saved.
    """
    find_interesting_logger.info("starting a new run...")

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
                project_path = checkIfInteresting(project_name, entry["default_branch"])
                if project_path:
                    ## write to file interesting.csv
                    #entry["rev"] = git_revision(project_path)
                    output.write(entry)
                else:
                    find_interesting_logger.warning("Subject {} not interesting".format(project_name))

                entries_counter += 1

if __name__ == "__main__":
    main({"language": "java", "archived": "false", "stars": ">=100"})

