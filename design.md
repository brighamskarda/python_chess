The new model will by object oriented.

An object will represent the current state of the board.

The current state of the board is the root node.

Generate and score all of the possible moves from the root node. There will be references going
both ways.

From here it will be tick based with a timer you can set:

1. Evaluate any move that puts the king in check.
	
	a. Generate all possible moves for enemy.
	
	b. Make all moves that put the enemy king in check again.

	c. Repeat for the number of times set by a constant variable. (Probably 3 per tick.)

2. Evaluate any moves where a piece is taken

	a. Generate all possible moves for enemy

3. Evaluate any moves where enemy takes a pice

	a. Generate all possible moves for you

4. Evaluate a number of the best performing moves for you. (Use a constant variable)

	a. If the leaf is their move, then take the best case scenario for them, and generate all of
	your possible moves.

	b. If the leaf is you're move, take the best case scenario for you, and generate all of their possible moves.

5. Evaluate a number of moves with the least depth. (Use a constant)

6. If any line leads to a checkmate at all leaves. Take that line.

7. Take the branch with the highest average leaf node score. (This is subject to to change.)


Constants needed:

- CHECK_DEPTH
- NUM_BEST
- NUM_LEAST_DEPTH

Functions needed:

- Score: How far pawns are advanced, how close pieces are to center (excluding king who is neutral),
Material difference, check,
- LeafNodes: Get all of the leaf nodes given a node object.

Node Member Variables Needed:

- board
- score
- takes piece
- children (list of nodes)
- parent (single node)

