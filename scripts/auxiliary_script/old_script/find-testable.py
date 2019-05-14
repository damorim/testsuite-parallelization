import os, re, csv, logging, datetime

from shutil import rmtree
from subprocess import call, check_output
from utils import CSVOutput, create_logger

logger = create_logger("find-testable", "find-testable.log")

'''
This script takes on input the file interesting.csv and produces as output 
file testing.csv. The input file contains potential projects (containing 
directives of test parallelization in pom.xml) whereas the output file contains
a subset of those projects that compile and successfully run all tests.
'''

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

    scripts_dir = os.getcwd()
    ## create download directory if it does not exit
    download_dir = "downloads"    
    download_dir = os.path.join(os.curdir, download_dir)
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    # layout of csv file
    output_header = ["full_name", "sha", "date"]
    testable_csv_output= CSVOutput("testable.csv", sorted(output_header))

    logger.info('starting...')
    # iterating through interesting.csv rows
    with open('interesting.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_name = row['full_name']
            branch = row['default_branch']
            depth = 1
            # destination directory for the project (fully-qualified name)
            dest_dir = os.path.join(os.path.join(os.getcwd(), download_dir), full_name.replace(os.sep, "_"))
            logger.warning("processing project {}".format(full_name))
            # clone only the head of the project into download directory
            git_cmd = "git clone http://github.com/{} -b {} --depth {} --recursive {}".format(full_name, branch, depth, dest_dir)
            call(git_cmd, shell=True)
            logger.warning("  cloned project")
            # clean project and download all dependencies
            os.chdir(dest_dir)
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
                    # move test reports to a file
                    collect_test_results_command = os.path.join(scripts_dir, "move-test-reports.sh ") + dest_dir
                    if call(collect_test_results_command, shell=True) == 0:
                        logger.warning("  successfully collected test results!")
                        ## save project name and sha in csv
                        entry = {"full_name": full_name, "sha": git_revision(dest_dir), "date": datetime.date.today().strftime("%B %d, %Y")}
                        testable_csv_output.write(entry)
                    else:
                        logger.warning("  could not collect test results!")
                else:
                    logger.warning("  test unsuccessful! aborting.")
            else:
                logger.warning("  build unsuccessful! aborting")

            ## clean the house for next project to come
            os.chdir(scripts_dir)
            rmtree(dest_dir)

if __name__ == "__main__":
   main()