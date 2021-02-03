from termcolor import colored
from production import forward_chain, backward_chain

from rules import loonie_rule, earthy_rule, martian_rule, jupiterian_rule, callistian_rule, asteroidian_rule, martian_rule2


rules = [loonie_rule, earthy_rule, martian_rule,martian_rule2, jupiterian_rule, callistian_rule, asteroidian_rule]
available_facts = ()


def show_answer_fwd_chain(rules, available_facts, verbose=False):
    res = forward_chain(rules, available_facts, verbose=verbose)
    # print("----   res for debug: ", res)
    
    if available_facts != res and set(res).difference(set(available_facts))!=set():
        print(colored("*** answer: ", "green"),set(res).difference(set(available_facts)) )
    else:
        found = False
        for r in res:
            if 'is' in r:
                print(colored("*** answer: ", "green"),r )
                found = True
                break
        if not found:                    
            print(colored("*** answer: Can't detect the type of tourist", 'magenta') )

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
    print(colored("clear()        -  clears the facts", "yellow"))
    print(colored("exit()         -  exit the program", "yellow"))
    print(colored("show_facts()   - prints the existing available facts", "yellow"))
    print(colored("show_answer()   - prints the answer based on the  existing available facts", "yellow"))
    print(colored("tell_me_about() - will show facts about hypothesis using backward chaining", "yellow"))

    print(colored("", "yellow"))

def show_answer_bkwd_chain(rules):
    print(colored("  Write your hypothesis please:", "blue"))
    input_h = input("   >> ") 
    r = backward_chain(rules, input_h)
    print(colored(" ---- I found out that: " + str(r), "green"))
    print()
    
    return r

INTERACTIVE = True


if __name__=='__main__':

    if INTERACTIVE==True:

        input_val = "*"
        while input_val!='exit()':
            print(colored("Enter your facts:  (to exit, write 'exit()', for help, write 'help()'", 'blue')) # facts sau questions?
            input_val = input(">> ") 
            
            print(input_val)
            if input_val=="help()":
               show_available_commands()

            elif input_val=='clear()':
                available_facts = ()
                if available_facts==():
                    print(colored("---facts cleared---", 'green'))
                else:
                    print(colored("---ERROR: error clearing facts---", "red"))
                print()

            elif input_val=='show_facts()':
                print(colored("---available facts:" + str(available_facts), "yellow"))
                print()

            elif input_val=="show_answer()":
                print(colored("---available facts:" + str(available_facts), "yellow"))

                res = show_answer_fwd_chain(rules, available_facts)
                res = ()
                
                available_facts = clear_facts_or_no(available_facts)

                print("----------")    
            elif input_val=="tell_me_about()":
               show_answer_bkwd_chain(rules)
            else:
                available_facts += tuple([input_val])
    

