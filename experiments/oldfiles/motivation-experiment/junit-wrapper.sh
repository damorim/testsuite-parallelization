#!/bin/bash
PATH_PREFIX="$HOME/.m2/repository"
JUNIT_PATH="$PATH_PREFIX/junit/junit/4.12/junit-4.12.jar"
HAMCREST_PATH="$PATH_PREFIX/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar"

PROJECT_HOME=$1
TEST_TARGET=$2

PROJECT_CP=
for cp in `find $PROJECT_HOME -name "*classes"`; do
    PROJECT_CP="$PROJECT_CP:./$cp"
done

CP="$PROJECT_CP:$JUNIT_PATH:$HAMCREST_PATH"
java -cp $CP org.junit.runner.JUnitCore $TEST_TARGET
