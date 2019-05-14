
SCRIPTS=./src
PROJECTS_DIR=./src/downloads
OUTPUT_DIR=./src/rawdata
RERUNS=3

echo "Started at `date`" >> runs.txt
for run in `seq 1 $RERUNS`; do
    $SCRIPTS/compile-test.sh 90m $PROJECTS_DIR $OUTPUT_DIR && echo "Finished run #$RERUNS at `date`" >> runs.txt
done

#echo "Generating variables at `date`"
#$SCRIPTS/dynamic-variables.rb -p $PROJECTS_DIR
#$SCRIPTS/static-variables.rb -p $PROJECTS_DIR

#echo "Speedup at `date`"
#bash speedup.sh
