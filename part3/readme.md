## Part 3: Group Assignments

Completed by Derrick Eckardt on October 2, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 1 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a1/blob/master/a1-v2.pdf).  This readme file provides the required elements and my discussion of the process and the findings.

## Getting Started

As directed in the assignment, to run this program type the following at the command line:

    ./assign.py [input-file] [k] [m] [n]

For a more details on the set-up, please see the [Assignment 1 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a1/blob/master/a1-v2.pdf)

## Summary of Problem

In general, think of this as a search problem.

**Initial State:** Each individual is there own group to start.

**Goal State:** Students organized into groups that minimize faculty time for grading and dealing with unhappy students.

**State Space:** Every possibile combination of groups.  For 50 students, it was on the order of 50!/13!.  Huge! Not actually searchable.

**Successor Function:** Take one group and combine it into the others. Score , and then place into priority queue

**Heurestic Function:** Summing the total amount of time that it would take.  What is interesting, is that I know exactly what that value is.  We are looking for a minimum, and do not know exactly when we will have achieved an acceptable level.

**Cost Function:** Everytime I merge groups, it will change the cost of the time to the faculty.  There is no cost to actually make the changes; however, some changes can reduce the time, and others can increase the time.

## Discussion of Approach

In this, I took a look a locla search approach, where I continuously looked for the best scenario.  In order to get the optimal answer, you would have to search the entire state space.  In that case, one has to determine what is acceptable.

For example, When I used the "ex-assign50.txt" dataset, which was provided by a classmate [Jonathan Branam via Piazza](https://piazza.com/class/jl1erlsbz1n6ax?cid=259) for testing, with an input line of k = 10, m = 10, and n = 2, my initial state had a value of 666 minutes.  Keeping all states, after evaluating 13000 states, it had found a state with a value 284 minutes, and continued to search.  Then, I added pruning, to have it throw away any state that was worse than the current best score.  I found that by pruning, the code speed up significantly (by as much as a factor of 10! on smaller classes) and the results were similar.  For the "ex-assign50.txt" dataset, the new minimum was 289 after 13000 states.  After 400,000+ states, it was still the same 289.  While this is a local minimum, it's pretty damn close.  A trade-off I would be willing to make for time and reduced computing resources.  This reduces the size of the fringe.  I found even a threshold of 1% was 

To enable pruning, I enabled the code to take an additional argument and works by entering the following at the command prompt:

    ./assign.py [input-file] [k] [m] [n] [max-buff]

Where [max-buff] is percent, as a two digit number of how much worse than the best will the program accept keeping.  For example typing a value of 20 for max-buff will prune any state where the state is more than 20% worse than the ideal state.  You can even use a negative value, although not practical.  In practice, a low value, such as 1 is sufficient to make signifcant pruning occur, without too much lost in optimization.

There is a potential limitation, that even with pruning, a solution may not be found in a reasonable time, depending on the complexity of the dataset.  The code would need to be modified to select an appropriate end point.

## Opportunities for Improvement

**Refactor, Refactor, Refactor:** This code runs really slow.  For classes larger than 50, it might be really slow.  Just depends on how fast your comptuer is, and home much time you're willing to wait for an optimized class. There are probably a million ways to refactor the code to improve it.

**Look for Gimmes:** In real life, we would have groups that decided to work together on their own, and their inputs reflect this.  We could change our initial state to combine those that clearily preselected themselves.  This would be a group of 3 where A asked for B and C, B asked for A and C, and C asked for A and B.  This could lead to some suboptimality based on other students desire to work with persons A, B, and C.  This is a tradeoff I would be willing to make since these were students who took the initiative to work together.  Similarily, we could also do this for groups of 2 where they asked to work with each (A puts B, and B puts A).  Of course, they would still be subject to having a third person added, but we get farther down the curve.

**Optimize for Student Happiness, Fewer Complaints, or Fewer Enemies:** This currently optimizes for faculty time.  What it we optimized by student happiness as measured by the percent of people who get exactly what they want? Or, the fewest amount of people that have to work with an enemy?  Ideally, we would spit out multiple best solutions, so that we could then evaluate based on some secondary criteria.  If faculty time is about the same in all of those other cases, wouldn't it best to optimize then for student happiness?