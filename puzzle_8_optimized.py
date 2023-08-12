#class for storing node metadata
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
        return (x >=0 and x <= 2) and (y-1)>=0 and (y-1) <= 2
    elif action == 2:
        return (x+1) >=0 and (x+1) <= 2 and y>=0 and y <= 2
    elif action == 1:
        return x >=0 and x <= 2 and (y+1)>=0 and (y+1) <= 2
    elif action == 0:
        return (x-1) >=0 and (x-1) <= 2 and y>=0 and y <= 2

#Goal Function
    
def checkFinalState(node):
    FINAL_STATE = [
        [0,1,2],
        [3,4,5],
        [6,7,8]
    ]
    for row in range(3):
        for col in range(3):
            if FINAL_STATE[row][col] != node.state[row][col]:
                return False

    return True

#Print State

def printState(sol):
    for state in sol:
        for row in state:
            for col in row:
                print(col, end=" ")
            print()
        print()

#Check if this node is previously visited

def isVisited(visited, pstate):
    if not visited:
        return False
    for state in visited:
        for row in range(3):
            flag = 0
            for col in range(3):
                if state[row][col] != pstate[row][col]:
                    flag = 1
                    break
            if flag:
                break
        if not flag:
            return True
    return False

#Approximate the next optimal node to visit

def calculateCost(node, action):
    FINAL_STATE = [
        [0,1,2],
        [3,4,5],
        [6,7,8]
    ]
    state = [[] for i in node.state]
    for index in range(len(node.state)):
        state[index].extend(node.state[index])
    if action==0:
        empty = (node.empty[0]-1, node.empty[1])
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
    elif action==1:
        empty = (node.empty[0], node.empty[1]+1)
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
    elif action==2:
        empty = (node.empty[0]+1, node.empty[1])
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
    elif action==3:
        empty = (node.empty[0], node.empty[1]-1)
        state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
    invalid_nodes = 0
    for row in range(3):
        for col in range(3):
            if FINAL_STATE[row][col] != state[row][col]:
                invalid_nodes += 1
    return node.level+invalid_nodes+1

#Check if the 8 puzzle problem is solvable.

def isSolvable(state):
    state_array = [col for row in state for col in row]
    state_array.pop(state_array.index(0))
    count = 0
    for i in range(len(state_array)):
        for j in range(i+1,len(state_array)):
            if (state_array[j] < state_array[i]):
                count+=1
    return (count%2)==0

#At each step choose the next possible node wisely using the utility calculateCost

def play_game(node, solution, visited):
    if solution:
        return True
    if (checkFinalState(node)):
        sol = []
        iter = node
        while (iter):
            sol.append(iter.state)
            iter = iter.parent
        printState(sol)
        return True
    action = {'top':0, 'right':1, 'left':3, 'down':2}
    cost = {}
    if isFeasible(node, action['top']):
        cost[0] = calculateCost(node, action['top'])
    if isFeasible(node, action['right']):
        cost[1] = calculateCost(node, action['right'])
    if isFeasible(node, action['down']):
        cost[2] = calculateCost(node, action['down'])
    if isFeasible(node, action['left']):
        cost[3] = calculateCost(node, action['left'])
    import operator as op
    sorted_cost = dict(sorted(cost.items(), key=op.itemgetter(1)))
    visited.append(node.state)
    for key in sorted_cost:
        if key == 0:
            state = [[] for i in node.state]
            for index in range(len(node.state)):
                state[index].extend(node.state[index])
            empty = (node.empty[0]-1, node.empty[1])
            state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
            if not isVisited(visited, state):
                newNode = Node(state, node, node.level+1, empty)
                solution = play_game(newNode, solution, visited)
        elif key == 1:
            state = [[] for i in node.state]
            for index in range(len(node.state)):
                state[index].extend(node.state[index])
            empty = (node.empty[0], node.empty[1]+1)
            state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
            if not isVisited(visited, state):
                newNode = Node(state, node, node.level+1, empty)
                solution = play_game(newNode, solution, visited)
        elif key == 2:
            state = [[] for i in node.state]
            for index in range(len(node.state)):
                state[index].extend(node.state[index])
            empty = (node.empty[0]+1, node.empty[1])
            state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
            if not isVisited(visited, state):
                newNode = Node(state, node, node.level+1, empty)
                solution = play_game(newNode, solution, visited)
        elif key == 3:
            state = [[] for i in node.state]
            for index in range(len(node.state)):
                state[index].extend(node.state[index])
            empty = (node.empty[0], node.empty[1]-1)
            state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
            if not isVisited(visited, state):
                newNode = Node(state, node, node.level+1, empty)
                solution = play_game(newNode, solution, visited)
        if solution:
            return True

def main():
    state = [
        [3,1,0],
        [2,4,5],
        [6,7,8]
    ]
    empty = (0,2)
    parent = None
    level = 0
    initial = Node(state, parent, level, empty)
    solution = False
    visited = []
    if (isSolvable(state)):
        solution = play_game(initial, solution, visited)
    else:
        print("Not solvable")
        return

if __name__ == '__main__':
    main()