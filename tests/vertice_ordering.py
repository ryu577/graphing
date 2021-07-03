from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee

# From scipy example.
graph = [
     [0, 1 , 2, 0],
     [0, 0, 0, 1],
     [2, 0, 0, 3],
     [0, 0, 0, 0]
     ]

graph = csr_matrix(graph)

reverse_cuthill_mckee(graph)


# Middle layer not inverted. Others inverted.
graph = [
    [0,0,0,0,1,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,1,1,0,0,0,1,1],
    [1,1,0,0,0,1,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,1,0,0,0,0]
    ]

graph = csr_matrix(graph)

reverse_cuthill_mckee(graph)


# Graph where all is good.
graph = [
    [0,0,0,1,0,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,0,1,0,0,0],
    [1,1,0,0,0,1,0,0],
    [0,1,1,0,0,0,1,1],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,1,0,0,0]
    ]

graph = csr_matrix(graph)

reverse_cuthill_mckee(graph)

