import numpy as np
import networkx as nx
from graphing.toy_graphs.ukraine import ukr_grph_ts

G = nx.DiGraph()

for k in ukr_grph_ts.keys():
    for kk in ukr_grph_ts[k].keys():
        G.add_edge(k, kk, weight=int(100*ukr_grph_ts[k][kk]), capacity=730)

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

##########################

ix_map = {'staging-1':1, 'staging-2':2, 'staging-3':3, 'staging-4':4, 'staging-5':5, 'staging-6':6, 'staging-7':7, 'kyiv':8}
i = 9
for k in ukr_grph_ts.keys():
    if k not in ix_map:
        ix_map[k] = i
        i+=1

from ortools.graph import pywrapgraph

min_cost_flow = pywrapgraph.SimpleMinCostFlow()

for k in ukr_grph_ts.keys():
    for kk in ukr_grph_ts[k].keys():
        min_cost_flow.AddArcWithCapacityAndUnitCost(ix_map[k], ix_map[kk], 800,
                                                1+int(ukr_grph_ts[k][kk]))


min_cost_flow.AddArcWithCapacityAndUnitCost(0, 1, 90000, 0)
min_cost_flow.AddArcWithCapacityAndUnitCost(0, 2, 90000, 0)
min_cost_flow.AddArcWithCapacityAndUnitCost(0, 3, 90000, 0)
min_cost_flow.AddArcWithCapacityAndUnitCost(0, 4, 90000, 0)
min_cost_flow.AddArcWithCapacityAndUnitCost(0, 5, 90000, 0)
min_cost_flow.AddArcWithCapacityAndUnitCost(0, 6, 90000, 0)
min_cost_flow.AddArcWithCapacityAndUnitCost(0, 7, 90000, 0)

min_cost_flow.SetNodeSupply(0, 5000)
min_cost_flow.SetNodeSupply(ix_map["kyiv"], -3000)
min_cost_flow.SetNodeSupply(ix_map["kharkiv"], -1000)
min_cost_flow.SetNodeSupply(ix_map["mariupol"], -500)
min_cost_flow.SetNodeSupply(ix_map["odesa"], -500)


status = min_cost_flow.Solve()

if status != min_cost_flow.OPTIMAL:
    print('There was an issue with the min cost flow input.')
    print(f'Status: {status}')
    exit(1)
print('Minimum cost: ', min_cost_flow.OptimalCost())
print('')
print(' Arc   Flow / Capacity  Cost')
for i in range(min_cost_flow.NumArcs()):
    cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
    print('%1s -> %1s    %3s   / %3s   %3s' %
          (min_cost_flow.Tail(i), min_cost_flow.Head(i),
           min_cost_flow.Flow(i), min_cost_flow.Capacity(i), cost))
