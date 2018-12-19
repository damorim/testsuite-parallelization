# This version of the miner searches for projects based in a search criteria
# over multiple time windows.
#
# This approach is necessary to increase the number of potential subjects to
# analyze because the GitHub Search API v3 limits the query response to the
# top 1000 results. The miner overcomes this limit by querying over multiple
# time windows and returning the union of all results.
#
# Author: Jeanderson Candido <http://jeandersonbc.github.io>
import os, re

from shutil import rmtree
from subprocess import call, check_output

from utils import TimeInterval, CSVOutput, Query, verify_maven_support, Filter


def git_revision(project_path):
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


def git_clone(full_name, branch="master", download_dir=os.curdir):
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
            print("Subject without pom.xml and ForkCount")
            output_dir = ""
        else:
            git_cmd = "git clone http://github.com/{} -b {} --depth {} --recursive {}"
            call(git_cmd.format(full_name, branch, 50, output_dir), shell=True)


    return output_dir


def fetcher(query_fields, output_dir):
    download_dir = os.path.join(os.curdir, output_dir)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    output_header = ["full_name", "fork", "size", "stargazers_count",
                     "default_branch", "created_at", "pushed_at",
                     "ismaven", "rev"]

    output = CSVOutput("fetched-projects.csv", sorted(output_header))

    total_entries = 0
    for min_date, max_date in TimeInterval("2018-12-01", delta=0):
        query_fields["pushed"] = "{}..{}".format(min_date, max_date)
        q = Query(query_fields)

        entries_counter = 0
        while q.has_next():
            print("Processing query", q)
            data = q.fetch()
            entries = data["items"]
            for entry in entries:
                project_path = git_clone(entry["full_name"], entry["default_branch"], download_dir)
                if project_path == "":
                    print("Subject has not parallel !!")
                else:
                    entry["rev"] = git_revision(project_path)
                    has_maven_support = verify_maven_support(project_path)
                    entry["ismaven"] = has_maven_support
                    output.write(entry)
                    print("Writing in CSV !!")


                    if os.path.exists(project_path) and not has_maven_support:
                        print("Pom.xml not found - removing path", project_path)
                        rmtree(project_path)

        
            entries_counter += len(entries)
            print("Progress: {}/{} items".format(entries_counter, data["total_count"]))

        total_entries += entries_counter
        print("Processed a total of {} items".format(total_entries))

    print("Results persisted in {}".format(output.name()))

    compile_cmd = "./compile-test-new.sh 90m ./downloads ./raw_data"
    call(compile_cmd, shell=True)
   

if __name__ == "__main__":
    fetcher({"language": "java", "archived": "false", "stars": ">=100"}, "downloads")

