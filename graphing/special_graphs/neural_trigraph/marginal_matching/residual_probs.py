from collections import Counter


def get_residual_targets(paths, probs_l, probs_c, probs_r, n):
    xs_l = Counter(paths[::, 0])
    xs_c = Counter(paths[::, 1])
    xs_r = Counter(paths[::, 2])
    qs_l = residual_probs(probs_l, xs_l, n)
    qs_c = residual_probs(probs_c, xs_c, n)
    qs_r = residual_probs(probs_r, xs_r, n)
    return qs_l, qs_c, qs_r


def residual_probs(ps, xs, n):
    qs = {}
    summ = 0
    for k in ps.keys():
        qs[k] = max((ps[k]*n - xs[k]), 0)
        summ += max((ps[k]*n - xs[k]), 0)
    for k in qs.keys():
        qs[k] /= summ
    return qs
