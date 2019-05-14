import os, re, csv, logging, datetime

from shutil import rmtree
from subprocess import call, check_output

'''
This script takes on input the file interesting.csv and produces as output 
file testing.csv. The input file contains potential projects (containing 
directives of test parallelization in pom.xml) whereas the output file contains
a subset of those projects that compile and successfully run all tests.
'''


def main():

    scripts_dir = os.getcwd()
    ## create download directory if it does not exit
    download_dir = "downloads"    
    download_dir = os.path.join(os.curdir, download_dir)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    # iterating through interesting.csv rows
    with open('long_medium_subject.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_name = row['name']
            branch = row['default_branch']
            depth = 1
            # destination directory for the project (fully-qualified name)
            dest_dir = os.path.join(os.path.join(os.getcwd(), download_dir), full_name.replace(os.sep, "_"))
            
            # clone only the head of the project into download directory
            git_cmd = "git clone http://github.com/{} -b {} --depth {} --recursive {}".format(full_name, branch, depth, dest_dir)
            call(git_cmd, shell=True)
            print("cloned project")
            
            
            

if __name__ == "__main__":
   main()