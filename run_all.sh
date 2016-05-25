#!/bin/bash
./download_subjects.sh

# Commented subjects were already executed and results should be available
# in the dropbox folder.
#
./run_mvn_experiment.sh "subjects/retrofit" "retrofit" > retrofit-summary.txt
#./run_mvn_experiment.sh "subjects/graphhopper" "core" > graphhopper-summary.txt
#./run_mvn_experiment.sh "subjects/jgit" "org.eclipse.jgit.test" > jgit-summary.txt
