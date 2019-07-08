# Maven Plugin - Parallel Test Flakys (PAG)

Parallel Test Flakys PAG is a plugin maven ...


## Installation

Add this plugin in your root pom.xml project:

    <plugin>
        <groupId>com.cin.pag</groupId>
        <artifactId>paralleltestpag-maven-plugin</artifactId>
        <version>1.0-SNAPSHOT</version>
        <configuration>
            <parallel>FC0</parallel>
        </configuration>
    </plugin>

## Usage

Choose which parallelization type you will use and add in `configuration` tag when add the plugin.

C1: Sequential classes; parallel methods.

C2: Parallel classes; sequential methods.

C3: Parallel classes; parallel methods.

FC0: Forked JVMs with Sequential methods.

FC1: Forked JVMs with Parallel methods.


run: `mvn paralleltestpag:testing`

### VERSIONS:

`maven 3`

`JUnit 3.8.1`