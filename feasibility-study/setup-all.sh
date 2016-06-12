#!/bin/bash
BASE_DIR="`pwd`"
SUBJECT_HOME="$BASE_DIR/subjects"

function download_git {
    local url=$1
    local name=$2
    local rev=$3

    if [ -z "$rev" ]; then rev="HEAD"; fi
    if [[ -z "$url" || -z "$name" ]]; then
        echo "Missing url or name";
        return;
    fi
    cd $SUBJECT_HOME
    [[ ! -d "$SUBJECT_HOME/$name" ]] && git clone $url $name
    cd "$name" && git reset --hard $rev
    cd "$BASE_DIR"
}

[[ ! -d "$SUBJECT_HOME" ]] && mkdir "$SUBJECT_HOME"

# Ref: https://travis-ci.org/graphhopper/graphhopper/builds/131435929
download_git "https://github.com/graphhopper/graphhopper.git" "graphhopper" "a5bfe93dc5d13bdd86c47f5b7fdacabf034a6cd3"
download_git "https://github.com/square/retrofit.git" "retrofit" "28d350d99430c87b4ada7d1aa9e08c96884cb388"

# Commented subjects were already executed and results should be available
# in the dropbox folder.
#
#./run_mvn_experiment.sh "subjects/retrofit" "retrofit" > retrofit-summary.txt
./setup.sh "subjects/graphhopper" "core"
./setup.sh "subjects/retrofit" "retrofit"

#./run_mvn_experiment.sh "subjects/jgit" "org.eclipse.jgit.test" > jgit-summary.txt
#./run_mvn_experiment.sh "subjects/camel/camel-core" > camel-core-summary.txt
#./run_mvn_experiment.sh "subjects/jetty.project" "jetty-client" > jetty.project-summary.txt
# ./run_mvn_experiment.sh "subjects/okhttp" "okhttp-tests" > okhttp-summary.txt
