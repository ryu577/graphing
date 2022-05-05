import numpy as np
import queue
from graphing.graph import Graph
from collections import defaultdict



class Node():
    def __init__(self,val,nxt=None,color="white",
                pi=None,d=np.inf,key=None):
        self.nxt=nxt
        self.val=val
        self.color=color
        self.pi=pi
        self.d=d
        if key is None:
            self.key=val
        else:
            self.key=key


class Graph():
    def __init__(self, edges, excl_verts={}):
        self.white_verts = set()
        self.grey_verts = set()
        self.black_verts = set()
        self.adj = defaultdict(dict)
        # We'll need the reverse graph as well.
        self.vert_props = {}
        self.edges = edges
        for ed in edges:
            vert_0 = ed[0]
            vert_1 = ed[1]
            if vert_0 not in excl_verts and vert_1 not in excl_verts:
                self.white_verts.add(vert_0)
                self.white_verts.add(vert_1)
                # Save graph as an adjacency list.
                self.adj[vert_0][vert_1] = 0
                self.vert_props[vert_0] = Node(vert_0)
                self.vert_props[vert_1] = Node(vert_1)

    def bfs(self, s):
        self.grey_verts.add(s)
        self.vert_props[s].d = 0
        q = queue.Queue()
        q.put(s)
        while q.qsize() > 0:
            u = q.get()
            for v in self.adj[u]:
                if v in self.white_verts and v not in self.grey_verts\
                 and v not in self.black_verts:
                    self.grey_verts.add(v)
                    self.vert_props[v].d = self.vert_props[u].d + 1
                    self.vert_props[v].pi = u
                    q.put(v)
            self.black_verts.add(u)


def tst2():
    edges = [['s1', 'a'],
             ['s1', 'd'],
             ['a', 'b'],
             ['d', 'b'],
             ['b', 'c'],
             ['d', 'e'],
             ['e', 'c'],
             ['c', 'd1'],
             ['s2', 'd'],
             ['d', 'e'],
             ['e', 'c'],
             ['e', 'f'],
             ['f', 'd2'],
             ['s3', 'g'],
             ['g', 'e'],
             ['e', 'f'],
             ['f', 'd2']]
    g1 = Graph(edges)
    g1.bfs('s1')


def bfs_minimal(g,s):
    s.color="grey"
    q=queue.Queue()
    q.put(s)
    while q.qsize()>0:
        u=q.get()
        for v in g.adj[u]:
            if v.color=="white":
                v.color="grey"
                q.put(v)
        u.color="black"


#####################
# Test cases..
def tst():
    edges = [[1,0], [0,3], [0,2], [3,2], [2,5], [4,5], [5,6], [2,4]]
    num_verts = 7
    g = Graph().init_from_edge_list(num_verts, edges)
    bfs_minimal(g, g.vertices[0])


if __name__ == "__main__":
    tst()
