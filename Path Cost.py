graph = {
    "A" : {'B':3,'J':4,'G':1},
    'B' : {'A':3,'D':10},
    'C' : {'H':3},
    'D' : {'B':10,'H':11,'J':3},
    'E' : {'F':2,'G':14,'I':1},
    'F' : {'H':4,'I':2,'G':8,'E':2},
    'G' : {'A':1,'E':14,'F':8,'J':6},
    'H' : {'C':3,'D':11,'F':4,'I':6},
    'I' : {'E':1,'F':2,'H':6},
    'J' : {'A':4,'D':3,'G':4}
}

class graphProblem: 

    def __init__(self,initial,goal,graph): 
        self.initial=initial 
        self.goal=goal 
        self.graph=graph 

    def actions(self,state): 
        return list(self.graph[state].keys()) 

    def result(self,state,action): 
        return action 

    def goal_test(self,state): 
        return state == self.goal 

    def path_cost(self,cost_so_far,state1,action,state2): 
        return cost_so_far + self.graph[state1][state2] 

class Node: 

    def __init__(self,state,parent=None,action=None,path_cost=0): 
        self.state=state 
        self.parent=parent 
        self.action=action 
        self.path_cost=path_cost 

    def expand(self,graphProblem): 
        return [self.child_node(graphProblem,action) 
                for action in graphProblem.actions(self.state)] 
  
    def child_node(self,graphProblem,action): 
        next_state=graphProblem.result(self.state,action)         
        return Node(next_state,self,action, 
                    graphProblem.path_cost(self.path_cost,self.state,action,next_state)) 

    def path(self):         
        node, path_back = self, [] 

        while node: 
            path_back.append(node) 
            node = node.parent 
        return list(reversed(path_back)) 

    def solution(self): 
        return [node.action for node in self.path()[1:]] 

class Queue: 

    def __init__(self,pop_index): 
        self.queue = [] 
        self.pop_index=pop_index 

    def append(self, item): 
        self.queue.append(item) 

    def sortAppend(self, item,f): 
        self.queue.append(item) 
        self.queue.sort(key=f)     

    def extend(self, items): 
        self.queue.extend(items)      

    def pop(self): 

        if len(self.queue) > 0: 
            return self.queue.pop(self.pop_index) 
        else: 
            raise Exception('FIFOQueue is empty') 

    def printQueue(self): 
        def __len__(self): 
            return len(self.queue) 

    def __contains__(self, item):         
        return item in self.queue 

def graph_search(problem,pop_index):     

    node=Node(problem.initial) 
    if problem.goal_test(node.state): return node 
    frontier = Queue(pop_index) 
    explored = set() 
    frontier.append(node) 

    while frontier: 

        frontier.printQueue() 
        node = frontier.pop() 

##        print("Parent:",node.state,'\n', 
##              "Childs:",[child.state for child in node.expand(problem)],'\n') 

        explored.add(node.state) 

        for child in node.expand(problem): 
            if problem.goal_test(child.state): return child 
            if child.state not in explored and child not in frontier: frontier.append(child) 

    return None 

def best_first_search(problem,f,pop_index=0): 

    node = Node(problem.initial) 
    if problem.goal_test(node.state): 
        return state 

    frontier = Queue(pop_index) 
    frontier.sortAppend(node,f) 
    explored = set() 

    while frontier: 

        frontier.printQueue() 
        node = frontier.pop() 

        if problem.goal_test(node.state): 
            return node 
        explored.add(node.state) 

        for child in node.expand(problem): 
            if child.state not in explored and child not in frontier: 
                frontier.sortAppend(child,f) 
    return None   

def uniform_cost_search(problem): 
    return best_first_search(problem, lambda node: node.path_cost)
 

print('\n=======Finding path using Uniform Cost Search========\n') 

all_nodes = list(graph.keys()) 

start = input('Enter starting position: ') 

end = input('Enter finishing position: ') 

print() 

if start not in all_nodes or end not in all_nodes: 
    print('Invalid Input') 
else: 
    gp = graphProblem(start,end,graph) 
    gpn = uniform_cost_search(gp) 
    path = list(gpn.solution()) 

    print('Path from {} to {} is:'.format(start,end)) 

    for i in range(len(path)): 
        if i is 0: 
            print(path[i],end="") 
        else: 
            print(' ->',path[i],end="") 
    print('\nPath Cost: ', gpn.path_cost) 
print()
