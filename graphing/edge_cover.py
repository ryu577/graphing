import numpy as np
import networkx as nx
from networkx.algorithms.flow import maximum_flow


def get_min_wts(edges,weights,n_verts):
    min_wts = [np.inf]*n_verts
    for i in range(len(edges)):
        ed = edges[i]
        min_wts[ed[0]-1] = min(min_wts[ed[0]-1],weights[i])
        min_wts[ed[1]-1] = min(min_wts[ed[1]-1],weights[i])
    return min_wts


def tst():
    edges = np.array([
                [1,4],
                [2,4],
                [2,5],
                [3,5],
                [3,4]
            ])
    weights=[1,5,3,2,4]

    n_verts = np.max(edges)
    l_verts = np.max(edges[:,0])
    r_verts = np.max(edges[:,1])

    edges_tilde = np.copy(edges)
    edges_tilde = edges_tilde + n_verts
    min_wts = get_min_wts(edges,weights,5)

    flow_graph = nx.Graph()
    for i in range(len(edges)):
        ed = edges[i]
        flow_graph.add_edge(ed[0],ed[1],capacity=1,\
                weight=weights[i])

    for i in range(len(edges_tilde)):
        ed = edges_tilde[i]
        flow_graph.add_edge(ed[0],ed[1],capacity=1,\
                weight=weights[i])

    for kk in set(edges.flatten()):
        flow_graph.add_edge(kk,kk+n_verts,capacity=1,\
                weight=2*min_wts[kk-1])

    for i in range(l_verts):
        flow_graph.add_edge(0,i+1,capacity=1,\
                weight=1)

    for i in range(n_verts+l_verts,2*n_verts):
        flow_graph.add_edge(0,i+1,capacity=1,\
                weight=1)

    for i in range(l_verts,r_verts):
        flow_graph.add_edge(i+1,2*n_verts+1,capacity=1,\
                weight=1)

    for i in range(n_verts+1,n_verts+1+l_verts):
        flow_graph.add_edge(i,2*n_verts+1,capacity=1,\
                weight=1)
