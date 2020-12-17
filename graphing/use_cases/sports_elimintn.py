import numpy as np
import networkx as nx
import cvxpy as cp

## https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-design-and-analysis-of-algorithms-spring-2015/lecture-notes/MIT6_046JS15_lec14B.pdf

class BaseballElim():
    w5=50; l5=134-w5
    #Won games
    w=np.array([75,71,69,63,w5])
    #Lost games
    l=np.array([59,63,75,71,l5])
    #Remaining games
    r=np.array([28,28,28,28,28])
    to_play = np.array([
        [0,5,7,4,3],
        [5,0,2,4,4],
        [7,2,0,4,0],
        [4,4,4,0,0],
        [3,4,0,0,0]
    ])
    
    @staticmethod
    def graph_optimizn():
        w5,l5,w,l,r,to_play=BaseballElim.w5,BaseballElim.l5,\
                    BaseballElim.w,BaseballElim.l,BaseballElim.r,\
                    BaseballElim.to_play
        g = nx.DiGraph()
        g.add_edge('s','1-2', capacity=to_play[0,1])
        g.add_edge('s','1-3', capacity=to_play[0,2])
        g.add_edge('s','2-3', capacity=to_play[1,2])
        g.add_edge('s','1-4', capacity=to_play[0,3])
        g.add_edge('s','2-4', capacity=to_play[1,3])
        g.add_edge('s','3-4', capacity=to_play[2,3])
        g.add_edge('1-2','1', capacity=np.inf)
        g.add_edge('1-2','2', capacity=np.inf)
        g.add_edge('1-3','1', capacity=np.inf)
        g.add_edge('1-3','3', capacity=np.inf)
        g.add_edge('2-3','2', capacity=np.inf)
        g.add_edge('2-3','3', capacity=np.inf)
        g.add_edge('1-4','1', capacity=np.inf)
        g.add_edge('1-4','4', capacity=np.inf)
        g.add_edge('2-4','2', capacity=np.inf)
        g.add_edge('2-4','4', capacity=np.inf)
        g.add_edge('3-4','3', capacity=np.inf)
        g.add_edge('3-4','4', capacity=np.inf)
        g.add_edge('1','t', capacity=w[4]+r[4]-w[0])
        g.add_edge('2','t', capacity=w[4]+r[4]-w[1])
        g.add_edge('3','t', capacity=w[4]+r[4]-w[2])
        g.add_edge('4','t', capacity=w[4]+r[4]-w[3])
        flow_value, flow_dict = nx.maximum_flow(g, 's', 't')

        #Greater than zero means eliminated
        detroit_eliminated = sum(sum(to_play[:4,:4]))/2-flow_value

    ######
    @staticmethod
    def detroit_eliminated_v2():
        w5,l5,w,l,r,to_play=BaseballElim.w5,BaseballElim.l5,\
                    BaseballElim.w,BaseballElim.l,BaseballElim.r,\
                    BaseballElim.to_play
        m=to_play
        x=cp.Variable((4,4),integer=True)
        z=cp.Variable()
        constraints = [x >= 0, x<=to_play[:4,:4]]
        constraints.append(w[4]+r[4]-w[:4]-sum(x)>=z)
        constraints.append(x+x.T==to_play[:4,:4])
        objective=cp.Maximize(z)
        prob = cp.Problem(objective, constraints)
        res = prob.solve()
        return x.value

