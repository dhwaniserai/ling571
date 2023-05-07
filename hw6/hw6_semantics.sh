#!/bin/sh
grammar=$1
sentences=$2
output=$3
/opt/python-3.6/bin/python3 ./semantics.py $grammar $sentences $output