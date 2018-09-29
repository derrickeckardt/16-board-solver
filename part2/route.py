#!/usr/bin/env python
# Indiana University Fall 2018 CSCI-B551 Elements of AI
# Assignment 1, Part 2 - Road Trip
#
# As directed in the assignment, to run this program type the following at the command line:
# ./route.py [start-city] [end-city] [routing-algorithm] [cost-function]
#
# where:
# [start-city] and [end-city are the cities we need a route between.
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

# import roads
road_segments = pd.read_csv('road-segments.txt', delimiter=' ', header=None, names=['city1', 'city2','length','speed_limit','hwy_name'])

# import city sements
city_segments = pd.read_csv('city-gps.txt', delimiter=' ', header=None, names=['city', 'latitude', 'longitude'])

print city_segments[:5]

print road_segments[:5]


# BFS Function
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

