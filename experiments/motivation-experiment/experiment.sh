#!/bin/bash
BASE_DIR="`pwd`"
BUILD_FILES_DIR="$BASE_DIR/buildfiles"

replace_build_file() {
    local target_dir=$1
    local file_path=$2
    local file_name="`basename $file_path`"

    cp $file_path $target_dir
    rm $target_dir/pom.xml
    mv $target_dir/$file_name $target_dir/pom.xml
}

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

cd "$PROJECT_PATH"
mvn clean install -DskipTest -Dmaven.javadoc.skip &>/dev/null
cd "$BASE_DIR"

echo "Running Experiment on subject \"$NAME\""
for file in `ls $BUILD_FILES_HOME`; do
    replace_build_file $PROJECT_PATH/$TEST_REL_PATH $BUILD_FILES_HOME/$file

    # Should have no difference since they have to be the same file after
    # replacing the original file
    diff $BUILD_FILES_HOME/$file $PROJECT_PATH/$TEST_REL_PATH/pom.xml

    VERSION="`basename ${file%.*xml}`"
    OUTPUT_FILE="$BASE_DIR/$NAME-$VERSION-summary.txt"
    {
        ./experiment.py $VERSION $PROJECT_PATH $TEST_REL_PATH
        echo "------------------"

    } >> $OUTPUT_FILE

done
