from termcolor import colored
from production import forward_chain, backward_chain, populate
from pprint import pprint

# from rules import loonie_rule, earthy_rule, martian_rule, jupiterian_rule, callistian_rule, asteroidian_rule, martian_rule2
from rules import all_rules
from qa import questions_answers

# rules = [loonie_rule, earthy_rule, martian_rule,martian_rule2, jupiterian_rule, callistian_rule, asteroidian_rule]
rules = all_rules

available_facts = ()
res = ()
question_nr = 0
questions = list(questions_answers.keys())

INTERACTIVE = True



def answer_fwd_chain(rules, available_facts, verbose=False):
    res = forward_chain(rules, available_facts, verbose=verbose)
    # print("----   res for debug: ", res)
    
    if available_facts != res and set(res).difference(set(available_facts))!=set():
        # print(colored("*** answer: ", "green"), set(res).difference(set(available_facts)) )
        return True, set(res).difference(set(available_facts))
        # found = True
    else:
        # found = False
        for r in res:
            if ' is ' in r:
                return True, r
                # print(colored("*** answer: ", "green"),r )
                # found = True
                
        # if not found:                    
            # print(colored("*** answer: Can't detect the type of tourist", 'magenta') )

    return False, "no_answer_found"

def clear_facts_or_no(available_facts):
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
    print(colored("-----------Commands:---------", "yellow"))
    print(colored("help()         -  shows help", "yellow"))
    print(colored("clear_and_restart()        -  clears the facts and restarts the system", "yellow"))
    print(colored("exit()         -  exit the program", "yellow"))
    print(colored("show_facts()   - prints the existing available facts", "yellow"))
    print(colored("show_answer()   - prints the answer based on the  existing available facts", "yellow"))
    print(colored("tell_me_about() - will show facts about hypothesis using backward chaining", "yellow"))

    print(colored("", "yellow"))

def show_answer_bkwd_chain(rules):
    # print(colored("  Write your hypothesis please:", "blue"))
    print(colored("  Write the type of tourist please:", "blue"))

    input_h = input("   >> ") 
    input_h = input_h.capitalize()
    print(colored("input: " + str( input_h), "yellow"))
    
    
    hypothesis = "Tourist is a " + input_h
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
    #else
    # print(colored(" ---- I found out that: " + str(r), "green"))
    
    print(colored(" ---- I found out that: ", "green"))
    print("OR:")
    pprint( tuple(r))

    print()
    
    return r

def clear_and_restart():
    global question_nr
    global available_facts
    global res

    question_nr = 0
    available_facts = ()
    res = ()
    print(colored("---System restarted, all cleared---", "yellow"))
    print()


if __name__=='__main__':

    if INTERACTIVE==True:

        input_val = "*"
        while input_val!='exit()':

            # print(colored("Enter your facts:  (to exit, write 'exit()', for help, write 'help()'", 'blue')) # facts sau questions?
            print(colored("?" + str(question_nr+1) + ": " + questions[question_nr] 
                + " (if don't know, write '-', to exit, write 'exit()', for help, write 'help())", 
                "blue"))
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

                res = show_answer_fwd_chain(rules, available_facts)
                clear_and_restart()

                # available_facts = clear_facts_or_no(available_facts)

                print("----------")    
            elif input_val=="tell_me_about()":
                show_answer_bkwd_chain(rules)
                clear_and_restart()
            elif input_val.lower().replace(" ", "")=="-":
                question_nr += 1
            else:
                answer = questions_answers[questions[question_nr]]
                
                if type(answer)==list:
                    input_val = input_val.lower().replace(" ", "")
                    if input_val=="yes":
                        fact = answer[0]
                    elif input_val=="no":
                        fact = answer[1]
                    else:
                        print(colored("Didn't understand, please repeat [yes or no]", "red"))
                        continue
                    
                else:
                    fact = populate(answer, {"a": input_val})

                question_nr +=1

                # print(input_val)
                # available_facts += tuple([input_val])

                print(fact)
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

            # print("---- question nr:", question_nr)