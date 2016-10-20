import os

BASE_DIR = os.path.abspath(os.curdir)

SUBJECT_DIR = os.path.join(os.path.abspath(os.curdir), "subjects")
SUBJECTS_CSV_HEADER_FIELDS = ["SUBJECT", "URL", "VERSION"]
SUBJECTS_CSV_FILE = os.path.join(BASE_DIR, "subjects.csv")
TIMECOST_CSV_FILE = os.path.join(BASE_DIR, "rawdata.csv")
COLUMN_SEP = ","
