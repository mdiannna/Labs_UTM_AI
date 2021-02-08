from termcolor import colored
from production import forward_chain, backward_chain, populate, match, AND, OR, IF, NOT, simplify
from pprint import pprint

# from rules import loonie_rule, earthy_rule, martian_rule, jupiterian_rule, callistian_rule, asteroidian_rule, martian_rule2
# rules = [loonie_rule, earthy_rule, martian_rule,martian_rule2, jupiterian_rule, callistian_rule, asteroidian_rule]

from rules import all_rules, intermediate_rules
from qa import questions_answers
from questions_generator import  get_questions_per_rule, generate_questions, extract_conditions_from_rule

rules = all_rules

available_facts = ()
res = ()
# question_nr = 0
questions = list(questions_answers.keys())

questions_already_asked = set()
rules_for_questions = list(set(rules))
questions_to_ask = set()

INTERACTIVE = True

X = "Tourist"


def simplify_rules(rules):
    """
    Simplifies the AND-OR tree for each rule from rules list
    -------
    parameters:
        rules(list of productions) - the list of rules to be simplified
    """
    new_rules = []
    for rule in rules:
        new_rules.append(simplify(rule))
    return new_rules

rules = simplify_rules(rules)



def matches_intermediate_answer(answer, intermediate_answers):
    """ 
    checks if an aswer matches any intermediate answer
    --------
    parameters:
        answer (str) - an answer to be tested
        intermediate_answers (list of str) - list of the intermediate answers (usually containing (?x))
    --------
    returns:
        _(boolean) - True if answer matches an intermediate answer or False otherwise
    """
    for i_answ in intermediate_answers:
        m = match(i_answ, answer)
        if m!= None:
            return True
    return False
        


def answer_fwd_chain(rules, available_facts, intermediate_answers, verbose=False):
    """
    This function applies forward chain to the available facts and rules, and outputs an
    answer about the type of the tourist, or "no_answer_found"
    --------
    parameters:
        rules (list) - the list of rules
        available_facts(tuple) - contains the facts about the tourist
        verbose(boolean) - outputs more if True (by default, False)
    --------
    returns:
        is_found(bool) - True if an answer was found, False otherwise
    """
    print(colored("---available facts:" + str(available_facts), "yellow"))

    res = forward_chain(rules, available_facts, verbose=verbose)

    if verbose==True:
        print("----   res for debug: ", res)
    
    possible_answers = set(res).difference(set(available_facts))
    
    answers = set()

    if available_facts != res and possible_answers!=set():
        for answ in possible_answers:
            if not matches_intermediate_answer(answ, intermediate_answers):
                answers.add(answ)
    else:
        for r in res:
            if ' is ' in r and (not matches_intermediate_answer(r, intermediate_answers)):
                answers.add(r)

    if len(answers)>0:
        return True, answers    

    return False, "no_answer_found"


def clear_facts_or_no(available_facts):
    """ 
    This function asks the user if to clear facts, and then, 
    depending on the answer of the user, clears or not the facts
    --------
    parameters:
        available_facts(tuple) - contains the facts about the tourist
    --------
    returns:
        available_facts(tuple) - the cleared (empty) tuple of facts
    """
    print(colored("    !? To clear facts? [Yes or No]", 'blue') )
    input_y_n = input("   [Yes or No] >> ") 
    if input_y_n == 'Yes':
        available_facts = ()
    elif input_y_n=='No':
        print(colored("   -- Ok, facts not cleared ---", "blue"))
    else:
        print(colored("   -- Didn't understand you, assumed no, facts not cleared ---", "blue"))

    return available_facts
        

def show_available_commands():
    """
    This function prints all the available commands in the console
    """

    print(colored("-----------Commands:---------", "yellow"))
    print(colored("help()                -  shows help", "yellow"))
    print(colored("clear_and_restart()   -  clears the facts and restarts the system", "yellow"))
    print(colored("exit()                -  exit the program", "yellow"))
    print(colored("show_facts()          -  prints the existing available facts", "yellow"))
    print(colored("show_answer()         -  prints the answer based on the  existing available facts", "yellow"))
    print(colored("tell_me_about()       -  will show facts about a type of tourist using backward chaining", "yellow"))

    print(colored("", "yellow"))


def print_green(s):
    """
    Shortcut function to print some string in green color
    -------
    parameters:
        s(str) - the string to be printed
    """
    print(colored(s, "green"))


def print_red(s):
    """
    Shortcut function to print some string in red color
    -------
    parameters:
        s(str) - the string to be printed
    """
    print(colored(s, "red"))



def print_bkwd_chain_result_human_readable(rule, verbose=False):
    """
    Important note: The result will always be an "OR" production, because it will show all the possible rules, and the tree simplified
    """
    print_green("===== One of the following options are true for the " + str(X) + " ======== :")
    res = []
    not_conditions = []

    if type(rule)==IF:
        ante = rule.antecedent()
        print_green("IF ")
    else:
        ante = rule
        
    if verbose:
        print("ante:", ante)

    if type(ante)==str:
        # print_green(ante)
        return [ante], not_conditions

    for item in ante:
        if type(item)==str:
            print_green(" * " + item)
            res.append(item)

        elif type(item)==NOT:
            item_condition = str(item)[5:-2]
            print_green("NOT (" + item_condition + ")")

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
            
            print_green(" * " + " OR ".join(e[0]))
            not_conditions.extend(e[1])
            
        elif type(item)==AND:
            e = extract_conditions_from_rule(item)
            if verbose:
                print(colored("e:(AND) ", "red"), e)
            res.extend(e[0])
            not_conditions.extend(e[1])
            print_green(" * " + " AND ".join(e[0]))

        elif type(item)==list:
            if verbose:
                print(colored("listitem:"), "red") 
            print(item)
            res.extend(item)

    return res, not_conditions

def show_answer_bkwd_chain(rules):
    """
    The function that applies backward chain to a hypothesis, but first reads the type of tourist from input 
    and then converts the type of tourist to a hypothesis and outputs all the rules about the tourist, like an encyclopedia
    --------
    parameters:
        rules (list) - the list of rules
    returns:
        r (production.OR) - the results, the rules for the given type of tourist
    """
    # print(colored("  Write your hypothesis please:", "blue"))
    print(colored("  Write the type of tourist please:", "blue"))

    input_h = input("   >> ") 
    input_h = input_h.capitalize()
    
    
    hypothesis = "Tourist is a " + input_h

    print(colored("input: " + str( input_h) + "   -- hypothesis: " + hypothesis, "yellow"))

    r = backward_chain(rules, hypothesis)

    
    # Try the variant with 'an'
    if r == "no answer matches your hypothesis, sorry":
        hypothesis = "Tourist is an " + input_h    
        r = backward_chain(rules, hypothesis)
    
    if r == "no answer matches your hypothesis, sorry":
        print(colored(" ---- I found out that: ", "green"))
        r = "no informations about this type of tourist, maybe there is a mistake?"
        print(colored(r, "red"))
        return r
    
    print(colored(" ---- I found out that: ", "green"))
    print("OR:")
    # pprint( tuple(r))
    # pprint(list(r), width=1)
    for item in r:
        pprint(item)

    print_green("---------- Human readable: ----------")
    print_bkwd_chain_result_human_readable(r)
    print_green("------------")


    print()
    
    return r


def clear_and_restart():
    """
    This function cleans all the available facts, the results obtained in the "res" tuple and resets all the needed variables
    """

    global available_facts
    global res
    global questions_already_asked
    global questions_to_ask
    global rules_for_questions

    available_facts = ()
    res = ()
    questions_already_asked = set()
    rules_for_questions = list(set(rules))
    questions_to_ask = set()

    print(colored("---System restarted, all cleared---", "yellow"))
    print()


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


def print_answer(answer, type="success"):
    """ 
    pretty print the answer
    ---------
    parameters:
        answer (str) - the answer to print
        type (str) - can be either "success" or "error", that will change the output style
        ---------
    """
    if type=="success":
        print(colored("=========================================", "green"))
        print(colored("*** answer: " + str(answer), "green"))
        print(colored("=========================================", "green"))
    else:
        print(colored("=========================================", "red"))
        print(colored("*** " + str(answer), 'red') )
        print(colored("=========================================", "red"))


    


if __name__=='__main__':

    intermediate_answers = detect_intermediate_answers(intermediate_rules)
    conditions_questions_mapping, questions_conditions_mapping, question_indexes = generate_questions(rules, intermediate_answers)


    if INTERACTIVE==True:

        input_val = "*"
        while input_val!='exit()':

            # print(colored("Enter your facts:  (to exit, write 'exit()', for help, write 'help()'", 'blue')) # facts sau questions?
            # print(colored("?" + str(question_nr+1) + ": " + questions[question_nr] 
            #     + " (if don't know, write '-', to exit, write 'exit()', for help, write 'help())", 
            #     "blue"))
            
            ###########################################
            
            if len(rules_for_questions)==0:
                print_answer("No answer found", type="error")

                clear_and_restart()

            while(len(questions_to_ask)==0) and len(rules_for_questions)>0:
                min_nr_rules = 0
                rule_idx = 0
                for idx, rule in enumerate(rules_for_questions):
                    set_questions = get_questions_per_rule(rule, conditions_questions_mapping)
                    nr_questions = len(set_questions)

                    if min_nr_rules==0:
                        min_nr_rules = nr_questions
                    elif min_nr_rules > nr_questions:
                        min_nr_rules = nr_questions
                        rule_idx = idx
                
                set_questions = get_questions_per_rule(rules_for_questions[rule_idx], conditions_questions_mapping)

                # print(colored("-----rule idx with min nr questions:", "red"), rule_idx)
                # print(colored("-----rule :", "red"), rules_for_questions[rule_idx])
                # print(colored("set of questions:", "red"), set_questions)
                questions_to_ask = set_questions.difference(questions_already_asked)

                rules_for_questions.remove(rules_for_questions[rule_idx])

            if len(questions_to_ask)>0:
                question = questions_to_ask.pop()
                print(colored("Q:" + question  + " \n(if don't know, write '-', to exit, write 'exit()', for help, write 'help())", "blue"))

          
                
            #############################################

            
            input_val = input(">> ").lower() 
    
            # print(input_val)

            if input_val=="exit()":
                break
            elif input_val=="help()":
               show_available_commands()
               questions_to_ask.add(question)

            elif input_val=='clear_and_restart()':
                clear_and_restart()
                if available_facts==():
                    print(colored("---facts cleared, system restarted---", 'green'))
                else:
                    print(colored("---ERROR: error clearing facts---", "red"))
                print()

            elif input_val=='show_facts()':
                print(colored("---available facts:" + str(available_facts), "yellow"))
                print()
                questions_to_ask.add(question)

            elif input_val=="show_answer()":

                is_found, r = answer_fwd_chain(rules, available_facts, intermediate_answers)

                print("----------------")
                if is_found:
                    print_answer(r, "success")
                else:
                    print_answer("No answer found", "error")
            
                clear_and_restart()

                print("----------")    
            elif input_val=="tell_me_about()":
                show_answer_bkwd_chain(rules)
                clear_and_restart()
                questions_to_ask.add(question)

            elif input_val.lower().replace(" ", "")=="-":
                questions_already_asked.add(question)
                continue

            elif '[yes(true) or no(false)]' in question:
                    input_val = input_val.lower().replace(" ", "")

                    if input_val in ["yes", "yes(true)", "true"]:
                        fact = X + " " + question.lower().replace('[yes(true) or no(false)]', '').strip().replace("?", "")
                        print(fact)
                        print(colored("---added fact:" + fact, "cyan"), )
                        available_facts += tuple([fact])

                    elif input_val in ["no", "no(false)", "false"]:
                        fact = ''
                    else:
                        print(colored("Sorry, didn't understand you, not saved", "red"))
                        questions_to_ask.add(question)
    
            else:    
                qc = questions_conditions_mapping[question]
                fact = populate(qc, {"a": input_val, "x": X})
                print(colored("---added fact:" + fact, "cyan"), )
                available_facts += tuple([fact])

            questions_already_asked.add(question)

                
            is_found, r = answer_fwd_chain(rules, available_facts, intermediate_answers)

            if is_found:
                print_answer(r, "success")

                clear_and_restart()          
                

