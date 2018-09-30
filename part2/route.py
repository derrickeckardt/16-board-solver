#!/usr/bin/env python
# Indiana University Fall 2018 CSCI-B551 Elements of AI
# Assignment 1, Part 2 - Road Trip
#
# As directed in the assignment, to run this program type the following at the command line:
# ./route.py [start-city] [end-city] [routing-algorithm] [cost-function]
#
# where:
# [start-city] and [end-city] are the cities we need a route between.
# [routing-algorithm] is one of:
# - bfs uses breadth-first search, which ignores edge weights in the state graph)
# - uniform is uniform cost search (the variant of bfs that takes edge weights into consideration)
# - dfs uses depth-first search
# - ids uses iterative deepening search
# - astar uses A* search, with a suitable heuristic function
# [cost-function] is one of:
# - segments tries to find a route with the fewest number of "turns" (i.e. edges of the graph)
# - distance tries to find a route with the shortest total distance
# - time tries to find the fastest route, for a car that always travels at the speed limit

# Import libraries
import sys
import pandas as pd

# Define some functions:
# BFS Function and DFS are similarily structured, just how we 
def bfs_function():
    return 0
    
# Cost Function
# DFS Function
# IDS Function
# A* Function


# Get command line inputs
start_city = sys.argv[1]
end_city = sys.argv[2]
routing_algorithm = sys.argv[3]
cost_function = sys.argv[4]

# import roads segments as rs
rs = pd.read_csv('road-segments.txt', delimiter=' ', header=None, names=['city1', 'city2','length','speed_limit','hwy_name'])

# import city sements as cs
cs = pd.read_csv('city-gps.txt', delimiter=' ', header=None, names=['city', 'latitude', 'longitude'])

# Data needs some clean-up as it is not perfectly formed.  Playing around with it
# in the Python console, in the road_segments date file, discovered there were two
# kids of data that were problematic: NaN (null, missing) and  0.0.  There were 19 
# instances where there was no speed limit, and 35 instances where the speed limit was 0.

# Zero Speed Limit Cases:
# The thing was most interesting is that the zero speed limit cases were federal
# interstates.  In the past, we might have been able to assume a federal speed limit
# of 55.  However, that is no longer valid as there is no longer a federal speed
# limit, and each state derives its own speed limit.  Which can vary from 60mph to
# 85 mph, which is a wide variance.  There are two options, we can assume a low speed
# limit, such as the minimum, or bottom quartile value, which won't get anyone 
# into too much trouble, or assume that road can't be  used and remove it from #
# our dataset.  Something to note is that the speed limit is only needed if 
# [cost-function] = time is selected.  So, for [cost-function]  equal to segments
# or distance, we can leave them in, as time is not a critical factor.  Opting to 
# be conservative in our routining for the time option, I eliminated those 35 data
# points if time was entered as the prompt.  

# Null speed limit cases:
# In road segments data, there were 19 data points with a null value.  Again, we
# don't know the values of these.  More so, these are principally located in
# in Nova Scotia, which could have some very different speed limits due to the
# cold, icy, remote nature of nova scotia.  For the sake of being conservative again
# probably best to eliminate those data points as well.

# Cleanup Road Segments data.  Eliminating 54 of 12000+ data points.  Adds a trivial
# amount of suboptimality to the overall solution. 

if cost_function == "time":
    rs=rs[rs.speed_limit!= 0].dropna(how="any")
    print rs.describe()
    print rs.count()
