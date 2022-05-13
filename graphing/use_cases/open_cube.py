import numpy as np
import queue
from collections import defaultdict
from itertools import combinations


def tst():
    edges = [['-00','0+0'],#2
             ['-00','0-0'],#1
             ['-00','00-'],#5
             ['-00','00+'],#8
             ['0-0','00+'],
             ['0-0','00-'],#12
             ['0-0','+00'],
             ['0+0','00+'],
             ['0+0','00-'],#11
             ['0+0','+00'],
             ['+00','00+'],#7
             ['+00','00-']]
    survive = {3, 10, 11, 8, 5}
    gr = Graph_cube(edges, survive)
    gr.dfs('00+')


def tst_all_combo():
    lst = [1,2,3,4]
    for combo in combinations(lst, 3):
        print(combo)


class Node():
    def __init__(self, val, nxt=None, color="white",
                 pi=None, d=np.inf, f=np.inf):
        self.nxt = nxt
        self.val = val
        self.color = color
        self.pi = pi
        self.d = d
        self.f = f
        self.x = char2coord(val[0])
        self.y = char2coord(val[1])
        self.z = char2coord(val[2])
        self.x1 = 0
        self.y1 = 0


def char2coord(ch):
    if ch == '0':
        return 0
    elif ch == '+':
        return 1
    elif ch == '-':
        return -1


class Graph_cube():
    def __init__(self, edges, survive_ros={}):
        self.white_verts = set()
        self.grey_verts = set()
        self.black_verts = set()
        self.adj = defaultdict(dict)
        self.vert_props = {}
        self.cov_p = set()
        self.edges = edges
        self.time = 0
        for ix in range(len(edges)):
            ed = edges[ix]
            vert_0 = ed[0]
            vert_1 = ed[1]
            if ix in survive_ros:
                self.white_verts.add(vert_0)
                self.white_verts.add(vert_1)
                # Save graph as an adjacency list.
                self.adj[vert_0][vert_1] = 0
                self.adj[vert_1][vert_0] = 0
                self.vert_props[vert_0] = Node(vert_0)
                self.vert_props[vert_1] = Node(vert_1)

    def print_vert_props(self):
        for k in self.vert_props.keys():
            print(str(self.vert_props[k].__dict__))

    def dfs(self, u):
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                if self.vert_props[v].x != self.vert_props[u].x:
                    if (self.vert_props[u].x1+1, self.vert_props[u].y1) not in self.cov_p:
                        self.vert_props[v].x1 = self.vert_props[u].x1+1
                    else:
                        self.vert_props[v].x1 = self.vert_props[u].x1-1
                    self.vert_props[v].y1 = self.vert_props[u].y1
                else:
                    if (self.vert_props[u].x1, self.vert_props[u].y1+1) not in self.cov_p:
                        self.vert_props[v].y1 = self.vert_props[u].y1+1
                    else:
                        self.vert_props[v].y1 = self.vert_props[u].y1-1
                    self.vert_props[v].x1 = self.vert_props[u].x1

                self.cov_p.add((self.vert_props[v].x1, self.vert_props[v].y1))
                self.dfs(v)
        self.vert_props[u].color = "black"

