#!/usr/bin/env python3
import csv
import os
import re 
import xml.etree.ElementTree as etree
import time, datetime
import shutil
from shutil import rmtree

from collections import Counter
from subprocess import check_output, CalledProcessError
from sys import argv




if __name__ == "__main__":
    LOGS_DIR = "./rawdata"
    if not os.path.exists(LOGS_DIR):
        print("Could not find directory \"%s\"\nExiting..." % LOGS_DIR)

    ENTRIES = []
    for project in os.listdir(LOGS_DIR):
        project_path = os.path.join(LOGS_DIR, project)
        print("PROJETO: {}".format(project_path))
        if not project_path == "./rawdata/.DS_Store":

            for files in os.listdir(project_path):
                print(files)
                print("{}/{}".format(project_path,files))
                if files == "0329094641": #0329094641 #0331025746
                    if os.path.isdir(files):
                        print("é diretorio!")
                        if os.path.exists("{}/{}".format(project_path,files)):
                            rmtree("{}/{}".format(project_path,files))
                    else:
                        print("não é diretorio!")
                        rmtree("{}/{}".format(project_path,files))
        #ENTRIES.extend(extract_data_from(project_path))

    #print("Moving files...{}".format(project_path))

