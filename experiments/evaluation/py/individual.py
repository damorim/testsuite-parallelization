#!/usr/bin/env python3
import argparse

from core import experiment

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to subject")
parser.add_argument("-f", "--force", help="force to cleanup test reports", action="store_true")

args = parser.parse_args()

# Print experiment results
print(experiment.run(args.path, clean=args.force))
