import numpy as np
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class DAGNode(object):
	def __init__(self, key='a', adj_lst=[]):
		self.nxt = None
		self.nxt_ix = -1

	def get_nxt(self, icm_cand):
		return 0


class RgxLstNode(DAGNode):
	def __init__(self):
		return None


class IfNode(DAGNode):
	def __init__(self):
		return None


class SevNode(DAGNode):
	def __init__(self):
		super().__init__()


class DecisionDAG():
	def __init__(self):
		self.mapper = {'CmpDeny': RgxLstNode(), 'HasEsclTo': IfNode()}
		self.adj = defaultdict(list)
		self.adj['CmpDeny'] = ['CmpAllow', 'SevDAG1']
		self.adj['CmpAllow'] = ['GlblDeny', 'SevDAG2']
		self.adj['GlblDeny'] = ['GlblAllow', 'SevDAG1']
		self.adj['GlblAllow'] = ['SevDAG2', 'SevDAG1']
		self.adj['SevDAG2'] = ['HasEsclTo']


class SeverityDAG():
	def __init__(self):
		return None


class ICMCandidate():
	def __init__(self):
		return 1


def tst():
	g = nx.Graph()
	g.add_edge('CmpDeny', 'CmpAllow')
	g.add_edge('CmpDeny', 'SevDAG1')
	g.add_edge('CmpAllow', 'GlblDeny')
	g.add_edge('CmpAllow', 'SevDAG2')
	g.add_edge('GlblDeny', 'GlblAllow')
	g.add_edge('GlblDeny', 'SevDAG1')
	g.add_edge('GlblAllow', 'SevDAG2')
	g.add_edge('GlblAllow', 'SevDAG1')
	g.add_edge('SevDAG2', 'HasEsclTo')
	nx.draw(g, with_labels=True)
	plt.show()
