import os


def detect_builder():
    if os.path.exists("pom.xml"):
        return Builder(name="Maven", args=["mvn", "clean", "install", "-DskipTests", "-Dmaven.javadoc.skip=true"],
                       test=["mvn", "test", "-Dmaven.javadoc.skip=true"])

    elif os.path.exists("gradlew"):
        return Builder(name="Gradle", args=["./gradlew", "clean", "build", "-X", "test"],
                       test=["./gradlew", "test"])

    elif os.path.exists("build.xml"):
        return Builder(name="Ant", args=["ant", "compile"], test=["ant", "test"])

    return None


class Builder:
    def __init__(self, name, args, test):
        self.name = name
        self.args = args
        self.test = test
