import numpy as np


class NeuralTriGraphCentralVert():
    def __init__(self, edge):
        self.key = max(edge)
        self.l_edges = []
        self.r_edges = []
        self.l_edges.append(min(edge))

    def add(self, edge):
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
        if l_size > r_size and r_size != 0:
            self.r_counts = distr_evenly(l_size, r_size)
        elif l_size < r_size and l_size != 0:
            self.l_counts = distr_evenly(r_size, l_size)


def distr_evenly(n, le):
    ceil = np.ceil(n/le)
    flr = ceil-1
    h = int(n-le*flr)
    j = int(le*ceil-n)
    h_arr = np.ones(h)*ceil
    j_arr = np.ones(j)*flr
    return np.concatenate((h_arr, j_arr))

if __name__=='__main__':
    # check if divide by zero error is encountered or not 
    try: 
        v = NeuralTriGraphCentralVert((1, 2))
        v.edge_counts() # should not throw zero division error because r_size = 0
    except ZeroDivisionError: 
        print('ZeroDivisionError occurred - FAILED')
    print('No ZeroDivisionError occurred - PASSED')


