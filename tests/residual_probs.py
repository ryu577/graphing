from collections import Counter
import numpy as np
from graphing.special_graphs.neural_trigraph.path_cover import min_cover_trigraph, complete_paths

# existing code for calculating residual probabilities 
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

def get_residual_targets(paths, probs_l, probs_c, probs_r, n):
    xs_l = Counter(paths[::, 0])
    xs_c = Counter(paths[::, 1])
    xs_r = Counter(paths[::, 2])
    qs_l = residual_probs(probs_l, xs_l, n)
    qs_c = residual_probs(probs_c, xs_c, n)
    qs_r = residual_probs(probs_r, xs_r, n)
    return qs_l, qs_c, qs_r

# new code for calculating residual probabilities (without n2 term)
def residual_probs2(ps, xs, n):
    # n2 = sum(list(xs.values()))
    qs = {}
    summ = 0
    for k in ps.keys():
        qs[k] = max((ps[k]*n - xs[k]), 0)
        summ += max((ps[k]*n - xs[k]), 0)
    for k in qs.keys():
        qs[k] /= summ
    return qs

def get_residual_targets2(paths, probs_l, probs_c, probs_r, n):
    xs_l = Counter(paths[::, 0])
    xs_c = Counter(paths[::, 1])
    xs_r = Counter(paths[::, 2])
    qs_l = residual_probs2(probs_l, xs_l, n)
    qs_c = residual_probs2(probs_c, xs_c, n)
    qs_r = residual_probs2(probs_r, xs_r, n)
    return qs_l, qs_c, qs_r

if __name__=="__main__":
    def even_probs(arr):
        st = set(arr)
        probs_l = {}
        for ix in st:
            probs_l[int(ix)] = 1/len(st)
        return probs_l

    edges1 = np.array([[1,4],[2,4],[2,5],[3,5]])
    edges2 = np.array([[4,6],[4,7],[5,8]])

    probs_l = even_probs(edges1[::, 0])
    probs_c = even_probs(edges1[::, 1])
    probs_r = even_probs(edges2[::, 1])

    paths2 = min_cover_trigraph(edges1,edges2)
    paths3 = np.array(complete_paths(paths2, edges1, edges2))

    test_cases = [100, 200, 300]
    thrs = 1e-10
    for n in test_cases:
        qs_l1, qs_c1, qs_r1 = get_residual_targets(paths3, probs_l,
                                                probs_c, probs_r, n)
        qs_l2, qs_c2, qs_r2 = get_residual_targets2(paths3, probs_l,
                                                probs_c, probs_r, n)

        pairs = [('left', qs_l1, qs_l2), ('center', qs_c1, qs_c2), 
            ('right', qs_r1, qs_r2)]
        for verts, qs_1, qs_2 in pairs: 
            print(f'Residual targets for {verts} vertices (1): {qs_1}')
            print(f'Residual targets for {verts} vertices (2): {qs_2}')
            assert qs_1.keys() == qs_2.keys(), (f'Key sets of residual targets'
                + ' for {verts} vertices do not match')
            for key in qs_1.keys(): 
                assert qs_1[key] - qs_2[key] < thrs, (f'Residual targets for'
                    + ' {verts} vertices do not match')
        print('#############')
    print(f'Residual targets all match (differences all below {thrs})')