from collections import defaultdict
import queue
import numpy as np


class Node():
    def __init__(self, key="a", val="a", nxt=None, color="wh",
                 pi=None, d=np.inf, f=np.inf):
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

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __neq__(self, other):
        return self.key != other.key

    def __str__(self):
        return str(self.key)


class Graph():
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
    
    def remove_vertices(self, vertices):
        remove_set = set(vertices)
        
        # remove edges from edge set
        self.edges = type(self.edges)(filter(
            lambda e: e[0] not in remove_set and e[1] not in remove_set,
            self.edges))

        # remove edges from adjacency list
        verts = set(self.adj.keys())
        for v1 in verts:
            if v1 in remove_set:
                self.adj.pop(v1)
            else:
                adj_verts = set(self.adj[v1].keys())
                for v2 in adj_verts:
                    if v2 in remove_set:
                        self.adj[v1].pop(v2)
        
        # remove vertices from vertex properties
        for vert in remove_set:
            self.vert_props.pop(vert)

        # remove vertices from sets of white, grey and black vertices
        self.white_verts.difference_update(remove_set)
        self.grey_verts.difference_update(remove_set)
        self.black_verts.difference_update(remove_set)

    def add_edges(self, edges):
        # add edges to edge set
        if type(self.edges) is list:
            self.edges += list(edges)
        elif type(self.edges) is set:
            self.edges = self.edges.union(set(edges))
        elif type(self.edges) is tuple:
            self.edges = tuple(list(self.edges) + list(edges))
        else:
            raise Exception('Invalid type for provided edges. Expected: '
                            + f'list, set, or tuple. Actual: {type(edges)}')

        # add edges to adjacency list, add vertex properties, and add vertices
        # to set of white vertices
        for ed in edges:
            vert_0 = ed[0]
            vert_1 = ed[1]
            self.white_verts.add(vert_0)
            self.white_verts.add(vert_1)
            # Save graph as an adjacency list.
            self.adj[vert_0][vert_1] = 0
            self.vert_props[vert_0] = Node(vert_0)
            self.vert_props[vert_1] = Node(vert_1)

    def print_vert_props(self):
        for k in self.vert_props.keys():
            print(str(self.vert_props[k].__dict__))

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

    def dfs(self):
        for u in self.vert_props.keys():
            if self.vert_props[u].color == "wh":
                self.dfs_visit(u)

    def dfs_visit(self, u):
        self.time += 1
        self.vert_props[u].d = self.time
        self.vert_props[u].color = "gr"
        for v in self.adj[u]:
            if self.vert_props[v].color == "wh":
                self.vert_props[v].pi = u
                self.dfs_visit(v)
        self.vert_props[u].color = "bl"
        self.time += 1
        self.vert_props[u].f = self.time


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
    g1.print_vert_props()
    g2 = Graph(edges)
    g2.dfs()
    g2.print_vert_props()
