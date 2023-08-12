#class to define a node in search space

class Node:
    def __init__(self, state, parent, level, empty):
        self.state = state
        self.parent = parent
        self.level = level
        self.empty = empty

#Check if empty block can move to a particular side
    
def isFeasible(node, action):
    x = node.empty[0]
    y = node.empty[1]
    if action == 3:
        return (0 <= x <= 2) and (0 <= (y-1) <= 2)
    elif action == 2:
        return (x+1) >=0 and (x+1) <= 2 and y>=0 and y <= 2
    elif action == 1:
        return x >=0 and x <= 2 and (y+1)>=0 and (y+1) <=2
    elif action == 0:
        return (x-1) >=0 and (x-1) <= 2 and y>=0 and y <= 2

#Goal Function
    
def checkFinalState(node):
    FINAL_STATE = [
        [0,1,2],
        [3,4,5],
        [6,7,8]
    ]

    return FINAL_STATE==node.state

#For Printing states

def printState(sol):
    for state in sol:
        for row in state:
            for col in row:
                print(col, end=" ")
            print()
        print()

#Check if this node is already visited

def isVisited(visited, pstate):

    if not visited:
        return False

    return pstate in visited

#Check if the 8 puzzle problem is solvable.

def isSolvable(state):
    state_array = [col for row in state for col in row]
    state_array.remove(0)
    count = 0
    for i in range(len(state_array)):
        for j in range(i+1,len(state_array)):
            if (state_array[j] < state_array[i]):
                count+=1
    return (count%2)==0

#Search continuously through the search space using dfs(order: top,right,down,left)

def play_game(node, solution, visited):
    import copy
    if (checkFinalState(node)):
        '''
        if this is a solution, add its path to the sol list and continue the search in the hope of finding a better one
        '''
        sol = []
        iter = node
        while (iter):
            sol.append(iter.state)
            iter = iter.parent
        if node.level not in solution.keys():
            solution[node.level] = []
        solution[node.level].append(sol)
        return solution
    action = {'top':0, 'right':1, 'left':3, 'down':2}
    visited.append(node.state)
    if isFeasible(node, action['top']):
        state = copy.deepcopy(node.state)
        empty = (node.empty[0]-1, node.empty[1])
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
        if not isVisited(visited, state):
            newNode = Node(state, node, node.level+1, empty)
            solution = play_game(newNode, solution, visited)
    if isFeasible(node, action['right']):
        state = copy.deepcopy(node.state)
        empty = (node.empty[0], node.empty[1]+1)
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
        if not isVisited(visited, state):
            newNode = Node(state, node, node.level+1, empty)
            solution = play_game(newNode, solution, visited)
    if isFeasible(node, action['down']):
        state = copy.deepcopy(node.state)
        empty = (node.empty[0]+1, node.empty[1])
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
        if not isVisited(visited, state):
            newNode = Node(state, node, node.level+1, empty)
            solution = play_game(newNode, solution, visited)
    if isFeasible(node, action['left']):
        state = copy.deepcopy(node.state)
        empty = (node.empty[0], node.empty[1]-1)
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
        if not isVisited(visited, state):
            newNode = Node(state, node, node.level+1, empty)
            solution = play_game(newNode, solution, visited)
    return solution

#Main Function
    
def main():
    state = [
        [3,1,2],
        [0,4,5],
        [6,7,8]
    ]
    empty = (1,0)
    parent = None
    level = 0
    initial = Node(state, parent, level, empty)
    solution = {}
    visited = []
    if isSolvable(state):
        sol = play_game(initial, solution, visited)
    else:
        print("Not Solvable")
        return
    import operator as op
    sorted_solution = sorted(sol.items(), key = op.itemgetter(0))
    final_sol = sorted_solution[0][1][0]
    printState(final_sol)


if __name__ == '__main__':
    main()
    
