from chunker_v2 import *
from schema import *

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


sent = raw_input(a)
sent = nltk.word_tokenize(sent)

table_list = []
attrib_list = []
const_list = []

for i in range(len(sent)):
    word = sent[i]
    if word[0] == '_':
        l = len(const_list)
        const_list.append(word[1:])
        sent[i] = 'CONST_'+str(l)
    elif word in tablenames:
        l = len(table_list)
        table_list.append(word)
        sent[i] = 'TABLE_'+str(l)
    elif word in attribs:
        l = len(attrib_list)
        attrib_list.append(word)
        sent[i] = 'ATTRIB_'+str(l)
    
query = give_sql(sent)
query = query.split()

for i in range(len(query)) :
    word = query[i]
    if word[:5] == 'TABLE':
        query[i] = table_list[int(word[6:])]
    elif word[:6] == 'ATTRIB':
        query[i] = attrib_list[int(word[7:])]
    elif word[:5] == 'CONST' :
        query[i] = '\''+const_list[int(word[6:])]+'\''

print 'Answer:'," ".join(query)



