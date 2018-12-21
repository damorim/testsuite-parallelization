import csv
import os
import re
import logging

## this is a hack to fool github servers in believing that this is not a robot
SLEEP_TIME=60

class CSVOutput:
    def __init__(self, file_name, header):
        self.__file_name = self.__verify(file_name)
        self.__file_path = os.path.abspath(self.__file_name)
        self.__fields = header
        with open(self.__file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.__fields)
            writer.writeheader()

    def name(self):
        return self.__file_name

    def write(self, entry):
        with open(self.__file_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.__fields)
            writer.writerow({k: v for k, v in entry.items() if k in self.__fields})

    def __verify(self, file_name, counter=1):
        if not os.path.exists(file_name):
            return file_name
        file_name = re.sub("(-[0-9]+)?\.", "-{}.".format(counter), file_name)
        return self.__verify(file_name, counter=counter + 1)


def create_logger(name, log_file):
    # Function setup as many loggers as you want
    formatter = logging.Formatter('[%(asctime)-15s] %(message)s')
    logger    = logging.getLogger(name)

    handler = logging.FileHandler(log_file,mode='a')
    handler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(streamHandler)

    return logger