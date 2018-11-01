GitHub Miner
------------

This subproject contains the script responsible for mining projects hosted on
GitHub.

The GitHub Miner script requires Python 3 and Git but it is
**highly recommended to use [Docker](https://www.docker.com/)** since it provides
a homogeneous execution environment.

* Python scripts require Python 3.4 or later
* Scripts use Git to clone projects

### Building the Docker image

All you need is to run the `buildimage.sh` script:

```bash
$ cd Docker
$ ./buildimage.sh
```

### Running the GitHub Miner Script
* Using Docker: `$ ./run-main.sh`
   * Make sure you built the required image (see the previous step)!
* Using your Python installation: `$ python3 github-miner.py`

### Tweaking

Feel free to tweak these scripts.
I provided two scripts (`testing.py` and `run-tests.sh`) that executes some tests that I wrote.
You could use it test some functionality without having to go with the end-to-end execution.

If you have any problems, or questions, don't be shy: drop me a message or open an issue :smile:
