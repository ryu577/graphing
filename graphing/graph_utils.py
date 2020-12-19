import numpy as np
import networkx as nx


def create_graph(edges):
    """
    Convert a collection of edges into networkx graph.
    """
    g = nx.Graph()
    for i in edges:
        g.add_edge(i[0],i[1],capacity=np.inf,weight=1)
    return g


def min_edge_cover(edges):
    g=create_graph(edges)
    mc = nx.min_edge_cover(g)
    res = set()
    for i in mc:
        res.add((min(i),max(i)))
    return res

