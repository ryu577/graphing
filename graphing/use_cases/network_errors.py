import queue
from collections import defaultdict
import numpy as np


class Node():
    def __init__(self, val, nxt=None, color="white",
                 pi=None, d=np.inf, key=None):
        self.nxt = nxt
        self.val = val
        self.color = color
        self.pi = pi
        self.d = d
        if key is None:
            self.key = val
        else:
            self.key = key


class Graph():
    def __init__(self, edges):
        self.white_verts = set()
        self.grey_verts = set()
        self.black_verts = set()
        self.adj = defaultdict(dict)
        # We'll need the reverse graph as well.
        self.adj_rev = defaultdict(dict)
        self.vert_wts = {}
        for ed in edges:
            vert_0 = ed[0]
            vert_1 = ed[1]
            self.white_verts.add(vert_0)
            self.white_verts.add(vert_1)
            # Save graph as an adjacency list.
            self.adj[vert_0][vert_1] = 0
            # We need both the regular graph and reversed graph.
            self.adj_rev[vert_1][vert_0] = 0
            self.vert_wts[vert_0] = 0
            self.vert_wts[vert_1] = 0

    def bfs_probs(self, s):
        self.vert_wts[s] = 1
        self.grey_verts.add(s)
        q = queue.Queue()
        q.put(s)
        while q.qsize() > 0:
            u = q.get()
            for v in self.adj[u]:
                if v in self.white_verts:
                    self.grey_verts.add(v)
                    q.put(v)
                self.adj[u][v] += self.vert_wts[u]/len(self.adj[u])
                self.vert_wts[v] += self.vert_wts[u]/len(self.adj[u])
            self.vert_wts[u] = 0
            self.black_verts.add(u)


def tst():
    # This kind of graph is not split neatly into layers.
    # So, one iteration of bfs is not enough.
    edges = [['s', 'a'],
             ['a', 'c'],
             ['s', 'e'],
             ['s', 'b'],
             ['b', 'd'],
             ['e', 'd'],
             ['c', 'd'],
             ['a', 'e']]
    g1 = Graph(edges)
    g1.bfs_probs('s')
    edges = [['s1', 'a'],
             ['s1', 'd'],
             ['a', 'b'],
             ['d', 'b'],
             ['b', 'c'],
             ['d', 'e'],
             ['e', 'c'],
             ['c', 'd1']]
    g2 = Graph(edges)
    g2.bfs_probs('s1')
