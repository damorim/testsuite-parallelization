#!/usr/bin/env python3
import argparse

from support.core import experiment

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to subject")
parser.add_argument("-f", "--force", action="store_true")
args = parser.parse_args()

[print(p) for p in experiment(args.path, override=args.force)]
