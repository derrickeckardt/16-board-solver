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
# Successor: Adding one individual to an existing group or into a new group 
# Heurestic Function: 
# Cost function: Everytime we add someone on, it will change the amount of time
#     which will increase the amount of time.  The perfect add would decrease
#     the time spent.


print "Oy, vey."