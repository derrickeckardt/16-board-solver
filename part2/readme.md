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

**Heurestic Function:** On this, for A-star, used a heuristic function to determine how far away we were.  The heuristic for distance chosen is the Haversine distance, which is the distance of two points on a curved surface.  This is admissable since it can never overestimate the distance as actual mileage will be longer.  Further, it is consistent as it still follows the triangle inequality.  This makes uniform cost and A-star prefer the faster (and then shorter) segments

For time, I still had to use Haversine as the starting point, and then divided by the fastest speed limit in the dataset (65mph).  This ensures that the time is never overestimated.  Similar for segments, I divided Haversine distance by the longest road length, was was 923 miles.

The one snag on this, is for A-star, there is virtually no difference between the performance on time, distance, and segments, since they are all effectively using the same heuristic.

Also, A-start using a segments heuristic, is essentially another version of BFS, just not quite as resource intensive.

The heuristic function does run into some trouble, since the latitude and longitude of the highway intersections are not known, which means it's hard to tell where I have moved to.  In order to account for this, the heuristic function uses the last known heuristic value.  On A*, this causes a lot of time to be spent chasing routes that should have been pruned off earlier on.

**Cost Function:** Everytime I merge groups, it will change the cost of the time to the faculty.  There is no cost to actually make the changes; however, some changes can reduce the time, and others can increase the time.

## Summary of Observations

BFS and DFS are both not practical for any long distances because of the high branching factors.  They can handle smaller routes like Bloomington to Louisville, but would never be able to do Los Angeles to New York before this semester was over.  Or if it did, the Burrow SysAdmin would be upset with the amount of resources I used to do so. IDS works a little better because it's light on resource usage, but again, not really effective for anything of significant difference.

Uniform search was very effective, and find results for longer distances in a relatively short amount of time.

A* search was rather disappointing.   Because of the high branching factor, and the inability to accurately measure latitude and longitude for the highway stops, it took a long time to get to answers and stuggled with longer routes.

## Data Cleanup!

It's worth noting, that some data validation had to be done. 

Data needs some clean-up as it is not perfectly formed.  Playing around with it in the Python console, in the road_segments date file, discovered there were two kids of data that were problematic: NaN (null, missing) and  0.0.  There were 19 instances where there was no speed limit, and 35 instances where the speed limit was 0.

### Zero Speed Limit Cases:

The thing was most interesting is that the zero speed limit cases were federal interstates.  In the past, we might have been able to assume a federal speed limit of 55.  However, that is no longer valid as there is no longer a federal speed limit, and each state derives its own speed limit.  Which can vary from 60mph to 85 mph, which is a wide variance.  There are two options, we can assume a low speed limit, such as the minimum, or bottom quartile value, which won't get anyone into too much trouble, or assume that road can't be  used and remove it from our dataset.  Opting to be conservative in our routining for the time option, I eliminated those 35 data points if time was entered as the prompt.  

### Null speed limit cases:

In road segments data, there were 19 data points with a null value.  Again, we don't know the values of these.  More so, these are principally located in in Nova Scotia, which could have some very different speed limits due to the cold, icy, remote nature of nova scotia.  For the sake of being conservative again probably best to eliminate those data points as well.

## Added Features -- Getting Greedy!!

Since I was not really that happy with how any of them came out, I added the ability to do a greedy best-first algorithm.  This works the absolute fastest (less than a second to go across North America!).  It is definitely not optimal.  With the extensive network map, we don't need it.  The answers provided are optimal enough.  As data scientists and engineers, we have to learn how to make tradeoffs between good-enough and optimization.

## Opportunities for Improvement

**Better A-start heuristics for time and segments:** There is likely a better heuristic for time and segments that is not directly proportional to distance.  If we can find that, that might allow for improved performance on those heuristics.

**Refactor, Refactor, Refactor:** This is the trend in my code.  It can be better.  However, as I wrote this one, I could tell I was definitely better than I was on Part 1.  In fact, I was bit overwhelmed when I realized there was no skeleton code!  Yet, it happened!  Future improvements can be made just by refactoring the code and how it handles data.