import numpy as np
import queue
from collections import defaultdict
from itertools import combinations


lst = [1,2,3,4]
for combo in combinations(lst, 3):
    print(combo)


edges = [['-00', '0+0'],  #2
         ['-00', '0-0'],  #1
         ['-00', '00-'],  #5
         ['-00', '00+'],
         ['0-0', '00+'],
         ['0-0', '00-'],
         ['0-0', '+00'],
         ['0+0', '00+'],
         ['0+0', '00-'],
         ['0+0', '+00'],
         ['+00', '00+'],
         ['+00', '00-']]


class Graph1():
    def __init__(self, edges, excl_verts={}):
        self.white_verts = set()
        self.grey_verts = set()
        self.black_verts = set()
        self.adj = defaultdict(dict)
        # We'll need the reverse graph as well.
        self.vert_props = {}
        self.edges = edges
        self.time = 0
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


class Node():
    def __init__(self, val, nxt=None, color="white",
                 pi=None, d=np.inf, f=np.inf, key=None):
        self.nxt = nxt
        self.val = val
        self.color = color
        self.pi = pi
        self.d = d
        self.f = f
        if key is None:
            self.key = val
        else:
            self.key = key
