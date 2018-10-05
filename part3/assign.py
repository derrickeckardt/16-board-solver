#!/usr/bin/env python
# Indiana University Fall 2018 CSCI-B551 Elements of AI
# Assignment 1, Part 3 - Group Assignments
##
###############################################################################
###############################################################################
#
# A full discussion and details can be found in the Readme file for Part 3, 
# which is located at:
# https://github.iu.edu/cs-b551-fa2018/derrick-a1/tree/master/part3
#
###############################################################################
###############################################################################

#

# Import library
import pandas as pd
import sys
from operator import itemgetter

# Get command line inputs
input_file = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

# Optional max consideration for new stages
if len(sys.argv) > 5:
    max_buff = 1+(float(sys.argv[5])/100)
else:
    # not capping it byanything useful way
    max_buff = 100000.0
    
# Define some functions
# Score the group
def score_group(group,m,n):
    # this would be calculated each time someone is added to a group
    # Group structure should be [name, name, name]
    wrong_size = 0
    m_size = 0
    n_size = 0
    for each in group:
        # calculate minutes spent dealing with complaints about group size
        if c_l[c_l['student'] == each]["pref"].values[0] != len(group) and c_l[c_l['student'] == each]["pref"].values[0] != 0:
            wrong_size +=1
        # calculate m for minutes assigned to group for each enemy that is assigned
        enemies = c_l[c_l['student'] == each]["enemies"].values[0].split(",")
        m_size += sum([m if enemy in group else 0 for enemy in enemies])

        # calculate n for minutes assigned to group for each friend that is not assigned
        friends = c_l[c_l['student'] == each]["friends"].values[0].split(",")
        n_size += sum([n if friend not in group and friend != "_" else 0 for friend in friends])
    return wrong_size + m_size + n_size
    
def score_all(groups, k,m,n):
    # this would be used to describe each state
    # we know the theoretical minimum value of this function is class_size / 3 * k.
    # of course, we know that has everyone in groups of 3.
    # Sum all of the individual scores for each group
    all_scores = sum(score_group(each,m,n) for each in groups)
    # calculate k for minutes for number of groups
    k_size = len(groups)*k
    # sum of all score groups plus k* groups
    return all_scores + k_size

def successors(groups):
    successor_set = []
    groups_iter = groups[0] * 1
    for group in groups_iter:
        groups_remaining_subset = groups[0][groups[0].index(group)+1:len(groups[0])] * 1
        # if already a group of 3, can't make a new state with it
        if len(group) < 3:
            for next_group in groups_remaining_subset:
                if len(next_group) +len(group) <=3:
                    # copy the original group
                    new_groups = groups[0] * 1
                    # create a merged group
                    new_groups.append(group+next_group)
                    # delete the previous two individual groups
                    new_groups.remove(group)
                    new_groups.remove(next_group)
                    successor_set.append([new_groups,score_all(new_groups,k,m,n)])
    return successor_set
            
def solve(initial_groups):
    best_groups = initial_groups[0] * 1
    best_score = initial_groups[1] * 1
    fringe = [initial_groups * 1]
    # print "Welcome to the GroupAssign 3000"
    # print "Sorting "+str(len(initial_groups[0]))+" students into groups.  Optimizing for time."
    i = 1
    while len(fringe) > 0:
        # Creates a priority queue
        fringe = sorted(fringe,key=itemgetter(1))
        for groups, score in successors(fringe.pop(0)):
            if score < best_score:
                best_groups = groups *1
                best_score = score
                worst_acceptable_score = float(best_score)*max_buff
            if score < worst_acceptable_score:
                fringe.append([groups,score])
            # Add a differentiator later to throw out bad values
            i += 1
    #         if i%1000==0:
    #             print i," states evaluated so far"
    #             print "Best Score: ", best_score
    #             print "Fringe Size: ",len(fringe)
    # print i," states evaluated in total"
    return best_groups, best_score
    
def print_groups(groups):
    for each in groups:
        line = ""
        for student in each:
            line += student + " "
        line=line.strip()
        print line
    return None

# Step Zero - Read in the datafile as a list of list
c_l = pd.read_csv(input_file, delimiter=" ",header=None,names=['student','pref','friends','enemies'])

# Next Step - Create Initial State
groups  = [[each] for each in c_l['student']]
initial_groups = [groups,score_all(groups,k,m,n)]

# Time to Solve
best_groups, best_score = solve(initial_groups)

# Prinout results
print_groups(best_groups)
print best_score