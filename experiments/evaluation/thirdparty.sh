#!/bin/bash
#
# Installs required third-party packages for vagrant provisioning.
#
# Author: Jeanderson Candido
BASE_DIR=$(pwd)
THIRDPARTY_HOME=$BASE_DIR/thirdparty

if [ ! -d "$THIRDPARTY_HOME" ]; then
    mkdir "$THIRDPARTY_HOME"
fi
cd "$THIRDPARTY_HOME"

wget http://ftp.unicamp.br/pub/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
wget http://mirror.nbtelecom.com.br/apache//ant/binaries/apache-ant-1.9.7-bin.tar.gz

# TODO INSTALL MAVEN/ANT/JAVA
