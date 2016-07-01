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

download_git "https://github.com/graphhopper/graphhopper.git" "graphhopper" "a5bfe93dc5d13bdd86c47f5b7fdacabf034a6cd3"
download_git "https://github.com/square/retrofit.git" "retrofit" "28d350d99430c87b4ada7d1aa9e08c96884cb388"
download_git "https://git.eclipse.org/r/jgit/jgit.git" "jgit" "1f86350c5a97d8c6966fe1146d649eb5cbc60f53"
