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
# Initial State: A blank list of groups
# Goal State: All students assigned to a group
# Successor: Adding one individual to an existing group or into a new group.  So, 
#    for each next state, we would have all the remaining individuals yet to be assigned.
# Heurestic Function: Summing the total amount of time that it would take
# Cost function: Everytime we add someone on, it will change the amount of time
#     which will increase the amount of time.  The perfect add would decrease
#     the time spent.


print "Oy, vey."

# Import library
import pandas as pd
import sys

# Get command line inputs
input_file = sys.argv[1]
k = sys.argv[2]
m = sys.argv[3]
n = sys.argv[4]


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
class_list = pd.read_csv(input_file, delimiter=" ",header=None,names=['student','pref','friends','enemies'])

print class_list 
# Next Step - 

