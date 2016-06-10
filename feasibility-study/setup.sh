#!/bin/bash
BASE_DIR="`pwd`"
SUBJECTS_HOME="$BASE_DIR/subjects"
POMFILES_HOME="$BASE_DIR/pomfiles"

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

function install_pom {
    local subject_path=$1
    local test_path=$2

    local name="`basename "$subject_path"`"
    local target="$subject_path/$test_path"

    echo "Swapping \"pom.xml\" from \"$target\""
    rm "$target/pom.xml"
    cp "$POMFILES_HOME/$name/pom.xml" "$target"
}

# Settings
PROJECT_PATH=$1
TEST_PATH=$2
[[ -z "$PROJECT_PATH" ]] && echo "Missing project path" && exit 1
[[ -z "$TEST_PATH" ]] && TEST_PATH="."

# Should not proceed if this is not a Maven project.
ls "$PROJECT_PATH" | grep "pom.xml" &>/dev/null
if [ `echo $?` -eq 1 ]; then
    (>&2 echo "Aborted: \"pom.xml\" not found") && exit 1
fi
NAME="`basename "$PROJECT_PATH"`"
LOGNAME_PREFFIX="`date +"$NAME-%m%d%H%M%S"`"

echo "Installing new \"pom.xml\" for \"$NAME\""
install_pom "$PROJECT_PATH" "$TEST_PATH"
echo "Building project \"$NAME\" with new pom.xml file"
compile_only "$PROJECT_PATH"

echo "Running test suite from \"$TEST_PATH\""
test_only "$PROJECT_PATH/$TEST_PATH"
