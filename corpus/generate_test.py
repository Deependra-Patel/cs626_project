#!/usr/bin/python2.7
from random import *
lines = 330
fract_testing = 0.10
fract_tuning = 0.20
full_en = open("./data.en",'r')
full_sql = open("./data.sql",'r')

lines_en = full_en.readlines()
lines_sql = full_sql.readlines()

x=[randint(0,lines) for p in range(0,int(lines*fract_testing))]
train_en = open("./training/train_en.txt", 'w')
train_sql = open("./training/train_sql.txt", 'w')
test_en = open("./testing/test_en.txt", 'w')
ref_sql = open("./testing/ref_sql.txt", 'w')

for i in range(lines):
	line_en = lines_en[i];
	line_sql = lines_sql[i];
	if i in x:
		test_en.write(line_en)
		ref_sql.write(line_sql)
	else:
		train_en.write(line_en)
		train_sql.write(line_sql)
print("testing ints")
print(x)
### Now writing tuning data
tuning_ints = [randint(0,lines) for p in range(0,int(lines*fract_tuning))]
tune_en = open("./tuning/tune_en.txt", 'w')
tune_sql = open("./tuning/tune_sql.txt", 'w')

for i in tuning_ints:
        line_en = lines_en[i];
        line_sql = lines_sql[i];
	tune_en.write(line_en)
	tune_sql.write(line_sql)

print("tuning integers")
print(tuning_ints)
print("generated testing/training/tuning output in testing/training/tuning folder")
