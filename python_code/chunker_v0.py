#!/usr/bin/python2.7
import nltk
        
line = raw_input()
tokens = nltk.word_tokenize(line)
tag_list = nltk.pos_tag(tokens)

grammar = """
	S:            {<SELECT><FROM><WHERE>}
	SELECT:       {<VB>?<NP>}
	FROM_BASE:    {<RP>?<IN>+}
	FROM:         {<FROM_BASE><NP>}
	WHERE_BASE:   {<WP$|WRB|JJ>?<DT*|JJ*|IN*>}
	WHERE:        {<WHERE_BASE><COMP>}
	NP:           {<PRP>?<JJ.*>*<NN.*>+}
	COMP_BASE:    {<VBZ>|<JJR|RBR><IN>|<VBZ><JJR|RBR><IN>}
	COMP:         {<NP|CD><COMP_BASE><NP|CD>}
	"""

chunker = nltk.RegexpParser(grammar)

parse_tree = chunker.parse(tag_list)
print parse_tree

