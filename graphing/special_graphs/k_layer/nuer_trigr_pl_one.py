"""
Special kinds of k-layer graph that is a neural 
trigraph along with one additional layer.
"""
import numpy as np
from graphing.special_graphs.neural_trigraph.path_cover \
    import min_cover_trigraph, min_cover_trigraph_heuristic1


def tst():
    edges1 = np.array([[1,4],[2,4],[2,5],[3,5]])
    edges2 = np.array([[4,6],[4,7],[5,8]])

    paths1 = min_cover_trigraph(edges1,edges2)


