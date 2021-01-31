# from termcolor import colored
from production import IF, AND, THEN, OR, DELETE
from production import forward_chain

print("Hello world! TODO: implement")

# instantiate("sister (?x) {?y)", {'x': 'Lisa', 'y': 'Bart'})
x = "Diana"
y = "test"

# rule1 = IF( AND( '(?x) is a Norwegian Blue parrot',
#                  '(?x) is motionless' ),
#             THEN( '(?x) is not dead' ) )

# rule2 = IF( NOT( '(?x) is dead' ),
#             THEN( '(?x) is pining for the fjords' ) )


theft_rule = IF( 'you have (?x)',
    THEN( 'i have (?x)' ),
    DELETE( 'you have (?x)' ))

data = ( 'you have apple',
'you have orange',
'you have pear' )

print (forward_chain([theft_rule], data, verbose=True))