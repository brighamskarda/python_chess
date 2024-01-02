New __king_check_moves()

Takes in a node where it is the opponents turn to move, and the depth left to go. (Can use a constant * the number of ticks)

Make sure the node has all of its children moves.

For each child, give it all its children

for each grand child that checks run __king_check_moves again.
