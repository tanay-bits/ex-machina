#!/usr/bin/env python

import facts_and_rules, read

def infer_from_fact(fact, rule, fb, rb):
    bindings = facts_and_rules.match(rule.lhs[0], fact)
    if bindings != False:           # valid match b/w rule and fact
        if (rule.type == "Assert"):
            if (len(rule.lhs) == 1):     # rule is a single pattern, so it can only infer a new fact, if any(?)
                new_fact = facts_and_rules.instantiate(rule.rhs.full, bindings)
                if (new_fact not in map(lambda x: fb[x].full, range(len(fb)))): # add new fact only if it's not already in fb
                    new_fact = facts_and_rules.statement(new_fact)
                    fb.append(new_fact)
                    return True
            else:                       # rule is a conjunction of patterns, so it can only infer a new rule, if any(?)
                new_rule_lhs = [facts_and_rules.instantiate(x.full, bindings) for x in rule.lhs[1:]]
                new_rule_rhs = facts_and_rules.instantiate(rule.rhs.full, bindings)
                new_rule = facts_and_rules.rule(new_rule_lhs, new_rule_rhs)
                if (new_rule.full not in map(lambda x: rb[x].full, range(len(rb)))): # add new rule only if it's not already in rb
                    rb.append(new_rule)
                    return True
        elif (rule.type == "Retract"):
            invalidated_fact = facts_and_rules.instantiate(rule.rhs.full, bindings)
            for f in fb:
                if (invalidated_fact == f.full):
                    fb.remove(f)    # TODO: break out of for loop here, if sure that facts are not duplicated
                    return True     # SHIFT this line after accounting for rule retraction
            # TODO: remove rules previously inferred from this fact

    else:
        return False

def assert_retract(fb, rb):
    for r in rb:
        for f in fb:
            inference_yield = infer_from_fact(f, r, fb, rb)
            if inference_yield:
                assert_retract(fb, rb)
    return fb, rb

def ask(patterns, fb):
    bindings_list = []
    for pattern in patterns:
        pattern_statement = facts_and_rules.statement(pattern)
        for f in fb:
            bindings = facts_and_rules.match(pattern_statement, f)
            if bindings != False:
                bindings_list.append(bindings)
    return bindings_list


# Main function:
if __name__ == '__main__':
    facts, rules = read.read_tokenize("statements.txt")

    FB = []
    RB = []

    for f in facts:
        FB.append(facts_and_rules.statement(f))
        # print KB[-1].pretty()

    for r in rules:
        RB.append(facts_and_rules.rule(r[0], r[1]))
        # print RB[-1].pretty()

    FB, RB = assert_retract(FB, RB)
    
    for f in FB:
        print f.pretty()
    print len(FB)
    print "------------------"
    for r in RB:
        print r.pretty()
    print len(RB)

    print "############################"

    bl = ask([['color', '?x', 'blue'], ['color', '?y', 'red'], ['flat', '?z'], ['inst', 'bigbox', '?w']], FB)
    print bl

    # FB, RB = assert_retract(FB, RB)
    
    # for f in FB:
    #     print f.pretty()
    # print len(FB)
    # print "------------------"
    # for r in RB:
    #     print r.pretty()
    # print len(RB)


