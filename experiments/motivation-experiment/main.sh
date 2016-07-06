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
RUNS=$1
[[ -z "$RUNS" ]] && echo "Usage: ./main.sh <RUNS>" && exit 1

../scripts/download_subjects.sh

./experiment.sh $RUNS "subjects/retrofit" "retrofit" > retrofit-summary.txt

# Possibly with deadlock when executed with parallel threads
# ./experiment.sh $RUNS "subjects/graphhopper" "core" > graphhopper-summary.txt

./experiment.sh $RUNS "subjects/jgit" "org.eclipse.jgit.test" > jgit-summary.txt
./experiment.sh $RUNS "subjects/camel/camel-core" > camel-core-summary.txt
./experiment.sh $RUNS "subjects/jetty.project" "jetty-client" > jetty.project-summary.txt
./experiment.sh $RUNS "subjects/okhttp" "okhttp-tests" > okhttp-summary.txt
