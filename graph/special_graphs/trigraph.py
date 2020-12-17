import numpy as np
import networkx as nx
from networkx.algorithms.flow import maximum_flow
from algorith.graphs.graph_utils import min_edge_cover
import re
import random
import collections


def min_cover_trigraph_edge_covers_heuristic(edges1,edges2):
    c1=min_edge_cover(edges1)
    c2=min_edge_cover(edges2)
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


class NeuralTriGraphCentralVert():
    def __init__(self,edge):
        self.key = max(edge)
        self.l_edges = []
        self.r_edges = []
        self.l_edges.append(min(edge))

    def add(self,edge):
        mi, mx = min(edge), max(edge)
        if mi == self.key:
            self.r_edges.append(mx)
        elif mx == self.key:
            self.l_edges.append(mi)

    def edge_counts(self):
        l_size = len(self.l_edges)
        r_size = len(self.r_edges)
        self.l_counts = np.ones(l_size)
        self.r_counts = np.ones(r_size)
        if l_size>r_size:
            self.r_counts = distr_evenly(l_size,r_size)
        elif l_size<r_size:
            self.l_counts = distr_evenly(r_size,l_size)


class NeuralTriGraph():
    """
    A neural tri-grpah is a special case of a tri-partite
    graph. In it, the vertices can be segregated into three
    layers. However unlike a tri-partite graph, connections
    exist only between successive layers (1 and 2; 2 and 3).
    Such graphs describe the layers of a neural network;
    hence the name.
    """
    def __init__(self, left_edges, right_edges):
        self.left_edges = left_edges
        self.right_edges = right_edges
        self.vertices = set(left_edges.flatten())\
                    .union(set(right_edges.flatten()))
        self.layer_1 = set(left_edges[:,0])
        self.layer_2 = set(left_edges[:,1])
        self.layer_3 = set(right_edges[:,1])
        self.layer_1_size = len(self.layer_1)
        self.layer_2_size = len(self.layer_2)
        self.layer_3_size = len(self.layer_3)
        self.layer_1_dict = {}
        for e in left_edges:
            if e[0] not in self.layer_1_dict:
                self.layer_1_dict[e[0]] = set([e[1]])
            else:
                self.layer_1_dict[e[0]].add(e[1])
        self.layer_3_dict = {}
        for e in right_edges:
            if e[1] not in self.layer_3_dict:
                self.layer_3_dict[e[1]] = set([e[0]])
            else:
                self.layer_3_dict[e[1]].add(e[0])
        self.central_vert_dict = create_central_vert_dict(left_edges,\
                                                        right_edges)

    def create_bipartite_graph(self):
        self.flow_graph = nx.DiGraph()
        for ed in self.left_edges:
            ## The vertices from which flow travels only out.
            v1 = "out_layer0_elem" + str(ed[0])
            v2 = "in_layer1_elem" + str(ed[1])
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for ed in self.right_edges:
            v1 = "out_layer1_elem" + str(ed[0])
            v2 = "in_layer2_elem" + str(ed[1])
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for k in self.central_vert_dict.keys():
            for l in self.central_vert_dict[k].l_edges:
                for r in self.central_vert_dict[k].r_edges:
                    v1 = "out_layer0_elem" + str(l)
                    v2 = "in_layer2_elem" + str(r)
                    self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        v1="source"
        for e in self.layer_1:
            v2 = "out_layer0_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_2:
            v2 = "out_layer1_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_3:
            v2 = "out_layer2_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        v2="sink"
        for e in self.layer_1:
            v1 = "in_layer0_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_2:
            v1 = "in_layer1_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
        for e in self.layer_3:
            v1 = "in_layer2_elem" + str(e)
            self.flow_graph.add_edge(v1,v2,capacity=1,weight=1)
    
    def obtain_paths(self):
        _, flow_dict = nx.maximum_flow(self.flow_graph, 'source', 'sink')
        self.vert_disjoint_paths = max_matching_to_paths(flow_dict)
        final_paths = []
        for pth in self.vert_disjoint_paths:
            if len(pth)==3:
                final_paths.append(pth)
            elif len(pth)==2:
                left_layer = self.determine_layer(pth[0])
                right_layer = self.determine_layer(pth[1])
                if left_layer==0 and right_layer==2:
                    central_candidates = self.layer_1_dict[pth[0]]\
                                    .intersection(self.layer_3_dict[pth[1]])
                    ## Randomly pick a central vertex.
                    central = random.sample(central_candidates,1)[0]
                    pth1 = [pth[0],central,pth[1]]
                    final_paths.append(pth1)
                elif left_layer==0:
                    right_sampled = random.sample(self.central_vert_dict[pth[1]]\
                            .r_edges,1)[0]
                    pth1 = [pth[0],pth[1],right_sampled]
                    final_paths.append(pth1)
                elif right_layer==2:
                    left_sampled = random.sample(self.central_vert_dict[pth[0]]\
                            .l_edges,1)[0]
                    pth1 = [left_sampled,pth[0],pth[1]]
                    final_paths.append(pth1)
        self.final_paths = final_paths

    def determine_layer(self,ind):
        if ind < self.layer_1_size:
            return 0
        elif ind < self.layer_2_size:
            return 1
        else:
            return 2

def distr_evenly(n,l):
    ceil=np.ceil(n/l)
    flr=ceil-1
    h=int(n-l*flr)
    j=int(l*ceil-n)
    h_arr = np.ones(h)*ceil
    j_arr = np.ones(j)*flr
    return np.concatenate((h_arr,j_arr))


def create_central_vert_dict(edges1,edges2):
    vert_set = {}
    for e in edges1:
        if e[1] not in vert_set:
            tg = NeuralTriGraphCentralVert(e)
            vert_set[e[1]] = tg
        else:
            vert_set[e[1]].add(e)
    for e in edges2:
        if e[0] not in vert_set:
            tg = NeuralTriGraphCentralVert(e)
            vert_set[e[0]] = tg
        else:
            vert_set[e[0]].add(e)
    return vert_set


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


def max_matching_to_paths_v1(flow_dict):
    paths = []; path=[]
    seen_verts = set()
    for k in sorted(flow_dict.keys()):
        if k.startswith("out_") and "layer0" in k:
            [_, vert_ind] = [int(st) for st in re.findall(r'\d+',k)]
            if vert_ind not in seen_verts:                
                curr_key = k
                while len(flow_dict[curr_key])>0:
                    [_, vert_ind] = [int(st) for st in re.findall(r'\d+',curr_key)]
                    if vert_ind not in seen_verts:
                        seen_verts.add(vert_ind)
                        if len(path)==0:
                            path = [vert_ind]
                        for k1 in flow_dict[curr_key].keys():
                            ## Qn: Why do we need the first if??
                            if k1 in flow_dict[curr_key] and flow_dict[curr_key][k1]>0:
                                [nx_layer, nx_vert_ind] = [int(st) for st in re.findall(r'\d+',k1)]
                                curr_key = "out_layer" + str(nx_layer) \
                                    + "_elem" + str(nx_vert_ind)
                                seen_verts.add(nx_vert_ind)
                                path.append(nx_vert_ind)
                if len(path)>0:
                    paths.append([i for i in path])
                    path=[]
    return paths


def tst1():
    ## Test case-1
    edges1 = np.array([[1,4],[2,4],[2,5],[3,5]])
    edges2 = np.array([[4,6],[4,7],[5,8]])
    nu = NeuralTriGraph(edges1,edges2)
    nu.create_bipartite_graph()
    ##For debugging:
    [e for e in nu.flow_graph.edges]
    flow_val, flow_dict = nx.maximum_flow(nu.flow_graph, 'source', 'sink')
    paths = max_matching_to_paths(flow_dict)

    ## Test case-2
    edges1 = np.array([[1,5],[2,5],[3,7],[4,6]])
    edges2 = np.array([[5,8],[5,9],[5,10],[7,11],[6,11]])

