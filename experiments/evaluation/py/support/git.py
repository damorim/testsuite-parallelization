import os
from subprocess import call, check_output


def clone(url, clone_home):
    base_dir = os.path.abspath(os.curdir)
    if not os.path.exists(os.path.join(clone_home, os.path.basename(url))):
        os.chdir(clone_home)
        call(["git", "clone", url])
    os.chdir(base_dir)


def which_revision():
    return check_output(["git", "rev-parse", "HEAD"]).decode().strip()
