import numpy as np
import networkx as nx

g = nx.DiGraph()

g.add_edge(4,6, capacity=1)
g.add_edge(6,9, capacity=1)
g.add_edge(9,4, capacity=1)

g.add_edge(4,8, capacity=1)

g.add_edge(4,7, capacity=1)
g.add_edge(7,10, capacity=1)
g.add_edge(10,4, capacity=1)

g.add_edge(5,8, capacity=1)
g.add_edge(8,9, capacity=1)
g.add_edge(10,5, capacity=1)

scc=nx.strongly_connected_components(g)


