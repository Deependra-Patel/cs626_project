#!/usr/bin/python2.7
import nltk
from nltk.tree import *
        

grammar1 = nltk.data.load('file:newgrammar.cfg')
rd_parser = nltk.RecursiveDescentParser(grammar1)

def give_sql(tokens) :

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
#print action

    fields = []
    temp = select_part
    while(True):
        temp = temp.get_child('FIELDS_')
        if temp == False:
            break
        fields.append(temp.get_child('FIELD').get_child('ATTRIB')[0])

#print ', '.join(fields)

    look = from_part.get_child('LOOK')[0]
    tables = []
    while look != 'from':
        from_part = from_part.get_child('FROM')
        look = from_part.get_child('LOOK')[0]
    if look == 'from':
        temp = from_part
        while True:
            temp = temp.get_child('INTO')
            if temp == False:
                break
            tables.append(temp.get_child('TABLE_').get_child('TABLE')[0])

#print ', '.join(tables)


    condmap = {'equal':'=', 'unequal':'!=', 'more':'>', 'less':'<', 'higher':'>', 'lower':'<', 'high':'>', 'low':'<', 'greater':'>', 'lesser':'<'}
    condmap_neg = {'equal':'!=', 'unequal':'=', 'more':'<=', 'less':'>=', 'higher':'<=', 'lower':'>=', 'high':'<=', 'low':'>=', 'greater':'<=', 'lesser':'>='}

    conds = []
    temp = where_part
    while True:
        cc = temp.get_child('CC')
        if cc != False:
            cc = cc[0]
            conds.append(cc)
        temp = temp.get_child('CONDS')
        if temp == False:
            break
        cond = temp.get_child('COND')
        val1 = cond[0][0][0]
        val2 = cond[2][0][0]
        vbx = cond[1].get_child('VBX')
        comp = cond[1].get_child('COMP')
        if comp == False and vbx[0] == 'is':
            cond = val1 + ' = ' + val2
        else :
            neg = comp.get_child('NEG')
            if neg == False:
                comp2 = comp.get_child('COMP2')[0]
                cond = val1 + ' ' + condmap[comp2] + ' ' + val2
            else :
                comp2 = comp.get_child('COMP2')[0]
                cond = val1 + ' ' + condmap_neg[comp2] + ' ' + val2
        conds.append(cond)

#print ' '.join(conds)

    return action + ' ' + ' , '.join(fields) + ' from ' + ' , '.join(tables) + ' where ' + ' '.join(conds)


#line = raw_input()
#tokens = nltk.word_tokenize(line)

#print give_sql(tokens)
