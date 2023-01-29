import numpy as np
import queue
from collections import defaultdict
from graphing.graph import Node


def dfs(g):
  for u in g.keys():
    if u.color == "wh":
      dfs_visit(g, u)


def dfs_visit(g, u):
  u.color = "gr"
  for v in g[u]:
    if v.color == "wh":
      dfs_visit(g, v)
  u.color = "bl"


def bfs(g, s):
  s.color = "gr"
  q = queue.Queue()
  q.put(s)
  while q.qsize() > 0:
    u = q.get()
    for v in g[u]:
      if v.color == "wh":
        v.color = "gr"
        v.d = u.d + 1
        q.put(v)
    u.color = "bl"
    print(u.key)


def dfs_it(g, u):
    u.color="gr"
    st=[u]
    while len(st)>0:
        u=st[len(st)-1]
        ## Are there any white children remaining?
        remains=False
        for v in g.adj[u]:
            if v.color=="wh":
                remains=True
                v.color="gr"
                st.append(v)
                # Exit the for loop to ensure
                # depth is prioritized. 
                break
        ## Nothing remains; let's remove this vertex.
        if not remains:
            st.pop()
            u.color="bl"


def create_graph(edges=[[1, 2], [1, 3], [1, 4], [2, 4]]):
    # For a given key, we need to make sure there is only
    # one object for it. If there are two objects
    # with the same key, changing the properties of one
    # won't change the properties of the other.
    verts = {}
    g = defaultdict(list)
    for ed in edges:
        if ed[0] in verts.keys():
            vert_0 = verts[ed[0]]
        else:
            vert_0 = Node(ed[0])
            verts[ed[0]] = vert_0
        if ed[1] in verts.keys():
            vert_1 = verts[ed[1]]
        else:
            vert_1 = Node(ed[1])
            verts[ed[1]] = vert_1
        g[vert_0].append(vert_1)
    for v in verts:
        n1 = Node(v)
        if n1 not in g:
            g[n1] = []
    return g, verts


def toy_graph1():
    """
    This graph is taken from figure 22.4
    of "Introduction to Algorithms" by Cormen.
    """
    edges = [['u', 'v'],
             ['u', 'x'],
             ['v', 'y'],
             ['x', 'v'],
             ['y', 'x'],
             ['w', 'y'],
             ['w', 'z'],
             ['z', 'z']
             ]
    # Add a print(u) at the very end of
    # dfs_visit.
    return create_graph(edges)


def toy_graph2():
    """
    This graph is taken from figure 22.3
    of "Introduction to Algorithms" by Cormen.
    Used to demonstrate BFS.
    """
    edges = [['r','s'],
             ['s','r'],
             ['r','v'],
             ['v','r'],
             ['s','w'],
             ['w','s'],
             ['w','t'],
             ['t','w'],
             ['t','x'],
             ['x','t'],
             ['t','u'],
             ['u','t'],
             ['u','x'],
             ['x','u'],
             ['u','y'],
             ['y','u'],
             ['x','y'],
             ['y','x']]
    return create_graph(edges)


def tst1():
    g, verts = toy_graph1()
    print("Before DFS everything is white")
    for v in verts.keys():
        print(verts[v].color)
    dfs(g)
    print("After DFS everything should be black")
    for v in verts.keys():
        print(verts[v].color)
    g, verts = toy_graph1()
    bfs(g, verts['u'])
    print("After BFS everything should be black")
    for v in verts.keys():
        print(verts[v].color)

