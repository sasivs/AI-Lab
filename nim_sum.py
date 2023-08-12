class Node:
    '''
    Node to hold the metadata about the piles in the game.
    '''
    def __init__(self, piles, player, utility=None, a=None, b=None):
        self.piles = piles
        self.turn = player
        self.utility = utility
        self.a = a
        self.b = b
    
class Game:
    '''
    Class to play the game.
    '''

    def terminal_test(self, piles):
        '''
        Check if this is the terminal state.
        '''
        return piles.count(0)==len(piles)

    def utility_function(self, piles, player):
        '''
        Utility function to assign values to the leaf nodes of the tree.
        '''

        if not self.terminal_test(piles):
            raise Exception("This is not terminal state and cannot assign utility to this state config.")
        
        if player:
            return 1
        return -1
    
    def minimax_decision_pruning(self, node, move, a,b):
        '''
        Use minimax algorithm with pruning to find the optimal move. 
        '''
        import copy
        successors = []
        for pile_index in range(len(node.piles)):
            if node.piles[pile_index] != 0:
                for stone in range(node.piles[pile_index]):
                    new_piles = copy.deepcopy(node.piles)
                    new_piles[pile_index] = stone
                    child = Node(new_piles, 1)
                    child.utility, child.a = getattr(self,move)(child.piles, a, b, True)
                    successors.append(child)
            
        successors = sorted(successors, key=lambda x:x.utility)
        if move == 'min_value_pruning':
            return successors[-1]
        else:
            return successors[0]

    def min_value_pruning(self, piles, a, b, player):
        '''
        Use alpha-beta pruninng to get the maximum_utility among the children
        '''
        import copy
        if self.terminal_test(piles):
            return self.utility_function(piles, player), a
        
        min_utility = float('inf')
        for pile_index in range(len(piles)):
            if piles[pile_index] != 0:
                for stone in range(piles[pile_index]):
                    new_piles = copy.deepcopy(piles)
                    new_piles[pile_index] = stone
                    utility, b = self.max_value_pruning(new_piles, a, b, not player)
                    if utility < min_utility: min_utility = utility
                    b = min(b, utility)
                    if (a>=b): return utility ,a
        return min_utility, a
    
    def max_value_pruning(self, piles, a, b, player):
        import copy
        if self.terminal_test(piles):
            return self.utility_function(piles, player), b
        
        max_utility = float('-inf')
        for pile_index in range(len(piles)):
            if piles[pile_index]!=0:
                for stone in range(piles[pile_index]):
                    new_piles = copy.deepcopy(piles)
                    new_piles[pile_index] = stone
                    utility, a = self.min_value_pruning(new_piles, a, b, not player)
                    if utility > max_utility: max_utility = utility
                    a = max(a, utility)
                    if (a>=b): return utility ,b
        return max_utility, b

    def start_game_pruning(self):
        '''
        Method to call game.
        '''
        import copy, random
        n_piles = random.randint(1,4)
        state = []
        for _ in range(n_piles):
            stones = random.randint(1,4)
            state.append(stones)
        node = Node(state, None)
        a=float('-inf')
        b=float('inf')
        start_player = random.randint(0,1)
        print('Initial State')
        print(node.piles)
        if start_player==1:
            start_player = True
            current_player = True
            print('Computer starts')
        else: 
            start_player = False
            current_player = False 
            print('Human starts')
        while(True):
            if self.terminal_test(node.piles):
                if node.turn == 1:
                    print('Computer wins')
                else:
                    print('Human wins')
                break
            if current_player:
                if start_player:
                    next = self.minimax_decision_pruning(node, 'min_value_pruning', a,b)
                    print('Computer Move')
                    print(next.piles)
                    node = next
                else:
                    next = self.minimax_decision_pruning(node, 'max_value_pruning', a,b)
                    print('Computer Move')
                    print(next.piles)
                    node = next
            else:
                new_piles = copy.deepcopy(node.piles)      
                while(True):
                    print('Enter the pile you want to reduce and new number of stones separated by a space:')
                    coord_map = [int(x) for x in input().split()]
                    if len(coord_map) == 2 and coord_map[0]<len(new_piles) and new_piles[coord_map[0]] != 0 and new_piles[coord_map[0]] > coord_map[1]:
                        break
                new_piles[coord_map[0]] = coord_map[1]
                node = Node(new_piles, 0)
                print('Human Move')
                print(node.piles)
            current_player = not current_player

def main():
    game = Game()
    game.start_game_pruning()

if __name__ == '__main__':
    main()