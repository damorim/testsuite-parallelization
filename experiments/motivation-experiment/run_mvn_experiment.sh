#!/bin/bash
BASE_DIR="`pwd`"
SAMPLES_HOME="$BASE_DIR/samples"
PARALLEL_SETTINGS_HOME="$BASE_DIR/parallel-settings"

function compile_only {
    local subject_path=$1
    local curdir="`pwd`"
    cd "$subject_path"
    mvn -Dmaven.javadoc.skip=true -DskipTests clean install
    cd "$curdir"
}

function test_only {
    local subject_path=$1
    local curdir="`pwd`"
    cd "$subject_path"
    mvn -Dmaven.javadoc.skip=true test
    cd "$curdir"
}

function parallel_version {
    local subject_path=$1
    local test_path=$2
    local name="`basename "$subject_path"`"
    [[ ! -d "$SAMPLES_HOME/$name" ]] && cp -r "$subject_path" "$SAMPLES_HOME"

    local target="$SAMPLES_HOME/$name/$test_path"
    echo "Swapping \"pom.xml\" from \"$target\""
    rm "$target/pom.xml"
    cp "$PARALLEL_SETTINGS_HOME/$name/pom.xml" "$target"
}

# Settings
RERUNS=$1
PROJECT_PATH=$2
TEST_PATH=$3

[[ -z "$PROJECT_PATH" ]] && echo "Missing project path" && exit 1
[[ -z "$TEST_PATH" ]] && TEST_PATH="."
[[ ! -d "$SAMPLES_HOME" ]] && mkdir -p "$SAMPLES_HOME"

NAME="`basename "$PROJECT_PATH"`"
LOGNAME_PREFFIX="`date +"$NAME-%m%d%H%M%S"`"

# Main
echo "Building project \"$NAME\""
compile_only "$PROJECT_PATH" &>/dev/null

# Tests may fail due to flakiness. However, it's important to have some notion
# about how much time was dedicated to test, so we can compare to parallel execution
# (which will certainly have failures due to race conditions).
echo "Running test suite from \"$PROJECT_PATH/$TEST_PATH\""
test_only "$PROJECT_PATH/$TEST_PATH" > "$LOGNAME_PREFFIX-testseq-log.txt"
echo "Log saved on \"$LOGNAME_PREFFIX-testseq-log.txt\""

echo "Creating parallel version of \"$NAME\""
parallel_version "$PROJECT_PATH" "$TEST_PATH"
echo "Building project \"$NAME\" with parallel settings"
compile_only "$SAMPLES_HOME/$NAME" &>/dev/null

echo "Running test suite from \"$SAMPLES_HOME/$NAME/$TEST_PATH\""
# Would this be faster than sequential?
test_only "$SAMPLES_HOME/$NAME/$TEST_PATH" > "$LOGNAME_PREFFIX-testpar-log.txt"
echo "Log saved on \"$LOGNAME_PREFFIX-testpar-log.txt\""

# Part 2: Find failing tests and check if they would fail individually...
echo "Detecting failing tests in parallel (Reruns: $RERUNS)..."
./multiple_mvn_tests.py $RERUNS "$SAMPLES_HOME/$NAME/$TEST_PATH" "$LOGNAME_PREFFIX-fails-parallel" > "$LOGNAME_PREFFIX-fails-parallel.txt"
cat "$LOGNAME_PREFFIX-fails-parallel.txt" | tail -n 1
echo "Log saved on \"$LOGNAME_PREFFIX-fails-parallel.txt\""

echo "Checking if detected failing tests would fail individually (Reruns: $RERUNS)..."
./check_failures.py $RERUNS "$SAMPLES_HOME/$NAME/$TEST_PATH" "$LOGNAME_PREFFIX-fails-parallel.txt" "$LOGNAME_PREFFIX-failed-individually" > "$LOGNAME_PREFFIX-failed-individually.txt"
cat "$LOGNAME_PREFFIX-failed-individually.txt" | tail -n 1
echo "Log saved on \"$LOGNAME_PREFFIX-failed-individually.txt\""
