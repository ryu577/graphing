import networkx as nx
import numpy as np


def get_schedule(probs_left, probs_right, edges, num_nodes=20):
    source = 0
    dest = np.max(edges)+1
    left_max_ix = max(edges[::, 0])
    right_max_ix = max(edges[::, 1])
    g = nx.DiGraph()

    for v in probs_left.keys():
        cap = int(probs_left[v]*num_nodes)
        g.add_edge(source, v, capacity=cap, weight=1/(cap+1e-3))

    for u, v in edges:
        g.add_edge(u, v, capacity=np.inf, weight=1)

    for v in probs_right.keys():
        cap = int(probs_right[v]*num_nodes)
        g.add_edge(v, dest, capacity=cap, weight=1/(cap+1e-3))

    flowed = 0
    while flowed < num_nodes:
        print("Now running networkx max-flow-min-cost " + str(right_max_ix))
        # res_dict = nx.max_flow_min_cost(g, source, dest)
        res_val, res_dict = nx.maximum_flow(g, source, dest)
        flowed = res_val
        if np.random.uniform() > 0.5:
            h = np.random.choice(left_max_ix) + 1
            g[0][h]['capacity'] += 1
        else:
            v = np.random.choice(np.arange(left_max_ix+1, right_max_ix+1))
            g[v][dest]['capacity'] += 1

    return res_dict


def tst():
    probs_left = {1: .3333, 2: .33333, 3: .33333}
    probs_right = {4: .25, 5: .25, 6: .25, 7: .25}
    edges = np.array([
                    [1, 4],
                    [1, 5],
                    [2, 4],
                    [3, 5],
                    [3, 6],
                    [3, 7]
    ])
    res = get_schedule(probs_left, probs_right, edges)

