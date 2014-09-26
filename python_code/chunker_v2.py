#!/usr/bin/python2.7
import nltk
        
line = raw_input()
tokens = nltk.word_tokenize(line)

grammar1 = nltk.data.load('file:mygrammar.cfg')
rd_parser = nltk.RecursiveDescentParser(grammar1)

for tree in rd_parser.parse(tokens):
    tree.draw()
#    print(tree)
#    print(tree[1][0])

