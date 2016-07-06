#!/bin/bash
BASE_DIR="`pwd`"
SAMPLES_HOME="$BASE_DIR/samples"
BUILDFILES_HOME="$BASE_DIR/buildfiles"

function generate_versions {
    local subject_path=$1
    local test_path=$2
    local name="`basename "$subject_path"`"

    if [ ! -d "$BUILDFILES_HOME/$name" ]; then
        echo "Aborting: No build file found for subject \"$NAME\""
        exit 1
    fi
    local destiny="$SAMPLES_HOME/$name"
    [[ ! -d "$destiny" ]] && mkdir -p "$destiny"

    for buildfile in `ls $BUILDFILES_HOME/$name`; do
        dirname="${buildfile%.*}"
        mkdir -p "$destiny/$dirname"
        cp -r $subject_path/* "$destiny/$dirname"

        local target="$destiny/$dirname/$test_path"
        rm "$target/pom.xml"
        cp "$BUILDFILES_HOME/$name/$buildfile" "$target"
        mv "$target/$buildfile" "$target/pom.xml"
    done
}

# Settings
PROJECT_PATH=$1
TEST_PATH=$2

[[ -z "$PROJECT_PATH" ]] && echo "Missing project path" && exit 1
[[ -z "$TEST_PATH" ]] && TEST_PATH="."

echo "Generating parallel and sequential versions of \"`basename ${PROJECT_PATH}`\""
generate_versions "$PROJECT_PATH" "$TEST_PATH"
