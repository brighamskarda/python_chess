# Python Chess

This is a personal project of mine to learn python while tackling the exponentially difficult
problem of playing chess. Python being a rather slow language means that I had to focus
more on optimizing my algorithms rather than brute-forcing the problem.

## How to Run

Before running the chess engine you will need to install the chess module for python.
(```pip install chess```) All development was done in python 3.12, but the code is likely compatible
back to 3.10.

To play against the chess engine run the pychess.py file. It will ask which color you want to play,
and then you enter your moves in the following format: square1square2 ex. e2e4. When it is the
computer's turn give it up to two minutes to think. Most moves will take much less time than this.

If you which to do a basic performance test run the performance.py file. This was mostly used for
development purposes.

## The Journey

Two of the initial goals I had with this project were to understand list comprehension better, and
to do some basic multi-core processing. Additionally I wanted to do some basic machine learning but
after some initial research I realized I wouldn't have the time to do that on this project. The last
remnant of this idea is the name of the chess engine file (mlchess.py)

The first version of the chess engine (commit c3bcd0bd4921c7264403cc0d4f2904589fef890d) was basic
and would evaluate all possible moves to the same depth. It had no storage structure for the
calculations it made, and thus it was difficult to prioritize certain lines over others.

The simple nature of the engine did lend itself easily to the multiprocessing module though. By just
passing a position to each thread, each thread could operate independently and give the position
score for its own position.

While utilizing multiple cores was useful, the lack of a storage structure made it difficult to
compute specific lines of play. After this commit I made a new version of the chess engine with a tree
structure, where each chess position was a node in the tree, with the parent node be the current
position on the board, the children being the possible moves that could be made. This allowed me
to easily traverse through the tree structure and evaluate key moves deeper than others.

Having a tree structure also allowed the computer to remember lines between moves. When the player
makes a move, that section of the tree can be kept, while the rest is pruned.

From there I made many incremental improvements to how the positions are scored and which lines are
explored. I got it to be decently good against the average human. But there is still much
improvement to be made.

The biggest area for improvement is implementing a better min-max algorithm. This is something I
will be researching in the future.

Another area for improvement I see is in reducing duplicate positions. If a position is duplicated,
all references should be pointing to the same place in the tree.
