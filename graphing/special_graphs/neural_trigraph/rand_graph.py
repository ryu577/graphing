import numpy as np
from graphing.special_graphs.neural_trigraph.path_cover\
            import min_cover_trigraph
from graphing.special_graphs.bipartite.rand_graph import bipartite_edges


def neur_trig_edges(left=5, c=4, r=7, shuffle_p=1.0):
    edges1 = bipartite_edges(left, c, shuffle_p)
    edges2 = bipartite_edges(c, r, shuffle_p)
    edges2[:, 0] += left
    edges2[:, 1] += left
    return edges1, edges2


def rep_graph(l_size=7, mid_size=5, r_size=7, reps=42):
    """
    Creates a bigger tri-graph by repeating smaller graphs
    and concatenating all of them a set number of times.
    """
    # The min path cover will be at-least this size.
    trivial_size = max(l_size, mid_size, r_size)
    edges1_fin = []
    edges2_fin = []
    paths1 = []
    for i in range(reps):
        k = 0
        # Only select challenging graphs where min-paths >= trivial_size+2
        while (len(paths1) < trivial_size+2 and k < 100) and (len(paths1) < trivial_size+1 and k < 300):
            k += 1
            edges1, edges2 = neur_trig_edges(l_size,
                                             mid_size,
                                             r_size,
                                             shuffle_p=0.94)
            paths1 = min_cover_trigraph(edges1, edges2)
        edges1[:, 0] += l_size*i
        edges1[:, 1] += l_size * reps + mid_size*i - l_size
        edges2[:, 0] += l_size * reps + mid_size*i - l_size
        edges2[:, 1] += l_size * (reps-1) + mid_size * (reps-1) + r_size*i
        paths1 = []
        if i == 0:
            edges1_fin = np.copy(edges1)
            edges2_fin = np.copy(edges2)
        else:
            edges1_fin = np.concatenate((edges1_fin, np.copy(edges1)))
            edges2_fin = np.concatenate((edges2_fin, np.copy(edges2)))
    return edges1_fin, edges2_fin


if __name__ == "__main__":
    be = bipartite_edges(5, 4)
    print(be)
    tri = neur_trig_edges(5, 4, 8)
    print(tri)
