import numpy as np
import networkx as nx
from graphing.special_graphs.neural_trigraph.rand_graph import neur_trig_edges
from graphing.special_graphs.neural_trigraph.path_cover import complete_paths
from graphing.special_graphs.neural_trigraph.path_cover \
            import min_cover_trigraph


def tst1():
    g = nx.DiGraph()

    g.add_edge(4, 6, capacity=1)
    g.add_edge(6, 9, capacity=1)
    g.add_edge(9, 4, capacity=1)

    g.add_edge(4, 8, capacity=1)

    g.add_edge(4, 7, capacity=1)
    g.add_edge(7, 10, capacity=1)
    g.add_edge(10, 4, capacity=1)

    g.add_edge(5, 8, capacity=1)
    g.add_edge(8, 9, capacity=1)
    g.add_edge(10, 5, capacity=1)

    scc = nx.strongly_connected_components(g)
    return scc


def get_toy_graph_matrix():
    l_size = 4
    mid_size = 4
    r_size = 4
    edges1, edges2 = neur_trig_edges(l_size,
                                        mid_size,
                                        r_size,
                                        shuffle_p=0.94)
    paths1 = min_cover_trigraph(edges1, edges2)
    comp_paths = complete_paths(paths1, edges1, edges2)
    edges3 = np.delete(comp_paths, 1, 1)
    m_edges_1 = [
                [[], edges1, []],
                [[], [], edges2],
                [[], [], []]
            ]
    m_edges_2 = [
                [[], edges1, edges3],
                [[], [], edges2],
                [[], [], []]
            ]
    return m_edges_1, m_edges_2
