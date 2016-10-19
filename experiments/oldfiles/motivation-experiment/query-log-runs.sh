#!/bin/bash
echo "Total: `cat $1 | grep "Tests run: .*, Skipped: [0-9]*$" | wc -l`"
cat $1 | grep "Tests run: .*, Skipped: [0-9]*$"
