'''
Created on 16-Jun-2012

@author: Raghavan
'''
import question
import answer_document
import nltk

#availablepredicates = [['p1','V,N'],['p2', 'N,V'], ['p3','V,N,SameSentence'], ['p4','V,N,threshold'], ['p4','V,N,moreVerb']
#Sample Ques pos = [WP, VBD, DT, JJ, NN, NN, IN, NNP, NNP]
#Verb is followed by noun
def predicate_verbPrecedesNoun(question, document):
    nCounter = 0
    idxMatrixAltered = 0
    if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: #Checking that there is atleast one verb and one noun
        if question.arrVerb[nCounter][1] < question.arrNoun[nCounter][1]: # In Question, verb is followed by noun
            for sVerb in question.arrVerb:
                for sNoun in question.arrNoun:
                    #print "Verb: ",sVerb[0]
                    #print "Noun: ",sNoun[0]
                    nVerb = document.noofoccurrences(sVerb[0])
                    nNoun = document.noofoccurrences(sNoun[0])
                    nVidx = document.firstOccurrence(sVerb[0])
                    nNidx = document.firstOccurrence(sNoun[0])
                    #print "Verb idx p1:", nVidx
                    #print "Noun idx p1: ",nNidx
                    if nVerb > 0 and nNoun > 0:
                        if nVidx < nNidx: # Whether in doc also, that verb is followed by that same noun
                            idxMatrixAltered = 1
                            loop = 0
                            break
                if idxMatrixAltered == 1:
                    break

    if idxMatrixAltered == 0:
        return False
    else:
        return True 

#Noun is followed by verb
def predicate_nounPrecedesVerb(question, document):
    nCounter = 0
    idxMatrixAltered = 0
    if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: #Checking that there is atleast one verb and one noun
        if question.arrVerb[nCounter][1] > question.arrNoun[nCounter][1]: # In Question, noun is followed by verb
            print "check:"
	    print question.arrVerb[nCounter][1] 
	    print question.arrNoun[nCounter][1]
	    for sVerb in question.arrVerb:
                for sNoun in question.arrNoun:
                    #print "Verb: ",sVerb[0]
                    #print "Noun: ",sNoun[0]
                    nVerb = document.noofoccurrences(sVerb[0])
                    nNoun = document.noofoccurrences(sNoun[0])
                    nVidx = document.firstOccurrence(sVerb[0])
                    nNidx = document.firstOccurrence(sNoun[0])
                    if nVerb > 0 and nNoun > 0:
                        if nVidx > nNidx: # Whether in doc also, that verb is followed by that same noun
                            # if true i.e verb is followed by noun
                            idxMatrixAltered = 1
                            loop = 0
                            break
                if idxMatrixAltered == 1:
                    break 

    if idxMatrixAltered == 0:
        # if false i.e verb is not followed by noun
        return False
    else:
        return True 

#Verb and noun occur in the same sentence
def predicate_verbNounSameSent(question, document):
    nCounter = 0
    loop = len(question.arrVerb)
    idxMatrixAltered = 0
    if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: #Checking that there is atleast one verb and one noun
        for sVerb in question.arrVerb:
            for sNoun in question.arrNoun:
                #print "Verb: ",sVerb[0]
                #print "Noun: ",sNoun[0]
                nVSent = document.findSentNo(sVerb[0]) #print "Verb Sent No: ", document.sentNo                    
                vsentence = document.findSentence(document.sentNo) #print "Verb Sentence: ", vsentence                    
                nNSent = document.findSentNo(sNoun[0]) #print "Noun sent no: ", document.sentNo
                #print "Verb sentNo: ",nVSent
                #print "Noun sentNo: ",nNSent
                if nVSent == nNSent and len(vsentence) > 0:
                    # Verb and Noun occurs in the same sentence in doc
                    idxMatrixAltered = 1
                    p3MatchSentNo = nNSent
                    break
            if idxMatrixAltered == 1:
                break
            
    if idxMatrixAltered == 0:
        return False
    else:
        return True

#Verb and noun occur within a threshold distance
def predicate_verbNounThreshDist(question, document):
    nCounter = 0
    loop = len(question.arrVerb)
    idxMatrixAltered = 0
    if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: #Checking that there is atleast one verb and one noun
        for sVerb in question.arrVerb:
            for sNoun in question.arrNoun:
                #print "Verb: ",sVerb[0]
                #print "Noun: ",sNoun[0]
                nVSent = document.findSentNo(sVerb[0])
                nNSent = document.findSentNo(sNoun[0])
                #print "Verb SentNo: ",nVSent
                #print "Noun SentNo: ",nNSent
                if isinstance(nVSent,int) and isinstance(nNSent,int) and nVSent != nNSent:
                    if nVSent > nNSent:
                        Diff = nVSent - nNSent
                    else:
                        Diff = nNSent - nVSent
                    if Diff <= 10:
                        # Verb and Noun occur within a distance of 10 sentences(considered to be a paragraph) separately
                        idxMatrixAltered = 1
                        break

            if idxMatrixAltered == 1:
                break
                        
    if idxMatrixAltered == 0:
        return False
    else:
        return True
    
#Noun occurs once and verb occurs more than once in the given text
def predicate_verbMore(question, document):
    nCounter = 0
    loop = len(question.arrVerb)
    idxMatrixAltered = 0
    if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: 
        for sVerb in question.arrVerb:
            for sNoun in question.arrNoun:
                #print "Verb: ",sVerb[0]
                #print "Noun: ",sNoun[0]
                nVOcc = document.noofoccurrences(sVerb[0])
                nNOcc = document.noofoccurrences(sNoun[0])
                #print "Verb Occ: ",nVOcc
                #print "Noun Occ: ",nNOcc
                if isinstance(nNOcc,int) and isinstance(nVOcc, int) and nNOcc >= 1 and nVOcc > nNOcc:
                    idxMatrixAltered = 1
                    break
            if idxMatrixAltered == 1:
                break

    if idxMatrixAltered == 0:
        return False
    else:
        return True

#Verb occurs once and noun occurs more than once in the given text
def predicate_nounMore(question, document):
    nCounter = 0
    loop = len(question.arrVerb)
    idxMatrixAltered = 0
    if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: #Checking that there is atleast one verb and one noun
        for sVerb in question.arrVerb:
            for sNoun in question.arrNoun:
                #print "Verb: ",sVerb[0]
                #print "Noun: ",sNoun[0]
                nVOcc = document.noofoccurrences(sVerb[0])
                nNOcc = document.noofoccurrences(sNoun[0])
                #print "Verb Occ: ",nVOcc
                #print "Noun Occ: ",nNOcc
                if isinstance(nVOcc,int) and isinstance(nNOcc, int) and nVOcc >= 1 and nNOcc > nVOcc:
                    idxMatrixAltered = 1
                    break
            if idxMatrixAltered == 1:
                break
            
    if idxMatrixAltered == 0:
        return False
    else:
        return True

#Check if question has noun phrase(s), if yes, check for the same noun phrases in the QD pair.
def predicate_NPSameSentence(question,document):
    ncounter = 0
    idxMatrixAltered = 0
    formNP = ""
    docNP = []
    grammar = """
            WHNP: {<W.*><NN>+}           # Chunk sequences of Wh phrases
            ADVP: {<RB.*>*}
            NP: {<DT|JJ.*|CD|ADVP|NN.*>+}          # Chunk sequences of DT, JJ, NN
            PP: {<IN><NP>}               # Chunk prepositions followed by NP
            VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
            CLAUSE: {<NP><VP>}           # Chunk NP, VP  
            """
    cp = nltk.RegexpParser(grammar)
    if len(question.arrNP) > 0:
        length = len(question.arrNP)
        for sent in document.sentences:
            #Checking and collecting the noun phrases in the sentence "sent", if any
            doc_sen_pos = nltk.pos_tag(nltk.word_tokenize(sent))
            tree = cp.parse(doc_sen_pos)
            for subtree in tree.subtrees():
                if subtree.node == "NP" :
                    for leaf in subtree.leaves():
                        if leaf[1] != "DT" and leaf[1] != "IN":
                            if len(formNP) > 2:
                                formNP = formNP + " " + leaf[0]
                            else:
                                formNP = leaf[0]
                    docNP.append(formNP)
                    formNP = ""
            #Checking whether the noun phrases in the question occurs in the collected noun phrases of this sentence
            for np in question.arrNP:
                if np not in docNP:
                    idxMatrixAltered = 0
                else:
                    ncounter = ncounter+1
            
            if ncounter == len(question.arrNP):
                idxMatrixAltered = 1 #True only when all the noun phrases of the question appear in the document sentence
    else:
        idxMatrixAltered = 0 # No Non phrases in question, hence not applicable

    if idxMatrixAltered == 0:
        return False
    else:
        return True

#Check if question has noun phrase(s), if yes, check for the same noun phrases in the QD pair.
def predicate_NPSamepara(question,document):
    qarrNP = []
    for np in question.arrNP:
        qarrNP.append(np)
        
    nSentNo = []
    idxMatrixAltered = 0
    formNP = ""
    docNP = []
    grammar = """
            WHNP: {<W.*><NN>+}            # Chunk sequences of Wh phrases
            ADVP: {<RB.*>*}               # Chunk sequences of Adverbial Phrases 
            NP: {<DT|JJ.*|CD|ADVP|NN.*>+} # Chunk sequences of DT, JJ, NN
            PP: {<IN><NP>}                # Chunk prepositions followed by NP
            VP: {<VB.*><NP|PP|CLAUSE>+$}  # Chunk verbs and their arguments
            CLAUSE: {<NP><VP>}            # Chunk NP, VP  
            """
    cp = nltk.RegexpParser(grammar)
    if len(question.arrNP) > 0:
        length = len(question.arrNP)
        for sent in document.sentences:
            #Checking and collecting the noun phrases in the sentence "sent", if any
            doc_sen_pos = nltk.pos_tag(nltk.word_tokenize(sent))
            tree = cp.parse(doc_sen_pos)
            for subtree in tree.subtrees():
                if subtree.node == "NP" :
                    for leaf in subtree.leaves():
                        if leaf[1] != "DT" and leaf[1] != "IN":
                            if len(formNP) > 2:
                                formNP = formNP + " " + leaf[0]
                            else:
                                formNP = leaf[0]
                    docNP.append(formNP)
                    formNP = ""
            #Checking whether the noun phrases in the question occurs in the collected noun phrases of this sentence
            for np in qarrNP:
                if np not in docNP:
                    idxMatrixAltered = 0
                else:
                    nSentNo.append(document.sentences.index(sent))
                    del qarrNP[qarrNP.index(np)]
            
            nlen = len(nSentNo)
            for x in xrange(0,nlen-1):
                if nSentNo[0] < nSentNo[x+1]:   
                    diff = nSentNo[x+1] - nSentNo[0]
                else:
                    diff = nSentNo[0] - nSentNo[x+1]
                if diff < 10:                  
                    idxMatrixAltered = 1 #True only when all the noun phrases of the question appear in the document sentence
                else:
                    idxMatrixAltered = 0
                    break;                
    else:
        idxMatrixAltered = 0 # No Non phrases in question, hence not applicable

    if idxMatrixAltered == 0:
        return False
    else:
        return True

#Noun phrase ordered differently [if multiple words]
def predicate_diffNPOrder(question, document):
    qarrNP = []
    docNP = []
    for np in question.arrNP:
        qarrNP.append(np)
    
    idxMatrixAltered  = 0
    formNP  = ""
    grammar = """
                WHNP: {<W.*><NN>+}            # Chunk sequences of Wh phrases
                ADVP: {<RB.*>*}               # Chunk sequences of Adverbial Phrases 
                NP: {<DT|JJ.*|CD|ADVP|NN.*>+} # Chunk sequences of DT, JJ, NN
                PP: {<IN><NP>}                # Chunk prepositions followed by NP
                VP: {<VB.*><NP|PP|CLAUSE>+$}  # Chunk verbs and their arguments
                CLAUSE: {<NP><VP>}            # Chunk NP, VP  
                """
    cp = nltk.RegexpParser(grammar)
    if len(question.arrNP) > 0:
        length = len(question.arrNP)
        for sent in document.sentences:
            #Checking and collecting the noun phrases in the sentence "sent", if any
            doc_sen_pos = nltk.pos_tag(nltk.word_tokenize(sent))
            tree = cp.parse(doc_sen_pos)
            for subtree in tree.subtrees():
                if subtree.node == "NP" :
                    for leaf in subtree.leaves():
                        if leaf[1] != "DT" and leaf[1] != "IN":
                            if len(formNP) > 2:
                                formNP = formNP + " " + leaf[0]
                            else:
                                formNP = leaf[0]
                    docNP.append(formNP)
                    formNP = ""
                    #Checking whether the noun phrases in the question occurs in the collected noun phrases of this sentence
            if len(qarrNP) > 0:           
                for np in qarrNP:
                    if np  in docNP:
                       del qarrNP[qarrNP.index(np)]
    
    if len(qarrNP) < 0: 
        idxMatrixAltered = 1
        
    if idxMatrixAltered  == 1:
        return True
    else:
        return False


#Noun phrase occur in the same order but dispersed through out the document
def predicate_NPOrderDocSame(question, document):
    qarrNP = []
    docNP = []
    for np in question.arrNP:
        qarrNP.append(np)
    
    idxMatrixAltered  = 0
    formNP  = ""
    grammar = """
                WHNP: {<W.*><NN>+}            # Chunk sequences of Wh phrases
                ADVP: {<RB.*>*}               # Chunk sequences of Adverbial Phrases 
                NP: {<DT|JJ.*|CD|ADVP|NN.*>+} # Chunk sequences of DT, JJ, NN
                PP: {<IN><NP>}                # Chunk prepositions followed by NP
                VP: {<VB.*><NP|PP|CLAUSE>+$}  # Chunk verbs and their arguments
                CLAUSE: {<NP><VP>}            # Chunk NP, VP  
                """
    cp = nltk.RegexpParser(grammar)
    if len(question.arrNP) > 0:
        length = len(question.arrNP)
        for sent in document.sentences:
            #Checking and collecting the noun phrases in the sentence "sent", if any
            doc_sen_pos = nltk.pos_tag(nltk.word_tokenize(sent))
            tree = cp.parse(doc_sen_pos)
            for subtree in tree.subtrees():
                if subtree.node == "NP" :
                    for leaf in subtree.leaves():
                        if leaf[1] != "DT" and leaf[1] != "IN":
                            if len(formNP) > 2:
                                formNP = formNP + " " + leaf[0]
                            else:
                                formNP = leaf[0]
                    docNP.append(formNP)
                    formNP = ""
            #Checking whether the noun phrases in the question occurs in the collected noun phrases of this sentence
            np = qarrNP[0]
            if np in docNP:
                del qarrNP[qarrNP.index(np)]
        
            if len(qarrNP) <= 0:
                idxMatrixAltered = 1
                break #No need to check the remaining sentences as all the noun phrases have been matched 
        
    if idxMatrixAltered == 1:
        return True
    else:
        return False

#Verb phrase checker
def predicate_VPSameSentence(question,document):
    ncounter = 0           
    idxMatrixAltered  = 0
    formVP  = ""
    docVP = []
    qarrVP = []
    for np in question.arrVP:
        qarrVP.append(np)
        
    grammar = """
                WHNP: {<W.*><NN>+}            # Chunk sequences of Wh phrases
                ADVP: {<RB.*>*}               # Chunk sequences of Adverbial Phrases 
                NP: {<DT|JJ.*|CD|ADVP|NN.*>+} # Chunk sequences of DT, JJ, NN
                PP: {<IN><NP>}                # Chunk prepositions followed by NP
                VP: {<VB.*><NP|PP|CLAUSE>+$}  # Chunk verbs and their arguments
                CLAUSE: {<NP><VP>}            # Chunk NP, VP  
                """
    cp = nltk.RegexpParser(grammar)
    if len(question.arrVP) > 0:
            length = len(question.arrVP)
            for sent in document.sentences:
                #Checking and collecting the noun phrases in the sentence "sent", if any
                doc_sen_pos = nltk.pos_tag(nltk.word_tokenize(sent))
                tree = cp.parse(doc_sen_pos)
                for subtree in tree.subtrees():
                    if subtree.node == "VP" :
                        for leaf in subtree.leaves():
                            if leaf[1] != "DT" and leaf[1] != "IN":
                                if len(formVP) > 2:
                                    formVP = formVP + " " + leaf[0]
                                else:
                                    formVP = leaf[0]
                        docVP.append(formVP)
                        formVP = ""
                        #Checking whether the noun phrases in the question occurs in the collected noun phrases of this sentence
                for np in question.arrVP:
                    if np not in docVP:
                        idxMatrixAltered = 0
                    else:
                        ncounter = ncounter+1
                
                if ncounter == len(question.arrNP):
                    idxMatrixAltered = 1 #True only when all the noun phrases of the question appear in the document sentence
    else:
        idxMatrixAltered = 0 # No Non phrases in question, hence not applicable
    
    if idxMatrixAltered == 0:
        return False
    else:
        return True


#occurrence of 'CD' in question and doc in same sentence, where the noun and the verb occurs
def predicate_occCDQDSameSent(question,document):
    idxMatrixAltered = 0
    if len(question.arrNum) > 0:
        length = len(question.arrNum)
        nCounter = 0
        loop = length
        idxMatrixAltered = 0
        p3MatchSentNo = 0
        while loop > 0: #Check for all the numbers, whether they occur in the same sentence
            nNum = question.arrNum[nCounter]
            if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: #Checking that there is atleast one verb and one noun
                for sVerb in question.arrVerb:
                    for sNoun in question.arrNoun:
                        nVSent = document.findSentNo(sVerb[0]) #print "Verb Sent No: ", document.sentNo                    
                        vsentence = document.findSentence(document.sentNo) #print "Verb Sentence: ", vsentence                    
                        nNSent = document.findSentNo(sNoun[0]) #print "Noun sent no: ", document.sentNo 
                        if nVSent == nNSent and len(vsentence) > 0:
                            # Verb and Noun occurs in the same sentence in doc
                            idxMatrixAltered = 1
                            p3MatchSentNo = nNSent
                            break
                    break
                        
            if isinstance(p3MatchSentNo, int): # Indicates that the verb followed by the noun occurs in the same sentence
                #nst = document.findSentNo(self.psMatchSentNo) #
                sSen = document.findSentence(p3MatchSentNo) #Retrieving the sentence using the retrieved sentence number from the predicate p3.
                if nNum[0] in sSen.lower():
                    idxMatrixAltered = 1
                    # The number in Q and Doc appears same and it appears in the same sentence as the verb and noun
                    break; #Hoping for atleast one matching occurrence
            nCounter = nCounter + 1
            loop = loop - 1
            
        if idxMatrixAltered == 0:
            return False # The number does not appear in the same sentence
        else:
            return True #this predicate is not applicable for this question,hence making the same false

#occurrence of 'CD' in question and doc
def predicate_occCDQD(question,document):
    if len(question.arrNum) > 0:
        length = len(question.arrNum)
        nCounter = 0
        loop = length 
        idxMatrixAltered = 0
        while loop > 0: #Check for all the numbers, whether they occur in the same senten
            nNum = question.arrNum[nCounter]
            for w in document.arrwords:
                if cmp(w ,nNum) == 0:
                    idxMatrixAltered = 1 #Hoping for atleast one matching occurrence
                    break
            nCounter = nCounter + 1
            loop = loop - 1

        if idxMatrixAltered == 1:
            return True #The number is present in the doc
        else:
            return False #The number is not present in the doc
    else:
        return False #this predicate is not applicable for this question,hence making the same false
    
#occurrence of 'JJ' in question and doc : Adjective followed by Noun. Taking the first occuring adjective and the first occuring noun from the question;
#checking whether these two occur in the document in the same sentence or with in a paragraph [10 sentences].
def predicate_occJJprecedesNounSS(question,document):
    if len(question.arrAdj) > 0:
        length = len(question.arrAdj)
        nCounter = 0
        loop = length
        bpresent = 0
        bword1 = 0
        bword2 = 0
        word1 = ""
        word2 = ""
        Jidx = 0
        Nidx = 0
        idxMatrixAltered = 0
        bAdjacent = 0
        for x in question.pos_tags:
            if x[1][0] == 'J' and len(word1) == 0: #Taking the first adjective
                word1 = x[0]
                Jidx = question.pos_tags.index(x)
            elif x[1][0] == 'N' and x[0][0] != 'W' and len(word2) == 0: #Taking the first noun
                word2 = x[0]
                Nidx = question.pos_tags.index(x)
            if len(word1) > 0 and len(word2) > 0:
                break
            
            #Checking the indices of Question : Adjective and Noun
            if Jidx == (Nidx-1):
                bAdjacent = 1
        
            #checking for those words in the doc
            if bAdjacent == 1:
                for w in document.arrwords:
                    if cmp(word1.lower(), w.lower()) == 0 and bword1 == 0:
                        bword1 = 1
                        w1idx = document.arrwords.index(w) 
                    elif cmp(word2.lower(), w.lower()) == 0 and bword2 == 0:
                        bword2 = 1
                        w2idx = document.arrwords.index(w)
                if (bword1 == 1) and (bword2 == 1) and isinstance(w1idx,int) and isinstance(w2idx,int) and (w1idx == (w2idx-1)): #Once the same words are found in the doc 
                    #The adjective is adjacent to noun in doc as in question
                    idxMatrixAltered = 1            
            else:
                w1sentno = document.findSentNo(word1)
                w2sentno = document.findSentNo(word2)
                if isinstance(w1sentno,int) and isinstance(w2sentno,int):
                    if w1sentno > w2sentno:
                        Diff = w1sentno - w2sentno
                    else:
                        Diff = w2sentno - w1sentno
                    if Diff <= 10:
                        # Adjective and noun occur within a distance of 10 sentences(considered to be a paragraph) separately
                        idxMatrixAltered = 1
                        break 
        if idxMatrixAltered == 0:
            return False #The adjective with noun is not present adjacent in the doc
        else:
            return True 
    else:
        return False #This predicate is not applicable

#occurrence of 'RB' in question and doc : Adverb followed by Verb
def predicate_occRBprecedesVB(question,document):
    if len(question.arrAdv) > 0:
        length = len(question.arrAdv)
        nCounter = 0
        loop = length
        bpresent = 0
        bword1 = 0
        dw1 = 0
        dw2 = 0
        dw3 = 0
        word2 = ""
        word3 = ""
        dw1idx = 0
        dw2idx = 0
        dw3idx = 0
        idxMatrixAltered = 0
        for x in question.pos_tags:
            if x[1][0] == 'R':
                word1 = x[0]
                break
        
        #getting the words in the question
        for w in question.arrqwords:
            if cmp(word1.lower(), w.lower()) == 0 and bword1 == 0:
                bword1 = 1
                w1idx = question.arrqwords.index(w)
                break
        if bword1 == 1:
            if w1idx > 1:
                word2 = question.arrqwords[w1idx-1]
            #if len(document.arrwords) > w1idx:
            #    word3 = question.arrqwords[w1idx+1]            
        #Checking for these matching words
        if bword1 == 1:
            if len(word2) > 0:
                for w in document.arrwords:
                    if cmp(word1.lower(), w.lower()) == 0 and dw1 == 0:
                         dw1idx = document.arrwords.index(w)
                         dw1 = 1
                    elif cmp(word2.lower(), w.lower()) == 0 and dw2 == 0:
                         dw2idx = document.arrwords.index(w)
                         dw2 = 1
            #if len(word3) > 0:
            #   for w in document.arrwords:
            #       if cmp(word3.lower(), w.lower()) == 0 and dw3 == 0:
            #             dw3idx = document.arrwords.index(w)
            #             dw3 = 1
        if bword1 == 1 and dw2 == 1:
            if dw2idx == (dw1idx-1):
                return True #The adverb with noun is present in the doc
            #if dw3 == 1:
            #    if dw3idx == (dw1idx+1):
            #        self.booleanmatrix[len(self.booleanmatrix)-1].append("1") #The adverb with noun is present in the doc                         
            #    else:
            #        self.booleanmatrix[len(self.booleanmatrix)-1].append("0") #The adverb with noun is not present in the doc
            else:
                return False #The adverb with noun is not present in the doc
        else:
            return False #The adverb with noun is not present in the doc
    else:
        return False #This predicate is not applicable

#Synset of the verb is followed by noun 
def predicate_synsetVBprecededNoun(question,document):
    nCounter = 0
    idxMatrixAltered = 0 
    if len(question.arrVerb) > 0 and len(question.arrNoun) > 0: #Checking that there is atleast one verb and one noun
	#print "printing..."	
	#print  question.arrVerb[nCounter][1] 
	#print  question.arrNoun[nCounter][1]
        if question.arrVerb[nCounter][1] < question.arrNoun[nCounter][1]: # In Question, verb is followed by noun
            for sVerb in question.arrVerb:
                sWord = sVerb[0]
                document.findSynsets(sWord)
                #print "Length of Synsets :", len(document.synsets)
                if len(document.synsets) > 0:
                    for sSyn in document.synsets:
                        nVerb = document.noofoccurrences(sSyn[0])
                        nVidx = document.firstOccurrence(sSyn[0])                            
                        for sNoun in question.arrNoun:
                            nNidx = document.firstOccurrence(sNoun[0])
                            nNoun = document.noofoccurrences(sNoun[0])
                            if nVerb > 0 and nNoun > 0 and (nNidx >0 and nVidx > 0):
                                #print "word: ", sWord
                                #print "Synsets: ", sSyn[0]
                                #print "vIdx: ", nVidx
                                #print "nIdx: ", nNidx
                                if nVidx < nNidx: # Whether in doc also, that verb is followed by that same noun                            
                                    return True # if true i.e verb is followed by noun
                                    idxMatrixAltered = 1
                                    break
                        if idxMatrixAltered == 1:
                            break
                if idxMatrixAltered == 1:
                            break
        
    if idxMatrixAltered == 0:
        return False # if false i.e verb is not followed by noun 












































