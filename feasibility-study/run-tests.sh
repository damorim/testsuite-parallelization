#!/bin/bash
BASEDIR="`pwd`"
OUTPUT_DIR="$BASEDIR/reports"
ANALYZER_JAR="dchecker-0.1.1-SNAPSHOT.jar"

if [ -f "$ANALYZER_JAR" ]; then
    echo " > Error: Analyzer Jar not found. Build \"dchecker\" first..."
    echo " > Aborted."
    exit 1;
fi

TEST_PATH="$1"
if [ -z "$TEST_PATH" ]; then
    echo " > Usage: ./run-tests <path to tests>"
    exit 1;
fi

timestamp_report() {
    cat "$OUTPUT_DIR/$1" | grep INFO: | sed "s/INFO: //g"
}

NAME="$2"
LOGPREFFIX="`date +"$NAME-%m%d%H%M%S"`"
[[ ! -d "$OUTPUT_DIR" ]] && mkdir "$OUTPUT_DIR"

cd "$TEST_PATH"

mvn test &> "$OUTPUT_DIR/$LOGPREFFIX-mvnlog.txt"
timestamp_report "$LOGPREFFIX-mvnlog.txt" > "$OUTPUT_DIR/$LOGPREFFIX-ts.csv"

#FIXME: Error: Unable to access jarfile dchecker-0.1.1-SNAPSHOT.jar
java -jar "$ANALYZER_JAR" "$OUTPUT_DIR/$LOGPREFFIX-ts.csv" > "$OUTPUT_DIR/$LOGPREFFIX-deps.txt"

cd "$BASEDIR"
