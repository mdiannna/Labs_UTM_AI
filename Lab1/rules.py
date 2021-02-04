from production import IF, AND, THEN, OR, DELETE, NOT

#########################################
#        Loonie rules
#########################################

loonie_rule_general = IF( AND(
    '(?x) speaks loonian language',
    '(?x) has gray skin',
    '(?x) has 2 legs',
    '(?x) has 2 arms',
    '(?x) does not wear a mask',
    '(?x) wears sunglasses',
    '(?x) walks fast',
    '(?x) has red hair'
    ), THEN( '(?x) is a Loonie' ))

loonie_rule2 = IF( AND(
    '(?x) speaks loonian language',
    '(?x) does not wear a mask',
    '(?x) wears sunglasses'
    ), THEN( '(?x) is a Loonie' )
)

loonie_rule3 = IF( AND(
    '(?x) does not wear a mask',
    '(?x) has red hair',
    '(?x) has gray skin',
    ), THEN( '(?x) is a Loonie' )
)

loonie_rules = [loonie_rule_general, loonie_rule2, loonie_rule3]

#########################################
#        Earthy rules
#########################################


earthy_rule_general = IF( AND(
    '(?x) wears a mask',
    '(?x) wears a spacesuit',
    OR('(?x) has yellow skin', '(?x) has pink skin', '(?x) has white skin', '(?x) has brown skin'),
    '(?x) speaks english language',
    AND('(?x) has 2 legs', '(?x) has 2 arms'),
    '(?x) walks slow'
    ), THEN('(?x) is an Earthy'))

earthy_rule2 = IF(
    OR('(?x) has yellow skin', '(?x) has pink skin', '(?x) has white skin', '(?x) has brown skin')
    , THEN('(?x) is an Earthy')
)

earthy_rule3 = IF(AND(
    '(?x) wears a mask',
    '(?x) wears a spacesuit'
    ), THEN('(?x) is an Earthy')
)

earthy_rule4 = IF(AND(
    '(?x) speaks english language',
    '(?x) has 2 legs',
    '(?x) has 2 arms'
    ), THEN('(?x) is an Earthy')
)


earthy_rules = [earthy_rule_general, earthy_rule2, earthy_rule3, earthy_rule4]

#########################################
#        Martian rules
#########################################

martian_rule_general = IF( AND(
    '(?x) wears a mask',
    NOT('(?x) wears a spacesuit'),
    '(?x) wears shiny clothes',
    '(?x) speaks martian language',
    AND('(?x) has 4 legs', '(?x) has 4 arms'),
    '(?x) wears sunglasses'
    ), THEN('(?x) is a Martian'))


martian_rule2 = IF('(?x) has green skin',THEN('(?x) is a Martian'))

martien_rule3 = IF(AND(
    '(?x) speaks martian language',
    '(?x) speaks martian language',
    '(?x) wears shiny clothes'
    ), THEN('(?x) is a Martian'))

martian_rules = [martian_rule_general, martian_rule2, martien_rule3]


#########################################
#        Jupiterian rules
#########################################

jupiterian_rule_general = IF( 
    AND(
    '(?x) has orange hair',
    '(?x) weights very much',
    '(?x) has orange skin',
    '(?x) wears yellow clothes',
    '(?x) speaks jupiterian language',
    AND('(?x) has 4 legs', '(?x) has 2 arms'),
    '(?x) wears sunglasses',
    '(?x) walks fast',
    ), THEN( '(?x) is a Jupiterian' ))

jupiterian_rule2 = IF(OR(
    AND(
        '(?x) has 4 legs',
        '(?x) has 2 arms',
        '(?x) has orange skin',
        '(?x) walks fast'
    ),
    AND(
        '(?x) wears sunglasses',
        '(?x) weights very much',
    ),
    AND(
        '(?x) has orange hair', 
        '(?x) has orange skin'
    ),
    AND('(?x) has orange hair',
    '(?x) has 4 legs')
    ), THEN( '(?x) is a Jupiterian' ) )

jupiterian_rules = [jupiterian_rule_general, jupiterian_rule2]

#########################################
#        Callistian rules
#########################################

callistian_rule_general = IF( AND(
    '(?x) is slim',
    '(?x) has orange skin',
    '(?x) wears yellow clothes',
    OR('(?x) speaks jupiterian language', '(?x) speaks callistian language', '(?x) speaks callistian dialect'),
    AND('(?x) has 2 legs', '(?x) has 2 arms'),
    '(?x) wears sunglasses',
    '(?x) walks slow',
    ), THEN( '(?x) is a Callistian' ))

callistian_rule2 = IF( AND(
    '(?x) has orange skin',
    '(?x) wears yellow clothes',
    '(?x) has 2 legs', 
    '(?x) has 2 arms',
    OR('(?x) speaks jupiterian language', '(?x) speaks callistian language', '(?x) speaks callistian dialect')
    ), THEN( '(?x) is a Callistian' ))

callistian_rule3 = IF( AND(
    '(?x) has orange skin',
    OR('(?x) speaks callistian language', '(?x) speaks callistian dialect')
    ), THEN( '(?x) is a Callistian' ))


callistian_rules = [callistian_rule_general, callistian_rule2, callistian_rule3]

#########################################
#        Asteroidian rules
#########################################
asteroidian_rule_general = IF( AND(
    '(?x) has gray skin',
    '(?x) has gray hair',
    '(?x) is slim',
    '(?x) wears shiny clothes',
    '(?x) communicates with high pitched sounds',
    AND('(?x) has 4 legs', '(?x) has 4 arms'),
    '(?x) walks fast',
    ), THEN( '(?x) is an Asteroidian' ))

# This can be written as a big rule with OR between all the following 3 rules
asteroidian_rule1 = IF( AND(
    '(?x) is slim',
    AND('(?x) has 4 legs', '(?x) has 4 arms'),
    '(?x) walks fast',
    ), THEN( '(?x) is an Asteroidian' ))

asteroidian_rule2 = IF( AND(
    '(?x) wears shiny clothes',
    '(?x) has gray skin',
    '(?x) has gray hair'
    ), THEN( '(?x) is an Asteroidian' )
)

asteroidian_rule3 = IF(
    OR(
    '(?x) communicates with high pitched sounds',
    '(?x) speaks high pitched sounds'
    ), THEN( '(?x) is an Asteroidian' )
)

asteroidian_rules = [asteroidian_rule_general, asteroidian_rule1, asteroidian_rule2, asteroidian_rule3]



#########################################
#        All rules
#########################################
all_rules = []
all_rules.extend(loonie_rules)
all_rules.extend(earthy_rules)
all_rules.extend(martian_rules)
all_rules.extend(jupiterian_rules)
all_rules.extend(callistian_rules)
all_rules.extend(asteroidian_rules)