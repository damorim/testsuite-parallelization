#!/bin/bash
#
# Main experiment script.
# Executes the experiment on each subject.
#
# Author: Jeanderson Candido
#
SUBJECTS_HOME="../subjects"

if [ ! -d "$SUBJECTS_HOME" ]; then
    echo "Download subjects first before proceeding"
    exit 1
fi

echo "Running experiment on \"Retrofit\""
time ./experiment.sh "$SUBJECTS_HOME/retrofit" "retrofit"

echo "Running experiment on \"JGit\""
time ./experiment.sh "$SUBJECTS_HOME/jgit" "org.eclipse.jgit.test"

echo "Running experiment on \"GraphHopper\""
time ./experiment.sh "$SUBJECTS_HOME/graphhopper" "core"

echo "Running experiment on \"Camel\""
time ./experiment.sh "$SUBJECTS_HOME/camel/camel-core"

echo "Running experiment on \"Jetty\""
time ./experiment.sh "$SUBJECTS_HOME/jetty.project" "jetty-client"

echo "Running experiment on \"OkHttp\""
time ./experiment.sh "$SUBJECTS_HOME/okhttp" "okhttp-tests"

echo "Running experiment on \"Eclipse Collections\""
time ./experiment.sh "$SUBJECTS_HOME/eclipse-collections" "unit-tests"

echo "Running experiment on \"JUnit4\""
time ./experiment.sh "$SUBJECTS_HOME/junit4"
