import networkx as nx
import numpy as np


## How do we express a matching? Its a set of edges.
class Matching():
    def __init__(self,edges,wts,gr):
        self.graph=gr
        self.mtch={}
        for i in range(len(edges)):
            self.mtch[edges[i]] = wts[i]
        self.l_verts_covered = set()
        self.r_verts_covered = set()
        for e in edges:
            self.l_verts_covered.add(e[0])
            self.r_verts_covered.add(e[1])


class Graph():
    def __init__(self,edges):
        self.verts = set()
        self.l_verts= set()
        self.r_verts = set()
        for e in edges:
            self.l_verts.add(e[0])
            self.r_verts.add(e[1])


if __name__=="__main__":
    edges=[[1,3],
            [1,4],
            [2,4],
            [2,5],
            [2,6],
            [2,7]]
    wts = [.4,.4,.1,.33,.33,.33]

