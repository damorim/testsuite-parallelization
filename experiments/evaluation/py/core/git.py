import os
from subprocess import call, check_output, DEVNULL


def clone(url, directory):
    base_dir = os.path.abspath(os.curdir)

    subject_dir = os.path.join(directory, os.path.basename(url))
    if not os.path.exists(subject_dir):
        os.chdir(directory)
        call(["git", "clone", url], stdout=DEVNULL)

    os.chdir(subject_dir)
    rev = which_revision()
    os.chdir(base_dir)

    return rev


def which_revision():
    return check_output(["git", "rev-parse", "HEAD"]).decode().strip()
