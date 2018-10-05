# Part 1: The 16-puzzle

Completed by Derrick Eckardt on October 2, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 1 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a1/blob/master/a1-v2.pdf).  This readme file provides the required elements and my discussion of the process and the findings.

## Summary of Problem and Problem Abstraction

We are given a 4 x 4 puzzle board, with tile pieces 1 to 16 that are not numerically in order.  An example board is:

    1  6  3  4
    5  9  7  8
    12 14 10 11
    13 2  15 16

We must find an algorithm using heuristic to put them in order from 1 to 16.  We may only shift a row to the left or the right or a column up or down one tile at a time, with the tiles wrapping around to the other side.  Our algorithm should solve for a board that that requires 12 moves.


**Initial State**: A 4 by 4 board with 16 tiles number from 1 to 16.  The tiles are not in numerical order.

**Goal State**: A 4 by 4 board with the 16 tiles arranged numberically, like so:

    1  2  3  4
    5  6  7  8
    9  10 11 12
    13 14 15 16

**Successor Function**: A single move consists of A) shifting a single row one square over to the left with the left-most tile assuming the far right position, B) shifting a single row one square over to the right with the right-most tile assuming the far left position, C) shifting a single column one square down with the bottom square assuming the top-most position, or D) shifting a single column one square up with the top-most square asumming the bottom-most position.  Since there are four rows and four columns and each can shift in two direction, our successor function calculates 16 possible new successor states.

**State Space**: Our state space is all the possible arrangements of the 16 tiles, which is 16! or approximately 2.1 x 10<sup>13</sup>.  That is a lot of states, for which breadth-first or depth-first searches will only be able to do the simplest of boards in a reasonable amount of time.

**Cost Function**:  No move is more expensive than any other move.  Each move will shift four tiles one square.

**Heuristic Function**: If the learning goal of this part of the assignment of understanding that finding a heuristic function can be incredibly difficult, I 100% achieved this. This was by far the most challenging part of this part of the assignment.  In fact, it deserves its own discussion below.

**Algorithm**: I implemented A-star in order to find my solutions.

## Summary of Observations -- Heuristic Functions are Hard

In my code, you will find 13 heuristic functions for running the code.  Read in order, they display the evolution in my thinking and understanding of a heuristic.  The first few heuristics I used manhattan distance as you would in the 15-puzzle.  I later realized that was in error, because these pieces move differently enough.  If a tile is three tiles away, in actuality, it is only one tile away if you go around the side.  Heuristics one, two, two_mod, three, and four all are variations on this where I either used the value or a subset.  Because of the erros before, these were doomed to fail, since they were not admissable.

In heuristic five, I tired permutation inversions, because, why not?  It was inadmissable as well.

In heuristic, six, I corrected my manhattan distance, and then cleaned it up in heuristic eight (which was actually written before heuristic 7).  Up until this point, I could only solve board2, board4, and board6 in the correct amount of moves. Board8a and board8b took 10 moves instead of 8.  Board 12 was not solvable.  At this point, I could now solve board8a and board8b in a relatively short amount of time.  The heuristic was now admissable, and was providing results that did not violate the triangle inequality, indicating it might also be a consistent heuristic.

Next, I did some research which lead to heuristics seven, nine, and ten.  Since the pieces looked similar to how rubik's cube pieces move, I looked for AI work on it for inspiration.  I found a post on [Stack Overflow about Rubik's cube heuristics](https://stackoverflow.com/questions/36490073/heuristic-for-rubiks-cube).  While not a one-to-one analogy, it gave some interesting ideas.  Alas, they did not work any better, but they are interesting to look at and could possibly lead to a better heuristic one day.

Lastly, I took another fresh look, and worked backwards from solution sets. I noticed that pieces tended to move around in pairs according to where they needed to meet up.  I counted these pairs in eleven and twelve.  No luck.

Of course, each of these also had slightly different versions that did not make the cut, so in total, I probably wrote another dozen that were so bad that they couldn't be put into the code.

In conclusion, writing heuristics is hard.  Lesson well learned.

## Greedy Search Fun

For fun, I changed the algorithm to be a greedy best algorithm, and it solved board12 in just 9 seconds! It only took it 158 moves!

    Start state: 
      5   7   8   1
     10   2   4   3
      6   9  11  12
     15  13  14  16
    Solving...
    (5, 7, 8, 1, 10, 2, 4, 3, 6, 9, 11, 12, 15, 13, 14, 16)
    Fringe.gets  1862
    Solution found in 158 moves:
     R1 L4 R2 D2 L2 U2 U3 R3 D4 L3 D3 D3 R3 U4 L3 U4 R3 D4 R3 U3 R3 D3 L3 L3 U4 R3
     D4 L3 U4 R3 D4 R2 D4 L2 U4 U4 R2 D4 L2 U4 L4 U4 R4 D4 D2 L4 U2 R4 D2 L4 U2 L4
     D2 R4 U2 L4 D2 L4 U2 R4 D2 R4 U2 R4 R4 D2 L4 U2 L4 D2 R4 U2 R4 D2 L4 U2 R4 U2
     L4 D2 R4 U2 L4 U2 L2 D2 R2 U2 R2 U2 L2 D2 L2 U2 R2 D2 R2 U2 L2 R4 U2 L4 D2 L4
     U4 R4 D4 L4 L4 U4 R4 D4 R4 R4 U4 R4 D4 L4 L4 U4 R4 D4 L4 U3 R4 D3 L4 U3 R4 D3
     L4 U3 L4 D3 R4 U3 R4 D3 L4 U4 R4 D4 L4 D4 R2 U4 L2 D4 D4 L3 U4 R3 R2 U4 L2 L3
     D4 R3
 

## Future improvements

A better heuristic.  One day, I will find it.