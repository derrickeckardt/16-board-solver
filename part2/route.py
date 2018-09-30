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

# Import command Prompt Values
start_city = sys.argv[1]
end_city = sys.argv[2]
routing_algorithm = sys.argv[3]
cost_function = sys.argv[4]


# Define some functions:
def successors(start_city):
    successor_cities = rs[(rs.city1==start_city)][["city2", "length","time"]].values.tolist()
    successor_cities += rs[(rs.city2==start_city)][["city1", "length","time"]].values.tolist()
    return successor_cities

# Solve BFS and DFS Function
def solve_BFS(start_city,end_city,routing_algorithm):
    fringe = [[start_city, 0, 0, str(start_city)+","]]
    # if routing_algorithm == "bfs":
    #     r_a = 0
    # elif routing_algorithm == "dfs":
    #     r_a = int()
    while len(fringe) > 0:
        [current_city, distance_so_far, time_so_far, route_so_far] = fringe.pop()
        for city, distance, time in successors( current_city):
            # Check to see if city has not been visited already on this route
            # if so, we've backtracked, and will move on to the next successor.
            if (","+city+",") not in route_so_far:
                if city==end_city:
                    return str(distance_so_far+distance) + " " + str(time_so_far+time) + " " + route_so_far + city
                fringe.append([city, distance_so_far+distance, time_so_far + time, route_so_far  + city + ","])
    return False

# Solve Uniform Cost

# Solve IDS

# Solve A*



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
# our dataset.  Opting to be conservative in our routining for the time option, 
# I eliminated those 35 data points if time was entered as the prompt.  

# Null speed limit cases:
# In road segments data, there were 19 data points with a null value.  Again, we
# don't know the values of these.  More so, these are principally located in
# in Nova Scotia, which could have some very different speed limits due to the
# cold, icy, remote nature of nova scotia.  For the sake of being conservative again
# probably best to eliminate those data points as well.

# Cleanup Road Segments data.  Eliminating 54 of 12000+ data points.  Adds a trivial
# amount of suboptimality to the overall solution. 

rs=rs[rs.speed_limit!= 0].dropna(how="any")

# Calculate time column and add to datatable
rs['time'] = rs.length / rs.speed_limit

# print "Appleton,_Wisconsin"
# successors("Appleton,_Wisconsin")
# print "Jct_FL_417_&_E-W_Expwy,_Florida"
# successors("Jct_FL_417_&_E-W_Expwy,_Florida")

# print "Los_Angeles,_California"
# successors("Los_Angeles,_California")

los_gehts = solve_BFS(start_city,end_city, routing_algorithm)
print los_gehts if los_gehts else "Sorry, no solution found. :("