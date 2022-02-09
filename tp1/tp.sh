#!/usr/bin/env bash

mkdir -p data
cd data

for n in {"10","50","100","500","1000","5000","10000","50000","100000","500000"}; do
    ../inst_gen.py -s $n -n 5
done
