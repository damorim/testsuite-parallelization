#!/bin/bash
#
# This script is related to the RQ3. It discovers parallel
# configurations statically and dynamically.
#
# The file "dataset-medlong.csv" is required.
#
# Author: Jeanderson Candido <http://jeandersonbc.github.io>
#
SCRIPTS=./src
PROJECTS_DIR=./projects/downloads

$SCRIPTS/dynamic-variables.rb -p $PROJECTS_DIR
$SCRIPTS/static-variables.rb -p $PROJECTS_DIR
