import os, re, csv

import logging

from shutil import rmtree
from subprocess import call, check_output

from utils import TimeInterval, CSVOutput, Query, verify_maven_support, Filter

logging.basicConfig(format='[%(asctime)-15s] %(message)s', filename="find-compiled.log", level=logging.DEBUG)
find_compiled_logger = logging.getLogger('find-compiled')

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

def main():

    ## create download directory if it does not exit
    output_dir = "downloads"    
    download_dir = os.path.join(os.curdir, output_dir)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    find_compiled_logger.info('starting...')
    # iterating through interesting.csv rows
    currentdir = os.getcwd()
    with open('interesting.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_name = row['full_name']
            branch = row['default_branch']
            depth = 1
            dest = os.path.join(output_dir, full_name.replace(os.sep, "_"))
            # clone only the head of the project into download directory
            git_cmd = "git clone http://github.com/{} -b {} --depth {} --recursive {}".format(full_name, branch, depth, dest)
            call(git_cmd, shell=True)
            find_compiled_logger.warning("cloned project {}".format(full_name))
            # clean project and download all dependencies
            os.chdir(dest)
            clean_command = "mvn clean dependency:go-offline"
            #TODO: check if we should interrupt if some depedencies are not satisfied
            call(clean_command, shell=True)

            # compile project
            compile_command = "mvn compile test-compile package -DskipTests -Drat.skip=true -Dmaven.javadoc.skip=true -Djacoco.skip=true -Dcheckstyle.skip=true -Dfindbugs.skip=true -Dcobertura.skip=true -Dpmd.skip=true -Dcpd.skip=true -Denforcer.skip=true"
            #TODO: abort if compile is not successful
            if call(compile_command, shell=True) == 0:
                find_compiled_logger.warning("build successful!")

            ## clean the house for next project to come
            os.chdir(currentdir)
            rmtree(dest)
            # compile project ...


if __name__ == "__main__":
    main()
