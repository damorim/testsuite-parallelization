#!/bin/bash
BASE_DIR="`pwd`"
SAMPLES_HOME="$BASE_DIR/samples"
PARALLEL_SETTINGS_HOME="$BASE_DIR/parallel-settings"
RERUNS=15

function build_only {
    local subject_path=$1
    local curdir="`pwd`"
    cd "$subject_path"
    mvn -Dmaven.javadoc.skip=true -DskipTests clean install
    cd "$curdir"
}

function build_all {
    local subject_path=$1
    local curdir="`pwd`"
    cd "$subject_path"
    mvn -Dmaven.javadoc.skip=true clean install
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

# Main
PROJECT_PATH=$1
TEST_PATH=$2
[[ -z "$PROJECT_PATH" ]] && echo "Missing project path" && exit 1
[[ -z "$TEST_PATH" ]] && TEST_PATH="."
[[ ! -d "$SAMPLES_HOME" ]] && mkdir -p "$SAMPLES_HOME"

# Should not proceed if this is not a Maven project.
ls "$PROJECT_PATH" | grep "pom.xml" &>/dev/null
if [ `echo $?` -eq 1 ]; then
    (>&2 echo "Aborted: \"pom.xml\" not found") && exit 1
fi
NAME="`basename "$PROJECT_PATH"`"
LOGNAME_PREFFIX="`date +"$NAME-%m%d%H%M%S"`"

echo "Building and testing project \"$NAME\""
build_all "$PROJECT_PATH" > "$LOGNAME_PREFFIX-build-all.txt"

echo "Creating parallel version of \"$NAME\""
parallel_version "$PROJECT_PATH" "$TEST_PATH"

echo "Building project \"$NAME\" with parallel settings"
build_only "$SAMPLES_HOME/$NAME" &>/dev/null

echo "Running tests multiple times ($RERUNS)..."
./multiple_mvn_tests.py $RERUNS "$SAMPLES_HOME/$NAME/$TEST_PATH" "$LOGNAME_PREFFIX" > "$LOGNAME_PREFFIX-parallel-fails.txt"
cat "$LOGNAME_PREFFIX-parallel-fails.txt" | tail -n 1

echo "Checking individual failures..."
./check_failures.py $RERUNS "$SAMPLES_HOME/$NAME/$TEST_PATH" "$LOGNAME_PREFFIX-parallel-fails.txt" "$LOGNAME_PREFFIX" > "$LOGNAME_PREFFIX-reruns.txt"
cat "$LOGNAME_PREFFIX-reruns.txt" | tail -n 1
