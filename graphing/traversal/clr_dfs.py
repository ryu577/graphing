import collections
import numpy as np


def dfs_visit_minimal(g,u):
    u.color="grey"
    for v in g.adj[u]:
        if v.color=="white":
            dfs_visit_minimal(g,v)
    u.color="black"

def dfs_minimal(g):
    for v in g.vertices:
        if v.color=="white":
            dfs_visit_minimal(g,v)
            # Can replace with iterative ver.

def dfs_minimal_it(g,u):
    u.color="grey"
    st=[u]
    while len(st)>0:
        u=st[len(st)-1]
        ## Are there any white children remaining?
        remains=False
        for v in g.adj[u]:
            if v.color=="white":
                remains=True
                v.color="grey"
                st.append(v)
                # Exit the for loop to ensure
                # depth is prioritized. 
                break
        ## Nothing remains; let's remove this vertex.
        if not remains:
            st.pop()
            u.color="black"


## Applications of dfs:
# For topological sorting see: algorith\leetc\graphs\course_schedule_2.py
# For detecting cycles see: algorith\leetc\graphs\course_schedule.py
