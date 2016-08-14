'''
Created on 16-Jun-2012

@author: Raghavan
'''
import nltk
from nltk.corpus import wordnet as wn

class AnswerDocument(object):
    
    pos = []
    arrwords = []
    sentences = []
    synsets = []
    noofocc = 0
    sentNo = 0
    sentOcc = ""
    content = ""
    '''
    classdocs
    '''
    file_path = ''

    def __init__(self, path):
        self.file_path = path
        
        doctext = ""
        #Open the file to read
        file = open(self.file_path, 'r')
        
        #Reading the content from the file and forming a string - doctext
        lines = file.readlines(100000)
        if lines:
            for line in lines:
                doctext += line
        
        self.content = doctext
        self.postag()
        
        '''
        Constructor
        '''

    def file_handle(self):
        return open(self.file_path, 'r')
        
    def postag(self):
        self.pos = nltk.pos_tag(nltk.word_tokenize(self.content))
        self.arrwords = []
        for x in self.pos:
            self.arrwords.append(x[0])
        self.sentences = nltk.sent_tokenize(self.content)
    
    def noofoccurrences(self, word):
        nCount = 0
        for w in self.arrwords:
            if cmp(w.lower(),word.lower()) == 0:
                nCount = nCount + 1
        self.noofocc = nCount #number of times that word occurs have to be searched
        return self.noofocc
        #print self.noofocc

    def firstOccurrence(self, word):
        nCount = 0
        for w in self.arrwords:
            if cmp(w.lower(),word.lower()) == 0:
                 nCount = self.arrwords.index(w)
                 break
        return nCount        
    
    def findSynsets(self,word):
        self.synsets = []
        import nltk.corpus
        from nltk.corpus import wordnet as wn
        synlems = wn.synsets(word)
        
        #Getting the lemma names
        #here we get synsets (lemmas) like dog.n.01 etc
        arrSynlemmas = []
        for lemma in synlems:
            if lemma.name not in arrSynlemmas:
                arrSynlemmas.append(lemma.name) #retreiving those names

        #Getting the different I rel direct synset words
        arrSynWords1 = []
        for m in range(len(arrSynlemmas)):
            for lemma in wn.synset(arrSynlemmas[m]).lemmas:
                if lemma.name not in arrSynWords1:
                    arrSynWords1.append(lemma.name)
                    self.synsets.append(lemma.name)

        #Getting all the synsets of the synsets retreived - synsets2
        arrSynLem2 = []
        for x in range(len(arrSynlemmas)):
            arrSynLem2.append(wn.synset(arrSynlemmas[x]))

        #Getting all the hypernyms using the retreived synsets2
        arrSynHyper2 = []
        for y in range(len(arrSynLem2)):
            for lemma in arrSynLem2[y].hypernyms():
                if lemma.name not in arrSynHyper2:
                    arrSynHyper2.append(lemma.name)

        #Retreiving the different words of hypernyms
        arrSynWords2 = []
        for z in range(len(arrSynHyper2)):
            for lemma in wn.synset(arrSynHyper2[z]).lemmas:
                if lemma.name not in arrSynWords2:
                    arrSynWords2.append(lemma.name)
                    self.synsets.append(lemma.name) 
         
        
    def findSentNo(self, word):
        for x in self.sentences:
            if word.lower() in x.lower():
                self.sentNo = self.sentences.index(x)
                return self.sentNo
        
        
    def findSentence(self, sentno):
        for x in self.sentences:
            if sentno is self.sentences.index(x):
                self.sentOcc = x #"This is the sentence in which the word occrs"
                return self.sentOcc
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    