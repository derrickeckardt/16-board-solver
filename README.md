# CS B551 - Assignment 1: Searching

Completed by Derrick Eckardt on October 2, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 1 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a1/blob/master/a1-v2.pdf)

## Part 0: Getting Started

Completed!  I successfully cloned the repository into my local environment.  Then, I successfully pushed it back to IU github.  Then, I logged into SOIC linux to make sure I was set-up there.  Then, I repeated cloning and pushing back to IU GIthub.  Overall, done!

## Part 1: The 16-puzzle

A full discussion and details can be found in the Readme file for Part 1, which is located at [Part 1 Readme File](https://github.iu.edu/cs-b551-fa2018/derrick-a1/tree/master/part1)

## Part 2: Road Trip!

A full discussion and details can be found in the Readme file for Part 2, which is located at [Part 2 Readme File](https://github.iu.edu/cs-b551-fa2018/derrick-a1/tree/master/part2)

## Part 3: Group Assignments

A full discussion and details can be found in the Readme file for Part 3, which is located at [Part 3 Readme File](https://github.iu.edu/cs-b551-fa2018/derrick-a1/tree/master/part3)

## Extra Credit: Bells and Whistles

Since I submitted it late, I did use the time to add some extra features and run some tests, so that perhaps you would be willing to reduce the 10% penalty.

**Part 1 -- Getting Greedy:** I ran a greedy-best algorithm in addition to A-star to find board12.  Click to the Page 1 readme to find out how that went!

**Part 2 -- Start on a Highway intersection:** For A-star and Greedy, you can start with any highway intersection that is in road segments, and not those in city segments.  For it to work, the highway intersection must be placed in quotes on the input line:

    ./route.py 'Jct_I-75_&_US_31,_Michigan' Alanson,_Michigan greedy time

A future improvement would be so you can also end in any route-segment.  Right now, you can only end in those listed in city-gps.txt

**Part 3 -- Add pruning:** While right now, it will search the entire state space, for larger classes, we might want some pruning available.  By entering an aidditional argument, the user can set a threshold for how high a value.  For large classes, rejecting any state that increases estimated faculty time improves perfomance significantly, with only a small amount of suboptimality introduced.  See [Assignment 3 Read Me](https://github.iu.edu/cs-b551-fa2018/derrick-a1/tree/master/part3) for additional details.

## Future considerations

This could use serious refactoring.  I believe my code got better as I went along.  One thing I would change would be the use of dataframes.  I really didn't take advantage of it, and found working in lists much easier.  I should focus on one data handling method, instead going between the two of them in Parts 2 and 3.

## Overall Thoughts

This stuff is fun.  I have learned a lot, and going through the pain, I feel like I really understand not just the algorithms, but the concepts behind them.

It's also really hard.