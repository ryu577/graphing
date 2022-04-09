import numpy as np


def bipartite_edges(left=5, r=6, shuffle_p=1.0):
    edges1 = set()
    l_set = set()
    r_set = set()
    while len(l_set) < left or len(r_set) < r:
        l_v = np.random.choice(left, p=gen_p(left, shuffle_p))+1
        r_v = np.random.choice(r, p=gen_p(r, shuffle_p))+left+1
        edges1.add((l_v, r_v))
        l_set.add(l_v)
        r_set.add(r_v)
    edges = []
    for ed in edges1:
        edges.append([ed[0], ed[1]])
    return np.array(edges)


def gen_p(left, shuffle_p=1.0):
    arr = np.arange(left)
    # arr = np.ones(l)
    arr = arr/sum(arr)
    if np.random.uniform() > shuffle_p:
        return arr
    else:
        return np.random.shuffle(arr)
