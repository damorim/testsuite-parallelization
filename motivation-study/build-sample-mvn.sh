#!/bin/bash
BASEDIR=`pwd`
SUBJECTS_HOME="$BASEDIR/subjects"
SAMPLES_HOME="$BASEDIR/samples"
RESOURCES_HOME="$BASEDIR/resources"

[[ ! -d "$RESOURCES_HOME/$SUBJECT" ]] && exit 1
[[ ! -d "$SAMPLES_HOME" ]] && mkdir "$SAMPLES_HOME"

SUBJECT=$1
TEST_DIR=$2

for pom_file in `ls "$RESOURCES_HOME/$SUBJECT"`; do
    SAMPLE_DIR="$SAMPLES_HOME/$SUBJECT"

    if [ ! -d "$SAMPLE_DIR/${pom_file%.xml}" ]; then
        [[ ! -d "$SAMPLE_DIR" ]] && mkdir -p "$SAMPLE_DIR"
        cp -r "$SUBJECTS_HOME/$SUBJECT" "$SAMPLE_DIR"
        mv "$SAMPLE_DIR/$SUBJECT" "$SAMPLE_DIR/${pom_file%.xml}"
    fi
    cd "$SAMPLE_DIR/${pom_file%.xml}"

    # Replacing POM file
    rm "$TEST_DIR/pom.xml"
    cp "$RESOURCES_HOME/$SUBJECT/$pom_file" "$TEST_DIR"
    mv "$TEST_DIR/$pom_file" "$TEST_DIR/pom.xml"

    cd $BASEDIR
done
