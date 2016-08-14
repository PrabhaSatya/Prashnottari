'''
Created on 16-Jun-2012

@author: Raghavan
'''

import glob
import types

import answer_document
import predicates
import question
import rule_learner


def parse_question_line(line):
    split_line = line.strip().split("):", 2)
    ques = split_line[1].strip()
    prefix = split_line[0].strip().split("(", 2)
    num = prefix[0].strip()
    if num.isdigit():
        return [('Q' + num.zfill(3) + '-' + prefix[1].strip()), ques]
    else:
        return None


def answer_docs(pnemonic, with_answer):
    path_prefix = ('../../TestData/' + pnemonic + '/' + \
                   ('Yes' if with_answer else 'No'))
    answer_files = []
    for answer_file in glob.glob(path_prefix + '/*.txt'):
        answer_files.append(answer_file)
    return answer_files


predicate_truth_matrix = [['Question', 'Document']]
predicate_name_prefix = 'predicate_'

def initialize_truth_matrix():
    all_fns = [a for a in dir(predicates)
                if isinstance(predicates.__dict__.get(a), types.FunctionType)]
    for p in range(len(all_fns)):
        if all_fns[p].startswith(predicate_name_prefix):
            predicate_name = all_fns[p].partition(predicate_name_prefix)[2]
            predicate_truth_matrix[0].append(predicate_name)
    predicate_truth_matrix[0].append('Has Answer')
    print 'No of Predicates:', (len(predicate_truth_matrix[0]) - 3)


initialize_truth_matrix()
n_question_doc_pairs = 0
with open(r'../../TestData/TestQuestions') as testFile:
    for line in testFile:
        pnemonic_question = parse_question_line(line)
        if pnemonic_question is not None:
            current_question = question.Question(pnemonic_question[1])
            for has_ans in [True, False]:
                doc_list = answer_docs(pnemonic_question[0], has_ans)
                if has_ans:
                    with_answer_docs = len(doc_list)
                    n_question_doc_pairs += with_answer_docs
                else:
                    without_answer_docs = len(doc_list)
                    n_question_doc_pairs += without_answer_docs
                for doc_path in doc_list:
                    doc_object = answer_document.AnswerDocument(doc_path)                    
                    current_predicate_truth_list = [pnemonic_question[0], doc_path]
                    for p in range(len(predicate_truth_matrix[0]) - 3):
                        predicate_call = 'predicates.' + predicate_name_prefix + \
                                            predicate_truth_matrix[0][p+2] + \
                                            '(current_question, doc_object)'
                        
                        current_predicate_truth_list.append(eval(predicate_call))
                    current_predicate_truth_list.append(has_ans)
                    predicate_truth_matrix.append(current_predicate_truth_list)
            print '{};\t\tWith Answer Docs: {};\t\tWithout Answer Docs: {}'.\
                    format(pnemonic_question[0], with_answer_docs, without_answer_docs)
        else:
            print '{}: Invalid Question format.'.format(pnemonic_question[0])

print 'Found {} question-document pairs for learning.'.format(n_question_doc_pairs)
print 'Learning ...'
learner = rule_learner.RuleLearner()
learner.learn_from(predicate_truth_matrix)
