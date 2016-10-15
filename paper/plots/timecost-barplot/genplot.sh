#!/bin/bash
DATA_PATH=$1
R --vanilla < script.r --args $DATA_PATH
