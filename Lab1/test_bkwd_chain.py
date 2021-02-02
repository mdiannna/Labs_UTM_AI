from production import match, populate, IF, THEN, AND, OR

print("----match:")
print(match("(?x) is a (?y)", "John is a student"))

print("----match:")
print(match("(?x) is a Martian", "John is a Martian"))

print("----populate:")
print(populate("(?x) is a (?y)", { "x": "John", "y": "student" }))

rule1 =  IF( AND( '(?x) has green skin' ),         # Z1
        THEN( '(?x) is a Martian' ))
print("--rule1:", rule1)

print("--antecedent:")
# returns the IF part of a rule, which is either a leaf or a RuleExpression.
# print(rule.antecedent(rule1))
print(rule1.antecedent())
a = rule1.antecedent()
print(a[0])
m = match(a[0], 'John is a Martian')
print("-- match: ", m)

print("--consequent:")
# returns the THEN part of a rule, which is either a leaf or a RuleExpression.
c = rule1.consequent()
print(c) 
print(c[0])
m = match(c[0], 'John is a Martian')
print("-- match: ", m)


def backward_chain(rules, hypothesis, verbose=False):
    """
    TODO
    Output the goal tree from having rules and hyphothesis
    """
    for rule in rules:
        c = rule.consequent()
        m = match(c[0], hypothesis)
        if m != None:
            if verbose:
                print("match of x:", m["x"])
            res = populate(rule.antecedent(), m)

            return res
    return "no answer matches your hypothesis, sorry"


