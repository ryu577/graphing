import numpy as np
import networkx as nx
from graphing.toy_graphs.ukraine import ukr_grph_ts

G = nx.DiGraph()

for k in ukr_grph_ts.keys():
    for kk in ukr_grph_ts[k].keys():
        G.add_edge(k, kk, weight=ukr_grph_ts[k][kk], capacity=700)

G.add_edge("s", 'staging-1', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-2', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-3', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-4', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-5', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-6', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-7', weight=0, capacity=np.inf)

G.add_node("s", demand=-5000)
G.add_node("kyiv", demand=3000)
G.add_node("kharkiv", demand=1000)
G.add_node("mariupol", demand=500)
G.add_node("odesa", demand=500)

flowDict = nx.min_cost_flow(G)
