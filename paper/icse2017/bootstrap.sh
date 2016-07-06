#!/bin/bash
#
# This script installs required tools to generate the final
# PDF file.
#
# Author: Jeanderson Candido

# Building tool
sudo apt-get install latexmk

# Installs missing fonts
sudo apt-get install texlive-fonts-recommended
