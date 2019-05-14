#!/bin/bash
#
# Invokes maven compile and test for projects from a given directory
#
# Usage:   ./compile-test.sh <TIMEOUT> <PROJECTS_DIR> <OUTPUT_DIR>
# Example: ./compile-test.sh 90m ./downloads/projects ./rawdata
#
TIMEOUT=$1

INPUT_DIR=$2
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Invalid path download"
    exit 1
fi

OUTPUT_DIR="`readlink -e $3`"
if [[ ! -d "$OUTPUT_DIR" ]]; then
    echo "Invalid path rawdata"
    exit 1
fi

MAVEN_SKIPS="-Drat.skip=true -Dmaven.javadoc.skip=true -Djacoco.skip=true \
             -Dcheckstyle.skip=true -Dfindbugs.skip=true -Dcobertura.skip=true \
             -Dpmd.skip=true -Dcpd.skip=true -Denforcer.skip=true"

TS="`date +"%m%d%H%M%S"`"

for PROJECT in `ls "$INPUT_DIR"`; do

    # Watch out for ending slash
    PROJECT_PATH="$INPUT_DIR/$PROJECT"
    if [[ ! -d "$PROJECT_PATH" ]]; then
        echo "Invalid path \"$PROJECT_PATH\". Skipping..."
        continue
    fi

    PROJECT_OUTPUT="$OUTPUT_DIR/$PROJECT/$TS"
    if [[ ! -d "$PROJECT_OUTPUT" ]]; then
        mkdir -p "$PROJECT_OUTPUT"
    fi
 
    pushd $PROJECT_PATH
    mvn clean dependency:go-offline 2>&1
    mvn compile test-compile package -DskipTests $MAVEN_SKIPS 2>&1 \
        | tee $PROJECT_OUTPUT/compile.log
    timeout -s SIGKILL $TIMEOUT mvn verify -fae $MAVEN_SKIP 2>&1 \
        | tee $PROJECT_OUTPUT/testing.log

    # Get reports from surefire dir
    for REPORT in `find . | grep --text "target/surefire-reports/TEST" | grep -v "junitreports\|resources\|test-classes"`; do
        mv $REPORT $PROJECT_OUTPUT
    done
    popd
done
