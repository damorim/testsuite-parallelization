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

./experiment.sh "$SUBJECTS_HOME/retrofit" "retrofit"
./experiment.sh "$SUBJECTS_HOME/jgit" "org.eclipse.jgit.test"
./experiment.sh "$SUBJECTS_HOME/graphhopper" "core"
./experiment.sh "$SUBJECTS_HOME/jetty.project" "jetty-client"
./experiment.sh "$SUBJECTS_HOME/okhttp" "okhttp-tests"
# FIXME: Nao compilou ./experiment.sh "$SUBJECTS_HOME/vert.x"
# FIXME: Nao executou testes ./experiment.sh "$SUBJECTS_HOME/eclipse-collections" "unit-tests"
./experiment.sh "$SUBJECTS_HOME/junit4"
./experiment.sh "$SUBJECTS_HOME/camel/camel-core"
