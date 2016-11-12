import FOPC

statement1 = ('clean', 'Cell 11') 
statement2 = ('clean', 'Cell 12') 
pattern = ('clean', '?x') 
bindings = {}

first = FOPC.match(statement1,pattern,bindings)
print first

second = FOPC.match(statement2,pattern,first)
print second

print FOPC.instantiate(statement1, first)

