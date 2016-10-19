import os

BASE_DIR = os.path.abspath(os.curdir)
RAW_DATA_DIR = BASE_DIR

SUBJECT_DIR = os.path.join(os.path.abspath(os.curdir), "subjects")
SUBJECTS_CSV_HEADER_FIELDS = ["SUBJECT", "URL", "VERSION"]
SUBJECTS_CSV_FILE = os.path.join(RAW_DATA_DIR, "subjects.csv")

TIMECOST_CSV_FILE = os.path.join(RAW_DATA_DIR, "timecost.csv")

COLUMN_SEP = ","
