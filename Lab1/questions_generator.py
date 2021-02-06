from rules import all_rules
from termcolor import colored
from production import NOT, simplify, match, populate, AND, OR, IF
from pprint import pprint
import collections
# from array import *

# alternative:
# from fuzzy_match import match
# https://pypi.org/project/fuzzy-match/

# https://pypi.org/project/fuzzywuzzy/
from fuzzywuzzy import fuzz, process


all_conditions = []
all_conditions_full = []


# TODO:
def extract_conditions_from_rule(rule, verbose=False):
    # print(rule)
    # print()
    # print("ante:", ante)
    # print(type(ante))
    # print(list(ante))
    res = []
    not_conditions = []

    if type(rule)==IF:
        ante = rule.antecedent()
    else:
        ante = rule

    if verbose:
        print("ante:", ante)

    if type(ante)==str:
        return [ante], not_conditions

    for item in ante:
        if type(item)==str:
            res.append(item)

        elif type(item)==NOT:
            item_condition = str(item)[5:-2]
           
                
            not_conditions.append(item_condition)
            item_transformed_not = item_condition.replace('(?x)', '(?x) does not')
            
            if verbose:
                print("--", type(item))
                print("str:", str(item))
                print("item_cond:", item_condition)
                print("type:", type(item_condition))
                print("transf not:", item_transformed_not)

            # res.append(item_transformed_not)
        #  !! atentie la recursie!!
        elif type(item)==OR:
            print("lst:", list(item))
            e = extract_conditions_from_rule(item)
            print(colored("e:(OR) ", "red"), e)
            res.extend(e[0])
            not_conditions.extend(e[1])
            
        elif type(item)==AND:
            e = extract_conditions_from_rule(item)
            print(colored("e:(OR) ", "red"), e)
            res.extend(e[0])
            not_conditions.extend(e[1])

        elif type(item)==list:
            if verbose:
                print(colored("listitem:"), "red") 
            print(item)
            res.extend(item)

    # return list(ante)
    return res, not_conditions

def filter_similarity_results(res):
    DELTA = 90
    res_filtered = [item for item in res if item[1]>DELTA]
    
    return res_filtered

def combine_list_into_str(lst):
    s = ""
    lst2 = [str(i) for i in lst]
    return s.join(lst2)


# input rules - list, or rule - 1 rule
def generate_questions(rules):
    global all_conditions
    global all_conditions_full

    all_conditions_list = []
    all_not_conditions = []

    for rule in rules:
        print(colored("rule:" + str(rule), "yellow"))
        conditions, not_conditions = extract_conditions_from_rule(rule)
        all_conditions_full.extend(conditions)
        all_not_conditions.extend(not_conditions)
        # print()
        # print("ante:", rule.antecedent())
        # print("conseq:", rule.consequent())
        
        print()
    print(colored("all_contitions full:", "red"))
    pprint( all_conditions_full)

    # Removing duplicates
    
    all_conditions = list(set(all_conditions_full))
    print("all_contitions")
    pprint( all_conditions)
    print()
    print("all_not_contitions")
    all_not_conditions = list(set(all_not_conditions))
    pprint( all_not_conditions)

    print(type(all_conditions[0]))

    all_similar_groups = set()
    for condition in all_conditions:
        similar_r = process.extract(condition, all_conditions)
        similar_r2 = filter_similarity_results(similar_r)
        # print(similar_r2)
        lst_similar_r2 = combine_list_into_str(similar_r2)
        all_similar_groups.add(lst_similar_r2)
    
    print("all similar groups:")
    for i in  all_similar_groups:
        print(i)

    


    # res_similarity = []
    # for condition1 in all_conditions:
    #     for condition2 in all_conditions:
    #         r = fuzz.token_sort_ratio(condition1, condition2)
    #         res_similarity


    

    # TODO: generate questions based on rules
    # Examples for generated questions:
    # Skin color? - daca detecteaza color from colors_list.txt
    # Provide suitable category for [color]
    # Or Yes/no
    # Or range questions (nr)

    #the rest that remain, ask :
    # The tourist wears a mask? [yes or no]   '(?x) wears a mask', - just replace (?x) with 'the tourist' and add question mark + [yes or no]


from rules import all_rules

rules = all_rules
if __name__=='__main__':
    ## q = QuestionsGenerator()
    generate_questions(rules)
    # print("conditions:", conditions)
    print()

all_conditions = [i.lower().strip() for i in all_conditions]
all_conditions_repl = [i.replace("(?x)", "").strip() for i in all_conditions]


print(all_conditions_repl)


# https://stackoverflow.com/questions/15238276/counting-the-repeating-of-words-in-a-list-python
from collections import Counter
import re

def count_repeating(lst_strings, nr_letters_min=3):
    # take words containing 3 or more letters
    reg = re.compile('\S{' + str(nr_letters_min) + ',}')


    c = dict(Counter(ma.group() for s in lst_strings for ma in reg.finditer(s) ))
    return c

c = count_repeating(all_conditions_repl)
print(c)


import nltk

def is_noun(word):
    if nltk.pos_tag([word])[0][1]=='NN':
        print(nltk.pos_tag([word])[0][1])

        return True

# is_noun = lambda pos: pos[:2] == 'NN'


for word in c.keys():
    # print(is_noun(word))
    if is_noun(word):
        print(word)



# from textblob import TextBlob
# # https://textblob.readthedocs.io/en/dev/quickstart.html#noun-phrase-extraction
# # https://stackoverflow.com/questions/33587667/extracting-all-nouns-from-a-text-file-using-nltk

# condition1 = all_conditions_repl[0]
# print("condition1:", condition1)
# blob = TextBlob(condition1)
# print(blob.noun_phrases)


# import nltk
# lines = 'lines is some string of words'
# # function to test if something is a noun
# is_noun = lambda pos: pos[:2] == 'NN'
# # do the nlp stuff
# tokenized = nltk.word_tokenize(condition1)
# nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
# print("nouns:", nouns)

from nltk import word_tokenize
# Some common structures:
#combinations: orange skin - Adj + noun
# wears yellow clothes, wears green ...     verb + adj + noun
# speaks english, speaks martian, etc verb + noun
# walks fast, walks slow: verb + adverb

#presupunem ca avem lista de culori


# + something cu verbul has

txt = "has orange skin"
txt = "speaks english language"

text = word_tokenize(txt)
print(nltk.pos_tag(text))


print("analyse has phrases")
has_conditions = []
for cond in all_conditions_repl:
    if 'has' in cond:
        print(cond)
        has_conditions.append(cond)

cr = count_repeating(has_conditions)
print(cr)

import operator
# https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-1.php
sorted_d = dict( sorted(cr.items(), key=operator.itemgetter(1),reverse=True))

print(sorted_d)



##### Working!!! ############
# TODO: group all the y into one question
# Se poate pentru constructiile "has x y" de pus Choose the y of tourist from list: [x1, x2, x3]
has_triplet_conds = []
all_y_options = {}
conditions_questions_mapping = {}
question_indexes = {}


# for cond in all_conditions_repl:
for cond in all_conditions:
    initial_condition = cond
    cond = cond.replace("(?x)", "").strip()
    cond_split = cond.split()
    m = match("has (?x) (?y)", cond)
    if m!=None:
        print(cond)
        print(m)
        y = m["y"]
        x = m["x"]
        
        has_triplet_conds.append((initial_condition, x, y))
        try:
            int(x)
        #     question = "How many " + y + "? (write a number)"
        #     print(colored(question, "blue"))
        #     conditions_questions_mapping[cond] = question

        #     # TODO: process these type of questions
        except:
            conditions_questions_mapping[initial_condition] = "?"
            if not y in all_y_options:
                all_y_options[y] = set()
            all_y_options[y].add(x)
    else:
        question = cond.capitalize() + "? [yes(true) or no(false)]"
        print(colored(question.capitalize(), "blue"))
        # TODO: process these type of questions & answers + de scos acele cu not
        conditions_questions_mapping[initial_condition] = question


  
for y, x in all_y_options.items():
    question = "Choose a category for " + str(y) + " from list: " + str(list(all_y_options[y])) + ""
    print(colored(question, "blue"))
    print()

for cond,x,y in has_triplet_conds:
    try:
        int(x)
        question = "How many " + y + "? (write a number)"
    except:
        question = "Choose a category for " + str(y) + " from list: " + str(list(all_y_options[y])) + ""

    conditions_questions_mapping[cond] = question

    print(colored(question, "blue"))
    print()

print("constructions has x y:")
print(has_triplet_conds)


print("mapping: ")
pprint(conditions_questions_mapping, width=1000)


def calculate_question_indexes(conditions_questions_mapping, all_conditions_full):
    question_indexes = {} # sau putem pastra sorted deodata

    for condition, question in conditions_questions_mapping.items():
        q_index = all_conditions_full.count(condition)
        question_indexes[question] = q_index

    return question_indexes

question_indexes = calculate_question_indexes(conditions_questions_mapping, all_conditions_full)
print(colored("questions indexes:", "yellow"))
pprint( question_indexes)
print(colored("questions indexes sorted:", "yellow"))
# sorted_d = dict( sorted(question_indexes.items(), key=operator.itemgetter(1),reverse=True))
# pprint(sorted(question_indexes))
# pprint(sorted_d)

sorted_questions_decreasing = sorted(question_indexes.items(), key=lambda x: x[1], reverse=True)

for i in sorted_questions_decreasing:
	print(i[0], i[1])

sorted_questions = [q[0] for q in sorted_questions_decreasing] 
print(colored("Final list of sorted questions:", "green"))
pprint(sorted_questions, width=1000)    

def get_nr_questions_per_rule(rule):
    conditions, not_conditions = extract_conditions_from_rule(rule)
    set_questions = set()
    for c in conditions:
        set_questions.add(conditions_questions_mapping[c])

    for c in not_conditions:
        set_questions.add(conditions_questions_mapping[c])
    print(colored("set of questions required:" + str( set_questions), "yellow"))
    # return len(conditions) + len(not_conditions)
    return len(set_questions)


for rule in rules:
    nr_quest = get_nr_questions_per_rule(rule)
    print("rule:", rule)
    print("nr of questions required:", nr_quest)
    print()


#TODO: alta conditie, x y z - verb adj subst, unde se repeta x si z
# alta conditie, y x, unde y e verb - walks slow, walks fast, cu conditia ca se repeta y


#TODO: need a mapping - rule, questions
# ca atare ar trebui la fiecare pas sa analizam care atribute ne-ar da entropia cea mai mare, daca am avea un set de date
# Algorithm:
# At each iteration, choose a rule/question in the following way:
# 1. choose the rules that are in the list (mapping), "then ", "A: is a Martian" consequent
# 2. see if there is any intermediate rule that has "A: is a Martian" consequent
# 3. if 2 yes, then choose the intermediate rule with the minimum nr of rules (& questions)
# modified #4 and #5: choose a question from list with better index (already sorted)

#old #4 and #5:
# 4. choose an intermediate rule, if exists, with minimum nr of questions required(random)
# 5. choose a rule with minimum nr of questions required (random)


# sau question care poate sa acopere mai multe rules
# question_index


#Alg2: 
# Atentie cat dureaza acest lucru! sa nu dureze prea mult! - Complexitate - nr*nq + intersectia
# la fiecare pas, nr of questions required minus card(intersectia quest_required cu questions_asked) pentru fiecare regula

# sau
# Alg3: (va fi mai rapid de calculat, dar posibil nu cel mai optimal dupa nr de intrebari) Complexitate: 1 daca e sortat, n daca nu
# la fiecare pas, intreaba intrebarea cu question_index cel mai mare 


# New alg:
# At each iteration, choose a rule/question in the following way:
# 1. choose the rules that are in the list (mapping), "then ", "A: is a Martian" consequent ("direct rule, not intermediate")
# 2.1 la fiecare pas, nr of questions required minus card(intersectia quest_required cu questions_asked) pentru fiecare regula
# 2.2  choose a question from list with better index (already sorted)
# 2.1 sau 2.2