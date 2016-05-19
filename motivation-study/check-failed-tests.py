#!/usr/bin/env python2
from sys import argv

def normalize_tname(raw_name):
    # Converts raw_name to be like 'com.example.TestClass#testMethod'
    i = raw_name.rfind(".")
    return raw_name[0:i] + "#" + raw_name[i+1:]

def run_test(name, freq=1):
    print name
    for i in range(freq):
        # run maven test
        # check result
        # add results
        # TODO: REFACT multiple-runs-mvn TO REUSE IT!
        pass

if __name__ == "__main__":
    reruns = int(argv[1])
    log_path = argv[2]

    input_data = open(log_path)
    for line in input_data:
        test_name = normalize_tname(line.split(" ")[0])
        run_test(name=test_name, freq=reruns)
