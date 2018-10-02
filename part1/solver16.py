#!/usr/bin/env python
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#

# hit segmentation fault, which means th
from Queue import PriorityQueue
from random import randrange, sample
import sys
import string
from operator import add
from math import sqrt

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

# Produces the x-y coordinates for a given tile on a grid of (0,3) by (0,3), where 0,0 is the upper left
def get_coordinates(tile):
    tile_x = (tile-1)%4
    tile_y = (tile-1)//4   #offsetting by one ensures that 16 doesn't yield y=4, since our grid only goes from 0 to 3
    return tile_x, tile_y

# Gets the manhattan distance of a tile from where it is to where it is in the goal state
def get_manhattan(current, goal):
    if current == goal:
        return 0
    else:
        current_x,current_y = get_coordinates(current)
        goal_x,goal_y = get_coordinates(goal)
        if abs(goal_x - current_x) == 3:
            d_man_x=1
        else:
            d_man_x= abs(goal_x - current_x)
        if abs(goal_y - current_y) == 3:
            d_man_y=1
        else:
            d_man_y= abs(goal_y - current_y)
        return d_man_x + d_man_y

def get_manhattan_euclid(current, goal):
    if current == goal:
        return 0
    else:
        current_x,current_y = get_coordinates(current)
        goal_x,goal_y = get_coordinates(goal)
        if abs(goal_x - current_x) == 3:
            d_man_x=1
        else:
            d_man_x= abs(goal_x - current_x)
        if abs(goal_y - current_y) == 3:
            d_man_y=1
        else:
            d_man_y= abs(goal_y - current_y)
        return sqrt(d_man_x^2 + d_man_y^2)




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
    heur_two = float(sum(heur_two_sum))/4.0
    #print heur_two
    return heur_two

# Proper Manhattan Distance inspired by the excerpt referenced in the question:
# https://stackoverflow.com/questions/36490073/heuristic-for-rubiks-cube
# Since this movement is similar to that of a rubik's cube, thought it might be helpful
def heurisitic_seven(state, goal_state):
    corners = [1,4,13,16]
    edges = [2,3,5,8,9,12,14,15]
    middles = [6,7,10,11]
    heur_seven_corners = [get_manhattan(state[i-1],i) for i in corners]
    heur_seven_corners = float(sum(heur_seven_corners)) / 2.0
    heur_seven_edges = [get_manhattan(state[i-1],i) for i in edges]
    heur_seven_edges = float(sum(heur_seven_edges)) / 4.0
    heur_seven_middles = [get_manhattan(state[i-1],i) for i in middles]
    heur_seven_middles = float(sum(heur_seven_middles)) / 2.0
    return sqrt(max([heur_seven_corners,heur_seven_edges,heur_seven_middles]))

# 
def heurisitic_eight(state, goal_state):
    heur_seven_interim = [get_manhattan(state[i-1],i) for i in goal_state]
    heur_seven = float(sum(heur_seven_interim)) / 4.0
    return heur_seven

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

def heurisitic_nine(state, goal_state):
    heur_one = float(sum(([1 if state[i-1] != goal_state[i-1] else 0 for i in state ])))
    return heurisitic_eight(state, goal_state) / heur_one

def heurisitic_ten(state, goal_state):
    heur_seven_interim = [get_manhattan_euclid(state[i-1],i) for i in goal_state]
    heur_seven = float(sum(heur_seven_interim)) / 4.0
    return heur_seven

# Trying whole new tact.  We will count the number of rows that do not have the 3 or 4 
# of the correct tiles in them.  Right before a final stage, it will have 4 rows of
# 3 out of 4 and 4 rows out of 4 with the right configuration.  Should also be
# admissable since when we are two 

# Look for number of pairs that are in the correct order (1,2),(2,3) (3,4) (4,1)
def heurisitic_eleven(state,goal_state):
    pairs_in_order = 0
    for j in range (0,16,4):
        for i in range(0+j,3+j):
            if state[i] != state[i+1] - 1:
                pairs_in_order += 1
    # Checking wrap around
        if state[j] != state[j+3] + 1:
            pairs_in_order += 1
    return float(pairs_in_order)/1.0

# Look for number of vertical pairs, and then take the max
# of this or heuristic_eleven
def heurisitic_twelve(state,goal_state):
    pairs_in_order = 0
    for j in range (0,12,4):
        for i in range(0+j,4+j):
            if state[i] != state[i+4] - 4:
                pairs_in_order += 1
    # Checking wrap around
    for j in range (12,16):
        if state[j] != state[j-12] - 4:
            pairs_in_order += 1
    return min([float(pairs_in_order),heurisitic_eleven(state,goal_state),heurisitic_eight(state,goal_state)])/1.0
    
    

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
    fringe.put((heurisitic_eight(initial_board,goal_state),[(initial_board),"",0]))
    visited_states =[]
    i = 1
    while not fringe.empty() > 0:
        (heurisitic_value, fringeitem) = fringe.get()
        [state, route_so_far,moves_so_far] = fringeitem
        if i%1000 == 0:
            print "i ",i
            print "state ", state
            print "heuristic value ", heurisitic_value
            print "heuristic value ", heurisitic_twelve(state,goal_state) ," + ",moves_so_far
            print "route_so_far ", route_so_far 
        #heuristic_value, moves_so_far, i
        for (succ, move) in successors( state ):
            if is_goal(succ):
                print "Fringe.gets ",i
                return( route_so_far + " " + move )
            if succ not in visited_states:
                fringe.put((heurisitic_eight(succ,goal_state)+moves_so_far+1, [(succ), route_so_far + " " + move,moves_so_far+1] ))
                visited_states.append(succ)
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

print "Solving..."
print tuple(start_state)
route = solve(tuple(start_state))

print "Solution found in " + str(len(route)/3) + " moves:" + "\n" + route