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

download_git() {
    local url=$1
    local rev=$2

    local name="`basename $url`"
    name=${name%.*}

    if [ -z "$url" ]; then
        echo "Missing url or name"
        return;
    fi
    if [ -z "$rev" ]; then
        rev="HEAD"
    fi
    cd $SUBJECT_HOME
    [[ ! -d "$SUBJECT_HOME/$name" ]] && git clone $url $name
    cd "$name" && git reset --hard $rev
    cd "$BASE_DIR"
}

[[ ! -d "$SUBJECT_HOME" ]] && mkdir "$SUBJECT_HOME"

download_git "https://github.com/graphhopper/graphhopper.git" "a5bfe93dc5d13bdd86c47f5b7fdacabf034a6cd3"
download_git "https://github.com/square/retrofit.git" "28d350d99430c87b4ada7d1aa9e08c96884cb388"
download_git "https://github.com/square/okhttp.git" "63ae84d0e647e43d381406a847061d46dcc30448"
download_git "https://github.com/square/picasso.git" "0230ba035e3c3aa7d0f31fa34359a66e62154b69"
download_git "https://git.eclipse.org/r/jgit/jgit.git" "1f86350c5a97d8c6966fe1146d649eb5cbc60f53"
download_git "https://github.com/eclipse/jetty.project.git" "012a5864be5627bd321b1f6bb637640c219daa3b"
download_git "https://github.com/eclipse/vert.x.git" "edf61c5b7c4b4675bb9c69c4f44467d67faa03f7"
download_git "https://github.com/eclipse/eclipse-collections.git" "c2e2effd20ca55334882ee653809ce1636a8ffcc"
download_git "https://github.com/apache/camel.git" "8447297a23203be0a39dcb971ef2c3c0f0f7909f"
download_git "https://github.com/junit-team/junit4.git" "41d44734f41aba0cf6ba5a11ff5d32ffed155027"
download_git "https://github.com/cbeust/testng.git" "73fce4a63c6dc24a547c159e76af66fa0bb93e9f"

echo "Downloads Finished"
