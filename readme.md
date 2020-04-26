# The 16-puzzle Solved Using A-star Algorithm

The assignment prompt can be found at [Assignment 1 Prompt](https://github.com/derrickeckardt/16-board-solver/blob/master/a1-v2.pdf).  This readme file provides an overview of the problem, key factors, and a discussion of the process and the findings.  I would love to discuss any questions or comments you may have about it.

Completed by Derrick Eckardt as part of CSCI-B551 at Indiana University in Fall 2018.

## To Run Program

The program may be run by typing:

    ./solver16.py boardfile
    
or 

    python solver16.py boardfile
    
where boardfile is a text file with the layout of the board to be solved.  Several are included in the same directory as solver16.py, such as board2, board4, board6, board8a, board8b, board8c, and board12.  The number in the file indicates the minimum number of moves required in an optimal solution.

## Summary of Problem and Problem Abstraction

We are given a 4 x 4 puzzle board, with tile pieces 1 to 16 that are not numerically in order.  An example board is:

    1  6  3  4
    5  9  7  8
    12 14 10 11
    13 2  15 16

We must find an algorithm using a heuristic function to put the tiles in order from 1 to 16.  We may only shift a row to the left or the right or a column up or down one tile at a time, with the tiles wrapping around to the other side.  Our algorithm should solve for a board that that requires up to 12 moves.  Not all boards are solveable.

**Initial State**: A 4 by 4 board with 16 tiles number from 1 to 16.  The tiles are not in numerical order.

**Goal State**: A 4 by 4 board with the 16 tiles arranged numberically, like so:

    1  2  3  4
    5  6  7  8
    9  10 11 12
    13 14 15 16

**Successor Function**: A single move consists of A) shifting a single row one square over to the left with the left-most tile assuming the far right position, B) shifting a single row one square over to the right with the right-most tile assuming the far left position, C) shifting a single column one square down with the bottom square assuming the top-most position, or D) shifting a single column one square up with the top-most square asumming the bottom-most position.  Since there are four rows and four columns and each can shift in two direction, our successor function calculates 16 possible new successor states.

**State Space**: Our state space is all the possible arrangements of the 16 tiles, which is 16! or approximately 2.1 x 10<sup>13</sup>.  That is a lot of states, for which breadth-first or depth-first searches will only be able to do the simplest of boards in a reasonable amount of time.

**Cost Function**:  No move is more expensive than any other move.  Each move will shift four tiles one square.

**Heuristic Function**: If the learning goal of this assignment was to understand the difficulty in finding a heuristic function, it was achieved.  In short, I settled on summing together a variant of a Manhattan-distance at each o the 16 squares.  See the discussion below for further details.

**Algorithm**: I implemented A-star in order to find my solutions.

## Summary of Observations -- Heuristic Functions are Hard

In my code, I tried 13 different heurestic functions.  Some showed early promise, some never worked, and some seem to work really well until a point.  The biggest issue was finding a heuristic function that was not inadmissable.

I did some benchmarking against heuristics used for calculating Rubik's cube, as that problem is analagous to this one: [Stack Overflow about Rubik's cube heuristics](https://stackoverflow.com/questions/36490073/heuristic-for-rubiks-cube). I looked at how the pieces moved and tried one where the pieces were in the correct pairs.  Ultimately, I settled on a version of the Manhattan Distance.  At each square, I evaluated the number in that position from where it should be, since for a square where it was supposed to be, this value would be 0.  Otherwise it was calculated with this function:

```python
def get_manhattan(current, goal):
    distance_x = (goal-1)%4 - (current-1)%4
    distance_y = (goal-1)//4 - (current-1)//4
    d_man_x = 1 if distance_x == 3 or distance_x == -3 else distance_x if distance_x >= 0 else distance_x*-1
    d_man_y = 1 if distance_y == 3 or distance_y == -3 else distance_y if distance_y >= 0 else distance_y*-1
    return (d_man_x**(0.91) + d_man_y**(0.91))**(1.414)
```
As you can see from the last line, the x-distance is raised to 0.91 (10/11), summed to the y-distance raised to 0.91, and that sum is then raised to 1.414 (square root of 2).  I found those numbers by manually fine-tuning them and comparing with the results.

## Speed Matters

In order to calculate board12, my code ends up having to evaluate about 500,000 different boards.  With 16 positions per board, there are number of calculations that have to be done 8,000,000 times.  I found my code actually worked faster with cascading if statements than using simipler forms, such as using absolute value.  This is something that is one of the benefits and drawbacks to python.  There are many different ways to achieve the same item, it's just a question of how you want to do it.  In this case, it results in not the prettiest code, but more effective than many others.