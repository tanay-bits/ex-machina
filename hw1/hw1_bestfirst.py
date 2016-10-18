#!/usr/bin/env python

import copy

class Node:
    def __init__(self, num_pegs, num_disks):
        self.num_pegs = num_pegs
        self.num_disks = num_disks
        self.state = []
        self.parent = None
        self.pathCost = 0
        self.eval = 0

    def possible_moves(self):
        moves = []
        for peg1index in range(self.num_pegs):
            for peg2index in range(self.num_pegs):
                if peg1index != peg2index:
                    if not (self.state[peg1index] == []):
                        if self.state[peg2index] == []:
                            stateCopy = copy.deepcopy(self.state)
                            peg1_topDisk = stateCopy[peg1index].pop()
                            stateCopy[peg2index].append(peg1_topDisk)
                            moves.append(stateCopy)
                        elif self.state[peg1index][-1] < self.state[peg2index][-1]:
                            stateCopy = copy.deepcopy(self.state)
                            peg1_topDisk = stateCopy[peg1index].pop()
                            stateCopy[peg2index].append(peg1_topDisk)
                            moves.append(stateCopy)
        return moves

def nodeSelect(frng):
    return frng[[nde.eval for nde in frng].index(max([nde.eval for nde in frng]))]

def goalTest(state, num_pegs, num_disks):
    if (state == [[] for i in xrange(num_pegs-1)] + [[i for i in xrange(num_disks,0,-1)]]):
        return True
    return False

def path_to(node):
    states_list = [node.state]
    if not (node.parent ==  None):
        states_list = states_list + path_to(node.parent)
    return states_list

def towerOfHanoi(num_pegs, num_disks):
    assert num_pegs > 2, 'Need at least 3 pegs'
    assert num_disks > 1, 'Need at least 2 disks'

    initial_node = Node(num_pegs, num_disks)
    initial_node.state = [[i for i in xrange(num_disks,0,-1)]] + [[] for i in xrange(num_pegs-1)]

    fringe = [initial_node]
    explored = set()

    counter = 0
    while(True):
        counter += 1
        # print counter

        if fringe == []:
            print "Failed to find a solution :("
            return -1

        node = nodeSelect(fringe)
        fringe.remove(node)
        explored.add(node)

        # print node.state

        for state_after_move in node.possible_moves():
            # print state_after_move
            if not ((state_after_move in [n.state for n in explored]) or (state_after_move in [n.state for n in fringe])):
                child_node = Node(num_pegs, num_disks)
                child_node.state = state_after_move
                child_node.parent = node
                child_node.pathCost = node.pathCost + 1
                child_node.eval = sum(state_after_move[-1])
                if goalTest(state_after_move, num_pegs, num_disks):
                    print "Solution found!"
                    path = path_to(child_node)
                    path.reverse()
                    return path, child_node.pathCost, counter
                fringe.append(child_node)


# main function:
if __name__ == '__main__':
    pegs = input("Enter the number of pegs (at least 3): ")
    disks = input("Enter the number of disks (at least 2): ")
    solution_path, solution_cost, search_iters = towerOfHanoi(pegs, disks)
    print "Solution trace: "
    print solution_path
    print "Number of moves: "
    print solution_cost
    print "Number of search iterations:", search_iters