from termcolor import colored
from production import forward_chain, backward_chain, populate
from pprint import pprint

# from rules import loonie_rule, earthy_rule, martian_rule, jupiterian_rule, callistian_rule, asteroidian_rule, martian_rule2
# rules = [loonie_rule, earthy_rule, martian_rule,martian_rule2, jupiterian_rule, callistian_rule, asteroidian_rule]

from rules import all_rules
from qa import questions_answers
from questions_generator import  get_questions_per_rule, generate_questions

rules = all_rules

available_facts = ()
res = ()
question_nr = 0
questions = list(questions_answers.keys())

questions_already_asked = set()
rules_for_questions = list(set(rules))
questions_to_ask = set()

INTERACTIVE = True

X = "Tourist"

def answer_fwd_chain(rules, available_facts, verbose=False):
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
    
    if available_facts != res and set(res).difference(set(available_facts))!=set():
        return True, set(res).difference(set(available_facts))
    else:
        for r in res:
            if ' is ' in r:
                return True, r
             
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
    pprint( tuple(r))

    print()
    
    return r


def clear_and_restart():
    """
    This function cleans all the available facts, the results obtained in the "res" tuple and resets 
    the question_nr counter
    """

    global question_nr
    global available_facts
    global res
    global questions_already_asked
    global questions_to_ask
    global rules_for_questions

    question_nr = 0
    available_facts = ()
    res = ()
    
    questions_already_asked = set()
    rules_for_questions = list(set(rules))
    questions_to_ask = set()

    print(colored("---System restarted, all cleared---", "yellow"))
    print()


if __name__=='__main__':

    conditions_questions_mapping, questions_conditions_mapping, question_indexes = generate_questions(rules)

    if INTERACTIVE==True:

        input_val = "*"
        while input_val!='exit()':

            # print(colored("Enter your facts:  (to exit, write 'exit()', for help, write 'help()'", 'blue')) # facts sau questions?
            # print(colored("?" + str(question_nr+1) + ": " + questions[question_nr] 
            #     + " (if don't know, write '-', to exit, write 'exit()', for help, write 'help())", 
            #     "blue"))
            
            ###########################################
            
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
                questions_already_asked.add(question)

            if len(rules_for_questions)==0:
                # print("----- No answer found ---")
                print(colored("*** answer: Can't detect the type of tourist", 'red') )

                clear_and_restart()
                
            #############################################

            
            input_val = input(">> ").lower() 
    
            # print(input_val)

            if input_val=="exit()":
                break
            elif input_val=="help()":
               show_available_commands()

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

            elif input_val=="show_answer()":
                print(colored("---available facts:" + str(available_facts), "yellow"))

                is_found, r = answer_fwd_chain(rules, available_facts)

                print("----------------")
                if is_found:
                    print(colored("*** answer: ", "green"), r)
                else:
                    print(colored("*** answer: Can't detect the type of tourist", 'red') )
                print("----------------")
            

                clear_and_restart()

                print("----------")    
            elif input_val=="tell_me_about()":
                show_answer_bkwd_chain(rules)
                clear_and_restart()
            elif input_val.lower().replace(" ", "")=="-":
                question_nr += 1
            elif '[yes(true) or no(false)]' in question:
                    input_val = input_val.lower().replace(" ", "")

                    if input_val in ["yes", "yes(true)", "true"]:
                        fact = X + " " + question.lower().replace('[yes(true) or no(false)]', '').strip().replace("?", "")
                        print(fact)
                        available_facts += tuple([fact])

                    elif input_val in ["no", "no(false)", "false"]:
                        fact = ''

                # answer = questions_answers[questions[question_nr]]
                
                # if type(answer)==list:
                #     input_val = input_val.lower().replace(" ", "")
                #     if input_val=="yes":
                #         fact = answer[0]
                #     elif input_val=="no":
                #         fact = answer[1]
                #     else:
                #         print(colored("Didn't understand, please repeat [yes or no]", "red"))
                #         continue
                    
                # else:
                #     fact = populate(answer, {"a": input_val})

                # question_nr +=1
    
            else:    
                # TODO:
                qc = questions_conditions_mapping[question]
                fact = populate(qc, {"a": input_val, "x": X})
                print(colored("fact:", "red"), fact)
                available_facts += tuple([fact])

                
            is_found, r = answer_fwd_chain(rules, available_facts)

            if is_found:
                print("----------------")
                print(colored("*** answer: ", "green"), r)
                print("----------------")
                clear_and_restart()

            if question_nr >= len(questions) and not is_found:
                print("----------------")
                print(colored("*** answer: Can't detect the type of tourist", 'red') )
                print("----------------")

                clear_and_restart()

           
            

