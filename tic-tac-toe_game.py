class Node:
    '''
    Node to hold the metadata about the vertex of the graph.
    '''

    def __init__(self, state, utility, a=None, b=None):
        self.state = state
        self.utility = utility


class Tic_Tac_Toe:
    '''
    Implementing Tic Tac Toe game using minmax algorithm and alpha beta pruning.
    '''
    
    def terminal_test(self, state):
        '''
        Check if the current state is terminal.
        '''
        # linear_state = [col for row in state for col in row]
        # if linear_state.count(-1) == 0: return False,None
        for i in range(3):
            if (state[i][0] != -1) and (state[i][0] == state[i][1] == state[i][2]):return True, state[i][0]
            if (state[0][i] != -1) and (state[0][i] == state[1][i] == state[2][i]):return True, state[i][1]
        if state[1][1]!=-1 and (state[0][0]==state[1][1]==state[2][2] or state[0][2]==state[1][1]==state[2][0]):return True, state[1][1]
        else: 
            linear_state = [col for row in state for col in row]
            if linear_state.count(-1) == 0: 
                return True, -1
            return False, None

    def utility_function(self, state):
        '''
        Returns the utility function value for the terminal state.
        '''
        boolean, _ = self.terminal_test(state)
        if not boolean:
            raise Exception("This is not terminal state and cannot calculate utility function")
        
        for i in range(3):
            if (state[i][0] != -1) and (state[i][0] == state[i][1] == state[i][2]):
                return state[i][0]
            if (state[0][i] != -1) and (state[0][i] == state[1][i] == state[2][i]):
                return state[0][i]
        
        if (state[0][0]==state[1][1]==state[2][2] or state[0][2]==state[1][1]==state[2][0]) and state[1][1]!=-1:
            return state[1][1]
        return 0.5
    
    def minimax_decision(self, node, move):
        '''
        Use minmax algorithm to find out the optimal move.
        '''
        import copy
        successors = []
        for row in range(3):
            for col in range(3):
                if node.state[row][col] == -1:
                    new_state = copy.deepcopy(node.state)
                    if move == 'min_value':
                        new_state[row][col] = 1
                    if move == 'max_value':
                        new_state[row][col] = 0
                    child = Node(new_state, -1)
                    child.utility = getattr(self,move)(child.state)
                    successors.append(child)

        successors = sorted(successors, key=lambda x:x.utility)
        if move == 'min_value':
            return successors[-1]
        else:
            return successors[0]

    def minimax_decision_pruning(self, node, move, a,b):
        '''
        Use minmax algorithm to find out the optimal move.
        '''
        import copy
        successors = []
        for row in range(3):
            for col in range(3):
                if node.state[row][col] == -1:
                    new_state = copy.deepcopy(node.state)
                    if move == 'min_value_pruning':
                        new_state[row][col] = 1
                    if move == 'max_value_pruning':
                        new_state[row][col] = 0
                    child = Node(new_state, -1)
                    if move == 'min_value_pruning':
                        child.utility = getattr(self,move)(child.state, a, b)
                    else:
                        child.utility = getattr(self,move)(child.state, a, b)
                    successors.append(child)

        successors = sorted(successors, key=lambda x:x.utility)
        if move == 'min_value_pruning':
            return successors[-1]
        else:
            return successors[0]

    def max_value(self, state):
        '''
        It returns the maximum utility that this state can achieve.
        '''
        import copy
        boolean, _ = self.terminal_test(state)
        if boolean:
            return self.utility_function(state)
        utility = float('-inf')
        for row in range(3):
            for col in range(3):
                if state[row][col] == -1:
                    new_state = copy.deepcopy(state)
                    new_state[row][col] = 1
                    utility = max(utility, self.min_value(new_state))
        return utility
    
    def min_value(self, state):
        '''
        It returns the minimum utility that this state can achieve.
        '''
        import copy
        boolean, _ = self.terminal_test(state)
        if boolean:
            return self.utility_function(state)
        utility = float('inf')
        for row in range(3):
            for col in range(3):
                if state[row][col] == -1:
                    new_state = copy.deepcopy(state)
                    new_state[row][col] = 0
                    utility = min(utility, self.max_value(new_state))
        return utility

    def max_value_pruning(self, state, a, b):
        '''
        Use alpha-beta pruning to get the maximum utility among the children
        '''
        import copy
        boolean, _ = self.terminal_test(state)
        if boolean:
            return self.utility_function(state)
        utility = float('-inf')
        for row in range(3):
            for col in range(3):
                if state[row][col] == -1:
                    new_state = copy.deepcopy(state)
                    new_state[row][col] = 1
                    utility = max(utility,self.min_value_pruning(new_state, a, b))
                    a = max(a,utility)
                    if (a>=b): return utility
        return utility

    def min_value_pruning(self, state, a, b):
        '''
        Use alpha-beta pruning to get the maximum utility among the children
        '''
        import copy
        boolean, _ = self.terminal_test(state)
        if boolean:
            return self.utility_function(state)
        utility = float('inf')
        for row in range(3):
            for col in range(3):
                if state[row][col] == -1:
                    new_state = copy.deepcopy(state)
                    new_state[row][col] = 0
                    utility = min(utility, self.max_value_pruning(new_state, a, b))
                    b = min(b,utility)
                    if (a>=b): return utility
        return utility

    
    def start_game(self):
        '''
        Function to start the game
        '''
        import copy
        state = [[-1 for _ in range(3)] for _ in range(3)]
        initial_node = Node(state, -1)
        for i in range(9):
            boolean, winner = self.terminal_test(initial_node.state)
            if boolean:
                if winner == 1: print('Computer')
                elif winner == 0: print("Human")
                else:print(-1)
                return
            if i%2 == 0: 
                move = 'min_value'
                next = self.minimax_decision(initial_node, move)
                self.print_state(next.state)
                initial_node = next
            else: 
                new_state = copy.deepcopy(initial_node.state)
                position_map = [-1,-1]
                while not 0<=position_map[0]<=2 or not 0<=position_map[1]<=2: 
                    print('Enter valid space separated integers of row and column:')
                    position_map = [int(x) for x in input().split()]
                    if len(position_map) < 2 or(len(position_map)==2 and new_state[position_map[0]][position_map[1]]!=-1):
                       position_map = [-1,-1]
                new_state[position_map[0]][position_map[1]] = 0
                initial_node = Node(new_state, -1)
                self.print_state(initial_node.state)
        print(-1)
    
    def start_game_pruning(self):
        '''
        Function to start the game
        '''
        import copy
        state = [[-1 for _ in range(3)] for _ in range(3)]
        initial_node = Node(state, -1)
        a=float('-inf')
        b=float('inf')
        for i in range(9):
            boolean, winner = self.terminal_test(initial_node.state)
            if boolean:
                if winner == 1: print('Computer')
                elif winner == 0: print("Human")
                else:print(-1)
                return
            if i%2 == 0: 
                move = 'min_value_pruning'
                next = self.minimax_decision_pruning(initial_node, move, a,b)
                self.print_state(next.state)
                initial_node = next
            else:
                new_state = copy.deepcopy(initial_node.state)
                position_map = [-1,-1]
                while not 0<=position_map[0]<=2 or not 0<=position_map[1]<=2: 
                    print('Enter valid space separated integers of row and column:')
                    position_map = [int(x) for x in input().split()]
                    if len(position_map) < 2 or(len(position_map)==2 and new_state[position_map[0]][position_map[1]]!=-1):
                        position_map = [-1,-1]
                new_state[position_map[0]][position_map[1]] = 0
                initial_node = Node(new_state, -1)
                self.print_state(initial_node.state)
        print(-1)

    def print_state(self, state):
        '''
        Helper function to print the state of the game
        '''
        for row in range(3):
            for col in range(3):
                if state[row][col] == 1:
                    print('X', end=' ')
                elif state[row][col] == 0:
                    print('O', end=' ')
                else:
                    print('-', end=' ')
            print()
        print('==================')

def main():
    game = Tic_Tac_Toe()
    # game.start_game()
    # print("Game is played using minimax")
    game.start_game_pruning()
    print("Game is played using alpha-beta pruning")

if __name__ == '__main__':
    main()
