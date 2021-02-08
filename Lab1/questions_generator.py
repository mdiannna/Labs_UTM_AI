from rules import all_rules, intermediate_rules
from termcolor import colored
from production import NOT, simplify, match, populate, AND, OR, IF
from pprint import pprint
import collections
rules = all_rules


all_conditions = []
all_conditions_full = []


def extract_conditions_from_rule(rule, verbose=False):
    """
    Extracts all conditions from one rule (for example '(?x) has green skin' is a condition)
    -----------
    parameters:
        rule (production) - the rule to be analyzed
        verbose (boolean) - if True prints more output
    -----------
    returns:
        res (list of str) - the list of conditions from rule (without NOT conditions)
        not_conditions  - the list of "NOT" conditions from rule
    """
   
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

        elif type(item)==OR:
            e = extract_conditions_from_rule(item)
            if verbose:
                print(colored("e:(OR) ", "red"), e)
            res.extend(e[0])
            not_conditions.extend(e[1])
            
        elif type(item)==AND:
            e = extract_conditions_from_rule(item)
            if verbose:
                print(colored("e:(AND) ", "red"), e)
            res.extend(e[0])
            not_conditions.extend(e[1])

        elif type(item)==list:
            if verbose:
                print(colored("listitem:"), "red") 
            print(item)
            res.extend(item)

    return res, not_conditions



def extract_all_conditions(rules, verbose=False):
    """
    Extracts all conditions from rules (for example '(?x) has green skin' is a condition)
    -----------
    parameters:
        rules (list of productions) - the list of all rules
        verbose (boolean) - if True prints more output
    -----------
    returns:
        all_conditions_full (list of str) - the list of all conditions (with possible duplicates)
        all_not_conditions_full (list of str) - the list of all not conditions (with possible duplicates)
        all_conditions (list of str) - the list of all conditions without duplicates
        all_not_conditions (list of str) - the list of all not conditions without duplicates
    """
    all_conditions_full = []
    all_not_conditions_full = []

    for rule in rules:    
        conditions, not_conditions = extract_conditions_from_rule(rule)
        all_conditions_full.extend(conditions)
        all_not_conditions_full.extend(not_conditions)
    

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
    """
    Calculates the "qestion indexes" for all questions - (for how many conditions a question can be asked) and will provide an answer
    -----------
    parameters:
        conditions_questions_mapping (dictionary (str,str))- the mapping condition <-> question
        all_conditions_full (list of str) - the list of all conditions (with possible duplicates)
    -----------
    returns:
        questions_indexes (dictionary (str, int)) - the dictionary containing the question indexes for all questions
    """
    question_indexes = {} # sau putem pastra sorted deodata

    for condition, question in conditions_questions_mapping.items():
        q_index = all_conditions_full.count(condition)
        question_indexes[question] = q_index

    return question_indexes



def get_questions_per_rule(rule, conditions_questions_mapping, verbose=False):
    """
    Finds the set of all the questions needed for a specific rule
    -----------
    parameters:
        rule (production) - the rule to be analyzed
        conditions_questions_mapping (dictionary (str,str))- the mapping condition <-> question
        verbose (boolean) - if True prints more output
    -----------
    returns:
        set_questions (set of str) - the set of all the questions needed for the specified rule
    """
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

    return set_questions


def get_nr_questions_per_rule(rule, conditions_questions_mapping):
    """
    Calculates the number of questions needed to ask for a specific rule
    -----------
    parameters:
        rule (production) - the rule to be analyzed
        conditions_questions_mapping (dictionary (str,str))- the mapping condition <-> question
    -----------
    returns:
        _ (int) - the number of questions needed to be asked for the specified rule
    """
    set_questions = get_questions_per_rule(rule, conditions_questions_mapping)    
    return len(set_questions)


# input rules - list, or rule - 1 rule
def generate_questions(rules, intermediate_answers, verbose=False):
    """
    Function to genereate questions for the specified rules
    -------------
    parameters:
        rules (list of productions) - the list of all rules
        intermediate_answers (list of string) - the list of all possible intermediate answers
        verbose (boolean) - if True prints more output
    -------------
    returns: 
        conditions_questions_mapping (dictionary (str,str))- the mapping condition <-> question
        questions_conditions_mapping  (dictionary (str,str)) - the inverse mapping  question <-> condition
        question_indexes (dictionary (str, int)) - the list of calculated indexes for each question (for how many conditions a question can be asked)
    """

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

    return conditions_questions_mapping, questions_conditions_mapping, question_indexes



def detect_intermediate_answers(intermediate_rules, verbose=False):
    """ 
    Detects the possible intermediate answers, for example '(?x) is an air_breather' 
    --------
    parameters:
        intermediate_rules (list) - the list of intermediate rules
        verbose (boolean) - if True prints more output
    --------
    returns:
        intermediate_answers (list) - the list of all possible intermediate answers
    """
    intermediate_answers = set()

    for rule in intermediate_rules:
        if verbose:
            print(list(rule.consequent())[0])
        intermediate_answers.add(list(rule.consequent())[0])

    return list(intermediate_answers)




# For testing purposes:
if __name__=='__main__':
    intermediate_answers = detect_intermediate_answers(intermediate_rules)

    conditions_questions_mapping, questions_conditions_mapping, question_indexes = generate_questions(rules, intermediate_answers)
    print("conditions_questions mapping: ")
    pprint(conditions_questions_mapping, width=1000)

    print("questions_conditions mapping: ")
    pprint(questions_conditions_mapping, width=1000)

    print(colored("questions indexes:", "yellow"))
    pprint( question_indexes)