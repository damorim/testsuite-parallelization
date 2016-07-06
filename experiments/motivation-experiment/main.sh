#!/bin/bash
#
# Main experiment script.
# Executes the experiment on each subject.
#
# Examples:
#     ~$ ./main.sh 10
#     ~$ ./main.sh 50
#     ~$ ./main.sh 100
#
# Author: Jeanderson Candido
#
SUBJECTS_HOME="../subjects"
RUNS=$1

[[ -z "$RUNS" ]] && echo "Usage: ./main.sh <RUNS>" && exit 1
if [ ! -d "$SUBJECTS_HOME" ]; then
    echo "Download subjects first before proceeding"
    exit 1
fi

./experiment.sh $RUNS "$SUBJECTS_HOME/retrofit" "retrofit" > retrofit-summary.txt

# Possibly with deadlock when executed with parallel threads
# ./experiment.sh $RUNS "$SUBJECTS_HOME/graphhopper" "core" > graphhopper-summary.txt

./experiment.sh $RUNS "$SUBJECTS_HOME/jgit" "org.eclipse.jgit.test" > jgit-summary.txt
./experiment.sh $RUNS "$SUBJECTS_HOME/camel/camel-core" > camel-core-summary.txt
./experiment.sh $RUNS "$SUBJECTS_HOME/jetty.project" "jetty-client" > jetty.project-summary.txt
./experiment.sh $RUNS "$SUBJECTS_HOME/okhttp" "okhttp-tests" > okhttp-summary.txt
