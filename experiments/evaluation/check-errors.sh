#!/bin/bash
echo "Not a maven project: `cat $1 | grep 'not a Maven project' | wc -l`"
echo "Couldn't solve dependencies: `cat $1 | grep 'dependency:go-offline' | wc -l`"
echo "Couldn't compile: `cat $1 | grep "install" | wc -l`"
echo "Couldn't find reports: `cat $1 | grep "Couldn't find" | wc -l`"
echo "Aborts detected: `cat $1 | grep "diverge" | wc -l`"
echo "Total: `cat $1 | wc -l`"
