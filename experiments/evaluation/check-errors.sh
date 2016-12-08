#!/bin/bash
ERROR_LOG=experiment-errors.csv

echo "Not a maven project: `cat $ERROR_LOG | grep 'not a Maven project' | wc -l`"
echo "Couldn't solve dependencies: `cat $ERROR_LOG | grep 'dependency:go-offline' | wc -l`"
echo "Couldn't compile: `cat $ERROR_LOG | grep "install" | wc -l`"
echo "Couldn't find reports: `cat $ERROR_LOG | grep "Couldn't find" | wc -l`"
echo "Aborts detected: `cat $ERROR_LOG | grep "diverge" | wc -l`"
echo "Total: `cat $ERROR_LOG | wc -l`"
