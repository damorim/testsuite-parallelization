#!/bin/bash
basedir="`pwd`"
for p in `ls downloads`; do
    cd downloads/$p
    git reset --hard HEAD
    cd $basedir
done;
