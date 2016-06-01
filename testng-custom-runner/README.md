## Getting Started

1. Install the TestNG Custom Runner in you local Maven repository (.m2) with `mvn install`.
2. Add the TestNG Custom Runner to your Maven Surefire settings:
```{xml}
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>${SUREFIRE.VERSION}</version>
            <configuration>
            ...
            <properties>
              <property>
                <name>listener</name>
                <value>br.ufpe.cin.jbc5.TestNGCustomRunner</value>
              </property>
            </properties>
            ...
        </configuration>
    </plugin>
```
3. Test your application with `mvn test`.
