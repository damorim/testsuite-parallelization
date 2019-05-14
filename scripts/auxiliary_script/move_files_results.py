#!/usr/bin/env python3
import csv
import os
import re 
import xml.etree.ElementTree as etree
import time, datetime
import shutil

from collections import Counter
from subprocess import check_output, CalledProcessError
from sys import argv


def extract_data_from(project_path):
    date_create  = datetime.date.today().strftime("%d%m%Y{}".format(time.strftime("%H%M%S")))
    project_name = os.path.basename(project_path)
    scripts_dir  = os.getcwd()
    
    print("{}".format(datetime.date.today().strftime("%d%m%Y{}".format(time.strftime("%H%M%S")))))
    print(project_path)

    os.chdir(project_path)
    date_create_dir = os.path.join(os.curdir, date_create)
    if not os.path.exists(date_create_dir):
        os.mkdir(date_create_dir)


    #destination = os.path.join(os.curdir, date_create_dir)
    os.chdir(scripts_dir)
    destination = os.path.join(project_path, date_create)

    print("destination: {}".format(destination))

    for files in os.listdir(project_path):
        print(files)
        if files.endswith(tuple([".xml",".log"])):
            shutil.move(os.path.abspath("logs/{}/{}".format(project_name,files)),destination)

    

    return "OK"


if __name__ == "__main__":
    LOGS_DIR = "./logs"
    if not os.path.exists(LOGS_DIR):
        print("Could not find directory \"%s\"\nExiting..." % LOGS_DIR)

    ENTRIES = []
    for project in os.listdir(LOGS_DIR):
        project_path = os.path.join(LOGS_DIR, project)
        ENTRIES.extend(extract_data_from(project_path))

    #print("Moving files...{}".format(project_path))

