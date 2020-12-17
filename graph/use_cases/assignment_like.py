import numpy as np
import networkx as nx
from networkx.algorithms.flow import maximum_flow
from algorith.graphs.trigraph import NeuralTriGraphCentralVert, min_cover_trigraph_edge_covers_heuristic
from algorith.graphs.graph_utils import create_graph


def create_bipartite_graph(edges,l_caps,r_caps):
    n_edges = np.max(edges)
    g = nx.DiGraph()
    for i in range(len(l_caps)):
        g.add_edge(0,i+1,capacity=l_caps[i],weight=1)
    for i in range(len(r_caps)):
        g.add_edge(i+1+len(l_caps),n_edges+1,capacity=r_caps[i],weight=1)
    for i in edges:
        g.add_edge(i[0],i[1],capacity=np.inf,weight=1)
    g.add_edges_from(edges)
    return g


def make_f_flow(edges,l_caps,r_caps,f):
    """
    See tst2 for sample usage.
    Note: this is sub-optimal and unnecessarily complex.
    """
    n_edges = np.max(edges)
    g = create_bipartite_graph(edges,l_caps,r_caps)
    flow_value, flow_dict = nx.maximum_flow(g, 0, n_edges+1)
    while flow_value < f:
        for i in range(len(l_caps)+len(r_caps)):
            if i<=len(l_caps)-1:
                edge = g[0][i+1]
                flow_val = flow_dict[0][i+1]
            else:
                edge = g[i+1][n_edges+1]
                flow_val = flow_dict[i+1][n_edges+1]
            if edge['capacity'] == flow_val:
                edge['capacity']+=1
                ## If we knew the upwards critical edges, we wouldn't have to run
                # max flow in a loop. 
                # See: http://people.csail.mit.edu/moitra/docs/6854hw4.pdf
                nu_flow_value, nu_flow_dict=nx.maximum_flow(g, 0, n_edges+1)
                if nu_flow_value==flow_value:
                    edge['capacity']-=1
                else:
                    flow_value, flow_dict = nu_flow_value, nu_flow_dict
                if nu_flow_value==f:
                    break
    flow_dict = nx.max_flow_min_cost(g,0,n_edges+1)
    return flow_dict


##########################################
## Test cases
def tst4():
    edges1 = np.array([[1,5],[2,5],[3,7],[4,6]])
    edges2 = np.array([[5,8],[5,9],[5,10],[7,11],[6,11]])
    min_cover_trigraph_edge_covers_heuristic(edges1, edges2)


def tst2():
    edges = np.array([[1,4],[2,4],[3,5]])
    l_caps = np.array([5,3,1])
    r_caps = np.array([4,5])
    flow = make_f_flow(edges,l_caps,r_caps,9)
    return flow

def tst3():
    edges = np.array([[1,4],[2,4],[3,5],[1,5]])
    g = create_graph(edges)
    min_cover = nx.min_edge_cover(g)
    res = set()
    for i in min_cover:
        res.add((min(i),max(i)))
    return res


def tst():
    G = nx.DiGraph()
    edges = [(0, 1, {'capacity': 5, 'weight': 1}),
            (0, 2, {'capacity': 3, 'weight': 0.5}),
            (0, 3, {'capacity': 1, 'weight': 1}),
            (4, 6, {'capacity': 4, 'weight': 1}),
            (5, 6, {'capacity': 5, 'weight': 1}),
            (1, 4, {'capacity': np.inf, 'weight': 1}),
            (2, 4, {'capacity': np.inf, 'weight': 1}),
            (3, 5, {'capacity': np.inf, 'weight': 1})
        ]
    G.add_edges_from(edges)
    mincostflow = nx.max_flow_min_cost(G,0,6)
    mincost=nx.cost_of_flow(G,mincostflow)
    max_flow=nx.maximum_flow_value(G, 0, 6)


