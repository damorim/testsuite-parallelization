#!/bin/bash
FILE_PATH="$1"

cat "$FILE_PATH" | grep pool- | sed "s/[0-9]) [0-9]*, [0-9]*, //g" | sed "s/,.*//g" | sort | uniq
cat "$FILE_PATH" | grep pool- | sed "s/[0-9]) [0-9]*, [0-9]*, //g" | sed "s/,.*//g" | sort | uniq | wc -l
