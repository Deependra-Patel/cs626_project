from chunker_v2 import *

f_en = open('../corpus/data.en')
f_sql = open('../corpus/data.sql')
f_out_en = open('output/data.en', 'w')
f_out_sql = open('output/data.sql', 'w')
f_out = open('output/data.out', 'w')

data_en = f_en.readlines()
data_sql = f_sql.readlines()
for i in range(len(data_en)):
    try:
        try:
            tokens = nltk.word_tokenize(data_en[i])
            query = give_sql(tokens)
            f_out_en.write(data_en[i])
            f_out_sql.write(data_sql[i])
            f_out.write(query+'\n')
        except TypeError:
            print 'type error occured for', i
    except ValueError:
        print 'error occured for',i
