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
        return (x >=0 and x <= 2) and (y-1)>=0 and (y-1) <= 2
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

#Check if the node is already visited

def isVisited(visited, explored, pstate):
    visited.extend(explored)
    if not visited:
        return False
    for state in visited:
        for row in range(3):
            flag = 0
            for col in range(3):
                if state.state[row][col] != pstate[row][col]:
                    flag = 1
                    break
            if flag:
                break
        if not flag:
            return True
    return False

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

#Loop through the search space horizontally using bfs and stop when the goal state is found

def play_game(node, visited):
    if not isSolvable(node.state):
        print("Not Solvable")
        return 
    action = {'top':0, 'right':1, 'left':3, 'down':2}
    explored = []
    while(len(visited)!=0):
        node = visited[0]
        for key in action:
            if key == 'top' and isFeasible(node, action['top']):
                state = [[] for i in node.state]
                for index in range(len(node.state)):
                    state[index].extend(node.state[index])
                empty = (node.empty[0]-1, node.empty[1])
                state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
                if not isVisited(visited, explored, state):
                    newNode = Node(state, node, node.level+1, empty)
            elif key == 'right' and isFeasible(node, action['right']):
                state = [[] for i in node.state]
                for index in range(len(node.state)):
                    state[index].extend(node.state[index])
                empty = (node.empty[0], node.empty[1]+1)
                state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
                if not isVisited(visited, explored, state):
                    newNode = Node(state, node, node.level+1, empty)
            elif key == 'down' and isFeasible(node, action['down']):
                state = [[] for i in node.state]
                for index in range(len(node.state)):
                    state[index].extend(node.state[index])
                empty = (node.empty[0]+1, node.empty[1])
                state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
                if not isVisited(visited, explored, state):
                    newNode = Node(state, node, node.level+1, empty)
            elif key == 'left' and isFeasible(node, action['left']):
                state = [[] for i in node.state]
                for index in range(len(node.state)):
                    state[index].extend(node.state[index])
                empty = (node.empty[0], node.empty[1]-1)
                state[node.empty[0]][node.empty[1]], state[empty[0]][empty[1]] = state[empty[0]][empty[1]], state[node.empty[0]][node.empty[1]]
                if not isVisited(visited, explored, state):
                    newNode = Node(state, node, node.level+1, empty)
            visited.append(newNode)
            if (checkFinalState(newNode)):
                sol = []
                iter = newNode
                while (iter):
                    sol.append(iter.state)
                    iter = iter.parent
                printState(sol)
                return True
        explored.append(visited.pop(0))
    return None

def main():
    state = [
        [3,1,2],
        [4,0,5],
        [6,7,8]
    ]
    empty = (1,1)
    parent = None
    level = 0
    initial = Node(state, parent, level, empty)
    visited = [initial]
    sol = play_game(initial, visited)

if __name__ == '__main__':
    main()