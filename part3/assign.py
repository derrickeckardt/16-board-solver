#!/usr/bin/env python
# Indiana University Fall 2018 CSCI-B551 Elements of AI
# Assignment 1, Part 3 - Group Assignments
#
# As directed in the assignment, to run this program type the following at the command line:
# ./assign.py [input-file] [k] [m] [n]
# 
# Where:
# [input-file] is the name of the text file that has everyone's preferences
# [k] is the minutes it takes to grade
# [m] is the minutes it takes to meet with the professor for everyone assigned
#     with someone they did not want to be assigned to
# [n] is the minutes it takes to respond to email  for every person not assigned
#     to their goup
#
# In general, think of this as a search problem.
# 
# Initial State: Each individual is there own group
# 
# Goal State: Students organized into groups that minimize faculty time.
#
# Successor: Take one group and combine it into the others. Score it, and then place
# into priority queue
#
# Heurestic Function: Summing the total amount of time that it would take.
#
# Cost function: Everytime we merge groups, it will change the cost to the faculty


print "Oy, vey."

# Import library
import pandas as pd
import sys

# Get command line inputs
input_file = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

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
    # Sum all of the individual scores for each group
    all_scores = sum(score_group(each,m,n) for each in groups)
    # calculate k for minutes for number of groups
    k_size = len(groups)*k
    # sum of all score groups plus k* groups
    return all_scores + k_size

# Given the scoring factors, there are somethings I can do to help myself, by
# simplifying the initial state.  Students have already done some work to make
# life easier on me
# 
# First: Look for groups of 3 that self-selected themselves together.  ie, person A said 
# they wanted B & C; B said they wanted A & c; C said they wanted A & B
# 
# Second: Look for a person A and B that self-selected themselves together.  They 
# will be placed into a group, with a slot available for a third person.  Later 
# on, we may have to add a third person.  If they didn;t ask for a third person, 
# if they complain about group size, it's only a 1 minute penalty per person for
# an otherwise happy group.
#
# These first two steps optimize for groups that were already formed and want to
# work together.  I'm going to assume this is optimal.  Now, there probably some chance
# this could actually be suboptimal, such as if there is a student in very
# high demand, such that a number greater than 2 persons wanted to work with them.
# There might be some optimally lost by actually breaking up the group.  As the course
# instructor, I'm willing to accept that if people self-organize, I'm willing take
# a short-term penalty for long-term student happiness.
# 
# These assumptions allow us to also reduce the number of future states to explore
# which makes our life a lot easier.

# Once completed, I will test all of these assumptions out by not letting them by
# used, and having the algorithm try to optimize.
#
# Test case ex-assign50 was provide by classmate Jonathan Branam via:
# https://piazza.com/class/jl1erlsbz1n6ax?cid=259 which linked to:
# https://gist.github.com/jonathanbranam/c2b121237d1954c574b0a2bbc075e662

# Step Zero - Read in the datafile as a list of list
c_l = pd.read_csv(input_file, delimiter=" ",header=None,names=['student','pref','friends','enemies'])

# Next Step - Create Initial State
groups  = [[each] for each in c_l['student']]
initial_groups = [groups,score_all(groups,k,m,n)]