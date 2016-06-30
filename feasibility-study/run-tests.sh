#!/bin/bash
BASEDIR="`pwd`"
ANALYZER_HOME="$BASEDIR/../dchecker/target"
ANALYZER_JAR="dchecker-0.0.1-SNAPSHOT.jar"

TEST_PATH="$1"
NAME="$2"
DTEST_PARAM="$3"
if [ -z "$TEST_PATH" ]; then
    echo " > Usage: ./run-tests <path to tests>"
    exit 1;
fi

create_timestamp_report() {
    local preffix=".*\[DCHECKER\]"
    cat "$1" | grep "$preffix" | sed "s/$preffix//g"
}

LOGPREFFIX="`date +"$NAME-%m%d%H%M%S"`"
OUTPUT_DIR="$BASEDIR/reports"

# Output files
MVNLOG_FILE="$OUTPUT_DIR/$LOGPREFFIX-mvnlog.txt"
TIMESTAMP_FILE="$OUTPUT_DIR/$LOGPREFFIX-ts.csv"
DEPENDENCY_FILE="$OUTPUT_DIR/$LOGPREFFIX-deps.txt"

[[ ! -d "$OUTPUT_DIR" ]] && mkdir "$OUTPUT_DIR"

cd "$TEST_PATH"
if [ -z "$DTEST_PARAM" ]; then
    mvn -DtrimStackTrace=false test &> $MVNLOG_FILE
else
    mvn -DtrimStackTrace=false -Dtest="$DTEST_PARAM" test &> $MVNLOG_FILE
fi
create_timestamp_report $MVNLOG_FILE > $TIMESTAMP_FILE
cd "$BASEDIR"

if [ ! -f "$ANALYZER_HOME/$ANALYZER_JAR" ]; then
    echo " > Error: Analyzer jar file \"$ANALYZER_JAR\" not found in \"$ANALYZER_HOME\"."
    echo " > Aborted."
    exit 1;
fi
java -jar "$ANALYZER_HOME/$ANALYZER_JAR" "$TIMESTAMP_FILE" > "$DEPENDENCY_FILE"
