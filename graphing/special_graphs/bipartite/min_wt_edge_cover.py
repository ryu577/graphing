import numpy as np
from graphing.special_graphs.bipartite.max_wt_matching import Graph, find_max_matchings

##Whiteboard: https://wbd.ms/share/v2/aHR0cHM6Ly93aGl0ZWJvYXJkLm1pY3Jvc29mdC5jb20vYXBpL3YxLjAvd2hpdGVib2FyZHMvcmVkZWVtL2VhZmIzODYyMTMxZTRlZmQ5YWY4ZjIyMWIyZGI0MGU0X0JCQTcxNzYyLTEyRTAtNDJFMS1CMzI0LTVCMTMxRjQyNEUzRA==

class MinWtEdgeCover():
    def __init__(self,gr):
        self.gr=gr
        self.construct_mus()
        self.construct_aux_graph()
        self.construct_edge_cov()
    
    def construct_mus(self):
        self.mus = np.ones(self.gr.max_ver_ix+1)*np.inf
        self.arg_mus = np.zeros(self.gr.max_ver_ix+1)

        for i in range(len(self.gr.edges)):
            ed = self.gr.edges[i]
            wt = self.gr.wts[i]
            v1,v2=ed[0],ed[1]
            if self.mus[v1] > wt:
                self.mus[v1] = wt
                self.arg_mus[v1] = v2
            if self.mus[v2] > wt:
                self.mus[v2] = wt
                self.arg_mus[v2] = v1

    def construct_aux_graph(self):
        gr = self.gr
        edges1 = gr.edges.copy()
        edges2 = gr.edges.copy()

        edges1[:,1]+=len(gr.r_verts)
        edges2[:,0]+=len(gr.r_verts)+gr.max_ver_ix
        # Reverse the edges.
        for i in range(len(edges2)):
            edges2[i]=edges2[i][::-1]

        self.max_left = max(gr.l_verts)
        edges3 = []; wts3 = []
        for v in range(1,gr.max_ver_ix+1):
            if v <= self.max_left:
                edges3.append([v,v+gr.max_ver_ix+len(gr.r_verts)])
            else:
                edges3.append([v,v+len(gr.r_verts)])
            wts3.append(self.mus[v])

        edges = np.concatenate((edges1,edges2,edges3))
        wts = np.concatenate((gr.wts,gr.wts.copy(),wts3))
        self.aux_gr = Graph(edges,wts)

    def construct_edge_cov(self):
        gr=self.gr
        self.aux_mtch = find_max_matchings(self.aux_gr)
        mt = self.aux_mtch
        edge_cover = []
        for m in mt[len(mt)-1].mtch:
            if m[0]<=self.max_left:
                if (gr.max_ver_ix<m[1] \
                        and m[1]<=gr.max_ver_ix+len(gr.r_verts)):
                    edge_cover.append([m[0],m[1]-len(gr.r_verts)])
                else:
                    edge_cover.append([m[0],int(self.arg_mus[m[0]])])
        self.edge_cover = edge_cover
        return edge_cover


def tst():    
    gr = Graph(np.array([[1,4],[2,4],[3,4],[3,5]]),\
            np.array([.5,.9,.5,.6]))
    ed = MinWtEdgeCover(gr)
    print(ed.edge_cover)


if __name__ == "__main__":
    tst()

