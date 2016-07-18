#!/bin/bash
#
# Main experiment script.
# Executes the experiment on each subject.
#
# Author: Jeanderson Candido
#
SUBJECTS_HOME="subjects"

../scripts/download_subjects.sh &>/dev/null

./experiment.sh "$SUBJECTS_HOME/retrofit" "retrofit"
./experiment.sh "$SUBJECTS_HOME/graphhopper" "core"
./experiment.sh "$SUBJECTS_HOME/jgit" "org.eclipse.jgit.test"
./experiment.sh "$SUBJECTS_HOME/jetty.project" "jetty-client"
#./experiment.sh "$SUBJECTS_HOME/okhttp" "okhttp-tests"
#./experiment.sh "$SUBJECTS_HOME/vert.x"
#./experiment.sh "$SUBJECTS_HOME/eclipse-collections" "unit-tests"
#./experiment.sh "$SUBJECTS_HOME/junit4"
#./experiment.sh "$SUBJECTS_HOME/camel/camel-core"
