class Node:
    '''
    Node to hold the metadata about the vertex in the graph
    '''

    def __init__(self, tour):
        self.tour = tour
        self.cost = 0

class LocalSearch:
    '''
    Local search algorithm attempt to get the tsp tour with least cost.
    '''

    def __init__(self, graph, initial_node):
        self.graph = graph
        self.initial_vertex = initial_node
        self.levels = self.get_levels(graph)
        # self.MAX_LIMIT = self.calculate_maximum_cost(graph)

    def get_levels(self, graph):
        '''
        Get number of levels in the search space.
        '''
        import math
        ver = len(graph.keys())
        return math.log(math.factorial(ver-1)*(((ver-1)*(ver-2)/2)-1)+1,(ver-1)*(ver-2)/2)
    
    def calculate_cost(self, node):
        '''
        Calculates the cost of the given tour.
        '''
        diff = set(node.tour) - set(self.graph.keys())
        if diff or node.tour.count(self.initial_vertex)!=2:
            raise Exception("Invalid tour! All vertices are not covered")
        cost = 0
        for ind in range(1,len(node.tour)):
            cost += self.graph[node.tour[ind-1]][ node.tour[ind]]
        return cost

    def get_random_tour(self, start_vertex):
        '''
        Returns a randomly generated tour with the given start vertex.
        '''
        import random
        vertices = list(self.graph.keys())
        tour = [start_vertex]
        while(len(tour)!=len(vertices)):
            random_index = random.randint(1,len(vertices))
            if not random_index in tour:
                tour.append(random_index)
        tour.append(start_vertex)
        print(tour)
        return tour

    def get_probability(self, iterations):
        '''
        Returns a lower bound on probability to select the bad move based on number of iterations 
        the algorithm executed and length of the graph.
        '''
        import math
        ver = len(self.graph.keys())
        return (iterations/(math.ceil(ver/10)**2*self.levels))

            
    def local_search(self):
        '''
        Starts with a tour and finds the successors by just interchanging any two vertices 
        other than start and end vertices.
        From all the possible moves, select k tours which are best(=cost diff of tours is +ve).
        If k best tours are not available, choose the ones that are best along with some bad tours 
        within a range of probability to aggregate k number of tours.
        From the k tours choose one tour randomly and proceed.
        The algorithm stops when no successor for the current tour can be selected.
        '''
        import copy, math, random
        node = Node(self.get_random_tour(self.initial_vertex))
        node.cost = self.calculate_cost(node)
        best_node = node
        iterations = 1
        while True:
            successors = []
            for outer in range(1,len(node.tour)-2):
                for inner in range(outer, len(node.tour)-1):
                    new_tour = copy.deepcopy(node.tour)
                    new_tour[outer], new_tour[inner] = new_tour[inner], new_tour[outer]
                    new_node = Node(new_tour)
                    new_node.cost = self.calculate_cost(new_node)
                    successors.append(new_node)
                    if new_node.cost < node.cost:
                        successors.append(new_node)
                    else:
                        prob = math.exp(-((new_node.cost-node.cost)/iterations))
                        if prob >= self.get_probability(iterations):
                            successors.append(new_node)
                    if len(successors)==(math.ceil((len(self.graph.keys())/10))):
                        break
                if len(successors)==(math.ceil((len(self.graph.keys())/10))):
                    break
            print(successors)
            if len(successors) == 0:
                return best_node
            node = successors[random.randint(0,len(successors)-1)]
            iterations += 1
            if node.cost<best_node.cost:
                best_node = node
    
def get_distance(a,b):
    '''
    computes the distance between a and b tuples.
    '''
    import math
    distance = (a[0]-b[0])**2 + (a[1]-b[1])**2
    return math.ceil(math.sqrt(distance))

def make_undirected_graph(vertices):
    '''
    Computes a undirected graph using the given vertices.
    '''
    vertices = list(vertices.items())
    graph = {}
    for ind in range(len(vertices)):
        outer_key = vertices[ind][0]
        graph[outer_key] = {}
        for inner_ind in range(len(vertices)):
            if vertices[inner_ind][0] != outer_key:
                inner_key = vertices[inner_ind][0]
                graph[outer_key][inner_key] = get_distance(vertices[ind][1], vertices[inner_ind][1])
    return graph

def main():
    vertices = {}
    with open("graph_co_ordinates.txt", encoding = 'utf-8') as f:
        line = f.readline()
        vertex = 1
        while line:
            line = line.strip()
            line = line.split()
            vertices[vertex] = (int(line[0]), int(line[1]))
            vertex+=1
            if vertex >10:
                break
            line = f.readline()
    graph = make_undirected_graph(vertices)
    print(graph)
    ls = LocalSearch(graph, 1)
    sol = ls.local_search()
    print(sol.tour, sol.cost)

if __name__ == '__main__':
    main()