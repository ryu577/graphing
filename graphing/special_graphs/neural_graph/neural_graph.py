import networkx as nx
from networkx.algorithms import bipartite

#idea is the following: 
# 1. create the bipartite graph. split each node v into two nodes v_top and v_bottom, where v_top connects with all outgoing edges of v, 
# and v_bottom connects with all incoming edges of v.
# 2. use max matching in networkx to generate the matching
# 3. recover the path in the transitive closure graph using the bipartite graph matching
# reference: https://towardsdatascience.com/solving-minimum-path-cover-on-a-dag-21b16ca11ac0

def max_matching(g):
    #generate bipartite
    b = nx.Graph()
    top_nodes = []
    bottom_nodes = []
    #generate nodes
    for v in g:
        v_top = str(v) + "t"
        v_bottom = str(v) + "b"
        top_nodes.append(v_top)
        bottom_nodes.append(v_bottom)
    #generate edges
    edges = []
    for v in g:
        nbrs = g[v]
        for u in nbrs:
            v_top = str(v) + "t"
            u_bottom = str(u) + "b"
            edges.append([v_top, u_bottom])
    b.add_nodes_from(top_nodes, bipartite=0)
    b.add_nodes_from(bottom_nodes, bipartite=1)
    b.add_edges_from(edges)

    #calculate maximum cardinality matching
    #matching: a dict maps node to node (both ways, represent edges)
    matching = bipartite.matching.hopcroft_karp_matching(b, top_nodes)

    #generate paths from matching
    #ret type: list of list
    paths = []
    visited_nodes = set()
    for v in sorted(g.keys()):
        path = []
        if v not in visited_nodes:
            visited_nodes.add(v)
            path.append(v)
            v_top = str(v) + "t"
            while v_top in matching:
                u_bottom = matching[v_top]
                u = int(u_bottom[:-1])
                path.append(u)
                visited_nodes.add(u)
                v_top = u_bottom[:-1] + "t"
        if len(path) > 0:
            paths.append(path)
    return paths

#recover the path in the original graph from
# the path in the transitive graph, using the "trans_path" dict
def recover_path(g):
    original_paths = []
    trans_path, trans_dict = transitive_closure(g)
    ret_paths = max_matching(trans_dict)
    for path in ret_paths:
        original_path = []
        for i in range(len(path)-1):
            v = path[i]
            u = path[i+1]
            v_u_path = trans_path[v][u]
            original_path.extend(v_u_path[:-1])
        original_path.append(path[-1])
        original_paths.append(original_path)
    return original_paths

#some of the original_paths may be non-complete. We want to construct the complete path 
#from the first layer to the last layer

#construct parent_dict: maps node v to node v's parent; if no parent, maps to None
def parent_dict(g):
    parent_dict = {}
    for v in g:
        nbrs = g[v]
        for u in nbrs:
            parent_dict[u] = v
    for v in g:
        if v not in parent_dict:
            parent_dict[v] = None
    return parent_dict

def construct_complete_path(g, paths):
    #recover the head part
    parent = parent_dict(g)
    print("parent", parent)
    for i in range(len(paths)):
        path = paths[i]
        while parent[path[0]] != None:
            path = [parent[path[0]]] + path
        paths[i] = path
    # recover the tail part
    for path in paths:
        while len(g[path[-1]]) > 0:
            path.append(g[path[-1]][0])
    return paths

#the main function; combines all previous functions
def min_path_cover(g):
    original_paths = recover_path(g)
    return construct_complete_path(g, original_paths)


if __name__ == "__main__":
    #test case 1
    g1 = {1:[4], 2:[4,5], 3:[5], 4:[6,7], 5:[8], 6:[], 7:[], 8:[]}
    paths = min_path_cover(g1)

    #test case 2
    g2 = {1:[4], 2:[4,5], 3:[5], 4:[6], 5:[6], 6:[]}
    paths = min_path_cover(g2)

    #test case 3
    g3 = {1:[4], 2:[5], 3:[6,7], 4:[8], 5:[8, 9, 10], 6:[10], 7:[9], 8:[11,12], 9:[12],
    10:[12, 13], 11:[], 12:[], 13:[]}
    paths = min_path_cover(g3)

    #test case 4
    g4 = {1:[4], 2:[5], 3:[6,7], 4:[8], 5:[8], 6:[8,9], 7:[10], 8:[11], 9:[11], 10:[12,13,14],
    11:[], 12:[], 13:[], 14:[]}
    paths = min_path_cover(g4)
