import copy
import sys

# switch active player:
def switchPlayer(active_player):
    if active_player == 'X':
        return 'O'
    elif active_player == 'O':
        return 'X'
    else:
        sys.exit("active player not valid")    #debug code

# define class for node:
class Node:
    def __init__(self, board, machine_symbol, active_player):
        self.state = board
        self.machine_symbol = machine_symbol
        self.active_player = active_player
        self.alpha = -1000
        self.beta = 1000
        self.move = None
        self.choice = None
        
    # check for game end state - either someone wins or board is full:
    def endTest(self):
        # someone wins:
        threes = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
        for each in threes:
            total = self.state[each[0]-1] + self.state[each[1]-1] + self.state[each[2]-1]
            if total == -3 or total == 3:
                return True
        # board is full:
        for val in self.state:
            if val == 0:
                return False
        return True
    
    # return a list containing possible spots (1-9 values):
    def spots(self):
        possible_spots = []
        for ind, val in enumerate(self.state):
            if val == 0:
                possible_spots.append(ind+1)
        return possible_spots
    
    # return the resulting 'node' if a particular (valid) move is taken:
    def result(self, spot):
        if spot in self.spots():
            boardCopy = copy.deepcopy(self.state)
            if self.active_player == 'X':
                boardCopy[spot-1] = 1
            elif self.active_player == 'O':
                boardCopy[spot-1] = -1
            else:
                print "active player not valid"    #debug code
                
            new_active_player = switchPlayer(self.active_player)
            child_node = Node(boardCopy, self.machine_symbol, new_active_player)
            child_node.move = spot
            return child_node
        else:
            print "You are testing a result from an INVALID move!"   #debug code

# calculate final score at end state:
def finalScore(node):
    if node.endTest():                  # game over... remove if condition later
        # print "Game over reached!"
        threes = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
        for each in threes:
            total = node.state[each[0]-1] + node.state[each[1]-1] + node.state[each[2]-1]
            if total == -3:                 # 'O' won
                # print "O won"
                if node.machine_symbol == 'O':   
                    return 10
                else:
                    return -10
            elif total == 3:                # 'X' won
                # print "X won"
                if node.machine_symbol == 'X':   
                    return 10
                else:
                    return -10
        return 0
    else:
        sys.exit("Cannot get score unless at end state!")

# alpha-beta algorithm:
def alphabeta(node):
    if node.endTest():
        final_score = finalScore(node)
        return final_score
    
    children = []    
    for available_spot in node.spots():
        possible_node = node.result(available_spot)
        children.append(possible_node)
        
    if node.active_player == node.machine_symbol:
        for child in children:
            score = alphabeta(child)
            if score > node.alpha:
                node.alpha = score
                node.choice = child.move
            if node.alpha >= node.beta:
                node.choice = child.move
                return node.alpha
        return node.alpha
    else:
        for child in children:
            score = alphabeta(child)
            if score < node.beta:
                node.beta = score
                node.choice = child.move
            if node.alpha >= node.beta:
                node.choice = child.move
                return node.beta
        return node.beta

# function used in GameApp:
def mymove(board, machine_symbol):
    print "Board as seen by the machine:",
    print board
    print "The machine is playing:",
    print machine_symbol

    initial_node = Node(board, machine_symbol, machine_symbol)
    utility = alphabeta(initial_node)
    bestmove = initial_node.choice
    return bestmove