from graphing.special_graphs.neural_trigraph.toy_graphs import ToyGraph1
from graphing.special_graphs.neural_trigraph.marginal_matching.marginal_matching1 import get_schedule


def score(flow_dict, probs_left, probs_center, probs_right):
    dest = max(probs_right.keys()) + 1
    source_flows = flow_dict[0]
    total_flow = sum(source_flows.values())
    summ = 0
    for k in probs_left.keys():
        if k in source_flows:
            summ += (source_flows[k]/total_flow-probs_left[k])**2/len(probs_left)
        else:
            summ += probs_left[k]**2/len(probs_left)
    for k in probs_right.keys():
        if k in flow_dict:
            summ += (probs_right[k] - flow_dict[k][dest]/total_flow)**2/len(probs_center)
        else:
            summ += probs_right[k]**2/len(probs_center)
    for k in probs_center.keys():
        if k in flow_dict:
            summ += (probs_center[k] -
                     sum(flow_dict[k].values())/total_flow)**2/len(probs_right)
        else:
            summ += probs_center[k]**2/len(probs_right)
    return summ


def tst():
	probs_left = {1: .25, 2: .25, 3: .25, 4: .25}
	probs_center = {5: .33333, 6: .3333, 7: .33333}
	probs_right = {8: .25, 9: .25, 10: .25, 11: .25}
	res_dict = get_schedule(probs_left, probs_right, ToyGraph1.edges1, ToyGraph1.edges2, 20)
	scr = score(res_dict, probs_left, probs_center, probs_right)
	print(scr)
