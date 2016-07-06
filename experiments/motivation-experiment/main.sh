#!/bin/bash
../scripts/download_subjects.sh

RUNS=50

# Commented subjects were already executed and results should be available
# in the dropbox folder.
#
# ./experiment.sh $RUNS "subjects/retrofit" "retrofit" > retrofit-summary.txt
# ./experiment.sh $RUNS "subjects/graphhopper" "core" > graphhopper-summary.txt
./experiment.sh $RUNS "subjects/jgit" "org.eclipse.jgit.test" > jgit-summary.txt
# ./experiment.sh $RUNS "subjects/camel/camel-core" > camel-core-summary.txt
./experiment.sh $RUNS "subjects/jetty.project" "jetty-client" > jetty.project-summary.txt
# ./experiment.sh $RUNS "subjects/okhttp" "okhttp-tests" > okhttp-summary.txt
