#!/bin/bash
../download_subjects.sh

RUNS=100
# Commented subjects were already executed and results should be available
# in the dropbox folder.
#
#./run_mvn_experiment.sh $RUNS "subjects/retrofit" "retrofit" > retrofit-summary.txt
#./run_mvn_experiment.sh $RUNS "subjects/graphhopper" "core" > graphhopper-summary.txt
#./run_mvn_experiment.sh $RUNS "subjects/jgit" "org.eclipse.jgit.test" > jgit-summary.txt
#./run_mvn_experiment.sh $RUNS "subjects/camel/camel-core" > camel-core-summary.txt
#./run_mvn_experiment.sh $RUNS "subjects/jetty.project" "jetty-client" > jetty.project-summary.txt
./run_mvn_experiment.sh $RUNS "subjects/okhttp" "okhttp-tests" > okhttp-summary.txt
