#!/bin/bash
#
# Installs required third-party packages for vagrant provisioning.
#
# Author: Jeanderson Candido
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update

# INSTALLING Python Packages
sudo apt-get install -y python3-lxml

# INSTALLING GIT
sudo apt-get install -y git

# INSTALLING ORACLE JDK 8
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
sudo apt-get install -y oracle-java8-installer

# INSTALLING MAVEN
if [ ! -d apache-maven-3.3.9 ]; then
    wget http://ftp.unicamp.br/pub/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
    tar zxvf apache-maven-3.3.9-bin.tar.gz
fi

echo "export MAVEN_HOME=/home/vagrant/apache-maven-3.3.9" >> /home/vagrant/.profile
echo "export PATH=\$MAVEN_HOME/bin:\$PATH" >> /home/vagrant/.profile
