class statement(object):

# A statement has a predicate, a set of arguments that it applies to and a list of 
# statements/rules that it supports (initially empty). Arguments are processed to 
# turn both variables and constants into objects.
                        
    def __init__(self, pattern):
        self.full = pattern
        self.predicate = pattern[0].upper()
        self.args = pattern[1:]
        self.facts = []
        self.rules = []


# Pretty hands back a nice looking string version of this object for printing
         
    def pretty(self):
        return "(" + " ".join(self.full) + ")"


# Add inferred facts and rules to a statement so that we can track them for later retraction
     
    def add_fact(self, fact):    
        self.facts.append(fact) 
      
    def add_rule(self, rule):    
        self.rules.append(rule)       


# Rules have a few more elements to them.  

# They have:
#  A left hand side (a list of patterns that have to be true for a rule to fire).
#  A right hand side (a pattern that needs to be instantiated)
#  A name (for convenience sake and use later).
#  The same list of facts and rules that it supports that facts have
#  The type of rule (does it Assert or Retract its conclusion
#  Note: Any rule where the right hand side begins with a "~" is marked as a "Retract"

class rule(object):

    count = 0

    def __init__(self, lhs, rhs):
        self.full = lhs + rhs
        self.type = "Assert"
        self.name = "Rule "+ str(rule.count) 
        self.lhs = map(lambda x: statement(x), lhs)
        if rhs[0][0] == "~":
            rhs[0] = rhs[0][1:]
            self.type = "Retract"
        self.rhs = statement(rhs)
        self.facts = []
        self.rules = []
        rule.count = rule.count + 1
 
 
# Pretty hands back a nice looking string version of this object for printing
      
    def pretty(self):
        return self.name + ": When <"+ " ".join(map(lambda x: x.pretty(), self.lhs)) + "> " + self.type + " " + self.rhs.pretty()

# Add inferred facts and rules to a rule so that we can track them for later retraction
     
    def add_fact(self, fact):    
        self.facts.append(fact) 
      
    def add_rule(self, rule):    
        self.rules.append(rule)  


# Match is designed around the statement structure

# Match takes two arguments, a pattern and a fact and returns either a bindings list
# if they match or False if they do not.

# It checks to see if the predicates are the same and then tests the arguments against 
# each other.

# The pattern may have variables in it. The fact may not.

def match (pattern,fact):
    p = pattern.full
    f = fact.full
    if p[0] != f[0]:
        return False
    return match_args(p[1:],f[1:])
 
 
# Match args just steps through two lists of arguments and returns the list of bindings 
# that have to be in place if they are going to match.  If it ever finds a mismatch,
# it returns False and stops checking. 
 
# It maintains a set of bindings so that repeated use of a variable can be noted and enforced.
      
def match_args(pattern_args, fact_args):
    bindings = {}
    for p,f in zip(pattern_args, fact_args):
        bindings = match_element(p, f, bindings)
        if False == bindings:
            return False
    return bindings

 
# Match_element takes two elements and a list of bindings and returns the bindings under
# which the elements match.  If both elements are contants, then it just checks to see if 
# they are the same.
# If the first element is a variable, it checks to see if it is already bound and tests the 
# other element against the value.
# If the variable is unbound, it adds the binding to the bindings list and returns it.
        
def match_element(p, f, bindings):
    if p == f:
        return bindings
    elif varq(p):
        bound = bindings.get(p, False)
        if bound:
            if f == bound:
                return bindings
            else:
                return False
        else:
            bindings[p] = f
            return bindings
    else:
        return False


# Instantiate takes a pattern and a set of bindings and creates a new statement with the 
# variables replaced with the values in the bindings list. It walks through the arguments
# and replaces any element that is in the bindings list with its value

def instantiate(pattern, bindings):
    predicate = pattern[0]
    args = map(lambda x: bindings.get(x, x), pattern[1:])
    args.insert(0, predicate)
    return args


# varq just checks to see if an element is a variable 

def varq(item):
    if item[0] == "?":
        return True
    else:
        return False