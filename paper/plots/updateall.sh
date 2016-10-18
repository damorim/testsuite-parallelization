#!/bin/bash
BASEDIR=$(pwd)
for d in $(ls .); do
    if [ -f "$d/main.sh" ]; then
        cd $d
        ./main.sh
        cd $BASEDIR
    fi
done
