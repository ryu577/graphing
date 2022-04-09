from graphing.special_graphs.neural_trigraph.marginal_matching.marginal_matching1 import get_schedule, get_schedule_rand
from graphing.special_graphs.neural_trigraph.marginal_matching.scoring import score
from graphing.special_graphs.neural_trigraph.toy_graphs import ToyGraph1
import numpy as np


def evolve(n_iter=100, prev_flow=None):
    probs_left, probs_center, probs_right = ToyGraph1.probs_left.copy(), ToyGraph1.probs_center.copy(), ToyGraph1.probs_right.copy()
    min_score = np.inf
    best_dict = {}
    for ix in range(n_iter):
        #res = get_schedule_rand(ToyGraph1.edges1, ToyGraph1.edges2)
        res = get_schedule(probs_left, probs_right, ToyGraph1.edges1, ToyGraph1.edges2)
        if ix == 0 and prev_flow is not None:
            res = prev_flow
        candidate_score = score(res, ToyGraph1.probs_left, ToyGraph1.probs_center, ToyGraph1.probs_right)
        print("Score: " + str(candidate_score))
        if candidate_score < min_score:
            min_score = candidate_score
            best_dict = res
            probs_left_bst, probs_center_bst, probs_right_bst = probs_left.copy(), probs_center.copy(), probs_right.copy()
            b_ix = ix
        if (candidate_score - min_score)/min_score > 0.3 and (ix-b_ix)>10:
            probs_left, probs_center, probs_right = probs_left_bst.copy(), probs_center_bst.copy(), probs_right_bst.copy()
        if ix%3==0:
            perturb(probs_left)
        elif ix%3==1:
            perturb(probs_center)
        else:
            perturb(probs_right)
    return best_dict, min_score


def perturb(probs):
    ix = np.random.choice(list(probs.keys()))
    perturb = np.random.normal(0,.03)
    probs[ix] = max(0, probs[ix]+perturb)
