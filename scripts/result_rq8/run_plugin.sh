#!/bin/bash
#
# RQ7 - How effective is selective re-execution in mitigating flakiness?
#
# This script generates analisys about test flaykiness and adjust subjects
# with parallel test.
# <MODE>: C1 - C2 - C3 - FC0 - FC1
#
# Author: Sotero Junior <https://soterojunior.github.io/>
#
# Usage:   ./run_plugin.sh <PROJECT_DIR> <MODE> 
# Example: bash ./run_plugin.sh ./your_subjects FC0 
#
#
MODES=(C1 C2 C3 FC0 FC1)
PROJECTS_DIR=./projects
PROJECT=$1
MODE=$2
BACKUP_FOLDER=./backup_original
OUTPUT_DIR=./rawdata
RERUNS=12

# Check if MODES is correct
if [[ ! " ${MODES[*]} " == *" $MODE "* ]]; then
    echo "Insert a Mode or Mode Incorrect"
    exit 1
fi

# Check if folder project is valid
if [[ ! -d "$PROJECTS_DIR" ]]; then
    echo "Invalid path projects"
    exit 1
fi

# Check if folder rawdata is valid
if [[ ! -d "$OUTPUT_DIR" ]]; then
    echo "Invalid path rawdata"
    exit 1
fi

# Check if exists folder backup original exists
if [[ ! -d "$BACKUP_FOLDER" ]]; then
    echo "Invalid path backup folder"
    exit 1
fi

# Check if project was copied to folder backup
CHECK_FOLDER=`find $BACKUP_FOLDER -maxdepth 1 -type d | wc -l`
if [ $CHECK_FOLDER -eq 2 ]
then
    echo "Project has been copied."
else
    echo "Copying project..."
    cp -R $PROJECT $BACKUP_FOLDER
    echo "Project copied."
fi

# New project name with mode parallel
NEW_PROJECT="${PROJECT}_${MODE}"

# Change folder name project to start the transformation
echo "Changing the project name..."
mv $PROJECT $NEW_PROJECT

# Transform project in Mode
./transform.rb --path $NEW_PROJECT

# After that transform move to ./projects folder
echo "Moving project to folder analisys..."
mv $NEW_PROJECT $PROJECTS_DIR

# Run the project with params Mode defined
echo "Started at `date`" >> runs.txt
for run in `seq 1 $RERUNS`; do
   ./compile-test.sh 90m $PROJECTS_DIR $OUTPUT_DIR && echo "Finished run #$RERUNS at `date`" >> runs.txt
done

# Generate report with the results tests
./parse-rawdata.py $OUTPUT_DIR

# Analyze if project has flakiness and generate report
./analyze_flakiness.py

# Check if exists folder backup original exists
if [[ ! -f "dataset-flakiness.csv" ]]; then
    echo "The project havent flakyniess!"
    exit 1
fi

##
# Start process transformation
TRANSFORMED_DIR="project_transformed"
TRANSFORMED_RAWDATA_DIR="rawdata_transformed"

echo "checking if exsits project transformed folder..."
if [[ ! -d "$TRANSFORMED_DIR" ]]; then
    echo "creating project transformed ..."
    mkdir $TRANSFORMED_DIR
fi

echo "checking if exsits project transformed folder..."
if [[ ! -d "$TRANSFORMED_RAWDATA_DIR" ]]; then
    echo "creating rawdata trasnformed folder ..."
    mkdir $TRANSFORMED_RAWDATA_DIR
fi

echo "copying project to transformation"
cp -R "./projects/${PROJECT}_${MODE}" ./

echo "moving subject to project trasnformed folder..."
mv "${PROJECT}_${MODE}" $TRANSFORMED_DIR

# Analyze the subject transformed
./analyze_transformed_subj.py

# selective re-execution in mitigating flakiness subjects
echo "Started at `date`" >> runs_transformed.txt
for run in `seq 1 $RERUNS`; do
   ./compile-test.sh 90m $TRANSFORMED_DIR $TRANSFORMED_RAWDATA_DIR && echo "Finished run #$RERUNS at `date`" >> runs_transformed.txt
done

# Generate results with transformation
./parse-rawdata-reexecutation.py $TRANSFORMED_RAWDATA_DIR

