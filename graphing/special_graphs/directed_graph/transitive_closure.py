from collections import defaultdict
import numpy as np


class Graph():
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph = defaultdict(list)
        self.tc_graph = defaultdict(list)
        # Transitive closure.
        self.tc = np.zeros((num_vertices, num_vertices))

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def dfs_traverse(self, s, v):
        self.tc[s][v] = 1
        self.tc_graph[s].append(v)

        for i in self.graph[v]:
            if self.tc[s][i] < 1:
                self.dfs_traverse(s, i)

    def transitive_closure(self):
        for i in range(self.num_vertices):
            self.dfs_traverse(i, i)


def helper(g, trans_path, v):
    """
    input: DAG g as an adjacency list representation
    b is in a's adj list if a --> b
    construct transitive closure g' using DFS
    store a path dict (trans_path), where key = vertice v,
    value = a dict maps reachable nodes u to a path of v to u
    store a graph dict trans_dict (transitive closure of g,
    adjacency list representation)
    for node v, return a dict maps all reachable nodes u to a path of v to u
    """
    if v in trans_path:
        return trans_path
    if len(g[v]) == 0:
        trans_path[v] = {}
        return trans_path
    nbrs = g[v]
    v_dict = {}
    for u in nbrs:
        recur = helper(g, trans_path, u)
        u_dict = recur[u]
        for node in u_dict:
            if node not in v_dict:
                v_dict[node] = [v] + u_dict[node]
        v_dict[u] = [v, u]
    trans_path[v] = v_dict
    return trans_path


def transitive_closure(g):
    trans_path = {}
    trans_dict = {}
    for v in g:
        helper(g, trans_path, v)
    for v in trans_path:
        reachables = []
        reachable_dict = trans_path[v]
        for u in reachable_dict:
            reachables.append(u)
        trans_dict[v] = reachables
    return trans_path, trans_dict


def tst():
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)
    g.transitive_closure()
    print(g.tc)


if __name__ == "__main__":
    print("Running tests for transitive closure.")
    tst()

# References
# [1] https://www.geeksforgeeks.org/transitive-closure-of-a-graph-using-dfs/
# [2] https://www.cs.princeton.edu/courses/archive/spr03/cs226/lectures/digraph.4up.pdf