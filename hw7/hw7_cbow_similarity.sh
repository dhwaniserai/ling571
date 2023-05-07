#!/bin/sh
window=$1
judgment_filename=$2
output_filename=$3
/opt/python-3.6/bin/python3 ./cbow_similarity.py $window $judgment_filename $output_filename