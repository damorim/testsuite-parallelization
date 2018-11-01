#!/bin/bash
docker run -it --rm --name github-miner -v "$PWD":/usr/src/myapp github-miner:latest
