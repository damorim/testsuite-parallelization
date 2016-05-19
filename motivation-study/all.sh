#!/bin/bash
# Subject: JGit
# git clone https://git.eclipse.org/r/jgit/jgit.git #master, bf15a72ea050f5c7f2244f48e1c3e56a266a8da7
# ./build-sample-mvn.sh jgit org.eclipse.jgit.test
# ./multiple-runs-mvn.py 10 samples/jgit/hybrid/ org.eclipse.jgit.test/ > jgit-results.txt

# Subject: Google Guava
# git clone https://github.com/google/guava.git #master, 370c604dda193d01913c02a05630f3ae80bdd688
# ./build-sample-mvn.sh guava guava-tests
./multiple-runs-mvn.py 10 samples/guava/hybrid/ guava-tests/ > guava-results.txt

# TODO
# git clone git://git.apache.org/storm.git
# git clone https://github.com/netty/netty.git

# git clone https://github.com/graphhopper/graphhopper.git
# git clone https://github.com/square/retrofit.git
# git clone https://github.com/JodaOrg/joda-time.git

# git clone git://git.eclipse.org/gitroot/jetty/org.eclipse.jetty.project.git
