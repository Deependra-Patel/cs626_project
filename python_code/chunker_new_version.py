#!/usr/bin/python2.7
import nltk
        
line = raw_input()
#line = '@ ' + line
tokens = nltk.word_tokenize(line)
tag_list = [('^','BEGIN')] + nltk.pos_tag(tokens) + [('.','.')]
print tag_list

grammar = """
	NP:           {<PRP>?<JJ.*>*<NN.*>+}
	SELECT:       {<BEGIN><VB>?<NP>}
	FROM:         {<IN><NP>}
	COMP2:        {<RB|RBR|JJR|JJ>*<IN|TO>}
	COMP_BASE:    {<VBZ>?<COMP2>?}
	COMP:         {<NP|CD><COMP_BASE><NP|CD><.>+}
	WHERE:        {<WRB>?<IN><><COMP>}
	"""

chunker = nltk.RegexpParser(grammar)
parse_tree = chunker.parse(tag_list)
print parse_tree


#grammar = """
#	NP:   {<PRP>?<JJ.*>*<NN.*>+}
#	COMP2: {<RB|RBR|JJR|JJ>*<IN|TO>}
#	COMP_BASE: {<VBZ>?<COMP2>?}
#	COMP: {<NP|CD><COMP_BASE><NP|CD>}
#	"""

#grammar = """
#	NP:           {<PRP>?<JJ.*>*<NN.*>+}
#	SELECT:       {<BEGIN><VB>?<NP>}
#	FROM:         {<IN><NP>}
#	COMP2:        {<RB|RBR|JJR|JJ>*<IN|TO>}
#	COMP_BASE:    {<VBZ>?<COMP2>?}
#	COMP:         {<NP|CD><COMP_BASE><NP|CD><.>+}
#	"""

