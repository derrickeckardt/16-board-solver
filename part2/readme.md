## Part 2: Road Trip!

Completed by Derrick Eckardt on October 2, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 1 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a1/blob/master/a1-v2.pdf).  This readme file provides the required elements and my discussion of the process and the findings.

## Getting Started

As directed in the assignment, to run this program type the following at the command line:

    ./route.py [start-city] [end-city] [routing-algorithm] [cost-function]

For a more details on the set-up, please see the [Assignment 1 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a1/blob/master/a1-v2.pdf)

## Summary of Problem

**Initial State:** A city somewhere in the U.S. or Canada.  This is [start-city] and this is located in the city_segments.txt file.

**Goal State:** A city somewhere in the U.S. or Canada.  This is [end-city] and this is located in the city_segments.txt file.

**State Space:** Any of the points (cities and highway junctions) in between.  In a road network with over 12000 edges, there are a lot of different ways to go from one city to another.  Further, many of these points are well connected, so there is a high branching factor.

**Successor Function:** Moving along one road segment (from road-segments.txt) file.

**Edge Weight**:  Here, the program has three different methods for optimizing.  Either time, distance, or segments.  Segments, is analagous to the number of terms.  This what we would normally thing of for breadth first search (BFS), Depth First Search (DFS), or Iterative Depth First Search (IDS). In those, we go down a number of steps, and we don't care about the weights of the edges.  In those, we can't actually optimize for time or distance.  In DFS, we can't even optimize for segments.

**Heurestic Function:** On this, for A*star, used a heuristic function to determine how far away we were.  The heuristic for distance chosen is the Havershine distance, which is the distance of two points on a curved surface.  This is admissable since it can never overestimate the distance as actual mileage will be longer.  Further, it is consistent as it still follows the triangle inequality.

For time, I still had to use Havershine as the starting point, and then divided by the fastest speed limit in the dataset (65mph).  This ensures that the time is never overestimated.

The heuristic function does run into some trouble, since the latitude and longitude of the highway intersections are not known, which means it's hard to tell where I have moved to.  In order to account for this, the heuristic function uses the last known heuristic value.  On A*, this causes a lot of time to be spent chasing routes that should have been pruned off earlier on.

**Cost Function:** Everytime I merge groups, it will change the cost of the time to the faculty.  There is no cost to actually make the changes; however, some changes can reduce the time, and others can increase the time.

## Summary of Observations

BFS and DFS are both not practical for any long distances because of the high branching factors.  They can handle smaller routes like Bloomington to Louisville, but would never be able to do Los Angeles to New York before this semester was over.  Or if it did, the Burrow SysAdmin would be upset with the amount of resources I used to do so. IDS works a little better because it's light on resource usage, but again, not really effective for anything of significant difference.

Uniform search was very effective, and find results for longer distances in a relatively short amount of time.

A* search was rather disappointing.   Because of the high branching factor, and the inability to accurately measure latitude and longitude for the highway stops, 

## Added Features

Since I was not really that happy with how any of them came out, I added the ability to do a greedy best-first algorithm.  This works the absolute fastest and most realibly.  This works