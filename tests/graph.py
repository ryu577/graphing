from graphing.graph import Graph, Node
from copy import deepcopy

def test_graph_constructor():
    # test case: (edge set, expected adjacency list, expected vertex props)
    TEST_CASES = [
        ({(0, 2), (1, 2), (2, 3), (2, 4)},
        {0: {2: 0}, 1: {2: 0}, 2: {3: 0, 4: 0}},
        {0: Node(0), 1: Node(1), 2: Node(2), 3: Node(3), 4: Node(4)}),
        ({(0, 1), (1, 2), (2, 3), (3, 4)},
        {0: {1: 0}, 1: {2: 0}, 2: {3: 0}, 3: {4: 0}},
        {0: Node(0), 1: Node(1), 2: Node(2), 3: Node(3), 4: Node(4)})
    ]
    for test_case in TEST_CASES:
        edge_set, exp_adj, exp_vert_props = test_case
        graph = Graph(edges=deepcopy(edge_set))
        assert graph.edges == edge_set, 'Incorrect set of edges. Expected: '\
            + f'{edge_set}. Actual: {graph.edges}'
        assert graph.adj == exp_adj, 'Incorrect adjacency list. Expected: '\
            + f'{exp_adj}. Actual: {graph.adj}'
        assert graph.vert_props == exp_vert_props, 'Incorrect vertex props. '\
            + f'Expected: {exp_vert_props}, Actual: {graph.vert_props}'
    print('Graph constructor test passed')


def test_add_edges():
    # test case: (edge set, edges to add)
    TEST_CASES = [
        ({(0, 2), (1, 2), (2, 3), (2, 4)}, {(0, 3), (1, 4)}),
        ({(0, 1), (1, 2), (2, 3), (3, 4)}, {(0, 2), (2, 4)})
    ]
    for test_case in TEST_CASES:
        edge_set, edges_to_add = test_case
        exp_edges = edge_set.union(edges_to_add)
        graph = Graph(edges=deepcopy(edge_set))
        graph.add_edges(edges_to_add)
        assert graph.edges == exp_edges, 'Incorrect set of edges. Expected: '\
            + f'{exp_edges}. Actual: {graph.edges}'
    print('Add edges test passed')


def test_remove_vertices():
    # test case: (edge set, vertices to remove, expected edge set, expected
    # adjacency list, expected vertex props)
    TEST_CASES = [
        ({(0, 2), (1, 2), (2, 3), (2, 4)}, {3, 4}, {(0, 2), (1, 2)},
        {0: {2: 0}, 1: {2: 0}, 2: dict()},
        {0: Node(0), 1: Node(1), 2: Node(2)}),
        ({(0, 1), (1, 2), (2, 3), (3, 4)}, {0, 4}, {(1, 2), (2, 3)},
        {1: {2: 0}, 2: {3: 0}, 3: dict()},
        {1: Node(1), 2: Node(2), 3: Node(3)})
    ]
    for test_case in TEST_CASES:
        edge_set, remove_verts, exp_edge_set, exp_adj_list,\
            exp_vert_props = test_case
        graph = Graph(edges=edge_set)
        graph.remove_vertices(remove_verts)
        assert graph.edges == exp_edge_set, 'Incorrect set of edges. '\
            + f'Expected: {edge_set}. Actual: {graph.edges}'
        assert graph.adj == exp_adj_list, 'Incorrect adjacency list. '\
            + f'Expected: {exp_adj_list}. Actual: {graph.adj}'
        assert graph.vert_props == exp_vert_props, 'Incorrect vertex props. '\
            + f'Expected: {exp_vert_props}, Actual: {graph.vert_props}'
    print('Remove vertices test passed')


if __name__ == '__main__':
    test_graph_constructor()
    test_add_edges()
    test_remove_vertices()