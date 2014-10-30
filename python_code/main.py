from chunker_v2 import *
from schema import *

#### Helper functions ####
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#### Setting up the database metadata initially in sets ####
tablenames = set([])
attribs = set([])
for t in tables:
    tablenames.add(t.table_name)
    for col in t.columns:
        attribs.add(col.column_name)


a = '''
Edit the config.py file and put the mysql_username, mysql_password and database name
Enter a query of the form 'get me ATTRIB and ATTRIB from TABLE such that ATTRIB = _CONST'
e.g. 'get me name and department from student such that cpi is greater than _9 and hostel is _8'

Enter your query : '''

#### Query input and then polished into generic form ####
def process_query(sent):
    #sent = raw_input(a)
    sent = nltk.word_tokenize(sent)
    #sent = sent.split()
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
        if collecting:
            if word[-1] == symbol:
                const_list.append(temp+word)
                sent[i] = 'CONST_'+str(l_const)
                l_const += 1
                collecting = False
                temp = ""
            else:
                temp = temp + word
        elif word[0] == "'" or word[0] == '"':
            if word[0] == word[-1]:
                const_list.append(word)
                sent[i] = 'CONST_'+str(l_const)
                l_const += 1
            else:
                collecting = True
                symbol = word[0]
                temp = word
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
    print sent
    query = give_sql(sent)
    query = query.split()
    for i in range(len(query)) :
        word = query[i]
        if word[:6] == 'TABLE_':
            query[i] = table_list[int(word[6:])]
        elif word[:7] == 'ATTRIB_':
            query[i] = attrib_list[int(word[7:])]
        elif word[:8] == 'CONST_' :
            query[i] = const_list[int(word[6:])]
    return " ".join(query)


