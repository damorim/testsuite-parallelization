This directory contains the scripts necessary to filter the downloaded projects
from the mining step.

How does it work?

You can use directly the `project-analyzer.sh` script directly in a directory
of projects; however, this approach is not scalable if you have
hundreds/thousands of projects.

To mitigate this scalability issue, use the `buildparts.py` script to create
subsets of the projects' directory. For each subset, use the
`dispatch-worker.sh` to run a Docker container for each subset in parallel.
