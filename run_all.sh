#!/bin/bash
./download_subjects.sh
./run_mvn_experiment.sh "subjects/graphhopper" "core" > graphhopper-summary.txt
./run_mvn_experiment.sh "subjects/jgit" "org.eclipse.jgit.test" > jgit-summary.txt
./run_mvn_experiment.sh "subjects/retrofit" "retrofit" > retrofit-summary.txt
# ./run_mvn_experiment.sh "subjects/guava" "guava-tests" > guava-summary.txt
