#!/usr/bin/env python
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#
from Queue import PriorityQueue
from random import randrange, sample
import sys
import string

# shift a specified row left (-1) or right (1)
def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)]
    return ( state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (-1) or down (1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print '%3d %3d %3d %3d' % (row[j:(j+4)])

# return a list of possible successor states
def successors(state):
    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ] 

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)

# Heuristic Function 1: Number of misplaced tiles
def heurisitic_one(state, goal_state):
    heur_one = sum(([1 if state[i-1] != goal_state[i-1] else 0 for i in state ]))
    return heur_one

# The solver! - using BFS right now
def solve(initial_board):
    fringe = PriorityQueue()
    fringe.put((heurisitic_one(initial_board,goal_state),[(initial_board),"",0]))
    i = 0
    while not fringe.empty() > 0:
        (heuristic_value, fringeitem) = fringe.get()
        [state, route_so_far,moves_so_far] = fringeitem
#        print heuristic_value, moves_so_far, i
        for (succ, move) in successors( state ):
#            print heurisitic_one(succ, goal_state)
            if is_goal(succ):
                return( route_so_far + " " + move )
            fringe.put((heurisitic_one(succ,goal_state)+moves_so_far+1, [(succ), route_so_far + " " + move,moves_so_far+1] ))
            i += 1
    return False

# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]
        print start_state

goal_state = sorted(start_state)

if len(start_state) != 16:
    print "Error: couldn't parse start state file"

print "Start state: "
print_board(tuple(start_state))

print "Solving..."
print tuple(start_state)
route = solve(tuple(start_state))

print "Solution found in " + str(len(route)/3) + " moves:" + "\n" + route