# graphing

This Python library provides several graphing-related utilities that can be used to apply graph theory concepts and graph algorithms to a variety of problems.

## Getting Started
This library is available for use on PyPI here: [https://pypi.org/project/graphing/](https://pypi.org/project/graphing/)

For local development, do the following. 
- Clone this repository.
- Set up and activate a Python3 virtual environment using `conda`. More info here: [https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
- Navigate to the `graphing` repo.
- Run the command: `python3 setup.py install` to install the package in the conda virtual environment. 
- As development progresses, run the above command to update the build in the conda virtual environment.

## Sample Code

Try to run the following sample code:

> from graphing.special_graphs.neural_trigraph.path_cover import min_cover_trigraph
> 
> from graphing.special_graphs.neural_trigraph.rand_graph import *
> ## Generate a random neural trigraph. Here, it is two sets of edges between layers 1 and 2 (edges1) and layers 2 and 3 (edges2)
> edges1, edges2 = neur_trig_edges(7, 3, 7, shuffle_p=.05)
> ## Find the full-path cover for this neural trigraph.
> paths1 = min_cover_trigraph(edges1, edges2)
> 
> print(paths1)
