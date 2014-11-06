import sys
from chunker_v2 import *
from schema import *
import os

#### Helper functions ####
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
        print "\nUnmatched quotation marks in the query! Check the query.\n"
        sys.exit()
    else:
        return stuff_string

#### Setting up the database metadata initially in sets ####
tablenames = set([])
attribs = set([])
for t in tables:
    tablenames.add(t.table_name)
    for col in t.columns:
        attribs.add(col.column_name)


a = '''
Edit the config.py file and put the mysql_username, mysql_password and database name
Enter a query in english, with constants (proper nouns) put within either single or double quotes.
e.g. 'get me name and department from student such that cpi is greater than 9 and hostel is 'hostel-2''

Enter your query : '''

#### Query input and then polished into generic form ####

def process_query(sent):
    sent = stuff(sent)
    print "Stuffed query: "+sent 
    sent = nltk.word_tokenize(sent)

    table_list = []
    attrib_list = []
    const_list = []

    l_table = 0
    l_attrib = 0
    l_const = 0

    collecting = False
    symbol = '~'
    temp = ""

    for i in range(len(sent)):

        word = sent[i]
        if word == "''" or word == "``":
            word = '"'

        if collecting:
            if word[-1] == symbol:
                const_list.append(temp+word)
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
        elif word in tablenames:
            table_list.append(word)
            sent[i] = 'TABLE_'+str(l_table)
            l_table += 1
        elif word in attribs:
            attrib_list.append(word)
            sent[i] = 'ATTRIB_'+str(l_attrib)
            l_attrib += 1

    sent_final = []
    for i in range(0,len(sent)):
        if sent[i]!='':
            sent[i] = sent[i].replace('_single_quote_',"'")
            sent[i] = sent[i].replace('_double_quote_','"')
            sent_final += [sent[i]]

    print "Final query sent for processing: "+" ".join(sent_final)
    query = give_sql(sent_final)
    query_stat = (os.popen('../stat_moses/convert.sh \''+' '.join(sent_final)+'\'')).read().split()
    query = query.split()

    for i in range(len(query)) :
        word = query[i]
        if word[:6] == 'TABLE_':
            query[i] = table_list[int(word[6:])]
        elif word[:7] == 'ATTRIB_':
            query[i] = attrib_list[int(word[7:])]
        elif word[:6] == 'CONST_' :
            query[i] = const_list[int(word[6:])]
    for i in range(len(query_stat)) :
        word = query_stat[i]
        if word[:6] == 'TABLE_':
            query_stat[i] = table_list[int(word[6:])]
        elif word[:7] == 'ATTRIB_':
            query_stat[i] = attrib_list[int(word[7:])]
        elif word[:6] == 'CONST_' :
            query_stat[i] = const_list[int(word[6:])]

    query = " ".join(query)
    query_stat = " ".join(query_stat)
    query = query.replace('*$*$',' ')
    query = query.replace('*%*%','\t')
    query = query.replace('*&*&','\n') 
    query_stat = query_stat.replace('*$*$',' ')
    query_stat = query_stat.replace('*%*%','\t')
    query_stat = query_stat.replace('*&*&','\n')
    return query,query_stat
