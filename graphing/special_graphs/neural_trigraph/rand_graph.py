import numpy as np
import networkx as nx


def bipartite_edges(l=5,r=6,shuffle_p=1.0):
    edges1 = set()
    l_set=set(); r_set=set()
    while len(l_set)<l or len(r_set)<r:
        l_v = np.random.choice(l,p=gen_p(l,shuffle_p))+1
        r_v = np.random.choice(r,p=gen_p(r, shuffle_p))+l+1
        edges1.add((l_v,r_v))
        l_set.add(l_v); r_set.add(r_v)
    edges=[]
    for ed in edges1:
        edges.append([ed[0],ed[1]])
    return np.array(edges)

def gen_p(l,shuffle_p=1.0):
    arr = np.arange(l)
    #arr = np.ones(l)
    arr = arr/sum(arr)
    if np.random.uniform()>shuffle_p:
        return arr
    else:
        return np.random.shuffle(arr)


def neur_trig_edges(l=5,c=4,r=7,shuffle_p=1.0):
    edges1 = bipartite_edges(l,c)
    edges2 = bipartite_edges(c,r)
    edges2[:,0] += l
    edges2[:,1] += l
    return edges1, edges2


if __name__=="__main__":
    be = bipartite_edges(5,4)
    print(be)
    tri = neur_trig_edges(5,4,8)
    print(tri)

