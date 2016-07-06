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

# Settings
RERUNS=$1
PROJECT_PATH=$2
TEST_PATH=$3

[[ -z "$PROJECT_PATH" ]] && echo "Missing project path" && exit 1
[[ -z "$TEST_PATH" ]] && TEST_PATH="."

../scripts/generate_versions.sh "$PROJECT_PATH" "$TEST_PATH"

NAME="`basename "$PROJECT_PATH"`"
LOGNAME_PREFFIX="`date +"$NAME-%m%d%H%M%S"`"

# Elapsed time comparison (avg)
for version in `ls samples/$NAME`; do
    echo "Building project \"$NAME\" version \"$version\""
    compile_only "samples/$NAME/$version" &>/dev/null
    for i in `seq 1 $RERUNS`; do
        test_only "samples/$NAME/$version/$TEST_PATH" | grep "[INFO] Total time:" >> $LOGNAME_PREFFIX-$version-elapsedTime.txt
    done
done

# # # Part 2: Find failing tests and check if they would fail individually...
# # echo "Detecting failing tests in parallel (Reruns: $RERUNS)..."
# # ./multiple_mvn_tests.py $RERUNS "$SAMPLES_HOME/$NAME/$TEST_PATH" "$LOGNAME_PREFFIX-fails-parallel" > "$LOGNAME_PREFFIX-fails-parallel.txt"
# # cat "$LOGNAME_PREFFIX-fails-parallel.txt" | tail -n 1
# # echo "Log saved on \"$LOGNAME_PREFFIX-fails-parallel.txt\""
# #
# # echo "Checking if detected failing tests would fail individually (Reruns: $RERUNS)..."
# # ./check_failures.py $RERUNS "$SAMPLES_HOME/$NAME/$TEST_PATH" "$LOGNAME_PREFFIX-fails-parallel.txt" "$LOGNAME_PREFFIX-failed-individually" > "$LOGNAME_PREFFIX-failed-individually.txt"
# # cat "$LOGNAME_PREFFIX-failed-individually.txt" | tail -n 1
# # echo "Log saved on \"$LOGNAME_PREFFIX-failed-individually.txt\""
