#!/bin/sh
window=$1
weighting=$2 
judgment_filename=$3 
output_filename=$4
/opt/python-3.6/bin/python3 ./dist_similarity.py $window $weighting $judgment_filename $output_filename