import numpy as np
import networkx as nx
from graphing.special_graphs.neural_trigraph.path_cover import *
from graphing.special_graphs.neural_trigraph.rand_graph import *
import matplotlib.pyplot as plt

if __name__=="__main__":
    diffs = []
    for i in range(100):
        edges1, edges2 = neur_trig_edges(7,5,8)

        paths1 = min_cover_trigraph(edges1,edges2)
        paths2 = min_cover_trigraph_heuristic1(edges1,edges2)

        print("optimal has: " + str(len(paths1)) + " paths")
        print(paths1)
        print("heuristic has: " + str(len(paths2)) + " paths")
        print(paths2)
        diffs.append(len(paths2)-len(paths1))
    plt.hist(diffs)
    plt.show()

