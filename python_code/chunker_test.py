#!/usr/bin/python2.7
import nltk
from nltk.tree import *

def parse(tokens):        
    grammar1 = nltk.data.load('file:grammar/mygrammar_v3.cfg')
    rd_parser = nltk.RecursiveDescentParser(grammar1)

    trees = rd_parser.parse(tokens)
    print "No. of parse trees = "+str(len(trees))
    for i in range(len(trees)):
        query_tree = trees[i]
        print query_tree
        query_tree.draw()
