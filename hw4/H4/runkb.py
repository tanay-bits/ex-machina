import Blocks_Code.facts_and_rules as fact_and_rule
import Blocks_Code.read as read

global KB
global RB
RB = []
KB =[]

def ask(pattern):
    bindings = []
    for fact in KB:
        # print temp.pretty(), fact.pretty()
        if pattern in fact.pretty():
            bindings.append(fact)
    if bindings == None:
        return False
    return bindings

def infer_from_fact(rule,fact):
    bindings = fact_and_rule.match(rule.lhs[0],fact);

    if bindings != False:
        if (rule.type == "Retract"):
            temp  = fact_and_rule.instantiate(rule.rhs.full,bindings)
            temp = fact_and_rule.statement(temp)
            KB.append(temp)
            for fact in KB:
                # print temp.pretty(), fact.pretty()
                if temp.pretty() in fact.pretty():
                    KB.remove(fact)
            for rule in RB:
                # print temp.pretty(), fact.pretty()
                if temp.pretty() in rule.pretty():
                    RB.remove(rule)

        elif(len(rule.lhs)==1):
            temp  = fact_and_rule.instantiate(rule.rhs.full,bindings)
            KB.append(fact_and_rule.statement(temp))
        else:
            tests = map(lambda x: fact_and_rule.instantiate(x.full, bindings), rule.lhs[1:])
            tests1 =fact_and_rule.instantiate(rule.rhs.full, bindings)
            a = fact_and_rule.rule(tests,tests1)
            RB.append(a)

facts,rules = read.read_tokenize("statements.txt")

for fact in facts:
    KB.append(fact_and_rule.statement(fact))


for new_rule in rules:
    # print fact_and_rule.rule(new_rule[0],new_rule[1]).pretty()
    RB.append(fact_and_rule.rule(new_rule[0],new_rule[1]))

# print RB[0].lhs[0].full

for rule in RB:
    for fact in KB:
        infer_from_fact(rule,fact)

for rule in RB:
    for fact in KB:
        infer_from_fact(rule,fact)

for rule in RB:
    for fact in KB:
        infer_from_fact(rule,fact)

# for fact in KB:
#     print fact.pretty()

result = ask("(covered cube1)")
for each in result:
    print each.pretty()

result = ask("(clear cube1)")
for each in result:
    print each.pretty()

# print KB[0].args
# for rule in RB:
#     print rule.pretty()

# print KB
# print RB

# def assert():
#         if match.match(r.lhs[0].full,fact.full):
#
# for fact in fats:
#     block.tatement(fact)
# for new_rule in rules:
#     block.rule(new_rule[0],new_rule[1])
#
#     def infer():
#         for r in KB:
#             bindings = match.match();
#             if bindings != False:
#                 if len(r.lhs)==1:
#                     Assert(blocks.statemate(match.instatiate(r.rhs.full,bingdings)  ))
#                 else:
#                     tests = map(lambda x: match.instatiate(x.full, bindings), r.rhs[1:]))
