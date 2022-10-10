from graphing.special_graphs.neural_trigraph.path_set import \
    path_arr_to_flow_dict, add_path_dicts, add_one_path
from graphing.special_graphs.neural_trigraph.marginal_matching.residual_probs \
    import get_residual_targets
from graphing.special_graphs.neural_trigraph.marginal_matching.\
    anneal.evolutor import Evolutor
from graphing.special_graphs.neural_trigraph.marginal_matching.scoring\
    import score
import copy
import numpy as np

def even_probs(arr):
    st = set(arr)
    probs_l = {}
    for ix in st:
        probs_l[int(ix)] = 1/len(st)
    return probs_l   

def _get_other_sim_anneal_args(edges1, edges2, complete_path_cover):
    flow_dict_cov = path_arr_to_flow_dict(complete_path_cover)
    probs_l = even_probs(edges1[::, 0]) 
    probs_c = even_probs(edges1[::, 1])
    probs_r = even_probs(edges2[::, 1])
    return flow_dict_cov, probs_l, probs_c, probs_r

def sim_anneal1(edges1, edges2, complete_path_cover, num_nodes):
    '''
    Simulated annealing with first satisfying coverage constraint with path 
    cover.
    '''
    flow_dict_cov, probs_l, probs_c, probs_r = _get_other_sim_anneal_args(
        edges1, edges2, complete_path_cover)
    qs_l, qs_c, qs_r = get_residual_targets(complete_path_cover, probs_l,
                                            probs_c, probs_r, num_nodes)
    ev = Evolutor(qs_l, qs_c, qs_r,
                  edges1, edges2,
                  num_nodes-len(complete_path_cover))
    ev.anneal(presv_cov=False, n_iter=5000)
    final_pths = add_path_dicts(ev.best_dict, flow_dict_cov)
    scr = score(final_pths, probs_l, probs_c, probs_r)
    return final_pths, scr

def sim_anneal2(edges1, edges2, complete_path_cover, num_nodes):
    '''
    Simulated annealing without first satisfying coverage constraint with path
    cover. 
    '''
    flow_dict_cov, probs_l, probs_c, probs_r = _get_other_sim_anneal_args(
        edges1, edges2, complete_path_cover)
    flow_dict_init = copy.deepcopy(flow_dict_cov)
    for _ in range(num_nodes-len(complete_path_cover)):
        flow_dict_init = add_one_path(flow_dict_init, edges1, edges2)
    ev1 = Evolutor(probs_l, probs_c, probs_r,
                   edges1, edges2, num_nodes,
                   start_dict=flow_dict_init)
    ev1.anneal(presv_cov=True, n_iter=5000)
    final_pths = ev1.best_dict
    scr = ev1.min_score
    return final_pths, scr

def _get_paths_from_dict(path_dict, dfs_stack, path_counts):
    curr = dfs_stack[-1]
    neighbors = path_dict[curr].keys()

    if max(path_dict.keys()) + 1 in neighbors: 
        path = tuple(dfs_stack[1:])
        min_val = float('inf')
        for i in range(len(path) - 1):
            min_val = min(min_val, path_dict[path[i]][path[i+1]])
        if min_val != 0:
            path_counts[path] = min_val 
            for i in range(len(path) - 1):
                path_dict[path[i]][path[i+1]] -= min_val 
        return 

    for neighbor in neighbors: 
        if path_dict[curr][neighbor] == 0: 
            continue 

        dfs_stack.append(neighbor)
        _get_paths_from_dict(path_dict, dfs_stack, path_counts)
        dfs_stack.pop()
        
def get_path_counts(path_dict):
    path_counts = dict() 
    dfs_stack = []
    dfs_stack.append(min(path_dict.keys()))
    _get_paths_from_dict(path_dict, dfs_stack, path_counts)
    dfs_stack.pop()
    return path_counts 

def simulated_annealing(edges1, edges2, complete_path_cover, num_nodes=300,
    sa_choice=0):
    '''
    sa_choice
    0: first approach (coverage constraint met first, then simulated annealing)
    1: second approach (simulated annealing with checking for coverage)
    else: best (lower score) of the previous two approaches
    '''
    if type(edges1) != np.ndarray: 
        edges1 = np.array(edges1)
    if type(edges2) != np.ndarray: 
        edges2 = np.array(edges2)
    if type(complete_path_cover) != np.ndarray:  
        complete_path_cover = np.array(complete_path_cover)

    if num_nodes - len(complete_path_cover) > 0:
        num_nodes -= len(complete_path_cover)

    if sa_choice == 0: 
        path_dict, _ = sim_anneal1(edges1, edges2, complete_path_cover, 
            num_nodes)
    elif sa_choice == 1: 
        path_dict, _ = sim_anneal2(edges1, edges2, complete_path_cover, 
            num_nodes)
    else: 
        path_dict1, scr1 = sim_anneal1(edges1, edges2, complete_path_cover, 
            num_nodes)
        path_dict2, scr2 = sim_anneal2(edges1, edges2, complete_path_cover, 
            num_nodes)
        if scr1 <= scr2: 
            path_dict = path_dict1
        else: 
            path_dict = path_dict2
    path_counts = get_path_counts(path_dict)
    return path_counts