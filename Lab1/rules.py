from production import IF, AND, THEN, OR, DELETE, NOT

loonie_rule = IF( AND(
    '(?x) speaks Loonian language',
    '(?x) has gray skin',
    '(?x) has 2 legs',
    '(?x) has 2 arms',
    '(?x) does not wear a mask',
    '(?x) wears sunglasses',
    '(?x) walks fast',
    '(?x) has red hair'),
    THEN( '(?x) is a Loonie' ))


earthy_rule = IF( AND(
    '(?x) wears a mask',
    '(?x) wears a spacesuit',
    OR('(?x) has yellow skin', '(?x) has pink skin', '(?x) has white skin', '(?x) has brown skin'),
    '(?x) speaks English language',
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
    '(?x) wears yellow clothes',
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