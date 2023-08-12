class Node:
    '''
    Node to hold the metadata about the vertex in the graph.
    '''

    def __init__(self, state, parent, path_cost, heu_cost):
        self.state = state
        self.parent = parent
        self.gen_cost = path_cost
        self.heu_cost = heu_cost
        self.f_cost = path_cost+heu_cost



class PatternDatabase:
    '''
    class to implement a pattern database type of heuristic.
    '''
    def __init__(self, goal_config):
        self.goal = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]
        x, y = self.getEmptyCoordinates(goal_config)
        if (x%3)<2: row = x+1
        else: row=x-1
        if (y%3) < 2:  col = y+1
        else: col = y-1
        for r in range(min(x,row), max(x,row)+1):
            for c in range(min(y,col), max(y,col)+1):
                self.goal[r][c] = goal_config[r][c]


    def getEmptyCoordinates(self, state):
        '''
        Gives row and col of empty block.
        '''
        for r in range(3):
            for c in range(3):
                if state[r][c]==0:
                    return r,c
        
        raise Exception("Invalid State configuration: No empty block")
        
    def is_valid(self, state, action):
        '''
        Checks if this action is valid for the present state.
        '''
        x,y = self.getEmptyCoordinates(state)
        if action == 3:
            return (x >=0 and x <= 2) and (y-1)>=0 and (y-1) <= 2
        elif action == 2:
            return (x+1) >=0 and (x+1) <= 2 and y>=0 and y <= 2
        elif action == 1:
            return x >=0 and x <= 2 and (y+1)>=0 and (y+1) <=2
        elif action == 0:
            return (x-1) >=0 and (x-1) <= 2 and y>=0 and y <= 2

    def inThisSet(self, nodes, newState):
        '''
        Checks if this state is already in the set of nodes.
        '''
        explored_list = [node[0] for node in nodes]
        return newState in explored_list
        
    def compute_heuristic(self):
        '''
        computes heuristic and saves them to a file.
        '''
        import copy, json
        frontier = [(self.goal,0)]
        explored = []
        while(len(frontier)!=0):
            p_state = frontier.pop(0)
            explored.append(p_state)
            x,y = self.getEmptyCoordinates(p_state[0])
            for action in range(4):
                if self.is_valid(p_state[0], action):
                    newState = copy.deepcopy(p_state[0])
                    if action == 0:
                        newState[x][y], newState[x-1][y] = newState[x-1][y], newState[x][y]
                    elif action == 1:
                        newState[x][y], newState[x][y+1] = newState[x][y+1], newState[x][y]
                    elif action == 2:
                        newState[x][y], newState[x+1][y] = newState[x+1][y], newState[x][y]
                    elif action == 3:
                        newState[x][y], newState[x][y-1] = newState[x][y-1], newState[x][y]
                    if not self.inThisSet(frontier, newState) and not self.inThisSet(explored, newState):
                        frontier.append((newState, p_state[1]+1))
        # with open('patterndb.out', 'w') as f:
        #     for state in sorted(explored, key=lambda c: c[1]):
        #         json.dump(state, f)
        #         f.write('\n') 
        return sorted(explored, key=lambda c: c[1])



class aStarGraph:
    '''
    Python class to solve the 8 puzzle problem using graph version of a star search.
    '''
    def __init__(self):
        import math
        self.MAX_LIMIT = math.factorial(9)
        self.states = None
        self.costs = None
        return 
    
    def getState(self):
        '''
        Genrates random state.
        '''
        import random as ran
        state = []
        for i in range(9):
            num = ran.randint(0,8)
            while num in state:
                num = ran.randint(0,8)
            state.append(num)
        new_state = []
        for r in range(3):
            row = [state[3*r+0], state[3*r+1], state[3*r+2]]
            new_state.extend([row])
        return new_state
    
    def getEmptyCoordinates(self, state):
        '''
        Gives row and col of empty block.
        '''
        for r in range(3):
            for c in range(3):
                if state[r][c]==0:
                    return r,c
        
        raise Exception("Invalid State configuration: No empty block")
    
    def isSolvable(self, goal, state):
        '''
        Checks if the state is solvable or not.

        Reference: https://medium.com/@hhuyqun/the-8-puzzle-problem-d543ce5d4e99
        '''
        g_list = [col for row in goal for col in row]
        s_list = [col for row in state for col in row]
        g_list.remove(0); s_list.remove(0)
        inversions = 0
        for i in range(8):
            g_index = g_list.index(s_list[i])
            g_set = set(g_list[g_index:])
            s_set = set(s_list[i:])
            inversions += len(s_set-g_set)
        import math
        if (math.sqrt(len(g_list)+1)%2) == 0:
            g_row, g_col = self.getEmptyCoordinates(goal)
            s_row, s_col = self.getEmptyCoordinates(state)
            return ((inversions+s_row)%2) == (g_row%2)
        else:
            return (inversions%2) == 0
    
    def goal_test(self, state, goal):
        '''
        Checks if the given state is goal state.
        '''
        return state == goal
    
    def misplaced_heuristic(self, state, goal):
        '''
        Gives number of misplaced tiles.
        '''
        misplaced = 0
        g_list = [col for row in goal for col in row]
        s_list = [col for row in state for col in row]
        for i in range(8):
            if g_list[i]!=0:
                if g_list[i]!=s_list[i]:
                    misplaced += 1
        return misplaced

    def manhattan_heuristic(self, state, goal):
        '''
        Gives the estimate of no of tiles to be moved to reach the goal state.
        '''
        state = [col for row in state for col in row]
        goal = [col for row in goal for col in row]
        manhattan = 0
        for ind in range(9):
            if state[ind]!=0:
                sx, sy = ind//3, ind%3
                gind = goal.index(state[ind])
                gx, gy = gind//3, gind%3
                manhattan += abs(sx-gx) + abs(sy-gy)
        return manhattan

    def pattern_database_heuristic(self, state, goal):
        '''
        Pattern database heuristic.
        '''
        x,y = self.getEmptyCoordinates(goal)
        if (x%3)<2: row = x+1
        else: row=x-1
        if (y%3) < 2:  col = y+1
        else: col = y-1
        req_pos = [goal[r][c] for r in range(min(x,row), max(x,row)+1) for c in range(min(y,col), max(y,col)+1)]
        iter_state = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
        for r in range(3):
            for c in range(3):
                if state[r][c] in req_pos:
                    iter_state[r][c] = state[r][c]
        return self.costs[self.states.index(iter_state)]
        

    def composite_heuristic(self, state, goal):
        '''
        Composite heuristic based on manhattan distance, misplaced tiles.
        '''
        return max(self.manhattan_heuristic(state, goal), self.misplaced_heuristic(state, goal), \
            self.pattern_database_heuristic(state, goal))

    def solution(self, start):
        '''
        Function to print the path of goal state.
        '''
        iter = start
        steps = 0
        while(iter):
            print(iter.state)
            iter = iter.parent
            steps += 1
        print("Steps: ",steps)
        return True
    
    def emit_shallow_node(self, frontier):
        '''
        Returns the next node popped along with updated frontier.
        '''
        new_frontier = sorted(frontier, key=lambda x: x.f_cost)
        first = new_frontier[0]
        new_frontier.pop(0)
        return first, new_frontier

    def is_valid(self, node, action):
        '''
        Checks if this action is valid for the present state.
        '''
        if isinstance(node, Node):
            x,y = self.getEmptyCoordinates(node.state)
        else:
            x,y = self.getEmptyCoordinates(node)
        if action == 3:
            return (x >=0 and x <= 2) and (y-1)>=0 and (y-1) <= 2
        elif action == 2:
            return (x+1) >=0 and (x+1) <= 2 and y>=0 and y <= 2
        elif action == 1:
            return x >=0 and x <= 2 and (y+1)>=0 and (y+1) <=2
        elif action == 0:
            return (x-1) >=0 and (x-1) <= 2 and y>=0 and y <= 2

    def getNewState(self, node, action):
        '''
        Returns a newState from the action carried out on the node.
        '''
        import copy
        if isinstance(node, Node):
            x,y = self.getEmptyCoordinates(node.state)
            newState = copy.deepcopy(node.state)
        else:
            newState = copy.deepcopy(node)
            x,y = self.getEmptyCoordinates(node)
        if action == 0:
            newState[x][y], newState[x-1][y] = newState[x-1][y], newState[x][y]
        elif action == 1:
            newState[x][y], newState[x][y+1] = newState[x][y+1], newState[x][y]
        elif action == 2:
            newState[x][y], newState[x+1][y] = newState[x+1][y], newState[x][y]
        elif action == 3:
            newState[x][y], newState[x][y-1] = newState[x][y-1], newState[x][y]
        else:
            raise Exception("Invalid Action")
        return newState

    def inThisSet(self, nodes, newState):
        '''
        Checks if this state is already in the set of nodes.
        '''
        explored_list = [node.state for node in nodes]
        return newState in explored_list

    def getNode(self, frontier, state):
        '''
        returns the node corresponding to the passed state.
        '''
        for index,node in enumerate(frontier):
            if node.state == state:
                return index
        raise Exception("State not found in passed list")

    def verify_consistency(self, goal, heuristic):
        import time
        '''
        Verifies the consistency of the by using a bfs on search space.
        '''
        node = Node(goal, None, 0, getattr(self, heuristic)(goal, goal))
        frontier = [(node.state,0)]
        explored = []
        start_time = time.time()
        while(len(frontier)!=0):
            state = frontier.pop(0)
            explored.append(state)
            for action in range(4):
                end_time = time.time()
                if (end_time-start_time)>10:
                    print(len(frontier)+len(explored))
                    start_time = end_time
                if self.is_valid(state[0], action):
                    newState = self.getNewState(state[0], action)
                    if not newState in explored and not newState in frontier:
                        heu_cost = getattr(self, heuristic)(newState, goal)
                        if (state[1]+1) < heu_cost:
                            print(newState, node.state)
                            return False
                        frontier.append((newState,heu_cost))
                        # if (node.heu_cost+1) < newNode.heu_cost:
                        #     if not self.inThisSet(inconsistent_nodes, newState):
                        #         inconsistent_nodes.append(newNode)
                        # else:
                        #     frontier.append(newNode)
                        #     if self.inThisSet(inconsistent_nodes, newState):
                        #         inconsistent_nodes.remove(newState)
        # if inconsistent_nodes:
        #     print([node.state for node in inconsistent_nodes])
        #     return False
        print(len(frontier)+len(explored))
        return True

    def a_star_search(self, init_state, goal_state, heuristic):
        if heuristic == 'pattern_database_heuristic' or heuristic == 'composite_heuristic':
            pdb_obj = PatternDatabase(goal_state)
            states = pdb_obj.compute_heuristic()
            self.states = [st[0] for st in states]
            self.costs = [st[1] for st in states]
        start = Node(init_state, None, 0, getattr(self, heuristic)(init_state, goal_state))
        if self.goal_test(start.state, goal_state):
            return self.solution(start)
        frontier = [start]
        explored = []
        while(len(frontier)!=0):
            node, frontier = self.emit_shallow_node(frontier)
            explored.append(node)
            if self.goal_test(node.state, goal_state):
                return self.solution(node)
            for action in range(4):
                if self.is_valid(node, action):
                    newState = self.getNewState(node, action)
                    if not self.inThisSet(explored, newState) and not self.inThisSet(frontier, newState):
                        newNode = Node(newState, node, node.gen_cost+1, getattr(self, heuristic)(newState, goal_state))
                        frontier.append(newNode)
                    elif self.inThisSet(frontier, newState):
                        reqNode = frontier[self.getNode(frontier, newState)]
                        newCost = node.gen_cost+1+getattr(self, heuristic)(newState, goal_state)
                        if newCost < (reqNode.gen_cost+reqNode.heu_cost):
                            reqNode.parent = node
                            reqNode.gen_cost = node.gen_cost+1
                            reqNode.heu_cost = newCost - node.gen_cost - 1
        return False 
    
    def call_rbfs(self, start, goal, heuristic):
        '''
        Helper function to call rbfs.
        '''
        if heuristic == 'pattern_database_heuristic' or heuristic == 'composite_heuristic':
            pdb_obj = PatternDatabase(goal)
            states = pdb_obj.compute_heuristic()
            self.states = [st[0] for st in states]
            self.costs = [st[1] for st in states]
        node = Node(start, None, 0, getattr(self, heuristic)(start, goal))
        return self.rbfs(node, goal, heuristic, self.MAX_LIMIT)

    def rbfs(self, node, goal, heuristic, f_limit):
        '''
        Recursive best first search by exploring and updating the f value in case of failure.
        '''
        if self.goal_test(node.state, goal):
            return self.solution(node), node.f_cost
        children = []
        for action in range(4):
            if self.is_valid(node, action):
                newState = self.getNewState(node, action)
                child = Node(newState, node, node.gen_cost+1, \
                    getattr(self, heuristic)(newState, goal))
                children.append(child)
        
        if not len(children):
            return False, self.MAX_LIMIT
        
        for c_node in children:
            c_node.f_cost = max(c_node.f_cost, node.f_cost)

        while True:
            best_node, children = self.emit_shallow_node(children)
            if best_node.f_cost > f_limit:
                return False, best_node.f_cost
            alt_node, children = self.emit_shallow_node(children)
            result, best_node.f_cost = self.rbfs(best_node, goal, heuristic, min(f_limit, alt_node.f_cost))
            if result:
                return result, best_node.f_cost
            children.append(best_node)
            children.append(alt_node)

    def solve(self):
        '''
        function to gen init state and goal state and call a_star search.
        '''
        import time
        import os
        import psutil
        # initial_state = [[5, 7, 6], [3, 8, 4], [0, 2, 1]]
        # goal_state = [[6, 3, 5], [4, 1, 8], [2, 7, 0]]
        # initial_state = [
        #     [3,1,2],
        #     [0,4,5],
        #     [6,7,8]
        # ]
        # goal_state = [
        #     [0,1,2],
        #     [3,4,5],
        #     [6,7,8]
        # ]
        # print(self.isSolvable(goal_state, initial_state))
        # print(self.verify_consistency(goal_state, 'misplaced_heuristic'))
        # print(self.a_star_search(initial_state, goal_state, 'pattern_database_heuristic'))
        initial_state = self.getState()
        goal_state = self.getState()
        print(initial_state, goal_state)
        print(self.isSolvable(goal_state, initial_state))
        while(not self.isSolvable(goal_state, initial_state)):
            initial_state = self.getState()
        process = psutil.Process(os.getpid())
        process_mem = process.memory_info().rss/(1024*1024)
        print("Process memory(Starting): ",process_mem) 
        print("Starting computing...")
        start_time = time.time()
        self.a_star_search(initial_state, goal_state, 'misplaced_heuristic')
        end_time = time.time()
        print("Time Taken(Misplaced): ", (end_time-start_time))
        process = psutil.Process(os.getpid())
        process_mem = process.memory_info().rss/(1024*1024) - process_mem
        print("Process memory(Misplaced): ",process_mem) 
        start_time = time.time()
        self.a_star_search(initial_state, goal_state, 'manhattan_heuristic')
        end_time = time.time()
        print("Time Taken(manhattan): ", (end_time-start_time))
        process = psutil.Process(os.getpid())
        process_mem = process.memory_info().rss/(1024*1024) - process_mem
        print("Process memory(Manhattan): ",process_mem) 
        start_time = time.time()
        self.a_star_search(initial_state, goal_state, 'pattern_database_heuristic')
        end_time = time.time()
        print("Time Taken(pdb): ", (end_time-start_time))
        process = psutil.Process(os.getpid())
        process_mem = process.memory_info().rss/(1024*1024) - process_mem
        print("Process memory(pdb): ",process_mem) 
        start_time = time.time()
        self.a_star_search(initial_state, goal_state, 'composite_heuristic')
        end_time = time.time()
        print("Time Taken(composite): ", (end_time-start_time))
        process = psutil.Process(os.getpid())
        process_mem = process.memory_info().rss/(1024*1024) - process_mem
        print("Process memory(composite): ",process_mem) 
        start_time = time.time()
        self.call_rbfs(initial_state, goal_state, 'composite_heuristic')
        end_time = time.time()
        print("Time Taken(rbfs(composite)): ", (end_time-start_time))
        process = psutil.Process(os.getpid())
        process_mem = process.memory_info().rss/(1024*1024) - process_mem
        print("Process memory(rbfs(composite)): ",process_mem) 

def main():
    aStarObj = aStarGraph()
    aStarObj.solve()

if __name__ == '__main__':
    main()

    