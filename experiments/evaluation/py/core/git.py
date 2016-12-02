import os
from subprocess import call, check_output, DEVNULL


def clone(url, directory):
    base_dir = os.path.abspath(os.curdir)
    if not os.path.exists(os.path.join(directory, os.path.basename(url))):
        os.chdir(directory)
        call(["git", "clone", url], stdout=DEVNULL)
    os.chdir(base_dir)


def which_revision():
    return check_output(["git", "rev-parse", "HEAD"]).decode().strip()
