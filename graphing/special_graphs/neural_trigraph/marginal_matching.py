import numpy as np
import networkx as nx
import pandas as pd
from graphing.special_graphs.neural_trigraph.rand_graph import neur_trig_edges


def get_schedule(probs_left, probs_right, edges1, edges2, num_nodes=20):
    source = 0
    dest = np.max(edges2)+1
    print("destination: " + str(dest))

    left_max_ix = max(edges1[::, 0])
    center_max_ix = max(edges1[::, 1])
    right_max_ix = max(edges2[::, 1])

    g = nx.DiGraph()
    for v in probs_left.keys():
        cap = int(probs_left[v]*num_nodes)
        g.add_edge(source, v, capacity=cap, weight=1/(cap+1e-3))

    for u, v in edges1:
        g.add_edge(u, v, capacity=np.inf, weight=1)

    for u, v in edges2:
        g.add_edge(u, v, capacity=np.inf, weight=1)

    for v in probs_right.keys():
        cap = int(probs_right[v]*num_nodes)
        g.add_edge(v, dest, capacity=cap, weight=1/(cap+1e-3))

    flowed = 0
    while flowed < num_nodes:
        print("Now running networkx max-flow-min-cost " + str(right_max_ix))
        # res_dict = nx.max_flow_min_cost(g, source, dest)
        res_val, res_dict = nx.maximum_flow(g, source, dest)
        flowed = res_val
        if np.random.uniform() > 0.5:
            h = np.random.choice(left_max_ix) + 1
            g[0][h]['capacity'] += 1
        else:
            v = np.random.choice(right_max_ix - center_max_ix - 1)\
                            + center_max_ix + 1
            v = min(v, right_max_ix)
            # TODO: Fix this band-aid and properly sample the right layer.
            try:
                if g[v][dest]['capacity'] > 1:
                    g[v][dest]['capacity'] += 1
                elif np.random.uniform() < 0.9:
                    g[v][dest]['capacity'] += 1
            except Exception:
                print("v: " + str(v) + "dest:" + str(dest))

    return res_dict


def flow_dict_to_arrs(flow_dict, lo_ix=0, hi_ix=50):
    first_arr = []
    second_arr = []
    num_nodes_arr = []
    for k in flow_dict.keys():
        if lo_ix <= k and k <= hi_ix:
            for kk in flow_dict[k].keys():
                if flow_dict[k][kk] > 0:
                    second_arr.append(kk)
                    first_arr.append(k)
                    num_nodes_arr.append(flow_dict[k][kk])
    return first_arr, second_arr, num_nodes_arr


def reconcile_layers_iter(a1=[5, 7, 3], a2=[7, 8]):
    """
    Reconciles the layers of a tri-graph. It works with one central node at
    a time. For example, if we have three layers
    in the graph, HW, VM and OS. And for a given VM (central node), we have
    three hardware's coming into it with 5 nodes, 7 nodes and 3 nodes
    respectively and two OS's going out from it with 7 nodes and 8 nodes
    respectively, the function
    converts this to the number of nodes for each HW-VM-OS combination that
    will satisfy this simultaneously. Note the solution isn't unique.
    args:
        a1: The number of nodes coming in from the first layer.
        a2: The number of nodes going out to the third layer.
        res_arr: The result array with number of nodes.
        l_arr: The IDs of the left property (HW)
        r_arr: The IDs of the right-most property (VM)
    """
    res_arr = []
    l_arr = []
    r_arr = []
    while sum(a1) > 0 or sum(a2) > 0:
        for i in range(len(a1)):
            if a1[i] > 0:
                num1 = a1[i]
                break
        for j in range(len(a2)):
            if a2[j] > 0:
                num2 = a2[j]
                break
        minn = min(num1, num2)
        a1[i] -= minn
        a2[j] -= minn
        res_arr.append(minn)
        l_arr.append(i+1)
        r_arr.append(j+1)
    return res_arr, l_arr, r_arr


def create_schedule(res, edges1, edges2):
    hw_max_ix = max(edges1[::, 0])
    min_vm_ix, max_vm_ix = min(edges1[::, 1]), max(edges1[::, 1])
    hws1, vms1, cnts1 = flow_dict_to_arrs(res, 1, hw_max_ix)
    vms2, os2, cnts2 = flow_dict_to_arrs(res, min_vm_ix, max_vm_ix)
    df1 = pd.DataFrame({"hw": hws1, "vm": vms1, "counts": cnts1})
    df2 = pd.DataFrame({"vm": vms2, "os": os2, "counts": cnts2})

    df1 = df1.sort_values(by='vm')
    df2 = df2.sort_values(by='vm')

    res_hws = []
    res_vms = []
    res_oses = []
    res_cnts = []
    vms = sorted(set(edges2[::, 0]))

    for vm in vms:
        # TODO: This is quadratic. Make it linear.
        arr1 = np.array(df1[df1.vm == vm]["counts"])
        arr2 = np.array(df2[df2.vm == vm]["counts"])
        if len(arr1) == 0 or len(arr2) == 0:
            print("VM: " + str(vm) + " not utilized.")
            continue
        hws = np.array(df1[df1.vm == vm]["hw"])
        oses = np.array(df2[df2.vm == vm]["os"])
        nodes_arr1, l_arr1, r_arr1 = reconcile_layers_iter(arr1, arr2)
        try:
            oses = oses[np.array(r_arr1)-1]
        except Exception:
            raise Exception("Exception when processing vm " + str(vm))
        res_oses = np.concatenate((res_oses, oses))
        hws = hws[np.array(l_arr1)-1]
        res_hws = np.concatenate((res_hws, hws))
        vms = np.ones(len(hws))*vm
        res_vms = np.concatenate((res_vms, vms))
        res_cnts = np.concatenate((res_cnts, nodes_arr1))
    return pd.DataFrame({"hw": res_hws.astype(int), "vm": res_vms.astype(int),
                         "os": res_oses.astype(int),
                         "nodes": res_cnts.astype(int)})


def tst():
    edges1, edges2 = neur_trig_edges(5, 3, 5, shuffle_p=.05)
    probs_left = {1: .2, 2: .2, 3: .2, 4: .2, 5: .1}
    probs_right = {9: .4, 10: .3, 11: .1, 12: .1, 13: .1}
    res = get_schedule(probs_left, probs_right, edges1, edges2, 20)
    # print(res)
    df = create_schedule(res, edges1, edges2)
    return df


def three_layer_schedule(probs_left, probs_right, edges1, edges2, num_nodes):
    res = get_schedule(probs_left, probs_right, edges1, edges2, num_nodes)
    df = create_schedule(res, edges1, edges2)
    return df


###

def reconcile_layers(a1=[5, 7, 3], a2=[7, 8], res_arr=[], l_arr=[], r_arr=[]):
    """
    Reconciles the layers of a tri-graph. It works with one central node at
    a time. For example, if we have three layers
    in the graph, HW, VM and OS. And for a given VM (central node), we have
    three hardware's coming into it with 5 nodes, 7 nodes and 3 nodes
    respectively and two OS's going out from it with 7 nodes and 8 nodes
    respectively, the function
    converts this to the number of nodes for each HW-VM-OS combination that
    will satisfy this simultaneously. Note the solution isn't unique.
    args:
        a1: The number of nodes coming in from the first layer.
        a2: The number of nodes going out to the third layer.
        res_arr: The result array with number of nodes.
        l_arr: The IDs of the left property (HW)
        r_arr: The IDs of the right-most property (VM)
    """
    if sum(a1) == 0 and sum(a2) == 0:
        return np.copy(res_arr), np.copy(l_arr), np.copy(r_arr)
    for i in range(len(a1)):
        if a1[i] > 0:
            num1 = a1[i]
            break
    for j in range(len(a2)):
        if a2[j] > 0:
            num2 = a2[j]
            break
    minn = min(num1, num2)
    a1[i] -= minn
    a2[j] -= minn
    res_arr.append(minn)
    l_arr.append(i+1)
    r_arr.append(j+1)
    return reconcile_layers(a1, a2, res_arr, l_arr, r_arr)
