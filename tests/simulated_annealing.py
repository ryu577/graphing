from graphing.special_graphs.neural_trigraph.marginal_matching.anneal\
    .simulated_annealing import simulated_annealing

TEST_CASES = [
    # edges1, edges2, complete_path_cover, probs_l, probs_c, probs_r, num_paths, 
    # sa_choice (0: first simulated annealing approach, 1: second simulated annealing 
    # approach, else best of 0 and 1), scr_threshold 
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], None, None, None, 300, 0, 0.1),
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], {1: 1/4, 2: 2/4, 3: 1/4}, {4: 2/3, 5: 1/3}, 
        {6: 3/8, 7: 3/8, 8: 2/8}, 300, 1, 0.1),
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], None, {4: 5/9, 5: 4/9}, None, 300, 2, 0.1),
    # num_paths is less than length of path cover for below test cases
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], None, {4: 5/9, 5: 4/9}, None, 2, 2, 0.1),
    ([[1,4],[2,4],[2,5],[3,5]], [[4,6],[4,7],[5,8]], [[1, 4, 7], [2, 4, 6], 
        [3, 5, 8]], None, {4: 5/9, 5: 4/9}, None, 3, 2, 0.1),
]

PASSES = []
FAILS = []
for i in range(len(TEST_CASES)):
    print('TEST CASE', i+1)
    (edges1, edges2, complete_path_cover, probs_l, probs_c, probs_r, 
        num_paths, sa_choice, scr_threshold) = TEST_CASES[i]
    path_counts, scr = simulated_annealing(edges1, edges2, complete_path_cover, 
        probs_l, probs_c, probs_r, num_paths, sa_choice)
    print('Path Counts:', path_counts, '\nScore:', scr)
    try: 
        # check for coverage of all vertices
        vertices = set()
        for edges in [edges1, edges2]:
            for v1, v2 in edges: 
                vertices.add(v1)
                vertices.add(v2) 
        covered = set() 
        for path in path_counts.keys(): 
            for v in path: 
                covered.add(v)
        assert vertices == covered, f'Test case {i+1}: Not all '\
            + 'vertices covered. Uncovered vertices: '\
            + f'{vertices.difference(covered)}'
        
        # check all paths are used
        if num_paths > len(complete_path_cover):
            assert sum(path_counts.values()) == num_paths, f'Test case {i+1}: '\
                + f'Not all paths were used. Expected: {num_paths}, Actual: '\
                + f'{sum(path_counts.values())}'
        else:
            assert sum(path_counts.values()) == len(complete_path_cover),\
                f'Test case {i+1}: Path cover was not preserved. '\
                + f'Expected: {num_paths}, Actual: {sum(path_counts.values())}'

        # check that score is less than threshold
        if num_paths > len(complete_path_cover): 
            assert scr <= scr_threshold, f'Test case {i+1}: Score ({scr})'\
                + f' was not below threshold ({scr_threshold})'
        
        PASSES.append(i + 1)
    except Exception as e: 
        FAILS.append((i + 1, repr(e)))
        print('Test case failed: ', e)
print('Passed: ', len(PASSES), '-', PASSES)
print('Failed: ', len(FAILS), '-', FAILS)
