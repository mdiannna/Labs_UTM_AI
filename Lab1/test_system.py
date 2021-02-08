#################################################################################################
# This file is only for some testing purposes, and doesn't test/show the full solution!
#################################################################################################

from production import forward_chain, backward_chain
from rules import all_rules

rules = all_rules

loonie_facts = ('Test_person speaks loonian language',
    'Test_person has gray skin',
    'Test_person has 2 legs',
    'Test_person has 2 arms',
    'Test_person does not wear a mask',
    'Test_person wears sunglasses',
    'Test_person walks fast',
    'Test_person has red hair')


earthy_facts = (
    'Test_person wears a mask',
    'Test_person wears a spacesuit',
    'Test_person has pink skin',
    'Test_person speaks english language',
    'Test_person has 2 legs', 
    'Test_person has 2 arms',
    'Test_person walks slow')


martian_facts = (
    'Test_person wears a mask',
    'Test_person has green skin',
    'Test_person wears shiny clothes',
    'Test_person speaks martian language',
    'Test_person has 4 legs', 'Test_person has 4 arms',
    'Test_person wears sunglases')


jupiterian_facts = (
    'Test_person has orange hair',
    'Test_person weights very much',
    'Test_person has orange skin',
    'Test_person wears yellow clothes',
    'Test_person speaks Jupiterian language',
    'Test_person has 4 legs', 'Test_person has 2 arms',
    'Test_person wears sunglasses',
    'Test_person walks fast')

callistian_facts = (
    'Test_person is slim',
    'Test_person has orange skin',
    'Test_person wears yellow clothes',
    'Test_person speaks callistian language',
    'Test_person has 2 legs', 
    'Test_person has 2 arms',
    'Test_person wears sunglasses',
    'Test_person walks slow')

asteroidian_facts = (
    'Test_person has gray skin',
    'Test_person has gray hair',
    'Test_person is slim',
    'Test_person wears shiny clothes',
    'Test_person comunicates with high pitched sounds',
    'Test_person has 4 legs', 'Test_person has 4 arms',
    'Test_person walks fast')


all_facts = [loonie_facts, earthy_facts, martian_facts, jupiterian_facts, callistian_facts, asteroidian_facts]

for fact_list in all_facts:
    print("facts:", fact_list)
    res = forward_chain(rules, fact_list, verbose=False)
    # print("res:", res)
    print("res:", set(res).difference(set(fact_list)))
    print()




