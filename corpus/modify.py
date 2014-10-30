
#sent = nltk.word_tokenize(sent)
for i in range(330):
    sent = raw_input()
    sent = sent.split()
    
    tablenames = ['student', 'instructor']
    attribs = ['rno', 'cpi', 'hostel', 'name', 'credits', 'department', 'count(*)', '*', 'salary']
    
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
        elif word[0] == '\'' and word[-1] == '\'':
    		sent[i] = '_'+word[1:-1]
        elif word.replace('.','').isdigit():
            sent[i] = '_'+word
    	
        
    print ' '.join(sent)
