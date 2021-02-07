from rules import all_rules
from termcolor import colored
from production import NOT, simplify, match, populate, AND, OR, IF
from pprint import pprint
import collections

all_conditions = []
all_conditions_full = []


# TODO: finish the program

def extract_conditions_from_rule(rule, verbose=False):
   
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
            e = extract_conditions_from_rule(item)
            if verbose:
                print(colored("e:(OR) ", "red"), e)
            res.extend(e[0])
            not_conditions.extend(e[1])
            
        elif type(item)==AND:
            e = extract_conditions_from_rule(item)
            if verbose:
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



def extract_all_conditions(rules, verbose=False):
    all_conditions_full = []
    all_not_conditions_full = []

    for rule in rules:    
        conditions, not_conditions = extract_conditions_from_rule(rule)
        all_conditions_full.extend(conditions)
        all_not_conditions_full.extend(not_conditions)
        # print()
        # print("ante:", rule.antecedent())
        # print("conseq:", rule.consequent())        
        # print()
    

    # Removing duplicates
    all_conditions = list(set(all_conditions_full))
    all_not_conditions = list(set(all_not_conditions_full))

    if verbose:
        print("all_contitions")
        pprint( all_conditions)
        print()
        print("all_not_contitions")
        pprint( all_not_conditions)
        print(colored("all_contitions full:", "red"))
        pprint( all_conditions_full)


    return all_conditions_full, all_not_conditions_full, all_conditions, all_not_conditions


def calculate_question_indexes(conditions_questions_mapping, all_conditions_full):
    question_indexes = {} # sau putem pastra sorted deodata

    for condition, question in conditions_questions_mapping.items():
        q_index = all_conditions_full.count(condition)
        question_indexes[question] = q_index

    return question_indexes



def get_questions_per_rule(rule, conditions_questions_mapping, verbose=False):
    conditions, not_conditions = extract_conditions_from_rule(rule)
    set_questions = set()
    for c in conditions:
        if c in conditions_questions_mapping:
            set_questions.add(conditions_questions_mapping[c])
        else:    
            return set()
             

    for c in not_conditions:
        if c in conditions_questions_mapping:
            set_questions.add(conditions_questions_mapping[c])
        else:
            return set()

        
    if verbose:
        print(colored("set of questions required:" + str( set_questions), "yellow"))
    # return len(conditions) + len(not_conditions)
    return set_questions


def get_nr_questions_per_rule(rule, conditions_questions_mapping):
    set_questions = get_questions_per_rule(rule, conditions_questions_mapping)    
    return len(set_questions)


# input rules - list, or rule - 1 rule
def generate_questions(rules, intermediate_answers, verbose=False):
    global all_conditions
    global all_conditions_full
    has_triplet_conds = []
    all_y_options = {}
    conditions_questions_mapping = {}
    questions_conditions_mapping = {}
    question_indexes = {}

    all_conditions_full, all_not_conditions_full, all_conditions, all_not_conditions = extract_all_conditions(rules)
    all_conditions = [i.lower().strip() for i in all_conditions]


    for cond in all_conditions:
        if cond not in intermediate_answers:
            initial_condition = cond
            cond = cond.replace("(?x)", "").strip()
            cond_split = cond.split()
            m = match("has (?x) (?y)", cond)
            if m!=None:
                y = m["y"]
                x = m["x"]
                
                has_triplet_conds.append((initial_condition, x, y))
                try:
                    int(x)
                except:
                    conditions_questions_mapping[initial_condition] = "?"
                    if not y in all_y_options:
                        all_y_options[y] = set()
                    all_y_options[y].add(x)
            else:
                question = cond.capitalize() + "? [yes(true) or no(false)]"
                # print(colored(question.capitalize(), "blue"))
                conditions_questions_mapping[initial_condition] = question


    for cond,x,y in has_triplet_conds:
        try:
            int(x)
            question = "How many " + y + "? (write a number)"
        except:
            question = "Choose a category for " + str(y) + " from list: " + str(list(all_y_options[y])) + ""

        conditions_questions_mapping[cond] = question
        questions_conditions_mapping[question] = '(?x) has (?a) ' + y

        if verbose:
            print(colored(question, "blue"))
            print()

    question_indexes = calculate_question_indexes(conditions_questions_mapping, all_conditions_full)

    if verbose:
        print("constructions has x y:")
        print(has_triplet_conds)

        print("mapping: ")
        pprint(conditions_questions_mapping, width=1000)

        print(colored("questions indexes:", "yellow"))
        pprint( question_indexes)

    # # Add inverse dictionary - questions_conditions_mapping
    # questions_conditions_mapping = {v: k for k, v in my_map.items()}

    return conditions_questions_mapping, questions_conditions_mapping, question_indexes




from rules import all_rules

rules = all_rules

if __name__=='__main__':
    ## q = QuestionsGenerator()
    conditions_questions_mapping, questions_conditions_mapping, question_indexes = generate_questions(rules)

    # print("conditions:", conditions)
    print()



# all_conditions_repl = [i.replace("(?x)", "").strip() for i in all_conditions]
# print(all_conditions_repl)



#TODO: integrate later, if we need this sort
# print(colored("questions indexes sorted:", "yellow"))
# sorted_questions_decreasing = sorted(question_indexes.items(), key=lambda x: x[1], reverse=True)

# for i in sorted_questions_decreasing:
# 	print(i[0], i[1])

# sorted_questions = [q[0] for q in sorted_questions_decreasing] 
# print(colored("Final list of sorted questions:", "green"))
# pprint(sorted_questions, width=1000)    


# for rule in rules:
#     nr_quest = get_nr_questions_per_rule(rule, conditions_questions_mapping)
#     print("rule:", rule)
#     print("nr of questions required:", nr_quest)
#     print()



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

# TODO: if we can distinguish rules, otherwise change step in the algorithm
# def find_direct_rules(rules, verbose=False):
#     for rule in rules:
#         if rule.antecedent()
#         if 'is a' 

# New alg2:
# Init: add a questions_to_be_asked list (as Q)
# 
# while answer not found:
#   if exists, choose the rules that are in the list (mapping), "then ", "A: is a Martian" consequent ("direct rule, not intermediate") (care require 1 question de fapt)
#   if Q is empty:
#      se ia regula care necesita cele mai putine intrebari -  nr of quest required minus card(intersectia quest_required cu questions_asked) min pt fiecare regula
#   else:
#      din Q se ia question with better index
#