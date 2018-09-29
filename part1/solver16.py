#!/usr/bin/env python
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#
from Queue import PriorityQueue
from random import randrange, sample
import sys
import string
from operator import add

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
# Changed it to use the stock goal_state so that we did not have sort.  Performance savings.
def is_goal(state):
    return goal_state == list(state) 

# Heuristic Function 1: Number of misplaced tiles
# Worked well for board3,4, and 6. Stalled after board12
def heurisitic_one(state, goal_state):
    heur_one = sum(([1 if state[i-1] != goal_state[i-1] else 0 for i in state ]))
    return heur_one

# Heuristic Function 2: Number of tiles away, manhattan distance
# Best performance to date.  it worked under 0.2 s for up to board 8, which it did in 10 moves
# however, ran for 10 minutes on board12 and would not compute a solution
#in practice, i ended up calculating the difference between the title that is actually there, and what the value should be
def heurisitic_two(state, goal_state):
    heur_two_interim = [ abs(state[i-1]-i) for i in state]
    heur_two_interim = [ (j%4)+(j//4) for j in heur_two_interim]
    heur_two = sum(heur_two_interim)
    return heur_two


def heurisitic_two_mod(state, goal_state):
    heur_two_interim = [ abs(state[i-1]-i) for i in goal_state]
    heur_two_x = [ (j%4) if (j%4) != 3 else 1 for j in heur_two_interim]
    heur_two_y = [ (j//4) if (j//4) !=3 else 1 for j in heur_two_interim]
    heur_two_sum = list( map(add, heur_two_x, heur_two_y)) 
    #print heur_two_sum
    heur_two = float(sum(heur_two_sum))/3.0
    #print heur_two
    return heur_two

def heurisitic_six(state, goal_state):
    corners = [goal_state[0], goal_state[3], goal_state[12], goal_state[15]]
    heur_two_interim = [ abs(state[i-1]-i) for i in corners]
    heur_two_x = [ (j%4) if (j%4) != 3 else 1 for j in heur_two_interim]
    heur_two_y = [ (j//4) if (j//4) !=3 else 1 for j in heur_two_interim]
    heur_two_sum = list( map(add, heur_two_x, heur_two_y)) 
    #print heur_two_sum
    heur_two = float(sum(heur_two_sum))/2.0
    #print heur_two
    return heur_two


# Heuristic Function 3: shortest, longest distance from origin
# Initially thought this might be a good heuristic, as it would prefer the arrangement
# that had the board arranged with the shortest, longest distance between pieces.
# The thought would be that it would focus on the ones that were the least mixed up.
# as i plaayed with it more, realize, that as it got higher the move count had little
# to no impact in my heuristic f(s) calculation
# Also realized it was most likely not admissible, since
# i could end up with the 16 in the 1 slot, which would yield 15, and that would 
# overestimate the cost.
def heurisitic_three(state, goal_state):
    heur_three_interim = [ abs(state[i-1]-i) for i in state]
    heur_three = max(heur_three_interim)
    return heur_three

# Heuristic Function 4: Shortest, longest distance, manhattan distance
# similar to before, but I used the manhattan distance used in #4, but the lostest it would be is 6
# which seems like that would still be admissable.  It did work for upto board 6 in 13 seconds.
def heurisitic_four(state, goal_state):
    heur_four_interim = [ abs(state[i-1]-i) for i in goal_state]
    heur_four = max(heur_four_interim)
    return heur_four


# Heuristic Function 5: Going back to the notes, let's calculate the permutation
# inversion for this board.  In the 8-puzzle, we found it to be inadmissable.  However, there are some differences
# between that puzzle and this puzzle.  First of all, how the pieces move, and 
# that there are 16 puzzle pieces, and not 15.
def heurisitic_five(state, goal_state):
    heur_five_interim = [ abs(state[i-1]-i) for i in goal_state]
#    print "distance slots", heur_two_interim
    #heur_five_interim = [ (j%4)+(j//4) for j in heur_five_interim]
#    print "distance board", heur_two_interim
    heur_five = sum(heur_five_interim)
    return heur_five



# The solver! - using BFS right now
def solve(initial_board):
    fringe = PriorityQueue()
    fringe.put((heurisitic_six(initial_board,goal_state),[(initial_board),"",0]))
    while not fringe.empty() > 0:
        (heuristic_value, fringeitem) = fringe.get()
        [state, route_so_far,moves_so_far] = fringeitem
        # print "state ", state
        # print "heuristic value ", heuristic_value
        # print "heuristic value ", heurisitic_six(state,goal_state) ," + ",moves_so_far
        # print "route_so_far ", route_so_far 
        heuristic_value, moves_so_far, i
        for (succ, move) in successors( state ):
            #print heurisitic_three(succ, goal_state)
            if is_goal(succ):
                return( route_so_far + " " + move )
            fringe.put((heurisitic_six(succ,goal_state)+moves_so_far+1, [(succ), route_so_far + " " + move,moves_so_far+1] ))
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

print "Solving..."
print tuple(start_state)
route = solve(tuple(start_state))

print "Solution found in " + str(len(route)/3) + " moves:" + "\n" + route