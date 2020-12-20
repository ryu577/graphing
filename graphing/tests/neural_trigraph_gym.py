import numpy as np
import networkx as nx
from graphing.special_graphs.neural_trigraph.path_cover import min_cover_trigraph, min_cover_trigraph_heuristic1
from graphing.special_graphs.neural_trigraph.rand_graph import *
import matplotlib.pyplot as plt


if __name__=="__main__":
    diffs = []
    for i in range(100):
        #edges1, edges2 = neur_trig_edges(70,100,100)
        edges1, edges2 = neur_trig_edges(50,71,70)

        paths1 = min_cover_trigraph(edges1,edges2)
        paths2 = min_cover_trigraph_heuristic1(edges1,edges2)

        print("optimal has: " + str(len(paths1)) + " paths")
        print(paths1)
        print("heuristic has: " + str(len(paths2)) + " paths")
        print(paths2)
        diffs.append(len(paths2)-len(paths1))
    plt.hist(diffs)
    plt.show()


def tst_real_dat():
    from regrsn_prvntn.azqualify.env_design.ingest_facts import FactData
    from regrsn_prvntn.azqualify.env_design.wl_schedule import ExpDes
    fd=FactData()
    fd.obtain_kusto_facts()
    ed=ExpDes()
    df_w_guest_os = ed.hw_vm_base_os(fd)
    paths1 = min_cover_trigraph(ed.edges1,ed.edges2)
    paths2 = min_cover_trigraph_heuristic1(ed.edges1,ed.edges2)
    print("optimal has: " + str(len(paths1)) + " paths")
    print(paths1)
    print("heuristic has: " + str(len(paths2)) + " paths")
    print(paths2)

