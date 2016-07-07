#!/bin/bash

function compile_only {
    local subject_path=$1
    local curdir="`pwd`"
    cd "$subject_path"
    mvn -Dmaven.javadoc.skip=true -DskipTests clean install # TODO: Ant,Gradle support
    cd "$curdir"
}

function test_only {
    local subject_path=$1
    local curdir="`pwd`"
    cd "$subject_path"
    mvn -Dmaven.javadoc.skip=true test # TODO: Ant,Gradle support
    cd "$curdir"
}

# Input parameters
PROJECT_PATH=$1
TEST_PATH=$2

# Assuming the relative path to test directory as "PROJECT_PATH"
[[ -z "$TEST_PATH" ]] && TEST_PATH="."

if [[ -z "$PROJECT_PATH" ]]; then
    echo "Usage: ./experiment.sh <PROJECT_PATH> [<TEST_PATH>]"
    exit 1
fi
../scripts/generate_versions.sh "$PROJECT_PATH" "$TEST_PATH"

NAME="`basename "$PROJECT_PATH"`"
LOGNAME_PREFFIX="`date +"$NAME-%m%d%H%M%S"`"
SAMPLE_HOME="samples/$NAME"

echo "Elapsed time comparison"
for version in `ls $SAMPLE_HOME`; do
    echo " - Building project \"$NAME\" version \"$version\""
    compile_only "$SAMPLE_HOME/$version" &>/dev/null
    test_only "$SAMPLE_HOME/$version/$TEST_PATH" | grep "\[INFO\] Total time:" | sed "s/\[INFO\]/ \- \[$version\]/g"
done

echo "Detecting failing tests in parallel execution..."
./find_parallel_failures.py "$SAMPLE_HOME/par/$TEST_PATH" "$LOGNAME_PREFFIX-fails-parallel" > "$LOGNAME_PREFFIX-fails-parallel.txt"
cat "$LOGNAME_PREFFIX-fails-parallel.txt" | tail -n 1
echo "Log saved on \"$LOGNAME_PREFFIX-fails-parallel.txt\""

echo "Checking if detected failing tests would fail individually..."
./check_failures_individually.py "$SAMPLE_HOME/par/$TEST_PATH" "$LOGNAME_PREFFIX-fails-parallel.txt" "$LOGNAME_PREFFIX-failed-individually" > "$LOGNAME_PREFFIX-failed-individually.txt"
cat "$LOGNAME_PREFFIX-failed-individually.txt" | tail -n 1
echo "Log saved on \"$LOGNAME_PREFFIX-failed-individually.txt\""
