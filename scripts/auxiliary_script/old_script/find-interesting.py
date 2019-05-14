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
import time
import logging
import json
from shutil import rmtree
from subprocess import call, check_output
from urllib.request import urlopen, HTTPError
from utils import CSVOutput, create_logger, SLEEP_TIME

find_interesting_logger = create_logger("find-interesting","find-interesting.log")

from datetime import date, timedelta
class TimeInterval:
    def __init__(self, since, until=None, delta=30):
        self.starting_date = self.datefromstr(since)
        self.ending_date = self.datefromstr(until) if until else date.today()
        self.delta = timedelta(days=delta)

    @staticmethod
    def datefromstr(datestr):
        fields = [int(e) for e in datestr.split("-")]
        return date(fields[0], fields[1], fields[2])

    def __iter__(self):
        return self

    def __next__(self):
        if self.starting_date > self.ending_date:
            raise StopIteration
        next_date = self.starting_date + self.delta
        interval = (self.starting_date.isoformat(), next_date.isoformat())
        self.starting_date = next_date + timedelta(days=1)
        return interval

class Query:
    """
    Represents a paginated query to the GitHub's Search API for repositories.
    Query fields are represented as a key-value map like the following:

        query_fields = {"language": "java", "stars": ">=1000"}

    Basic Usage:

        q = Query({"language": "java", "stars": ">=1000"})
        while (q.has_next()):
            q.fetch()
    """
    def __init__(self, fields):
        self.__url_template = "https://api.github.com/search/repositories?q={query}&per_page=100&page={page}"
        self.__fields = "+".join(["{}:{}".format(k, v) for k, v in fields.items()])
        self.__page = 1
        self.__max_page = Query.__request_handler(self.__get_last_page)

    def has_next(self):
        return self.__page <= self.__max_page

    def fetch(self):
        if not self.has_next():
            raise Exception("Query has exhausted")
        data = Query.__request_handler(self.__fetch_data)
        self.__page += 1
        return data

    @staticmethod
    def __request_handler(callee):
        try:
            return callee()
        except HTTPError as e:
            if e.code == 403:
                find_interesting_logger.warning("sleeping")
                time.sleep(SLEEP_TIME)
                return callee()

    def __get_last_page(self):
        with urlopen(str(self)) as response:
            header_link = response.getheader("Link")
            if header_link is None:
                return self.__page
            else:
                last_link = [link for link in header_link.split(",") if "rel=\"last\"" in link][0]
                sub_field = re.search("&page=[0-9]+", last_link).group(0)
                return int(re.search("[0-9]+", sub_field).group(0))

    def __fetch_data(self):
        data = {}
        with urlopen(str(self)) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data

    def __repr__(self):
        return self.__url_template.format(query=self.__fields, page=self.__page)


class Filter:
    """
    Represents a paginated query to the GitHub's Search API for repositories.
    Query fields are represented as a key-value map like the following:

        query_fields = {"language": "java", "stars": ">=1000"}

    Basic Usage:

        q = Query({"language": "java", "stars": ">=1000"})
        while (q.has_next()):
            q.fetch()
    """
    def __init__(self, fields):
        self.__url_template = "https://api.github.com/search/code?q=forkcount+in:pom.xml+filename:pom.xml+repo:{query}"
        self.__fields = fields

    def fetch(self):
        try:
            return self.__fetch_data()
        except HTTPError as e:
            if e.code == 403:
                find_interesting_logger.warning("sleeping")
                time.sleep(SLEEP_TIME)
                return self.__fetch_data()

    def __fetch_data(self):
        #msgLogger.warning("Checking Project {} ...".format(self.__fields))
        data = {}
        with urlopen(str(self)) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data

    def __repr__(self):
        return self.__url_template.format(query=self.__fields)



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

