#!/usr/bin/python2.7
import nltk
from nltk.tree import *

try:    
	line = raw_input()
	tokens = nltk.word_tokenize(line)

	print(tokens)
	grammar1 = nltk.data.load('file:mygrammar_sql.cfg')
	rd_parser = nltk.RecursiveDescentParser(grammar1)

	query_tree = rd_parser.parse(tokens)[0]
	print 'correct'
	query_tree.draw()

except ValueError:
	print 'incorrect syntax'
