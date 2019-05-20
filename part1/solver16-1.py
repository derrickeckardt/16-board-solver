#!/usr/bin/env python
# Indiana University Fall 2018 CSCI-B551 Elements of AI
# Assignment 1, Part 1 - 16-Puzzle
#
###############################################################################
###############################################################################
#
# A full discussion and details can be found in the Readme file for Part 1,
# which is located at:
# https://github.iu.edu/cs-b551-fa2018/derrick-a1/tree/master/part1
#
###############################################################################
###############################################################################

from Queue import PriorityQueue
from heapq import *
from random import randrange, sample
from collections import Counter
import sys
import string
import operator
from operator import add
from math import sqrt
import profile

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

# Gets the manhattan distance of a tile from where it is to where it is in the goal state
def get_manhattan(current, goal):
    distance_x = (goal-1)%4 - (current-1)%4
    distance_y = (goal-1)//4 - (current-1)//4
    d_man_x = 1 if distance_x == 3 or distance_x == -3 else distance_x if distance_x >= 0 else distance_x*-1
    d_man_y = 1 if distance_y == 3 or distance_y == -3 else distance_y if distance_y >= 0 else distance_y*-1
    return (d_man_x**(0.91) + d_man_y**(0.91))**(1.414)

# check if we've reached the goal
# Changed it to use the stock goal_state so that we did not have sort.  Performance savings.
def is_goal(state):
    return goal_state == list(state) 

def heuristic_eight(state, goal_state):
    total = 0.0
    for i in goal_state:
        total += get_manhattan(state[i-1],i)
    return total/4.0

# The solver! - using BFS right now
def solve(initial_board):
    fringe = PriorityQueue()
    fringe.put((heuristic_eight(initial_board,goal_state),[(initial_board),"",0]))

    visited_states = {}
    i = 1
    while not fringe.empty() > 0:
        (heuristic_value, [state, route_so_far,moves_so_far]) = fringe.get()
        #  = fringeitem
        for (succ, move) in successors( state ):
            if succ not in visited_states:
                if is_goal(succ):
                    print "Fringe.gets ",i
                    return( route_so_far + " " + move )
                fringe.put((heuristic_eight(succ,goal_state)+moves_so_far+1, [(succ), route_so_far + " " + move,moves_so_far+1] ))
                visited_states[succ] = True
        i += 1
    return False

def solve_dict(initial_board):
    heuristic_values = {}
    fringe={}
    fringe[0] = {"board": (initial_board), "route_so_far" : "", "moves_so_far" : 0}
    heuristic_values[0] = heuristic_eight(initial_board,goal_state)
    visited_states = {}
    i = 1
    while bool(fringe):
        mk = min(heuristic_values, key=heuristic_values.get)
        # mk = sorted(heuristic_values.items(), key=operator.itemgetter(1))[0][0]
        heuristic_value, state, route_so_far, moves_so_far = heuristic_values[mk], fringe[mk]["board"], fringe[mk]["route_so_far"], fringe[mk]["moves_so_far"]
        heuristic_values.pop(mk)
        for (succ, move) in successors(state):
            if succ not in visited_states:
                if is_goal(succ):
                    print "Fringe.gets ",i
                    return( route_so_far + " " + move )
                heuristic_values[len(fringe)] = heuristic_eight(succ,goal_state)+moves_so_far+1
                fringe[len(fringe)] = {"board":(succ), "route_so_far":route_so_far + " " + move,"moves_so_far":moves_so_far+1}
                visited_states[succ] = True
        i += 1
    return False


def solve_heap(initial_board):
    fringe = []
    heappush(fringe,((heuristic_eight(initial_board,goal_state),[(initial_board),"",0])))
    visited_states = {}
    i = 1
    while len(fringe) > 0:
        (heuristic_value, [state, route_so_far,moves_so_far]) = heappop(fringe)
        #  = fringeitem
        for (succ, move) in successors( state ):
            if succ not in visited_states:
                if is_goal(succ):
                    print "States Tested from Fringe:",i
                    return( route_so_far + " " + move )
                heappush(fringe, ((heuristic_eight(succ,goal_state)+moves_so_far+1, [(succ), route_so_far + " " + move,moves_so_far+1] )))
                visited_states[succ] = True
        i += 1
    return False

# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

goal_state = sorted(start_state)

if len(start_state) != 16:
    print "Error: couldn't parse start state file"

print "Start state: "
print_board(tuple(start_state))

start_state_tuple = tuple(start_state)
print "Solving..."
print start_state_tuple
route = solve_heap(start_state_tuple)
# profile.run("route = solve(start_state_tuple)")

print "Solution found in " + str(len(route)/3) + " moves:" + "\n" + route
print "\n"