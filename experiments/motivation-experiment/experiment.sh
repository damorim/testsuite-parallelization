#!/bin/bash
BASE_DIR="`pwd`"
BUILD_FILES_DIR="$BASE_DIR/buildfiles"

# Input parameters
PROJECT_PATH=$1
TEST_REL_PATH=$2

if [ -z "$PROJECT_PATH" ]; then
    echo "Usage: ./experiment.sh <project path> [<test relative path>]"
    exit 1
fi

# Assuming the relative path to test directory as "PROJECT_PATH"
[[ -z "$TEST_REL_PATH" ]] && TEST_REL_PATH="."

NAME="`basename "$PROJECT_PATH"`"
BUILD_FILES_HOME="$BUILD_FILES_DIR/$NAME"

echo "Running Experiment on subject \"$NAME\""

# Uncomment to log execution
#LOG="`basename $PROJECT_PATH`-`date +"%m%d%H%M"`-summary.txt"
#{
    echo "Started at `date`"
    ./experiment.py $BUILD_FILES_HOME $PROJECT_PATH $TEST_REL_PATH
    echo "Finished at `date`"

#} > $LOG
