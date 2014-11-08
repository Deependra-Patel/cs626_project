#!/usr/bin/python2.7
import sys
import os
import pattern.en
from nltk.stem import WordNetLemmatizer

#### Helper functions ###########################################################################################

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_plural(word):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma

def lemmatize(word, mode):
    try:
        wnl = WordNetLemmatizer()
        if mode=='n' :
            return wnl.lemmatize(word, 'n')
        elif mode=='v' :
            return wnl.lemmatize(word, 'v')
        return word
    except:
        print "WordNet Lemmatizer failed."
        return ''

def correct_form(word):
    word2 = word
    if word2 == "''" or word2 == "``":
        word2 = '"'
    if word2[-15:] in ['_single_quote_s','_double_quote_s']:
        word2 = word2[:-15]
    if word2[-14:] in ['_single_quote_','_double_quote_']:
        word2 = word2[:-14]
    return word2
    
#### Function to stuff white space characters within string constants with patterns #############################

def stuff(s):
    stuff_string = ''
    within_quote = False
    quote_char = '~'
    prev_space = True

    for i in range(0,len(s)):
        if within_quote:
            if s[i]==quote_char:
                stuff_string = stuff_string + s[i]
                within_quote = False
            elif s[i]==' ':
                stuff_string = stuff_string + "*$*$"
            elif s[i]=='\t':
                stuff_string = stuff_string + "*%*%"
            elif s[i]=='\n':
                stuff_string = stuff_string + "*&*&"
            else:
                stuff_string = stuff_string + s[i]
        else:
            if s[i]=="'" or s[i]=='"':
                if prev_space:
                    stuff_string = stuff_string + s[i]
                    within_quote = True
                    quote_char = s[i]
                elif s[i]=="'":
                    stuff_string = stuff_string + '_single_quote_'
                else:
                    stuff_string = stuff_string + '_double_quote_'
            else:
                stuff_string = stuff_string + s[i]

        if s[i]==' ' or s[i]=='\t' or s[i]=='\n':
            prev_space = True
        else:
            prev_space = False

    if within_quote == True:
        print "Unmatched quotation marks in the query."
        return ''
    else:
        return stuff_string

#### Method for polishing an english query into a generic form ##################################################

def process_query(sent, entity_list, attrib_list, const_list, attrib_map, entity_map):

    sent = stuff(sent)
    if sent == '':
        print "Could not stuff the query with appropriate escape characters."
        return []
    print "Stuffed the query with appropriate escape characters."

    sent = nltk.word_tokenize(sent)

    l_entity = 0
    l_attrib = 0
    l_const = 0

    # Some temporary variables for collecting words of string constants
    collecting = False
    symbol = '~'
    temp = ""

    for i in range(len(sent)):
        word = sent[i]      
        word = correct_form(word)
        word2 = lemmatize(word,'n')
        word3 = lemmatize(word,'v')

        if collecting:
            if word[-1] == symbol:
                temp = temp + word
                temp = temp.replace('*$*$',' ')
                temp = temp.replace('*%*%','\t')
                temp = temp.replace('*&*&','\n') 
                const_list.append(temp)
                sent[i] = 'CONST_'+str(l_const)
                l_const += 1
                collecting = False
                temp = ""
            else:
                temp = temp + word
                sent[i] = ''
        elif word[0] == "'" or word[0] == '"':
            if word[0] == word[-1] and len(word) != 1:
                const_list.append(word)
                sent[i] = 'CONST_'+str(l_const)
                l_const += 1
            else:
                collecting = True
                symbol = word[0]
                temp = word
                sent[i] = ''
        elif is_number(word):
            const_list.append(word)
            sent[i] = 'CONST_'+str(l_const)
            l_const += 1
        elif word in attrib_map.keys():
            attrib_list.append(word)
            sent[i] = 'ATTRIB_'+str(l_attrib)
            l_attrib += 1
        elif word in entity_map.keys():
            entity_list.append(word)
            sent[i] = 'ENTITY_'+str(l_entity)
            l_entity += 1
        elif word2 in attrib_map.keys():
            attrib_list.append(word2)
            sent[i] = 'ATTRIB_'+str(l_attrib)
            l_attrib += 1
        elif word3 in attrib_map.keys():
            attrib_list.append(word3)
            sent[i] = 'ATTRIB_'+str(l_attrib)
            l_attrib += 1
        elif word2 in entity_map.keys():
            entity_list.append(word2)
            sent[i] = 'ENTITY_'+str(l_entity)
            l_entity += 1
        elif word3 in entity_map.keys():
            entity_list.append(word3)
            sent[i] = 'ENTITY_'+str(l_entity)
            l_entity += 1
        else:
            sent[i] = word.lower()

    sent_final = []
    for i in range(0,len(sent)):
        if sent[i]!='':
            sent_final += [sent[i]]

    print "Unstuffed the query after successfully processing the generic query."    
    return sent_final

#### Function for getting rule-based SQL output from tokenized generic query ####################################
def get_rule_based_sql(tokenized_query, entity_list, attrib_list, const_list, attrib_map, entity_map):
    query_rule = give_sql(tokenized_query, entity_list, attrib_list, const_list, attrib_map, entity_map)
    if query_rule == '':
        return 'NULL'
    return query_rule

#### Function for getting statistical SQL output from tokenized generic query ###################################
def get_statistical_sql(query_tokens, entity_list, attrib_list, const_list, attrib_map, entity_map):

    try:
        query_stat = (os.popen('../stat_moses/convert.sh \''+' '.join(query_tokens)+'\'')).read().split()
        print "Statistical: Mosses could convert the generic query (correctness not guaranteed)."
    except MossesFailedToConvert:
        print "Statistical: Mosses Failed to convert the query to SQL."
        query_stat = []

    try:
        for i in range(len(query_stat)) :
            word = query_stat[i]
            if word[:7] == 'ENTITY_':
                query_stat[i] = entity_map[entity_list[int(word[7:])]]
            elif word[:7] == 'ATTRIB_':
                query_stat[i] = attrib_list[int(word[7:])]
            elif word[:6] == 'CONST_' :
                query_stat[i] = const_list[int(word[6:])]
        print "Statistical: Mapped back the converted generic query to its normal form."
    except CouldNotConvertBack:
        print "Statistical: Could not map the generic SQL query back to specific."
        query_stat = []

    query_stat = " ".join(query_stat)
    if query_stat == '':
        return 'NULL'
    return query_stat

#################################################################################################################
#### Main Program starts here ###################################################################################
#################################################################################################################

if len(sys.argv) < 2:
    print "Usage: ./main_v1.py mode"
    sys.exit()
if sys.argv[1] == '0':
    from chunker_v3 import *
else:
    from chunker_v4 import *

from schema import *

#### Setting up the database metadata initially #################################################################

attrib_map = {}       # Mapping of each of the attributes (eg: name,cpi) to a list of tables containing the attribute(eg: student)
entity_map = {}       # Mapping of entity names (eg: takes, take) to table names (eg: takes) 

for t in tables:
   entity_map[t.table_name] = t.table_name
   entity_map[lemmatize(t.table_name,'n')] = t.table_name
   entity_map[lemmatize(t.table_name,'v')] = t.table_name

   for col in t.columns:
       if col in attrib_map.keys():
           attrib_map[col.column_name].add(t.table_name)
       else:
           attrib_map[col.column_name] = set([t.table_name])

#### Take the input english query & produce output queries ######################################################
a = '''
Enter an english query (with string constants put within single or double quotes):'''
print a

try:
    english = raw_input()
except:
    print "Could not take the input"
    sys.exit()
print ''

# Initialize arrays for storing mapping of generics to specifics
entity_list = []
attrib_list = []
const_list = []

# Now tokenize the query into generic form
tokenized_query = process_query(english, entity_list, attrib_list, const_list, attrib_map, entity_map)

if tokenized_query == []:
    print "Could not process the query to its generic form or Query is empty."
    query_rule_based = 'NULL'
    query_statistical = 'NULL'
else:
    # Obtain the SQL query
    query_rule_based = get_rule_based_sql(tokenized_query, entity_list, attrib_list, const_list, attrib_map, entity_map)
    if query_rule_based == 'NULL':
        print "Rule Based: Could not obtain the SQL query."
    else:
        print "Rule Based: Obtained the SQL query successfully"

    # Obtain the rule-based query
    query_statistical = get_statistical_sql(tokenized_query, entity_list, attrib_list, const_list, attrib_map, entity_map)
    if query_statistical == 'NULL':
        print "Statistical: Could not obtain the SQL query."
    else:
        print "Statistical: Obtained the SQL query successfully"

print "\nRule Based Query: "
print query_rule_based
print "\nStatistical Query: "
print query_statistical
