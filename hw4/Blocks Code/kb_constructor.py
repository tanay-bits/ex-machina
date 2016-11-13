#!/usr/bin/env python

import facts_and_rules, read

'''
Make statement or rule object from string pattern provided like a line from statements.txt
''' 
def make_obj(str_pattern):
    if str_pattern[0:5] == "fact:":
        list_pattern = str_pattern[5:].replace(")","").replace("(","").rstrip().strip().split()
        obj = facts_and_rules.statement(list_pattern)
        return obj

    if str_pattern[0:5] == "rule:":
        list_pattern = str_pattern[5:].split("->")
        rhs = list_pattern[1].replace(")","").replace("(","").rstrip().strip().split()
        lhs = list_pattern[0].rstrip(") ").strip("( ").replace("(","").split(")")
        lhs = map(lambda x: x.rstrip().strip().split(), lhs)
        obj = facts_and_rules.rule(lhs, rhs)
        return obj


'''
Compare a fact against a rule, and infer new facts/rules
'''
def infer_from_fact(fact, rule, fb, rb):
    bindings = facts_and_rules.match(rule.lhs[0], fact)

    # if valid match b/w rule and fact
    if bindings != False:
        if (rule.type == "Assert"):

            # if rule lhs is a single pattern, it can only infer a new fact
            if (len(rule.lhs) == 1):
                new_fact = facts_and_rules.instantiate(rule.rhs.full, bindings)

                # return new fact, even if it's already in fb (assert_fr will take care of that)
                new_fact = facts_and_rules.statement(new_fact)
                return new_fact

            # if rule lhs is a conjunction of patterns, it can only infer a new rule
            else:
                new_rule_lhs = [facts_and_rules.instantiate(x.full, bindings) for x in rule.lhs[1:]]
                new_rule_rhs = facts_and_rules.instantiate(rule.rhs.full, bindings)
                new_rule = facts_and_rules.rule(new_rule_lhs, new_rule_rhs)

                # return new rule, even if it's already in rb
                return new_rule

        elif (rule.type == "Retract"):
            invalidated_fact = facts_and_rules.instantiate(rule.rhs.full, bindings)
            
            # create invalidated_fact as a statement object
            invalidated_fact = facts_and_rules.statement(invalidated_fact)
            
            # populate its children and return the invalidated fact
            for f in fb:
                if (f.full == invalidated_fact.full):
                    invalidated_fact.facts = f.facts
                    invalidated_fact.rules = f.rules
                    return invalidated_fact

            # if no children, simply return the invalidated fact
            return invalidated_fact

        else:
            raise ValueError("rule type is neither Assert nor Retract")

     # if no valid match b/w rule and fact
    else:
        return False


'''
Compare each existing fact against each existing rule, to infer and expand the initial KB
'''
def expand_existing(fb, rb):
    for r in rb:
        for f in fb:
            inference_yield = infer_from_fact(f, r, fb, rb)
            if (inference_yield != False):
                if (r.type == "Retract"):
                    fb, rb = retract_fr(inference_yield, fb, rb)
                elif (r.type == "Assert"):
                    fb, rb = assert_fr(inference_yield, fb, rb)
                else:
                    raise ValueError("rule type is neither Assert nor Retract")
    return fb, rb


'''
Assert a new fact (or rule) into KB; also assert other facts/rules INFERRED from comparing this new fact 
(or rule) with the existing rules (or facts)
'''
def assert_fr(obj, fb, rb):
    # if obj is a fact
    if (type(obj) is facts_and_rules.statement):

        # add new fact only if it's not already in fb
        if (obj.full not in map(lambda x: x.full, fb)):
            fb.append(obj)
            
            # now infer and add/retract more facts or rules
            for r in rb:
                inference_yield = infer_from_fact(obj, r, fb, rb)
                if (inference_yield != False):
                    
                    # if the newly added fact triggers a retraction, remove the now invalidated fact
                    # and all facts/rules that it supports
                    if (r.type == "Retract"):
                        fb, rb = retract_fr(inference_yield, fb, rb)

                    # if the newly added fact triggers an assertion, assert the inferred fact/rule to KB
                    # but first make that the child of the fact+rule that triggered the assertion
                    elif (r.type == "Assert"):
                        if (type(inference_yield) is facts_and_rules.statement):
                            obj.add_fact(inference_yield)
                            r.add_fact(inference_yield)
                        elif (type(inference_yield) is facts_and_rules.rule):
                            obj.add_rule(inference_yield)
                            r.add_rule(inference_yield)
                        fb, rb = assert_fr(inference_yield, fb, rb)
                    else:
                        raise ValueError("rule type is neither Assert nor Retract")
        return fb, rb

    # else if obj is a rule
    elif (type(obj) is facts_and_rules.rule):
         
        # add new rule only if it's not already in rb
        if (obj.full not in map(lambda x: x.full, rb)):
            rb.append(obj)

            # now infer and add/retract more facts or rules
            for f in fb:
                inference_yield = infer_from_fact(f, obj, fb, rb)
                if (inference_yield != False):

                    # if the newly added rule triggers a retraction, remove the now invalidated fact
                    # and all facts/rules that it supports
                    if (obj.type == "Retract"):
                        fb, rb = retract_fr(inference_yield, fb, rb)
                    
                    # if the newly added rule triggers an assertion, assert the inferred fact/rule to KB
                    # but first make that the child of the rule+fact that triggered the assertion
                    elif (obj.type == "Assert"):
                        if (type(inference_yield) is facts_and_rules.statement):
                            obj.add_fact(inference_yield)
                            f.add_fact(inference_yield)
                        elif (type(inference_yield) is facts_and_rules.rule):
                            obj.add_rule(inference_yield)
                            f.add_rule(inference_yield)
                        fb, rb = assert_fr(inference_yield, fb, rb)
                    else:
                        raise ValueError("rule type of obj is neither Assert nor Retract")
        return fb, rb

    else:
        raise ValueError("obj type is neither fact nor rule")


'''
Retract an existing fact (or rule) from KB, as well as all facts/rules which it supported
'''
def retract_fr(obj, fb, rb):
     # base case:
    if ((len(obj.facts) == 0) and (len(obj.rules) == 0)):
        if (type(obj) is facts_and_rules.statement):
            for f in fb:
                if (f.full == obj.full):
                    fb.remove(f)
                    return fb, rb

        elif (type(obj) is facts_and_rules.rule):
            for r in rb:
                if (r.full == obj.full):
                    rb.remove(r)
                    return fb, rb

     # non-base case:
    else:
        children = obj.facts + obj.rules
        for child in children:
            fb, rb = retract_fr(child, fb, rb)

        if (type(obj) is facts_and_rules.statement):
            for f in fb:
                if (f.full == obj.full):
                    fb.remove(f)
                    return fb, rb

        elif (type(obj) is facts_and_rules.rule):
            for r in rb:
                if (r.full == obj.full):
                    rb.remove(r)
                    return fb, rb
        else:
            raise ValueError("retract_fr function failed")


'''
Given a list of patterns, like [['color', '?x', 'blue'], ['inst', 'bigbox', '?w']], return the bindings in KB 
that hold when those patterns are true
'''
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

    # populate FB and RB with initial knowledge from file
    FB = []
    RB = []
    for f in facts:
        FB.append(facts_and_rules.statement(f))
    for r in rules:
        RB.append(facts_and_rules.rule(r[0], r[1]))

    # infer more knowledge from initial file knowledge
    FB, RB = expand_existing(FB, RB)
    
    # display everything inferred from initial KB
    print "Facts and Rules given in and inferred from file:"
    for f in FB:
        print f.pretty()
    print "no. of facts: ", len(FB)
    print "----------------------------"    
    for r in RB:
        print r.pretty()
    print "no. of rules: ", len(RB)
    print "----------------------------"

    # prompt user to ASK or ASSERT
    prompt_flag = True
    while (prompt_flag == True):
        option = input("What do you want to do? (Enter \"ask\" or \"assert\" or \"quit\", with quotes):\n")
        if (option == "ask"):
            query = input("Enter the list of patterns to query, like \"((color ?x blue), (flat ?z))\":\n")
            query = [x.replace(')','').replace('(','').split() for x in query.strip('(').strip(')').split(',')]
            bl = ask(query, FB)
            print "For Ask query: ", query
            print "the answers are: ", bl
            print "----------------------------"
        if (option == "assert"):
            prompt = "Enter the fact or rule to assert into KB, like \"fact: (clear cube3)\",\n" + \
            "or \"rule: ((married ?x ?y) (love ?x ?y)) -> (happy ?x)\", with quotes:\n"
            assertion = input(prompt)
            assertion = make_obj(assertion)
            FB, RB = assert_fr(assertion, FB, RB)
            print "Knowledge base after making assertion:"
            for f in FB:
                print f.pretty()
            print "no. of facts: ", len(FB)
            print "----------------------------"    
            for r in RB:
                print r.pretty()
            print "no. of rules: ", len(RB)
            print "----------------------------"
        if (option == "quit"):
            prompt_flag = False


