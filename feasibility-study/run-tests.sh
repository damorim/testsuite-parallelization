#!/bin/bash
BASEDIR="`pwd`"
ANALYZER_JAR="dchecker-0.0.1-SNAPSHOT.jar"

TEST_PATH="$1"
NAME="$2"
if [ -z "$TEST_PATH" ]; then
    echo " > Usage: ./run-tests <path to tests>"
    exit 1;
fi

create_timestamp_report() {
    cat "$1" | grep INFO: | sed "s/INFO: //g"
}

LOGPREFFIX="`date +"$NAME-%m%d%H%M%S"`"
OUTPUT_DIR="$BASEDIR/reports"

# Output files
MVNLOG_FILE="$OUTPUT_DIR/$LOGPREFFIX-mvnlog.txt"
TIMESTAMP_FILE="$OUTPUT_DIR/$LOGPREFFIX-ts.csv"
DEPENDENCY_FILE="$OUTPUT_DIR/$LOGPREFFIX-deps.txt"

[[ ! -d "$OUTPUT_DIR" ]] && mkdir "$OUTPUT_DIR"

cd "$TEST_PATH"
mvn test &> $MVNLOG_FILE
create_timestamp_report $MVNLOG_FILE > $TIMESTAMP_FILE
cd "$BASEDIR"

if [ ! -f "$ANALYZER_JAR" ]; then
    echo " > Error: Analyzer jar file \"$ANALYZER_JAR\" not found in the current directory"
    echo " > Aborted."
    exit 1;
fi
java -jar "$ANALYZER_JAR" "$TIMESTAMP_FILE" > "$DEPENDENCY_FILE"
