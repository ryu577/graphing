from collections import defaultdict
import numpy as np


class Graph():
    def __init__(self,vertices=None):
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

