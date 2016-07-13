#!/bin/bash
BASE_DIR="`pwd`"

# Input parameters
PROJECT_PATH=$1
TEST_PATH=$2

# Assuming the relative path to test directory as "PROJECT_PATH"
[[ -z "$TEST_PATH" ]] && TEST_PATH="."

if [[ -z "$PROJECT_PATH" ]]; then
    echo "Usage: ./experiment.sh <PROJECT_PATH> [<TEST_PATH>]"
    exit 1
fi

NAME="`basename "$PROJECT_PATH"`"
SAMPLE_HOME="$BASE_DIR/samples/$NAME"

# Removing old files before generating new project
rm -rf "$SAMPLE_HOME"
../scripts/generate_versions.sh "$PROJECT_PATH" "$TEST_PATH"

echo "Running Experiment on subject \"$NAME\""
for version in `ls $SAMPLE_HOME`; do
    OUTPUT_FILE="$BASE_DIR/$NAME-$version-summary.txt"
    echo -e "\n\t* Running setup \"$version\"" >> $OUTPUT_FILE
    echo -e "\t* Started: `date`\n" >> $OUTPUT_FILE
    ./flakiness_experiment.py "$NAME" "$SAMPLE_HOME/$version" "$TEST_PATH" >> $OUTPUT_FILE
    echo -e "\n\t* Finished: `date`\n" >> $OUTPUT_FILE
done

[[ ! -d outputs ]] && mkdir outputs
mv *testLog* outputs
