from rules import all_rules
from termcolor import colored
from production import NOT, simplify, match, populate
from pprint import pprint
import collections
# from array import *

# alternative:
# from fuzzy_match import match
# https://pypi.org/project/fuzzy-match/

# https://pypi.org/project/fuzzywuzzy/
from fuzzywuzzy import fuzz, process


# TODO:
def extract_conditions_from_rule(rule):
    # print(rule)
    # print()
    ante = rule.antecedent()
    # print("ante:", ante)
    # print(type(ante))
    # print(list(ante))
    res = []
    not_conditions = []
    if type(ante)==str:
        return [ante], not_conditions

    for item in ante:
        if type(item)==str:
        # try:
            # item.antecedent()
        # except:
            res.append(item)
        elif type(item)==NOT:
            print("--", type(item))
           
            print("str:", str(item))
            # print(item.replace('NOT(', ''))
            # print(item[3::-1])


            item_condition = str(item)[5:-2]
            print("item_cond:", item_condition)
            print("type:", type(item_condition))
            not_conditions.append(item_condition)
            item_transformed_not = item_condition.replace('(?x)', '(?x) does not')
            print("transf not:", item_transformed_not)
            res.append(item_transformed_not)

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
    all_conditions = []
    all_not_conditions = []

    for rule in rules:
        print(colored("rule:" + str(rule), "yellow"))
        conditions, not_conditions = extract_conditions_from_rule(rule)
        all_conditions.extend(conditions)
        all_not_conditions.extend(not_conditions)
        # print()
        # print("ante:", rule.antecedent())
        # print("conseq:", rule.consequent())
        
        print()
    print("all_contitions")
    # Removing duplicates
    all_conditions = list(set(all_conditions))
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

# +TOLOWER + replace numbers with words?? 

all_conditions = ['(?x) has 2 arms',
 '(?x) speaks english language',
 '(?x) has gray skin',
 '(?x) walks fast',
 '(?x) wears sunglasses',
 '(?x) speaks jupiterian language',
 '(?x) speaks loonian language',
 '(?x) has yellow skin',
 '(?x) wears shiny clothes',
 '(?x) wears a mask',
 '(?x) walks slow',
 '(?x) speaks high pitched sounds',
 '(?x) has orange skin',
 '(?x) speaks martian language',
 '(?x) communicates with high pitched sounds',
 '(?x) wears yellow clothes',
 '(?x) is slim',
 '(?x) has gray hair',
 '(?x) has pink skin',
 '(?x) has white skin',
 '(?x) weights very much',
 '(?x) does not wear a mask',
 '(?x) has brown skin',
 '(?x) has orange hair',
 '(?x) has 2 legs',
 '(?x) has green skin',
 '(?x) does not wears a spacesuit',
 '(?x) wears a spacesuit',
 '(?x) has red hair']

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
for cond in all_conditions_repl:
    cond_split = cond.split()
    m = match("has (?x) (?y)", cond)
    if m!=None:
        print(cond)
        print(m)
        y = m["y"]
        x = m["x"]
        has_triplet_conds.append(cond)
        
        try:
            int(x)
            question = "How many " + y + "? (write a number)"
        except:
            question = "Choose a category for " + str(y) + " from list: [" + str(x) + "]"
        print(colored(question, "blue"))
        print()
    
    # if cond_split[0]=='has' and len(cond_split)==3:
    #     print(cond)
    #     has_triplet_conds.append(cond)
    #     # m = match(cond,"has (?x) (?y)")
    #     m = match("has (?x) (?y)", cond)

    #     # re.match( AIStringToRegex(template), 
    #                     #  AIStr ).groupdict()
    #     print(m)
    #     if m!=None:


print("constructions has x y:")
print(has_triplet_conds)