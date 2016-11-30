#!/usr/bin/env bash
echo $@
R --vanilla --slave < analytics/Audit.R --args $@