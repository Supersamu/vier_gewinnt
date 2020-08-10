Project overview:

Goal:
Create a neural net that can play four-in-a-row competently


First, create a batch of neural nets with random weights
Pre-Tournament: Let them train against a player that makes random moves,
reducing the likelihood of illegal moves

Evolutionary Method:
Then, play them against each other in a tournament-fashion,
where top-performers can reproduce and bottom-performers are removed
The top-performing neural nets survive and replicate in a slightly altered form

Traditional Method:
Let them play a batch of games, remembering good moves and bad moves.
For each neural net, change some weights in a random fashion and iterate over the batch,
keeping the changes if they improved the score

Submethods:
- Evolutionary Tournament:
	N number of nets play in a round-robin; One net can play as first and second player
	After the round-robin, the elo score of each neural net is calculated.
	The bottom X% are removed (X = 25?)
	The top X% are allowed to replicate and are slightly altered in the process

How to save the gamestate:
A 3-dimensional matrix;
for each of the two players a layer with a 1 where a ball was placed for that player
For the neural nets, this 3-dimensional matrix is flattened and then put through the neural net

gamelogic.py:

Class board description

Attributes:
- how many rows and columns the board has;
- how many contiguous balls need to be placed for one of the players to win
- a 3-dimensional matrix: 2, num_rows, num_columns
- player on move
- if the gamestate is legal
- the move number

Functions:
- print the board: 1 for player 1, 2 for player 2
- check_if_legal: checks if the move supplied by the neural net is legal
- makemove: makes a move for the current player in the column provided and changes which player is on move
- check_liste: checks if a list contains the necessary number of 1s in a row for one player to win
- check_if_prev_player_has_won: returns True if previous player has made a winning move


matchlogic.py

A match consists of a movelist and a gamestatelist.
These lists have to be splitted into winning moves and their respective gamestates
and losing moves and their respective gamestates
A parameter determines how far back into the match
the winning and losing moves are provided for the neural nets