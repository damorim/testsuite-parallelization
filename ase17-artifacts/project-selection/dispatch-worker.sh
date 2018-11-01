#!/bin/bash
DIR=$1

TIMEOUT=240m
JDK_VERSION=jdk-8

OUTPUT_DIR="rawdata"
if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir $OUTPUT_DIR
fi

docker run --rm -it -d -v "$(pwd)":/usr/src/mymaven -w /usr/src/mymaven maven:3.5.2-$JDK_VERSION \
    /bin/bash src/compile-test.sh $TIMEOUT $DIR $OUTPUT_DIR

