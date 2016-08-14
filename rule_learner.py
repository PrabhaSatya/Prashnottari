'''
Created on 19-Jun-2012

@author: Raghavan
'''
import random
import csv

import orange, orngTree, orngAssoc

class RuleLearner(object):
    _tab_separated_data_file_ = '..\..\TestData\TabSeparatedData.txt'
    _comma_separated_data_file_ = '..\..\TestData\Results.csv'
    _data_set_ = []
    _skew_limit_ = 0.05
    '''
    classdocs
    '''


    def __init__(self):
        return
        
        '''
        Constructor
        '''
    
    def learn_from(self, predicate_truth_matrix):
        self._preprocess_truth_matrix_(predicate_truth_matrix)
        self._write_to_data_file_()
        data = orange.ExampleTable(self._tab_separated_data_file_)
        rules = orange.AssociationRulesInducer(data,support = 0.4,classificationRules = 1)

        print "%i rules with support higher than or equal to %5.3f found.\n" % (len(rules), 0.4)
        orngAssoc.sort(rules,["support", "confidence"])

        for r in rules:
            print "%5.3f  %5.3f  %s" % (r.support, r.confidence, r)
        
        
        #tree = orngTree.TreeLearner(data, sameMajorityPruning=1, mForPruning=2)
        #print "Possible classes:", data.domain.classVar.values
        #print "Probabilities for democrats:"
        #for i in range(50):
        #    p = tree(data[i], orange.GetProbabilities)
        #    c = tree(data[i])
        #    print "%d: %5.3f (originally %s) classified as %s" % (i+1, p[1], data[i].getclass(), c)
        #     print "%d: %s (originally %s)" % (i+1, c, data[i].getclass())
               
        #print
        #orngTree.printTxt(tree)
        #orngTree.printDot(tree, fileName='tree.dot', internalNodeShape="ellipse", leafShape="box")


        
        
        

    def _shuffle_data_set_rows_(self):
        print 'Random shuffling of truth matrix rows ...'
        new_data_set = [self._data_set_.pop(0)]
        while self._data_set_:
            n = random.randrange(0,len(self._data_set_))
            new_data_set.append(self._data_set_.pop(n))
        self._data_set_ = new_data_set


    def _remove_skewed_rows_(self):
        print 'Removing skewed rows ...'
        n_predicates = len(self._data_set_[0]) - 3
        skew_limit = self._skew_limit_ * n_predicates
        row = 1
        while row < len(self._data_set_):
            truths = 0
            for col in range(len(self._data_set_[row]) - 3):
                truths += (1 if self._data_set_[row][col+2] else 0)
            if truths <= skew_limit or truths >= (n_predicates - skew_limit):
                print 'Removing Question: {}; Document: {} pair. {} Truths out of {}.'.\
                        format(self._data_set_[row][0], self._data_set_[row][1], truths, n_predicates)
                self._data_set_.pop(row)
            else:
                row += 1


    def _remove_skewed_cols_(self):
        print 'Removing skewed columns ...'
        n_tests = len(self._data_set_) - 1
        skew_limit = self._skew_limit_ * n_tests
        col = 2
        while col < (len(self._data_set_[0]) - 1):
            truths = 0
            for row in range(n_tests-1):
                truths += (1 if self._data_set_[row+1][col] else 0)
            if truths <= skew_limit or truths >= (n_tests - skew_limit):
                print 'Removing column for predicate: {}; {} Truths out of {}.'.\
                        format(self._data_set_[0][col], truths, n_tests)
                for row in self._data_set_:
                    row.pop(col)
            else:
                col += 1


    def _preprocess_truth_matrix_(self, truth_matrix):
        self._data_set_ = truth_matrix
        #self._remove_skewed_rows_()
        #self._remove_skewed_cols_()
        #self._shuffle_data_set_rows_()


    def _write_to_data_file_(self):
        print 'Writing to tab separated data file ...'
        fh = open(self._tab_separated_data_file_, 'w')
        tabbed_line = ''
        
        for col in range(len(self._data_set_[0])-2):
            tabbed_line += (self._data_set_[0][col+2] + '\t') 
        fh.write(tabbed_line.strip() + '\n')
        if len(self._data_set_) > 1:
            for row in range(len(self._data_set_)-1):
                row += 1
                tabbed_line = ''
                for col in range(len(self._data_set_[row])-2):
                    tabbed_line += (('1' if self._data_set_[row][col+2] else '0') + '\t')
                fh.write(tabbed_line.strip() + '\n')





        #print 'Writing to tab separated data file ...'
        #fh = csv.writer(open(self._comma_separated_data_file_, 'wb'), delimiter = ',', quoting=csv.QUOTE_MINIMAL)
        #tabbed_line = ''
        #for col in range(len(self._data_set_[0])):
        #    tabbed_line += "'" + (self._data_set_[0][col] + "'" + ',')
             
        #fh.writerow([tabbed_line.strip()])
        #if len(self._data_set_) > 1:
        #    for row in range(len(self._data_set_)-1):
        #        row += 1
        #        tabbed_line = ''
        #        for col in range(len(self._data_set_[row])):
        #            print col                    
        #            if col < 2:
        #                print self._data_set_[row][col]
        #                tabbed_line += ("'" +  self._data_set_[row][col] + "'" + ',')
        #            else:                    
        #                tabbed_line += "'" + (('1' if self._data_set_[row][col] else '0') + "'" + ',')
        #        fh.writerow([tabbed_line.strip()])



























