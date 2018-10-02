# Part 1: The 16-puzzle

Completed by Derrick Eckardt on October 2, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 1 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a1/blob/master/a1-v2.pdf).  This readme file provides the required elements and my discussion of the process and the findings.

## Summary of Problem

We are given a 4 x 4 puzzle board, with tile pieces 1 to 16 that are not numerically in order.  An example board is:

''' python
1 6 3 4
5 9 7 8
12 14 10 11
13 2 15 16
'''

We must find an algorithm using heuristic to put them in order from 1 to 16.  We may only shift a row to the left or the right or a column up or down one tile at a time, with the tiles wrapping around to the other side.  Our algorithm should solve for a board that that requires 12 moves.

## Problem Abstraction

*Initial State*: A 4 by 4 board with 16 tiles number from 1 to 16.  The tiles are not in numerical order.

*Goal State*: A 4 by 4 board with the 16 tiles arranged numberically, like so:

''' python
1  2  3  4
5  6  7  8
9  10 11 12
13 14 15 16
'''

*Successor Function*: A single move consists of A) shifting a single row one square over to the left with the left-most tile assuming the far right position, B) shifting a single row one square over to the right with the right-most tile assuming the far left position, C) shifting a single column one square down with the bottom square assuming the top-most position, or D) shifting a single column one square up with the top-most square asumming the bottom-most position.  Since there are four rows and four columns and each can shift in two direction, our successor function calculates 16 possible new successor states.

*State Space*: Our state space is all the possible arrangements of the 16 tiles, which is 16! or approximately 2.1 x 10<sup>13</sup>.  That is a lot of states, for which breadth-first or depth-first searches will only be able to do the simplest of boards in a reasonable amount of time.

*Cost Function*:  No move is more expensive than any other move.  Each move will shift four tiles one square.

*Heuristic Function*: This was by far the most challenging part of this part of the assignment.  
