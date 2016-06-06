## Getting Started

### Important!
The current implementation does not support multiple JVM forks.

1. Install the TestNG Custom Runner in you local Maven repository (.m2) with `mvn install`.
2. Declare a new dependency in your `pom.xml` file:
```{xml}
<dependency>
    <groupId>br.ufpe.cin.jbc5</groupId>
    <artifactId>testng-custom-runner</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <scope>test</scope>
</dependency>
```
3. Add the TestNG Custom Runner to your Maven Surefire settings (`pom.xml`):
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
