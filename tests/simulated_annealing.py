import numpy as np
from graphing.special_graphs.neural_trigraph.marginal_matching.anneal\
    .simulated_annealing import simulated_annealing

TEST_CASES = [
    # edges1, edges2, complete_path_cover, number of nodes, simulated annealing 
    # choice (0: first approach, 1: second approach, else best of 0 and 1)
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], 300, 0),
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], 300, 1),
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], 300, 2),
]

PASSES = []
FAILS = []
for i in range(len(TEST_CASES)):
    print('TEST CASE', i+1)
    edges1, edges2, complete_path_cover, num_nodes, sa_choice = TEST_CASES[i]
    path_counts, scr = simulated_annealing(edges1, edges2, complete_path_cover, 
        num_nodes, sa_choice)
    print('Path Counts:', path_counts, '\nScore:', scr)
    try: 
        # check for coverage 
        vertices = set()
        for edges in [edges1, edges2]:
            for v1, v2 in edges: 
                vertices.add(v1)
                vertices.add(v2) 
        covered = set() 
        for path in path_counts.keys(): 
            for v in path: 
                covered.add(v)
        assert len(vertices) == len(covered)
        
        # check all VMs are used 
        assert sum(path_counts.values()) == num_nodes
        
        PASSES.append(i + 1)
    except: 
        FAILS.append(i + 1)
print('Passed: ', len(PASSES), '-', PASSES)
print('Failed: ', len(FAILS), '-', FAILS)
