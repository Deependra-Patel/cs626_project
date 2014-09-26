#!/usr/bin/python2.7
import nltk

f = open("../corpus/data.en","r")
f2 = open("../corpus/tagged_data","w")
lines = f.readlines()

for line in lines: 
    tokens = nltk.word_tokenize(line)
    tag_list = nltk.pos_tag(tokens)
    print>> f2, tag_list
#    f2.write(tag_list)

