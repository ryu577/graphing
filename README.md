# graphing

To install the library on your local machine, clone it and run from the base directory:

> python setup.py install

Then, try to run the following sample code:

> from graphing.special_graphs.neural_trigraph.path_cover import min_cover_trigraph
> from graphing.special_graphs.neural_trigraph.rand_graph import *
> # Generate a random neural trigraph. Here, it is two sets of edges between layers 1 and 2 (edges1) and layers 2 and 3 (edges2)
> edges1, edges2 = neur_trig_edges(7, 3, 7, shuffle_p=.05)
> # Find the full-path cover for this neural trigraph.
> paths1 = min_cover_trigraph(edges1, edges2)
> print(paths1)
