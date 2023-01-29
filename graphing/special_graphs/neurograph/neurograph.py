import numpy as np
from collections import defaultdict
from graphing.graph import Graph
from graphing.special_graphs.neural_trigraph import\
    unify_edges

## This is actually a trigraph and not a general
# neurograph. TODO: create general neuro graph.
class NeuroGraph(Graph):
    def __init__(self, edges1, edges2):
        self.edges1 = edges1
        self.edges2 = edges2
        edges = unify_edges(edges1, edges2)
        g1 = Graph(edges)

