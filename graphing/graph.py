from collections import defaultdict
import numpy as np


class Graph():
    def __init__(self, vertices=None):
        ##We'll assume for now a staggered array.
        self.adj=[]
        self.vertices=vertices

    def init_from_edge_list(self,num_verts,edges):
        self.vertices = [Node(i) for i in range(num_verts)]
        self.adj = defaultdict(list)
        for ed in edges:
            vert_0 = self.vertices[ed[0]]
            vert_1 = self.vertices[ed[1]]
            self.adj[vert_0].append(vert_1)
        return self


class Node():
    def __init__(self,val,next=None,color="white",\
                pi=None,d=np.inf,key=None):
        self.next=next
        self.val=val
        self.color=color
        self.pi=pi
        self.d=d
        if key is None:
            self.key=val
        else:
            self.key=key


def remove_zeros(res):
    """
    res is expected to be a dictionary of dictionaries
    representing a flow graph.
    """
    res1 = {}
    for k in res.keys():
        res2 = {}
        for kk in res[k].keys():
            if res[k][kk] > 0:
                res2[kk] = res[k][kk]
        if len(res2) > 0:
            res1[k] = res2
    return res1

