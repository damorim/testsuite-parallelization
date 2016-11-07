#!/usr/bin/env bash
#
# Execute scripts with test parameters
# Author: Jeanderson Candido
#
cd ..
./main.py "test/verified-subjects.csv" --output "test/raw-data.csv" $1