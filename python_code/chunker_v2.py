#!/usr/bin/python2.7
import nltk
from nltk.tree import *
        
line = raw_input()
tokens = nltk.word_tokenize(line)

grammar1 = nltk.data.load('file:mygrammar.cfg')
rd_parser = nltk.RecursiveDescentParser(grammar1)

query_tree = rd_parser.parse(tokens)[0]

#for tree in rd_parser.parse(tokens):
    #tree.draw()
    #print tree['select']
#    print(tree)
#    print(tree[1][0])

wordmap = {'get':'select', 'fetch':'select', 'select':'select', 'find':'select', 'show':'select'}

select_part = query_tree[0]
from_part = query_tree[1]
where_part = query_tree[2]


def get_child(self, node_val):
    for subt in self:
        if subt.node == node_val:
            return subt
    return False

nltk.Tree.get_child = get_child

action = wordmap[select_part.get_child('VB').get_child('VERB')[0]]
print action

fields = []
temp = select_part
while(True):
    temp = temp.get_child('FIELDS_')
    if temp == False:
        break
    fields.append(temp.get_child('FIELD').get_child('ATTRIB')[0])

print ', '.join(fields)

print from_part

