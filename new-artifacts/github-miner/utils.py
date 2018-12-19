import csv
import os
import re
import time
import json

from datetime import date, timedelta
from urllib.request import urlopen, HTTPError


MAVEN_SKIPS="-Drat.skip=true -Dmaven.javadoc.skip=true " \
            "-Djacoco.skip=true -Dcheckstyle.skip=true " \
            "-Dfindbugs.skip=true -Dcobertura.skip=true " \
            "-Dpmd.skip=true -Dcpd.skip=true"


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


class CSVOutput:
    def __init__(self, file_name, header):
        self.__file_name = self.__verify(file_name)
        self.__file_path = os.path.abspath(self.__file_name)
        self.__fields = header
        with open(self.__file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.__fields)
            writer.writeheader()

    def name(self):
        return self.__file_name

    def write(self, entry):
        with open(self.__file_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.__fields)
            writer.writerow({k: v for k, v in entry.items() if k in self.__fields})

    def __verify(self, file_name, counter=1):
        if not os.path.exists(file_name):
            return file_name
        file_name = re.sub("(-[0-9]+)?\.", "-{}.".format(counter), file_name)
        return self.__verify(file_name, counter=counter + 1)


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
                print("Seems like I exceeded the number of requests per minute...")
                print("I'm gonna sleep for 1 min and try again later...")
                time.sleep(60)
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
        data = Filter.__request_handler(self.__fetch_data)
        return data

    @staticmethod
    def __request_handler(callee):
        try:
            return callee()
        except HTTPError as e:
            if e.code == 403:
                print("Seems like I exceeded the number of requests per minute...")
                print("I'm gonna sleep for 1 min and try again later...")
                time.sleep(60)
                return callee()

    def __fetch_data(self):
        print("OPENURL Nome do PRojeto {}".format(self.__fields))
        data = {}
        with urlopen(str(self)) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data

    def __repr__(self):
        return self.__url_template.format(query=self.__fields)


def verify_maven_support(project_path):
    return os.path.exists(os.path.join(project_path, "pom.xml"))

