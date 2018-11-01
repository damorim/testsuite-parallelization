FROM maven:3.5.2-jdk-8

MAINTAINER Jeanderson Candido - http://jeandersonbc.github.io

RUN apt-get update && apt install -y git python3

WORKDIR /usr/src/myapp

ENTRYPOINT ["python3", "github-miner.py"]

CMD ["-h"]

