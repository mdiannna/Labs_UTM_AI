from termcolor import colored
from production import IF, AND, THEN, OR, DELETE, NOT, forward_chain, backward_chain

loonie_rule = IF( AND(
    # '(?x) speaks Loonian language',
    # '(?x) has gray skin',
    '(?x) has 2 legs',
    # '(?x) has 2 arms',
    # '(?x) does not wear a mask',
    # '(?x) wears sunglasses',
    '(?x) walks fast',
    '(?x) has red hair'),
    THEN( '(?x) is a Loonie' ))


earthy_rule = IF( AND(
    # '(?x) wears a mask',
    # '(?x) wears a spacesuit',
    # OR('(?x) has yellow skin', 'has pink skin', 'has white skin', 'has brown skin'),
    # '(?x) speaks English language',
    AND('(?x) has 2 legs', '(?x) has 2 arms'),
    '(?x) walks slow'
    ), THEN('(?x) is an Earthy'))


martian_rule = IF( AND(
    '(?x) wears a mask',
    '(?x) has green skin',
    NOT('(?x) wears a spacesuit'),
    '(?x) wears shiny clothes',
    '(?x) speaks Martian language',
    AND('(?x) has 4 legs', '(?x) has 4 arms'),
    '(?x) wears sunglases'
    ),THEN('(?x) is a Martian'))


jupiterian_rule = IF( AND(
    '(?x) has orange hair',
    '(?x) weights very much',
    '(?x) has orange skin',
    '(?x) wears yellow clothes'
    '(?x) speaks Jupiterian language',
    AND('(?x) has 4 legs', '(?x) has 2 arms'),
    '(?x) wears sunglasses',
    '(?x) walks fast',
    ), THEN( '(?x) is a Jupiterian' ))

callistian_rule = IF( AND(
    '(?x) is slim',
    '(?x) has orange skin',
    '(?x) wears yellow clothes',
    OR('(?x) speaks Jupiterian language', '(?x) speaks Callistian', '(?x) speaks Callistian dialect'),
    AND('(?x) has 2 legs', '(?x) has 2 arms'),
    '(?x) wears sunglasses',
    '(?x) walks slow',
    ), THEN( '(?x) is a Callistian' ))

asteroidian_rule = IF( AND(
    '(?x) has gray skin',
    '(?x) has gray hair',
    '(?x) is slim',
    '(?x) wears shiny clothes',
    '(?x) comunicates with high pitched sounds',
    AND('(?x) has 4 legs', '(?x) has 4 arms'),
    '(?x) walks fast',
    ), THEN( '(?x) is an Asteroidian' ))


# Example usage:
# data = ('tim has 2 legs', 'tim walks slow', 'tim has 2 arms', 'ana has 2 legs', 'ana walks fast', 'ana has red hair')
# print (forward_chain([earthy_rule, loonie_rule], data, verbose=True))

rules = [loonie_rule, earthy_rule, martian_rule, jupiterian_rule, callistian_rule, asteroidian_rule]
available_facts = ()

INTERACTIVE = False

if __name__=='__main__':

    if INTERACTIVE==True:

        input_val = "*"
        while input_val!='exit()':
            print(colored("Enter your facts:  (to exit, write 'exit()', for help, write 'help()'", 'blue')) # facts sau questions?
            input_val = input(">> ") 
            
            print(input_val)
            if input_val=="help()":
                print(colored("-----------Commands:---------", "yellow"))
                print(colored("help()         -  shows help", "yellow"))
                print(colored("clear()        -  clears the facts", "yellow"))
                print(colored("exit()         -  exit the program", "yellow"))
                print(colored("show_facts()   - prints the existing available facts", "yellow"))
                print(colored("show_answer()   - prints the answer based on the  existing available facts", "yellow"))
                print(colored("", "yellow"))

            elif input_val=='clear()':
                available_facts = ()
                if available_facts==():
                    print(colored("---facts cleared---", 'green'))
                else:
                    print(colored("---ERROR: error clearing facts---", "red"))
            elif input_val=='show_facts()':
                print(colored("---available facts:" + str(available_facts), "yellow"))
            elif input_val=="show_answer()":
                print(colored("---available facts:" + str(available_facts), "yellow"))

                res = forward_chain(rules, available_facts, verbose=False)
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
                        # TODO: or use decision tree to compute
                        print(colored("   !? do you want to use the decision tree algorithm for a possible answer?[Yes or No]", "blue"))
                        input_y_n = input("   [Yes or No] >> ") 
                        if input_y_n == 'Yes':
                            print(colored("  --TODO: use DT", "red"))
                        elif input_y_n=='No':
                            print(colored("   -- Ok :) ---", "blue"))
                        else:
                            print(colored("   -- Didn't understand you, assumed no :) ---", "blue"))
                        
                
                print(colored("    !? To clear facts? [Yes or No]", 'blue') )
                input_y_n = input("   [Yes or No] >> ") 
                if input_y_n == 'Yes':
                    res = ()
                    available_facts = ()
                elif input_y_n=='No':
                    print(colored("   -- Ok, facts not cleared ---", "blue"))
                else:
                    print(colored("   -- Didn't understand you, assumed no, facts not cleared ---", "blue"))
                    

                print("----------")
                    
            else:
                available_facts += tuple([input_val])
                res = forward_chain(rules, available_facts, verbose=False)
                
            
    # from test_bkwd_chain import backward_chain

    print(backward_chain(rules, "John is a Martian"))


