#!/bin/bash
echo $1 | ./mosesdecoder-RELEASE-1.0/bin/moses -f ./data/train/model/moses.ini > output 2>log
cat output
rm log output
