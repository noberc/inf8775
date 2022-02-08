#!/usr/bin/env bash

mkdir -p data
cd data

for n in {"10","20","40","80","160","320","640","1280"}; do
    ../inst_gen.py -s $n -n 5
done
