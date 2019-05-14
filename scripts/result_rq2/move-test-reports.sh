#!/bin/bash
PROJECT_DIR=$1 # the project directory with contents after running test suite

if [ -z ${PROJECT_DIR} ] || [ ! -d ${PROJECT_DIR} ];
then
    echo "Could not find project directory"
    exit -1    
fi

# return the directory where this file is located regardless from where it is called from
# https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

OUTPUT_DIR=${THISDIR}/$(basename $PROJECT_DIR)-testreports

## create directory if it does not exist
mkdir -p ${OUTPUT_DIR}

# move reports from surefire dir to some directory for later processing
for REPORT in `find ${PROJECT_DIR} | grep --text "target/surefire-reports/TEST" | grep -v "junitreports\|resources\|test-classes"`; do
    mv $REPORT ${OUTPUT_DIR}
done
