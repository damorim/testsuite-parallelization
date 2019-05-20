#!/bin/bash
#
# This script installs required tools and packages to build the final PDF file.

# Building tool
sudo apt-get install -y latexmk

# Missing fonts
sudo apt-get install -y texlive-fonts-recommended

# Missing packages
sudo apt-get install -y texlive-latex-extra mathpartir
