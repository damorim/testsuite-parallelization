#!/bin/bash
#
# This script downloads all the listed subjects to a subdirectory named "SUBJECT_HOME"
# in the current directory.
#
# - If "SUBJECT_HOME" does not exist, it will be automatically created.
# - If there is no revision informed, the latest commit will be used.
#
# Author: Jeanderson Candido
#
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
download_git "https://github.com/square/okhttp.git" "okhttp" "63ae84d0e647e43d381406a847061d46dcc30448"
download_git "https://github.com/square/picasso.git" "picasso" "0230ba035e3c3aa7d0f31fa34359a66e62154b69"

download_git "https://git.eclipse.org/r/jgit/jgit.git" "jgit" "1f86350c5a97d8c6966fe1146d649eb5cbc60f53"
download_git "https://github.com/eclipse/jetty.project.git" "jetty.project" "012a5864be5627bd321b1f6bb637640c219daa3b"
download_git "https://github.com/eclipse/vert.x.git" "vert.x" "edf61c5b7c4b4675bb9c69c4f44467d67faa03f7"
download_git "https://github.com/eclipse/eclipse-collections.git" "eclipse-collections" "c2e2effd20ca55334882ee653809ce1636a8ffcc"

download_git "https://github.com/apache/camel.git" "camel" "8447297a23203be0a39dcb971ef2c3c0f0f7909f"
