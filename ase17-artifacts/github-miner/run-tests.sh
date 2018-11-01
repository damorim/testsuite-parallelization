#!/bin/bash
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp \
    python:3.5-alpine \
    python testing.py
