import numpy as np
import queue
from graphing.graph import Graph

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


######################
## Test cases..
def tst():
    edges=[[1,0],[0,3],[0,2],[3,2],[2,5],[4,5],[5,6],[2,4]]
    num_verts=7
    g=Graph().init_from_edge_list(num_verts,edges)
    bfs_minimal(g,g.vertices[0])

if __name__=="__main__":
    tst()

