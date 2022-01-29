from graphing.special_graphs.neural_trigraph.central_vert\
    import NeuralTriGraphCentralVert
from graphing.special_graphs.neural_trigraph.neural_trigraph\
    import NeuralTriGraph
from graphing.graph_utils import min_edge_cover
import networkx as nx
import numpy as np
import re


def min_cover_trigraph(edges1, edges2):
    nu = NeuralTriGraph(edges1, edges2)
    nu.create_bipartite_graph()
    flow_val, flow_dict = nx.maximum_flow(nu.flow_graph, 'source', 'sink')
    paths = max_matching_to_paths(flow_dict)
    return paths
    #return complete_paths(paths,edges1,edges2)


def complete_paths(paths, edges1, edges2):
    l_verts = max(edges1[:, 0])
    c_verts = max(edges1[:, 1])
    comp_paths = []
    for pt in paths:
        if len(pt) == 3:
            comp_paths.append(pt)
        elif len(pt) == 2:
            l_layer = 1 if pt[0] <= l_verts else (2 if pt[0] <= c_verts else 3)
            r_layer = 1 if pt[1] <= l_verts else (2 if pt[1] <= c_verts else 3)
            if l_layer == 1 and r_layer == 2:
                third = edges2[edges2[:,0]==pt[1]][0][1]
                comp_paths.append([pt[0],pt[1],third])
            elif l_layer==2 and r_layer==3:
                first = edges1[edges1[:,1]==pt[0]][0][0]
                comp_paths.append([first,pt[0],pt[1]])
            elif l_layer==1 and r_layer==3:
                l_cand = edges1[edges1[:,0]==pt[0]][:,1]
                r_cand = edges2[edges2[:,1]==pt[1]][:,0]
                candidts = [val for val in l_cand if val in r_cand]
                comp_paths.append([pt[0],candidts[0],pt[1]])
        else:
            layer = 1 if pt[0] <= l_verts else (2 if pt[0] <= c_verts else 3)
            if layer == 1:
                c_cand = edges1[edges1[:, 0] == pt[0]][0][1]
                r_cand = edges2[edges2[:, 0] == c_cand][0][1]
                comp_paths.append([pt[0], c_cand, r_cand])
            elif layer == 2:
                l_cand = edges1[edges1[:, 1] == pt[0]][0][0]
                r_cand = edges2[edges2[:, 1] == pt[0]][0][1]
                comp_paths.append([l_cand, pt[0], r_cand])
            else:
                c_cand = edges2[edges2[:, 1] == pt[0]][0][0]
                l_cand = edges1[edges1[:, 1] == c_cand][0][0]
                comp_paths.append([l_cand, c_cand, pt[0]])
    return comp_paths


def edge_cover_heuristic_vert_set(edges1, edges2):
    c1 = min_edge_cover(edges1)
    c2 = min_edge_cover(edges2)
    vert_set = {}
    for e in c1:
        if e[1] not in vert_set:
            tg = NeuralTriGraphCentralVert(e)
            vert_set[e[1]] = tg
        else:
            vert_set[e[1]].add(e)
    for e in c2:
        if e[0] not in vert_set:
            tg = NeuralTriGraphCentralVert(e)
            vert_set[e[0]] = tg
        else:
            vert_set[e[0]].add(e)
    for key in vert_set:
        vert_set[key].edge_counts()
    return vert_set


def vert_set_to_paths(vert_set):
    dat = []
    for k in vert_set.keys():
        l_edges = vert_set[k].l_edges
        r_edges = vert_set[k].r_edges
        n = max(len(l_edges), len(r_edges))
        for i in range(n):
            l_ver = l_edges[i % len(l_edges)]
            r_ver = r_edges[i % len(r_edges)]
            dat.append([l_ver, k, r_ver])
    return dat


def min_cover_trigraph_heuristic1(edges1, edges2):
    v_set = edge_cover_heuristic_vert_set(edges1, edges2)
    return vert_set_to_paths(v_set)


def min_cover_trigraph_edge_covers_heuristic(edges1, edges2):
    return edge_cover_heuristic_vert_set(edges1, edges2)


def obtain_paths(self):
    """
    Used to be a method of NeuralTriGraph. Moved here to avoid circular import.
    the argument, self is an instance of NeuralTriGraph.
    """
    _, flow_dict = nx.maximum_flow(self.flow_graph, 'source', 'sink')
    self.vert_disjoint_paths = max_matching_to_paths(flow_dict)
    final_paths = []
    for pth in self.vert_disjoint_paths:
        if len(pth) == 3:
            final_paths.append(pth)
        elif len(pth) == 2:
            left_layer = self.determine_layer(pth[0])
            right_layer = self.determine_layer(pth[1])
            if left_layer == 0 and right_layer == 2:
                central_candidates = self.layer_1_dict[pth[0]]\
                                .intersection(self.layer_3_dict[pth[1]])
                # Randomly pick a central vertex.
                central = np.random.sample(central_candidates, 1)[0]
                pth1 = [pth[0], central, pth[1]]
                final_paths.append(pth1)
            elif left_layer == 0:
                right_sampled = np.random.sample(self.central_vert_dict[pth[1]]
                                                 .r_edges, 1)[0]
                pth1 = [pth[0], pth[1], right_sampled]
                final_paths.append(pth1)
            elif right_layer == 2:
                left_sampled = np.random.sample(self.central_vert_dict[pth[0]]
                                                .l_edges, 1)[0]
                pth1 = [left_sampled, pth[0], pth[1]]
                final_paths.append(pth1)
    self.final_paths = final_paths


def max_matching_to_paths(flow_dict):
    paths = []; path=[]
    seen_verts = set()
    # Prioritize earlier layers to avoid starting larger paths from the middle,
    # which will incorrectly split them into multiple paths.
    for k in sorted(flow_dict.keys()):
        # What if there is a path that doesn't start at layer0?
        if k.startswith("out_"):
            [_, vert_ind] = [int(st) for st in re.findall(r'\d+',k)]
            if vert_ind not in seen_verts:
                path.append(vert_ind)
                curr_vert = k
                ## Embark on a walk along this path. 
                ## Let's see how long it is.
                #while len(flow_dict[curr_vert])>0:
                while True:
                    flow_out = 0
                    for k1 in flow_dict[curr_vert].keys():
                        if flow_dict[curr_vert][k1]>0:
                            flow_out+=1
                            [nx_layer, nx_vert_ind] = [int(st) for st in re.findall(r'\d+',k1)]
                            curr_vert = "out_layer" + str(nx_layer) \
                                    + "_elem" + str(nx_vert_ind)
                            path.append(nx_vert_ind)
                            seen_verts.add(nx_vert_ind)
                            break
                    if flow_out==0:
                        break
            if len(path)>0:
                paths.append([i for i in path])
                path = []
    return paths


if __name__=="__main__":
    edges1 = np.array([[1,4],[2,4],[2,5],[3,5]])
    edges2 = np.array([[4,6],[4,7],[5,8]])
    v_set = edge_cover_heuristic_vert_set(edges1,edges2)
    paths = vert_set_to_paths(v_set)
    print(paths)
    paths2 = min_cover_trigraph(edges1,edges2)
    print(paths2)

