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
from operator import itemgetter
import math

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

# Solve BFS Function
def solve_BFS(start_city,end_city):
    print 'Solving with BFS...'
    fringe = [[start_city, 0, 0, str(start_city)+" "]]
    while len(fringe) > 0:
        [current_city, distance_so_far, time_so_far, route_so_far] = fringe.pop(0)
        for city, distance, time in successors( current_city):
            # Check to see if city has not been visited already on this route
            # if so, we've backtracked, and will move on to the next successor.
            if (city+",") not in route_so_far:
                if city==end_city:
                    return str(distance_so_far+distance) + " " + str(time_so_far+time) + " " + route_so_far + city
                fringe.append([city, distance_so_far+distance, time_so_far + time, route_so_far  + city + " "])
    return False

# Solve DFS Function
# originally I had this combined with BFS since there was one difference.  However,
# the only way I could figure out was to use an if statement on each iteration
# which was way too many operations. I rather have longer code than fewer, clunkier
# function.  Of course, there might have been a more graceful way than I was I thinking
# of doing it.  A better coder might see a cleaner way to incorporate them.

# since IDF is a version of DFS which goes with DFS as well.  For DFS, we set it to 
# an absurdly high level, effectively infiniti.  This allows us to us the same 
# function for IDS and DFS
def solve_DFS(start_city,end_city,routing_algorithm):
    if routing_algorithm == "dfs":
        print "Solving with DFS..."
        start_depth = 1000000 
    elif routing_algorithm == "ids":
        print "Solving with IDS..."
        start_depth = 1
    for i in range(start_depth,1000001):
        # print "depth = ",i
        fringe = [[start_city, 0, 0, str(start_city)+" ",0]]
        while len(fringe) > 0:
            [current_city, distance_so_far, time_so_far, route_so_far,depth_so_far] = fringe.pop()
            for city, distance, time in successors( current_city):
                # Check to see if city has not been visited already on this route
                # if so, we've backtracked, and will move on to the next successor.
                if (city+" ") not in route_so_far:
                    if city==end_city:
                        return str(distance_so_far+distance) + " " + str(time_so_far+time) + " " + route_so_far + city
                    if depth_so_far+1 != i: # 
                        # print "Depth ",depth_so_far+1
                        fringe.append([city, distance_so_far+distance, time_so_far + time, route_so_far  + city + " ",depth_so_far+1])
    return False

# DFS can't get anything in reasonable amount of time.  With 12000 road segments,
# it's really easy for the it to take a route away from the segment, and just keep
# moving around.  IDS helps brings tames thafot, and makes it much easier to actually
# find something.  DFS is suboptimal, but it runs much faster than BFS in most cases
# since it saves on the amount of states it saves in the fringe.

# Solve Uniform Cost
def solve_Uniform(start_city,end_city, cost_function):
    print 'Solving with Uniform Cost with a cost function of ' +cost_function + '...'
    fringe = [[start_city, 0, 0, str(start_city)+" "]]
    goal_time = 1000000
    goal_distance = 1000000
    goal_route = ""
    if cost_function == "distance":
        cost_column = 1
    elif cost_function == "time":
        cost_column = 2
    elif cost_function == "segments":
        #bfs stops when it finds it, and goes segment by segment.  reuse that code here.
        return solve_BFS(start_city,end_city)
    while len(fringe) > 0:
        # Learned how to sort list of list from, and then applied it to my case
        # https://stackoverflow.com/questions/5201191/method-to-sort-a-list-of-lists
        fringe = sorted(fringe, key=itemgetter(cost_column))
        #print fringe
        [current_city, distance_so_far, time_so_far, route_so_far] = fringe.pop(0)
        # print distance_so_far, " ",goal_distance, " | ", time_so_far, " ", goal_time
        if (goal_time < time_so_far and cost_column == 2) or (goal_distance < distance_so_far and cost_column ==1):
            return "yes "+str(goal_distance) + " " + str(goal_time) + " " + goal_route
        for city, distance, time in successors( current_city):
            # Check to see if city has not been visited already on this route
            # if so, we've backtracked, and will move on to the next successor.
            if (city+" ") not in route_so_far:
                if city==end_city and ((goal_time > time_so_far + time and cost_column == 2) or (goal_distance > distance_so_far + distance and cost_column ==1)):
                    goal_distance = distance_so_far + distance
                    goal_time = time_so_far + time
                    goal_route = route_so_far + city
#                    print "GOAL: "+str(goal_distance) + " " + str(goal_time) + " " + goal_route
                else:
                    fringe.append([city, distance_so_far+distance, time_so_far + time, route_so_far  + city + " "])
    return False

# Heuristic Function - Halversine Distance
# The straight line distance between two cities is the heuristic of choice.
# Since the Earth is curved, will use a haversine distance, as opposed the euclidian distance.
# Since this is a known calculation, updated code from the following for htis purpose:
# https://gist.github.com/rochacbruno/2883505
# Github gists are available with the above attribution.
#
# If I complete cotnrol over environment, would use the Halverson library available
# through Pypi
def heuristic_halversine(start_city, end_city):
    lat1, lon1 = cs[cs['city'] == start_city].values[0][1:3]
    lat2, lon2 = cs[cs['city'] == end_city].values[0][1:3]
    radius = 3959 # miles

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def heuristic_halversine_time(start_city,end_city):
    # Distance is still the best heuristic, but since we want to optimize for time
    # Will use find the distance and then fastest U.S. speed limit of 85mph to
    # keep it admissable
    time = float(heuristic_halversine(start_city,end_city))
    return time/85.0

# Solve A*
def solve_Astar(start_city,end_city,cost_function):
    fringe = [heuristic_halversine(start_city,end_city), [start_city, 0, 0, str(start_city)+" ",0]]
    visited_segments =[]
    i = 1
    while len(fringe) > 0:
        print fringe
        [heurisitic_value, fringeitem] = fringe.pop(0)
        print heurisitic_value
        print fringeitem
        [current_city, distance_so_far, time_so_far, route_so_far,depth_so_far] = fringeitem
        for city, distance, time in successors(current_city):
            if (city+" ") not in route_so_far:
                if city==end_city:
                    print "Fringe.gets ",i
                    return str(distance_so_far+distance) + " " + str(time_so_far+time) + " " + route_so_far + city
                if city in cs['city'].values.tolist():
                    # If the road segment city is in city-gps file, recalculate city
                    fringe.append([heuristic_halversine(city,end_city),[city, distance_so_far+distance, time_so_far + time, route_so_far  + city + " ",depth_so_far+1]])
                else:
                    # If the road segment city is not in city_gps, will estimate the heuristics by taking the previous heuristic value and subtracting the road length
                    # This could result in some oddities such as a "negative" heuristic. This will be corrected once the route comes across a city that is in city_segments
                    # This keeps our heuristic admissable since it will be underestimating our heuristic.
                    # Future improvement, move this logic into the heurestic function.  This keeps
                    fringe.append([heurisitic_value-distance,[city, distance_so_far+distance, time_so_far + time, route_so_far  + city + " ",depth_so_far+1]])
        i += 1
    return False


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


# Check to see if start city and end city are possible city pairs, kick out if not
##############################################################
# Still to do!
##############################################################
##############################################################

if cost_function == "segments" or cost_function== "distance" or cost_function == "time":
    if start_city not in cs['city'].values.tolist() or end_city not in cs['city'].values.tolist():
        los_gehts = "'start_city' or 'end_city' is not in city-gps.txt.  Please check your input for any potential errors."
    elif routing_algorithm == "bfs":     
        los_gehts = solve_BFS(start_city,end_city)
    elif routing_algorithm == "dfs":
        los_gehts = solve_DFS(start_city,end_city, routing_algorithm)
    elif routing_algorithm == "ids":
        los_gehts = solve_DFS(start_city,end_city, routing_algorithm)
    elif routing_algorithm == "uniform":
        los_gehts = solve_Uniform(start_city,end_city, cost_function)
    elif routing_algorithm == "astar":
        los_gehts = solve_Astar(start_city,end_city, cost_function)
    else:
        los_gehts = "Valid routing_algorithm not found. Only 'bfs', 'dfs', 'ids', 'uniform', and 'astar' are accepted. Please check your input for any potential errors."
else:
    los_gehts = "Valid cost_function not found.  Only 'segments', 'distance', and 'time' are accepted.  Please check your input for any potential errors."

print los_gehts if los_gehts else "Sorry, no solution found. :("