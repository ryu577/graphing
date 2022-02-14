import numpy as np
import copy
from graphing.special_graphs.neural_trigraph.marginal_matching.\
    anneal.evolutor import Evolutor
from graphing.special_graphs.neural_trigraph.path_set import PathSet
from graphing.special_graphs.neural_trigraph.path_cover import\
    min_cover_trigraph, complete_paths
from graphing.special_graphs.neural_trigraph.path_set import\
    path_arr_to_flow_dict, add_one_path, add_path_dicts
from graphing.special_graphs.neural_trigraph.marginal_matching.scoring\
    import score
from collections import Counter


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


def get_residual_targets(paths, probs_l, probs_c, probs_r, n):
    xs_l = Counter(paths[::,0])
    xs_c = Counter(paths[::,1])
    xs_r = Counter(paths[::,2])
    qs_l = residual_probs(probs_l, xs_l, n)
    qs_c = residual_probs(probs_c, xs_c, n)
    qs_r = residual_probs(probs_r, xs_r, n)
    return qs_l, qs_c, qs_r


def residual_probs(ps, xs, n):
    n2 = sum(list(xs.values()))
    qs = {}
    summ = 0
    for k in ps.keys():
        qs[k] = max((ps[k]*n - xs[k])/n2, 0)
        summ += max((ps[k]*n - xs[k])/n2, 0)
    for k in qs.keys():
        qs[k] /= summ
    return qs


edges1, edges2 = prep_trigr_edges()

probs_l = even_probs(edges1[::, 0])
probs_c = even_probs(edges1[::, 1])
probs_r = even_probs(edges2[::, 1])


## Coverage schedule.
paths1 = min_cover_trigraph(edges1, edges2)
paths2 = np.array(complete_paths(paths1, edges1, edges2))
flow_dict_cov = path_arr_to_flow_dict(paths2)


n = 300
## Approach-1
qs_l, qs_c, qs_r = get_residual_targets(paths2, probs_l,
                                        probs_c, probs_r, n)


ev = Evolutor(qs_l, qs_c, qs_r,
              edges1, edges2,
              n-len(paths2))
ev.anneal(presv_cov=False, n_iter=5000)

final_pths = add_path_dicts(ev.best_dict, flow_dict_cov)

scr1 = score(final_pths, probs_l, probs_c, probs_r)

## Approach-2

# First create a random set of paths above coverage.
flow_dict_init = copy.deepcopy(flow_dict_cov)

for ix in range(n-len(paths2)):
    flow_dict_init = add_one_path(flow_dict_init, edges1, edges2)

ev1 = Evolutor(probs_l, probs_c, probs_r,
              edges1, edges2, n, 
              start_dict=flow_dict_init)

ev1.anneal(presv_cov=True, n_iter=5000)

scr2 = ev1.min_score

print("Score for first approach: " + str(scr1))
print("####################")
print("Score for second approach: " + str(scr2))

