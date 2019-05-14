# This version of the miner searches for projects based in a search criteria
# over multiple time windows.
#
# This approach is necessary to increase the number of potential subjects to
# analyze because the GitHub Search API v3 limits the query response to the
# top 1000 results. The miner overcomes this limit by querying over multiple
# time windows and returning the union of all results.
#
# Author: Jeanderson Candido <http://jeandersonbc.github.io>, Sotero Junior <https://soterojunior.github.io/>

import os, re, csv
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
    Represents a query to the GitHub's Search API check inside filename parallelism tag.

    tag = tag in parallel (Ex.: threadcount, forkcount etc..)
    repo  = repositories name
    """
    def __init__(self, params, fields):
        self.__url_template = "https://api.github.com/search/code?q={tag}+in:pom.xml+filename:pom.xml+repo:{repo}"
        self.__fields = fields
        self.__params = params

    def fetch(self):
        try:
            return self.__fetch_data()
        except HTTPError as e:
            if e.code == 403:
                find_interesting_logger.warning("sleeping")
                time.sleep(SLEEP_TIME)
                return self.__fetch_data()

    def __fetch_data(self):
        data = {}
        with urlopen(str(self)) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data

    def __repr__(self):
        return self.__url_template.format(tag=self.__params, repo=self.__fields)



def checkIfInteresting(full_name):
    """
    Checks if a project (identified by full_name) is interesting

    The project full name is the suffix of the GitHub url "{user}/{repo_name}".
    For instance, in "www.github.com/foo/bar", the full name is "foo/bar".
    """
    params_parallelism = ["parallel","forkcount",
                          "reuseforks","threadcount",
                          "useunlimitedthreads","threadcountsuites",
                          "threadcountclasses","threadcountmethods",
                          "percorethreadcount","parallelOptimized"]
    
    items_counter = 0

    for item in params_parallelism:
        find_interesting_logger.warning("Checking pom.xml with parallel params: {}".format(item))
        filter_obj = Filter(item,full_name)
        data_result = filter_obj.fetch()

        if not data_result["items"]:
            find_interesting_logger.warning("Not Found parallel params: {}".format(item))
        else:
            find_interesting_logger.warning("Found Out parallel params: {}".format(item))
            items_counter += 1
            with open('interesting_params_parallelism.csv', 'a', newline='') as fout:
                csvout = csv.DictWriter(fout, fieldnames=["full_name", "type_params_parallel"])
                csvout.writerows([{'full_name': full_name,'type_params_parallel': item}])


    return 1 if items_counter > 0 else 0


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

    params_header = ["full_name", "type_params_parallel"]

    output = CSVOutput("interesting.csv", sorted(output_header))

    output_parallel = CSVOutput("interesting_by_tag_parallel.csv", sorted(params_header))

    ## only covers projects in a certain interval range
    for min_date, max_date in TimeInterval("2017-11-01", delta=0):
        query_fields["pushed"] = "{}..{}".format(min_date, max_date)
        find_interesting_logger.warning("Date Range: {}..{}".format(min_date, max_date))
        q = Query(query_fields)
        entries_counter = 1

        ## iterates through the page objects returned from the github api
        while q.has_next():
            data = q.fetch()
            if not data["items"]:
                find_interesting_logger.warning("Search in {}..{} not found subjects!".format(min_date, max_date))
            else:
                entries = data["items"]
                ## iterates through projects from a page
                for entry in entries:
                    find_interesting_logger.warning("Starting with Subject: {}".format(entry["full_name"]))
                    project_name = entry["full_name"]
                    project_path = checkIfInteresting(project_name)
                    if project_path == 1:
                        ## write to file interesting.csv
                        find_interesting_logger.warning("Subject interesting: {} !!".format(project_name))
                        output.write(entry)
                    else:
                        find_interesting_logger.warning("Subject {} not interesting".format(project_name))

                    entries_counter += 1

if __name__ == "__main__":
    main({"language": "java", "archived": "false", "stars": ">=100"})

