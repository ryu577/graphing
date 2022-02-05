import numpy as np
from graphing.special_graphs.neural_trigraph.marginal_matching.anneal.evolutor import Evolutor


def get_probs(arr):
    st = set(arr)
    probs_l = {}
    for ix in st:
        probs_l[int(ix)] = 1/len(st)
    return probs_l

edges1 = np.loadtxt("edges1.csv")
edges2 = np.loadtxt("edges2.csv")

edges1 = edges1.astype(int)
edges2 = edges2.astype(int)

# edges1 is 0-indexed, so add 1's
edges1 += 1
edges2 += 1

probs_l = get_probs(edges1[::, 0])
probs_c = get_probs(edges1[::, 1])
probs_r = get_probs(edges2[::, 1])

ev = Evolutor(probs_l, probs_c, probs_r, edges1, edges2, 280)

ev.anneal()
