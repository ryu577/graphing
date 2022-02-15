import numpy as np
from collections import defaultdict
from graphing.graph import Graph, remove_zeros
import copy


class PathSet():
    def __init__(self, path_graph, graph=None, edges1=None, edges2=None):
        """
        path_list is a dictionary of dictionaries
        """
        self.path_graph = path_graph
        self.orig_graph = graph
        self.edges1 = edges1
        self.edges2 = edges2


def remove_one_path(path_graph, dest=None, preserv_cov=False):
    """
    Removes one path from the path set in a way that
    the vertices covered by the set of paths does not
    decrease.
    """
    complete = False
    ix = 0
    if dest is None:
        dest = max(list(path_graph.keys())) + 1
    while not complete:
        ix += 1
        if ix == 100:
            print(res)
            raise Exception("Looks like a near infinite loop.")
        res1 = copy.deepcopy(path_graph)
        # First, remove one path.
        # 0 is the source and the source connects to the first layer.
        strt_key = np.random.choice(list(res1[0].keys()))            
        if len(res1[strt_key]) == 1 and list(res1[strt_key].values())[0] == 1\
                and preserv_cov:
            continue
        res1[0][strt_key] -= 1
        
        scnd_key = np.random.choice(list(res1[strt_key].keys()))
        if len(res1[scnd_key]) == 1 and list(res1[scnd_key].values())[0] == 1\
                and preserv_cov:
            continue
        res1[strt_key][scnd_key] -= 1
        
        thrd_key = np.random.choice(list(res1[scnd_key].keys()))
        if res1[thrd_key][dest] == 1 and preserv_cov:
            continue
        res1[scnd_key][thrd_key] -= 1
        res1[thrd_key][dest] -= 1
        complete = True
    return remove_zeros(res1)


def add_one_path(path_graph, edges1, edges2):
    res1 = copy.deepcopy(path_graph)
    dest = max(edges2[::, 1]) + 1
    strt_ix = np.random.choice(edges1[::, 0])
    if strt_ix in res1[0]:
        res1[0][strt_ix] += 1
    else:
        res1[0][strt_ix] = 1
    
    mid_ix = np.random.choice(edges1[edges1[::, 0] == strt_ix][::, 1])
    if strt_ix in res1 and mid_ix in res1[strt_ix]:
        res1[strt_ix][mid_ix] += 1
    elif strt_ix in res1:
        res1[strt_ix][mid_ix] = 1
    else:
        res1[strt_ix] = {}
        res1[strt_ix][mid_ix] = 1
    
    end_ix = np.random.choice(edges2[edges2[::, 0] == mid_ix][::, 1])
    if mid_ix in res1 and end_ix in res1[mid_ix]:
        res1[mid_ix][end_ix] += 1
    elif mid_ix in res1:
        res1[mid_ix][end_ix] = 1
    else:
        res1[mid_ix] = {}
        res1[mid_ix][end_ix] = 1

    if end_ix in res1:
        res1[end_ix][dest] += 1
    else:
        res1[end_ix] = {}
        res1[end_ix][dest] = 1
    return res1


def path_arr_to_flow_dict(path_arr, dest=None):
    if dest is None:
        dest = np.max(path_arr) + 1
    flow_dict = defaultdict(dict)
    flow_dict[0] = {}
    for pth in path_arr:
        [l1, l2, l3] = pth
        if l1 in flow_dict[0]:
            flow_dict[0][l1] += 1
        else:
            flow_dict[0][l1] = 1
        if l2 in flow_dict[l1]:
            flow_dict[l1][l2] += 1
        else:
            flow_dict[l1][l2] = 1
        if l3 in flow_dict[l2]:
            flow_dict[l2][l3] += 1
        else:
            flow_dict[l2][l3] = 1
        if dest in flow_dict[l3]:
            flow_dict[l3][dest] += 1
        else:
            flow_dict[l3][dest] = 1
    return flow_dict


def add_path_dicts(pth1, pth2):
    pth_res = copy.deepcopy(pth1)
    for k in pth2.keys():
        for kk in pth2[k].keys():
            if k in pth_res and kk in pth_res[k]:
                pth_res[k][kk] += pth2[k][kk]
            elif k in pth_res:
                pth_res[k][kk] = pth2[k][kk]
            else:
                pth_res[k] = {kk: pth2[k][kk]}
    return pth_res

