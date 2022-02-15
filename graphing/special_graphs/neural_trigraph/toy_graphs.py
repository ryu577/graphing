import numpy as np
import networkx as nx


class ToyGraph1():
	edges1 = np.array([
					[1, 5],
					[2, 5],
					[3, 6],
					[3, 7],
					[4, 7]
					])

	edges2 = np.array([
					[5, 8],
					[5, 9],
					[6, 9],
					[6, 10],
					[7, 11]
					])
	probs_left = {1: .25, 2: .25, 3: .25, 4: .25}
	probs_center = {5: .33333, 6: .33333, 7: .33333}
	probs_right = {8: .25, 9: .25, 10: .25, 11: .25}

	# The best solution to the marginal matching problem so far.
	res = {0: {1: 4, 2: 4, 3: 7, 4: 6},
	  1: {5: 4},
	  2: {5: 4},
	  3: {6: 7, 7: 0},
	  4: {7: 6},
	  5: {8: 5, 9: 3},#2
	  6: {9: 2, 10: 5},#2
	  7: {11: 6},#2
	  8: {12: 5},
	  9: {12: 5},
	  10: {12: 5},
	  11: {12: 6},
	  12: {}}

	sc = 0.02154195014671201
