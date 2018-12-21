import os, re, csv

import logging

from shutil import rmtree
from subprocess import call, check_output

from utils import TimeInterval, CSVOutput, Query, verify_maven_support, Filter, setup_logger


logger = setup_logger("find-compiled","find-compiled.log")

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

    logger.info('starting...')
    # iterating through interesting.csv rows
    currentdir = os.getcwd()
    with open('interesting.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_name = row['full_name']
            branch = row['default_branch']
            depth = 1
            dest = os.path.join(output_dir, full_name.replace(os.sep, "_"))
            logger.warning("processing project {}".format(full_name))
            # clone only the head of the project into download directory
            git_cmd = "git clone http://github.com/{} -b {} --depth {} --recursive {}".format(full_name, branch, depth, dest)
            call(git_cmd, shell=True)
            logger.warning("  cloned project")
            # clean project and download all dependencies
            os.chdir(dest)
            clean_command = "mvn clean dependency:go-offline"
            #TODO: check if we should interrupt if some depedencies are not satisfied
            call(clean_command, shell=True)
            logger.warning("  loaded dependencies")
            # compile project
            compile_command = "mvn compile test-compile package -DskipTests -Drat.skip=true -Dmaven.javadoc.skip=true -Djacoco.skip=true -Dcheckstyle.skip=true -Dfindbugs.skip=true -Dcobertura.skip=true -Dpmd.skip=true -Dcpd.skip=true -Denforcer.skip=true"
            if call(compile_command, shell=True) == 0:
                logger.warning("  compilation successful!")
                # testing project
                testing_command = "timeout -s SIGKILL 90m mvn verify -fae -Drat.skip=true -Dmaven.javadoc.skip=true -Djacoco.skip=true -Dcheckstyle.skip=true -Dfindbugs.skip=true -Dcobertura.skip=true -Dpmd.skip=true -Dcpd.skip=true -Denforcer.skip=true"
                if call(testing_command, shell=True) == 0:
                    logger.warning("  test successful!")
                    #TODO: save project name and SHA
                else:
                    #TODO: save error log to check if this project is rescuable
                    logger.warning("  test unsuccessful! aborting.")
            else:
                logger.warning("  build unsuccessful! aborting")

            ## clean the house for next project to come
            os.chdir(currentdir)
            rmtree(dest)

if __name__ == "__main__":
    main()
