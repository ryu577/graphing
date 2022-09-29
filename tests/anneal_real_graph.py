import numpy as np
import copy
from graphing.special_graphs.neural_trigraph.marginal_matching.\
    anneal.evolutor import Evolutor
from graphing.special_graphs.neural_trigraph.path_cover import\
    min_cover_trigraph, complete_paths
from graphing.special_graphs.neural_trigraph.path_set import\
    path_arr_to_flow_dict, add_one_path, add_path_dicts
from graphing.special_graphs.neural_trigraph.marginal_matching.scoring\
    import score
from graphing.special_graphs.neural_trigraph.marginal_matching.residual_probs import\
    get_residual_targets


def even_probs(arr):
    st = set(arr)
    probs_l = {}
    for ix in st:
        probs_l[int(ix)] = 1/len(st)
    return probs_l


def prep_trigr_edges():
    edges1 = np.loadtxt("edges1.csv")
    edges2 = np.loadtxt("edges2.csv")

    edges1 = edges1.astype(int)
    edges2 = edges2.astype(int)

    # edges1 is 0-indexed, so add 1's
    edges1 += 1
    edges2 += 1
    return edges1, edges2


def tst():
    edges1, edges2 = prep_trigr_edges()

    probs_l = even_probs(edges1[::, 0])
    probs_c = even_probs(edges1[::, 1])
    probs_r = even_probs(edges2[::, 1])

    # Coverage schedule.
    paths1 = min_cover_trigraph(edges1, edges2)
    paths2 = np.array(complete_paths(paths1, edges1, edges2))
    flow_dict_cov = path_arr_to_flow_dict(paths2)

    n = 300
    # Approach-1
    qs_l, qs_c, qs_r = get_residual_targets(paths2, probs_l,
                                            probs_c, probs_r, n)

    ev = Evolutor(qs_l, qs_c, qs_r,
                  edges1, edges2,
                  n-len(paths2))
    ev.anneal(presv_cov=False, n_iter=5000)

    final_pths = add_path_dicts(ev.best_dict, flow_dict_cov)

    scr1 = score(final_pths, probs_l, probs_c, probs_r)

    # Approach-2
    # First create a random set of paths above coverage.
    flow_dict_init = copy.deepcopy(flow_dict_cov)

    for _ in range(n-len(paths2)):
        flow_dict_init = add_one_path(flow_dict_init, edges1, edges2)

    ev1 = Evolutor(probs_l, probs_c, probs_r,
                   edges1, edges2, n,
                   start_dict=flow_dict_init)

    ev1.anneal(presv_cov=True, n_iter=5000)

    scr2 = ev1.min_score

    print("Score for first approach: " + str(scr1))
    print("####################")
    print("Score for second approach: " + str(scr2))

def tst_input_edges(edges1, edges2): 
    probs_l = even_probs(edges1[::, 0])
    probs_c = even_probs(edges1[::, 1])
    probs_r = even_probs(edges2[::, 1])

    # Coverage schedule.
    paths1 = min_cover_trigraph(edges1, edges2)
    paths2 = np.array(complete_paths(paths1, edges1, edges2))
    flow_dict_cov = path_arr_to_flow_dict(paths2)

    n = 300
    # Approach-1
    qs_l, qs_c, qs_r = get_residual_targets(paths2, probs_l,
                                            probs_c, probs_r, n)

    ev = Evolutor(qs_l, qs_c, qs_r,
                  edges1, edges2,
                  n-len(paths2))
    ev.anneal(presv_cov=False, n_iter=5000)

    final_pths = add_path_dicts(ev.best_dict, flow_dict_cov)

    scr1 = score(final_pths, probs_l, probs_c, probs_r)

    # Approach-2
    # First create a random set of paths above coverage.
    flow_dict_init = copy.deepcopy(flow_dict_cov)

    for _ in range(n-len(paths2)):
        flow_dict_init = add_one_path(flow_dict_init, edges1, edges2)

    ev1 = Evolutor(probs_l, probs_c, probs_r,
                   edges1, edges2, n,
                   start_dict=flow_dict_init)

    ev1.anneal(presv_cov=True, n_iter=5000)

    scr2 = ev1.min_score

    return scr1, scr2

if __name__=='__main__':
    edges = [
        (
            np.array([
                [1,12],
                [2,11],
                [3,18],[3,20],
                [4,15],[4,12],
                [5,13],
                [6,14],
                [7,11],[7,19],
                [8,20],[8,11],
                [9,16],
                [10,17]
            ]), 
            np.array([
                [11,24],
                [12,29],[12,23],
                [13,21],
                [14,22],
                [15,27],[15,26],
                [16,26],
                [17,29],
                [18,27],[18,28],
                [19,30],
                [20,25]
            ])
        ),
        (
            np.array([
                [1,16],[1,30],
                [2,16],
                [3,18],[3,20],
                [4,17],[4,19],
                [5,17],
                [6,26],
                [7,21],[7,19],
                [8,20],[8,23],
                [9,16],
                [10,17],
                [11,22],
                [12,25],[12,24],
                [13,28],
                [14,27],[14,29],
                [15,24]
            ]), 
            np.array([
                [16,33],[16,36],[16,38],
                [17,32],
                [18,41],
                [18,31],
                [19,34],
                [20,36],
                [21,33],[21,37],
                [22,39],[22,31],
                [23,37],
                [24,42],
                [25,45],
                [26,43],
                [27,44],
                [28,40],
                [29,41],
                [30,35]
            ])
        )
    ]
    scrs = []
    for edges1, edges2 in edges:
        scr1, scr2 = tst_input_edges(edges1, edges2)
        scrs.append((scr1, scr2))

    print()
    for i in range(len(edges)): 
        print(f'TEST CASE {i+1}')
        print(f'Edges 1: {edges[i][0]}')
        print(f'Edges 2: {edges[i][1]}')
        print(f'Approach 1 score: {scrs[i][0]}')
        print(f'Approach 2 score: {scrs[i][1]}')
        print('###################')