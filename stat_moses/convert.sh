#!/bin/bash
echo $1 | ../stat_moses/mosesdecoder-RELEASE-1.0/bin/moses -f ../stat_moses/data/train/model/moses.ini > ../stat_moses/output.txt 2>log
cat ../stat_moses/output.txt
rm ../stat_moses/output.txt
