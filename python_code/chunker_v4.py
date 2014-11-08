#!/usr/bin/python2.7
import nltk
import sys
from nltk.tree import *

#### Method for getting a specific child of a node ####################################################
def get_child(self, node_val):
    try:
        for subt in self:
            if type(subt)== nltk.tree.Tree and subt.node == node_val:
               return subt
        return False
    except:
        print "Rule Based: get_child() method called on unsupported type."
        return False

#### Method for replacing a string with another if it matches it ######################################
def substitute(word, key, replace):
    if word == key:
        return replace
    return word

#### Method for putting underscores in between complex comparators ####################################
def convert_complex_comp(tokens):

    select_map = {'get':'select', 'fetch':'select', 'select':'select', 'find':'select', 'show':'select', 'return':'select', 'display':'select', 'print':'select', 'give':'select', 'name':'select', 'list':'select'}
    agent_map = {'me':'agent', 'them':'agent', 'these':'agent', 'those':'agent', 'him':'agent', 'her':'agent', 'us':'agent', 'my':'agent', 'our':'agent', 'their':'agent', 'your':'agent', 'such':'agent'}
    relative_map = {'friend':'relative', 'father':'relative', 'mother':'relative', 'son':'relative', 'daughter':'relative', 'brother':'relative', 'sister':'relative', 'dad':'relative', 'mom':'relative', 'bro':'relative', 'aunt':'relative', 'uncle':'relative', 'cousin':'relative'}
    wh_map = {'what':'wh_question', 'which':'wh_question', 'who':'wh_question', 'where':'wh_question', 'whose':'wh_question', 'when':'wh_question', 'how':'wh_question', 'why':'wh_question'}
    table_extra_map = {'table':'table', 'relation':'table', 'data':'table'}
    info_word_map = {'information':'information', 'info':'information', 'data':'information', 'detail':'information', 'details':'information'}
    phrase_map = {'greater than or equal':'greater_than_or_equal', 'lesser than or equal':'lesser_than_or_equal', 'higher than or equal':'greater_than_or_equal', 'lower than or equal':'lesser_than_or_equal', 'larger than or equal':'greater_than_or_equal', 'smaller than or equal':'lesser_than_or_equal', 'bigger than or equal':'greater_than_or_equal', 'as well as':'as_well_as', 'as well':'as_well'}
    conj_map = {'and':'and', 'or':'or', ',':'and', 'as_well_as':'and', 'as_well':'and', 'neither':'not', 'either':'or', 'nor':'not', 'not':'not'}
    filler3_map = {'does':'filler3', 'do':'filler3', 'it':'filler3'}
    extra_map = {'to':'comp_extra', 'than':'comp_extra', 'by':'comp_extra'}
    comp_sp2_map = {'maximum':'maximum', 'minimum':'minimum', 'highest':'maximum', 'lowest':'minimum', 'least':'minimum', 'smallest':'minimum', 'largest':'maximum', 'greatest':'maximum', 'small':'low', 'low':'low', 'high':'high', 'large':'high', 'big':'high', 'huge':'high'}
    filler1_map = {'were':'filler1', 'are':'filler1', 'have':'filler1', 'had':'filler1', 'has':'filler1', 'was':'filler1', 'it':'filler1', 'all':'filler1', 'for' :'filler1', 'been':'filler1', 'some':'filler1', 'few':'filler1', 'any':'filler1', 'from':'filler1', 'that':'filler1', 'a':'filler1', 'an':'filler1', 'the':'filler1', 'among':'filler1', 'inside':'filler1', 'also':'filler1', 'they':'filler1', 'out':'filler1', 'will':'filler1', 'would':'filler1', 'however':'filler1', 'although':'filler1', 'though':'filler1', 'even':'filler1', 'whereas':'filler1', 'with':'filler1', 'while':'filler1', 'all':'filler1'}

    list_of_maps = [select_map, agent_map, relative_map, wh_map, table_extra_map, info_word_map, conj_map, filler3_map, extra_map, comp_sp2_map, filler1_map]
    list_of_group_maps = [phrase_map]

    try:
        sentence = " ".join(tokens)
        for map_ in list_of_group_maps:
            for key in map_.keys():
                sentence.replace(key,map_[key])
        sentence = sentence.split()
        for map_ in list_of_maps:
            for key in map_.keys():
                sentence = [substitute(w,key,map_[key]) for w in sentence]
        print sentence
        return sentence
    except:
        return []

#### Method for getting the [attribs,entities] pair of a field ########################################
def get_field_tuple(field):
    attribs = []
    entities = []

    try:
        temp = field.get_child('FIELD')
        while(True):
            temp = temp.get_child('ATTRIB1_')
            if temp==False:
                break
            attrib_val = temp.get_child('ATTRIB1').get_child('ATTRIB2')[0] 
            if attrib_val.node == 'ATTRIB':
                attribs += [attrib_val[0]]
    except:
        print "Rule Based: Unable to extract attribs from FIELD in get_field_tuple()."

    try:
        temp = field.get_child('FIELD')
        while(True):
            temp = temp.get_child('ENTITY1_')
            if temp==False:
                break
            entities += [temp.get_child('ENTITY1').get_child('ENTITY2').get_child('ENTITY')[0]]
    except:
        print "Rule Based: Unable to extract entities from FIELD in get_field_tuple()."

    return [attribs, entities]

#### Method for filling the fields list with (attrib,entity) pairs ####################################
def fill_fields(fields_list, query_tree):

    try:
        temp = query_tree.get_child('SELECT')
        while(True):
            temp = temp.get_child('FIELD_')
            if temp == False:
                break
            fields_list.append(get_field_tuple(temp))
    except:
        print "Rule Based: Exception in fill_fields() function."
    return

#### Method for getting the 5-tuple of each condition #################################################
def get_cond_tuple(condition):
    is_special = False
    value1 = False
    negate = False
    comp = False
    value2 = False

    try:
        if condition.get_child('COMP_')==False and condition.get_child('COMP_SP')==False:
            if len(condition) == 1:
                value2 = condition[0]
            else:
                value1 = condition[0]
                value2 = condition[1]
            comp = 'is'
        elif condition.get_child('COMP_')==False:
            is_special = True
            comp = condition.get_child('COMP_SP').get_child('COMP_SP1').get_child('COMP_SP2')[0]
            negate = condition.get_child('COMP_SP').get_child('COMP_SP1').get_child('NEGATE')
            if negate != False:
                negate = True
            value1 = condition.get_child('VALUE')
        else:
            comp = condition.get_child('COMP_').get_child('COMP1').get_child('COMP2').get_child('COMP3')[0]
            negate = condition.get_child('COMP_').get_child('COMP1').get_child('NEGATE')
            if negate != False:
                negate = True

            if condition[0].node == 'VALUE':
                value1 = condition[0]
                value2 = condition[2]
            elif len(condition)==2:
                value2 = condition[1]
            elif len(condition)==3:
                value1 = condition[1]
                value2 = condition[2]
    except:
        print "Rule Based: Exception in get_cond_tuple() function."

    return [is_special,value1,negate,comp,value2]

#### Method for filling the conds list with 5-tuples of conditions ####################################
def fill_conds(conds_list, query_tree):

    try:
        temp = query_tree
        while(True):
            temp = temp.get_child('WHERE')
            if temp == False:
                break
            if len(temp) >= 2 :
                if temp[0].node == 'CONJ1_':
                    conds_list.append(temp[0])
                elif temp[1].node == 'CONJ1_':
                    condition = temp.get_child('COND1').get_child('COND')
                    conds_list.append(get_cond_tuple(condition))
                    conds_list.append(temp[1])
                else:
                    condition = temp.get_child('COND1').get_child('COND')
                    conds_list.append(get_cond_tuple(condition))
                    conds_list.append('')
            else:
                condition = temp.get_child('COND1').get_child('COND')
                conds_list.append(get_cond_tuple(condition))
    except:
        print "Rule Based: Exception in fill_conds() function."
    return

#### Method for getting list of mapped join words from tree of join words #############################
def get_join_list(cond_tuple,join_map):

    answer = []
    try:
        temp = cond_tuple
        while(temp):
            temp2 = temp.get_child('CONJ1')
            answer += [join_map[temp2[0]]]
            temp = temp.get_child('CONJ1_')
    except:
        print "Rule Based: Exception in get_join_list() function."
    return answer

#### Method for forming the select + from part of the query ###########################################
def get_select_from(fields_list, attrib_used, table_aliases, attrib_list, entity_list, attrib_map, entity_map):

    select_string = ''
    from_string = ''

    count = 1
    selects = []
    froms = []

    try:
        for i in range(len(fields_list)):
            attribs, entities = fields_list[i]
            if attribs==[] and entities==[]:
                continue
            elif attribs==[]:
                selects += ['T'+str(count)+'.*']
                from_temp = entity_map[entity_list[int(entities[0].replace('ENTITY_',''))]]
                for j in range(1,len(entities)):
                    from_temp += (' NATURAL JOIN '+ entity_map[entity_list[int(entities[j].replace('ENTITY_',''))]])
            elif entities==[]:
                temp_tables = set([])
                for j in range(0,len(attribs)):
                    attrib_number = int(attribs[j].replace('ATTRIB_',''))
                    selects += ['T'+str(count)+'.'+attrib_list[attrib_number]]
                    temp_tables = temp_tables | attrib_map[attrib_list[attrib_number]]
                from_temp = ''
                temp_count = 1
                for table in temp_tables:
                    from_temp += table
                    if temp_count != len(temp_tables):
                        from_temp += ' NATURAL JOIN '
                    temp_count += 1
            else:
                for j in range(0,len(attribs)):
                    attrib_number = int(attribs[j].replace('ATTRIB_',''))
                    selects += ['T'+str(count)+'.'+attrib_list[attrib_number]]
                from_temp = entity_map[entity_list[int(entities[0].replace('ENTITY_',''))]]
                for j in range(1,len(entities)):
                    from_temp += (' NATURAL JOIN '+ entity_map[entity_list[int(entities[j].replace('ENTITY_',''))]])

            if len(from_temp.split())>1:
                from_temp = '( SELECT * FROM ' + from_temp + ' )'
            from_temp += (' AS T'+str(count))
            froms += [from_temp]
            count += 1

            table_aliases += ['T'+str(count-1)]
            attrib_used += selects

        select_string = 'SELECT '
        for i in range(0,len(selects)):
            select_string += (selects[i])
            if (i+1) != len(selects):
                select_string += ' , '

        from_string = 'FROM '
        for i in range(0,len(froms)):
            from_string += (froms[i])
            if (i+1) != len(froms):
                from_string += ' , ' 

        return select_string, from_string

    except:
        print "Rule Based: Exception in get_select_from() function. Returning empty select, from strings."
        return '',''

#### Method for forming the where part of the query ##########################################################
def get_where(conds_list, attribs_used, table_aliases, attrib_list, entity_list, const_list, attrib_map, entity_map):

    where_string = ''
    wheres = []

    try:
        # Initialize the condition mappings 
        cond_map = {'is':'$ = &', 'in':'$ in &', 'belongs':'$ in &', 'belong':'$ in &', 'belonging':'$ in &', 'equal':'$ = &', 'equals':'$ = &', 'unequal':'$ != &', 'higher':'$ > &', 'lower':'$ < &', 'greater':'$ > &', 'lesser':'$ < &', 'more':'$ > &', 'less':'$ < &', 'larger':'$ > &', 'bigger':'$ > &', 'smaller':'$ < &', 'greater_than_or_equal':'$ >= &', 'lesser_than_or_equal':'$ <= &', 'divisible':'$ % & = 0', 'of':'$ = &', 'same':'$ = &', 'much':'$ = &', 'not':'$ != &', 'as':'$ = &'}
        cond_sp_map = {'maximum':'$ = MAX($)', 'minimum':'$ = MIN($)', 'low':'$ < CUTOFF', 'high':'$ > CUTOFF'}

        # Initialize the join phrase mappings (Cond : [to_be_ANDed?,is_NEGATed?])
        join_map = {'and':[True,False], 'or':[False,False], 'not':[True,True], 'but':[True,False]}

        current_state = [True,False]
        prev_cond_exists = False

        for i in range(0,len(conds_list)):
            if conds_list[i] == '':
                continue
            if type(conds_list[i]) is nltk.tree.Tree and conds_list[i].node == 'CONJ1_':
                join_vars = get_join_list(conds_list[i],join_map)
                for j in range(0,len(join_vars)):
                    current_state[0] &= join_vars[j][0]
                    current_state[1] ^= join_vars[j][1] 
            else:
                #[IS_SPECIAL,VALUE,NEGATE,COMP,VALUE]
                if conds_list[i][0] == True:
                    current_state[1] ^= conds_list[i][2]
                    value = ''
                    if conds_list[i][1] == False:
                        if attribs_used==[]:
                            value = 'missing_val'
                        else:
                            value = attribs_used[len(attribs_used)-1]
                    else:
                        if conds_list[i][1].get_child('CONSTANT') == False:
                            value = attrib_list[int(conds_list[i][1].get_child('ATTRIB')[0].replace('ATTRIB_',''))]
                            if len(table_aliases)>0 :
                                value = table_aliases[len(table_aliases)-1]+'.'+value
                            attribs_used += [value]
                        else:
                            value = const_list[int(conds_list[i][1].get_child('CONSTANT')[0].replace('CONST_',''))]

                    if prev_cond_exists :
                        if current_state[0]==True:
                            wheres += ['and']
                        else:
                            wheres += ['or']
                    if current_state[1]==True:
                        wheres += ['not']
                    wheres += [cond_sp_map[conds_list[i][3]].replace('$',value)]
    
                else:
                    current_state[1] ^= conds_list[i][2]
                    value1 = ''
                    value2 = ''

                    if conds_list[i][1] == False:
                        if attribs_used==[]:
                            value1 = 'missing_val'
                        else:
                            value1 = attribs_used[len(attribs_used)-1]
                    else:
                        if conds_list[i][1].get_child('CONSTANT') == False:
                            value1 = attrib_list[int(conds_list[i][1].get_child('ATTRIB')[0].replace('ATTRIB_',''))]
                            if len(table_aliases)>0 :
                                value1 = table_aliases[len(table_aliases)-1]+'.'+value1
                            attribs_used += [value1]
                        else:
                            value1 = const_list[int(conds_list[i][1].get_child('CONSTANT')[0].replace('CONST_',''))]

                    if conds_list[i][4].get_child('CONSTANT') == False:
                        value2 = attrib_list[int(conds_list[i][4].get_child('ATTRIB')[0].replace('ATTRIB_',''))]
                        if len(table_aliases)>0 :
                            value2 = table_aliases[len(table_aliases)-1]+'.'+value2
                    else:
                        value2 = const_list[int(conds_list[i][4].get_child('CONSTANT')[0].replace('CONST_',''))]

                    if prev_cond_exists :
                        if current_state[0]==True:
                            wheres += ['and']
                        else:
                            wheres += ['or']
                    if current_state[1]==True:
                        wheres += ['not']

                    if cond_map[conds_list[i][3]].split()[1] == 'in' and value2[0]=="'":
                        temp_value2 = value2[1:-1]
                        if temp_value2[0] != '(':
                            temp_value2 = "('" + temp_value2 + "')"
                        wheres += [cond_map[conds_list[i][3]].replace('$',value1).replace('&',temp_value2)]
                    else:
                        wheres += [cond_map[conds_list[i][3]].replace('$',value1).replace('&',value2)]

                prev_cond_exists = True
                current_state = [True,False]

        if wheres == []:
            return ''
        where_string = 'WHERE ' + " ".join(wheres)
        return where_string

    except:
        print "Rule Based: Exception in get_where() function. Returning empty where string."
        return ''

##############################################################################################################
#### The main driver method for conversion of query to SQL ###################################################
##############################################################################################################

def give_sql(tokens, entity_list, attrib_list, const_list, attrib_map, entity_map):

    try:
        grammar1 = nltk.data.load('file:grammar/mygrammar_v4.cfg')
        rd_parser = nltk.SteppingRecursiveDescentParser(grammar1)
        #rd_parser = nltk.RecursiveDescentParser(grammar1)
        nltk.tree.Tree.get_child = get_child
        print "Rule Based: Created the parser object from the CFG"
    except:
        print "Rule Based: Could not create the parser object instance. Check the CFG!"
        return ''

    tokens = convert_complex_comp(tokens)

    if tokens == []:
        print "Rule Based: Could not convert the complex comparators to simple ones."
        return ''
    else:
        print "Rule Based: Converted complex comparators to simple ones."

    try:
        sys.stdout.write("Rule Based: Parsing the generic english query... ")
        sys.stdout.flush()
        rd_parser.initialize(tokens)
        while(rd_parser.parses() == []):
            rd_parser.step()
        query_tree = rd_parser.parses()[0]
        query_tree = query_tree.get_child('P')
        print "Done"
        query_tree.draw()
    except:
        print "Failed to parse !"
        return ''

    #query_tree = Tree('P', [Tree('SELECT', [Tree('ACTION', [Tree('DO', [Tree('VERB', ['give']), Tree('TARGET_', [Tree('TARGET', [Tree('AGENT_', [Tree('AGENT', ['me'])])]), Tree('CONJ1_', [Tree('CONJ1', ['and'])]), Tree('TARGET_', [Tree('TARGET', [Tree('AGENT_', [Tree('AGENT', ['my'])]), Tree('RELATE', ['friend'])])])])])]), Tree('FIELD_', [Tree('FIELD', [Tree('ATTRIB1_', [Tree('ATTRIB1', [Tree('FILLER_', [Tree('FILLER', ['the'])]), Tree('ATTRIB2', [Tree('ATTRIB', ['ATTRIB_0'])])]), Tree('CONJ1_', [Tree('CONJ1', [',']), Tree('CONJ1_', [Tree('CONJ1', ['and'])])]), Tree('ATTRIB1_', [Tree('ATTRIB1', [Tree('ATTRIB2', [Tree('ATTRIB', ['ATTRIB_1'])])])])]), Tree('ENTITY1_', [Tree('ENTITY1', [Tree('FILLER_', [Tree('FILLER', ['from'])]), Tree('ENTITY2', [Tree('ENTITY', ['ENTITY_0'])])])])])])]), Tree('WHERE', [Tree('COND1', [Tree('FILLER2_', [Tree('FILLER2', ['with']), Tree('FILLER2_', [Tree('FILLER2', [Tree('FILLER', ['the'])])])]), Tree('COND', [Tree('VALUE', [Tree('ATTRIB', ['ATTRIB_2'])]), Tree('COMP_', [Tree('COMP1', [Tree('COMP2', [Tree('COMP3', ['more']), Tree('EXTRA', ['than'])])])]), Tree('VALUE', [Tree('CONSTANT', ['CONST_0'])])])])])])

    #query_tree = Tree('P', [Tree('SELECT', [Tree('ACTION', [Tree('DO', [Tree('VERB', ['give']), Tree('TARGET_', [Tree('TARGET', [Tree('AGENT_', [Tree('AGENT', ['me'])])]), Tree('CONJ1_', [Tree('CONJ1', ['and'])]), Tree('TARGET_', [Tree('TARGET', [Tree('AGENT_', [Tree('AGENT', ['my'])]), Tree('RELATE', ['friend'])])])])])]), Tree('FIELD_', [Tree('FIELD', [Tree('ENTITY1_', [Tree('ENTITY1', [Tree('FILLER_', [Tree('FILLER', ['the'])]), Tree('ENTITY2', [Tree('ENTITY', ['ENTITY_0'])])])])]), Tree('CONJ1_', [Tree('CONJ1', ['and'])]), Tree('FIELD_', [Tree('FIELD', [Tree('ATTRIB1_', [Tree('ATTRIB1', [Tree('ATTRIB2', [Tree('ATTRIB', ['ATTRIB_0'])])])])])])])]), Tree('WHERE', [Tree('COND1', [Tree('FILLER2_', [Tree('FILLER2', [Tree('FILLER', ['which'])]), Tree('FILLER2_', [Tree('FILLER2', [Tree('FILLER', ['have'])]), Tree('FILLER2_', [Tree('FILLER2', [Tree('FILLER', ['a'])])])])]), Tree('COND', [Tree('VALUE', [Tree('ATTRIB', ['ATTRIB_1'])]), Tree('COMP_', [Tree('COMP1', [Tree('COMP2', [Tree('COMP3', ['greater_than_or_equal']), Tree('EXTRA', ['to'])])])]), Tree('VALUE', [Tree('CONSTANT', ['CONST_0'])])])])])])

    fields_list = []                           # List for containing pairs [[ATTRIBs],[ENTITYs]]
    fill_fields(fields_list, query_tree)       # Populate the list
    attribs_used = []                          # List of attributes used in the query in sequential order till select,from
    table_aliases = []						   # List of aliases for native tables (or their joins) in the query
    
    # Now get the select and from strings
    select_string, from_string = get_select_from(fields_list, attribs_used, table_aliases, attrib_list, entity_list, attrib_map, entity_map)

    conds_list = []                            # List for holding conds, each of form [IS_SPECIAL,VALUE,NEGATE,COMP,VALUE] or [JOIN_TYPE]
    fill_conds(conds_list, query_tree)         # Populate the list

    # Now get the where string
    where_string = get_where(conds_list, attribs_used, table_aliases, attrib_list, entity_list, const_list, attrib_map, entity_map)

    # Return the suitable query
    if select_string == '' or from_string == '':
        print "Rule Based: Could not create select & from parts of the SQL query."
        return ''
    else:
        print "Rule Based: Obtained the select & from parts of the SQL query."

    if where_string == '':
        print "Rule Based: where part of the SQL query is empty."
        return select_string+'\n'+from_string+' ;'
    else:
        print "Rule Based: where part of the SQL query is non-empty."
        return select_string+'\n'+from_string+'\n'+where_string+' ;'
