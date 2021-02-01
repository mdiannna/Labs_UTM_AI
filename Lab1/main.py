from termcolor import colored
from production import IF, AND, THEN, OR, DELETE
from production import forward_chain

# rule1 = IF( AND( '(?x) is a Norwegian Blue parrot',
#                  '(?x) is motionless' ),
#             THEN( '(?x) is not dead' ) )

# rule2 = IF( NOT( '(?x) is dead' ),
#             THEN( '(?x) is pining for the fjords' ) )


# theft_rule = IF( 'you have (?x)',
#     THEN( 'i have (?x)' ),
#     DELETE( 'you have (?x)' ))

# theft_rule2 = IF( (AND( 'you have (?x)',
#     'you have 2 (?x)')),
#     THEN( 'i have (?x)' ),
#     DELETE( 'you have (?x)' ))


# data = ( 'you have apple',
# 'you have orange',
# 'you have 2 orange',
# 'you have pear' )


# print (forward_chain([theft_rule2], data, verbose=True))



loonie_rule = IF( AND(
    # '(?x) speaks Loonian',
    # '(?x) has gray skin',
    '(?x) has 2 legs',
    # '(?x) has 2 arms',
    # '(?x) does not wear a mask',
    # '(?x) wears sunglasses',
    '(?x) walks fast',
    '(?x) has red hair'),
    THEN( '(?x) is a Loonie' ))


earthy_rule = IF( AND(
    # '(?x) comes from Earth',
    # '(?x) wears a mask',
    # OR('(?x) wears a white spacesuit', 'wears a blue spacesuit', 'wears an orange spacesuit'),
    # OR('(?x) has yellow skin', 'has pink skin', 'has white skin', 'has brown skin'),
    # '(?x) can speak English',
    '(?x) has 2 legs',
    '(?x) has 2 arms',
    '(?x) walks slow'
    ), THEN('(?x) is an Earthy'))


# Example usage:
# data = ('tim has 2 legs', 'tim walks slow', 'tim has 2 arms', 'ana has 2 legs', 'ana walks fast', 'ana has red hair')
# print (forward_chain([earthy_rule, loonie_rule], data, verbose=True))



if __name__=='__main__':

    available_facts = ()
    rules = [earthy_rule, loonie_rule]

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
            if available_facts==('d'):
                print(colored("---facts cleared---", 'green'))
            else:
                print(colored("---ERROR: error clearing facts---", "red"))
        elif input_val=='show_facts()':
            print(colored("---available facts:" + str(available_facts), "yellow"))
        elif input_val=="show_answer()":
            print(colored("---available facts:" + str(available_facts), "yellow"))

            res = forward_chain(rules, available_facts, verbose=False)
            
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
            res = ()
            available_facts = ()
            print("----------")
                
        else:
            available_facts += tuple([input_val])
            res = forward_chain(rules, available_facts, verbose=False)
            
        

