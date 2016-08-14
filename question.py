'''
Created on 16-Jun-2012

@author: Raghavan
'''

import nltk

class Question(object):
    question = ""
    pos_tags = []
    nooftags = 0
    arrqwords = []
    arrVerb = []
    arrNoun = []
    arrNum = []
    arrAdj = []
    arrAdv = []
    arrNP = []
    arrVP = []
    nCounter = 0
    '''
    classdocs
    '''

    def __init__(self, text):
        self.question = text
        self.pos_tags = nltk.pos_tag(nltk.word_tokenize(self.question))
        print self.pos_tags
        for x in self.pos_tags:
            self.arrqwords.append(x[0])
        self.nooftags = len(self.pos_tags)
        print self.nooftags
        self.collecttok_indices()
                
        #Find the noun phrases
        self.arrNP = []
        formNP = ""
        grammar = """
                    WHNP: {<W.*><NN>+}           # Chunk sequences of Wh phrases
                    ADVP: {<RB.*>+}
                    NP: {<DT|JJ.*|CD|ADVP|NN.*>+}          # Chunk sequences of DT, JJ, NN
                    PP: {<IN><NP>}               # Chunk prepositions followed by NP
                    VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
                    CLAUSE: {<NP><VP>}           # Chunk NP, VP  
                    """
        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(self.pos_tags)
        for subtree in tree.subtrees():
            if subtree.node == "NP" :
                for leaf in subtree.leaves():
                    if leaf[1] != "DT" and leaf[1] != "IN":
                        if len(formNP) > 2:
                            formNP = formNP + " " + leaf[0]
                        else:
                            formNP = leaf[0]
		
                self.arrNP.append(formNP)
                formNP = ""       
        
        for subtree in tree.subtrees():
            if subtree.node == "VP" :
                for leaf in subtree.leaves():
                    if leaf[1] != "DT" and leaf[1] != "IN":
                        if len(formNP) > 2:
                            formNP = formNP + " " + leaf[0]
                        else:
                            formNP = leaf[0]
                        print formNP	 
                self.arrVP.append(formNP)
                formNP = ""

    def text(self):
        return self.question


    def pos(self):
        return self.pos_tags
    
    def collecttok_indices(self):
        self.arrVerb = []
        self.arrNoun = []
        self.arrNum = []
        self.arrAdj = []
        self.arrAdv = []
        for x in self.pos_tags:
            if x[1][0] == 'V':
                self.arrVerb.append([x[0],self.pos_tags.index(x)])
	    elif x[1][0] == 'N' and x[0][0] != 'W':
                self.arrNoun.append([x[0],self.pos_tags.index(x)])
            elif x[1][0] == 'C':
                self.arrNum.append([x[0],self.pos_tags.index(x)])
            elif x[1][0] == 'J':
                self.arrAdj.append([x[0],self.pos_tags.index(x)])
            elif x[1][0] == 'R':
                self.arrAdv.append([x[0],self.pos_tags.index(x)])
                
 
                    
    
