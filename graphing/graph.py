from collections import defaultdict
import queue
import numpy as np


class Node1():
    def __init__(self, key="a", color="w"):
        self.color = color
        self.key = key

    def __hash__(self):
        return self.key

    def __eq__(self, other):
        return self.key == other.key

    def __neq__(self, other):
        return self.key != other.key

    def __str__(self):
        return str(self.key)


## Under construction, doesn't work as expected.
def dfs(g):
  for u in g.keys():
    if u.color == "w":
      dfs_visit(u, g)


def dfs_visit(u, g):
  u.color = "gr"
  for v in g[u]:
    if v.color == "w":
      dfs_visit(v, g)
  u.color = "bl"


def bfs(g, s):
  s.color = "gr"
  q = queue.Queue()
  q.put(s)
  while q.qsize() > 0:
    u = q.get()
    for v in g[u]:
      if v.color == "w":
        v.color = "gr"
        v.d = u.d + 1
        q.put(v)
    u.color = "bl"


def tst1():
    edges = [[1,2],[1,3],[1,4], [2,4]]
    g = defaultdict(list)
    for ed in edges:
        vert_0 = Node1(ed[0])
        vert_1 = Node1(ed[1])
        g[vert_0].append(vert_1)
    return g



## The graph is clr_traversal is superior to this and
# should be used instead of this for most purposes.
class Graph():
    def __init__(self, vertices=None):
        ##We'll assume for now a staggered array.
        self.adj=[]
        self.vertices=vertices

    def init_from_edge_list(self,num_verts,edges):
        self.vertices = [Node(i) for i in range(num_verts)]
        self.adj = defaultdict(list)
        self.adj_lst = defaultdict(list)
        self.edges = edges
        self.num_verts = num_verts
        for ed in edges:
            vert_0 = self.vertices[ed[0]]
            vert_1 = self.vertices[ed[1]]
            self.adj[vert_0].append(vert_1)
            self.adj_lst[ed[0]].append(ed[1])
        return self


class Node():
    def __init__(self,val,next=None,color="white",
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

