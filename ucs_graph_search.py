class Node:
    '''
    Node to hold the metadata about the vertex in the graph.
    '''

    def __init__(self, vertex, parent):
        self.vertex = vertex
        self.parent = parent

class PriorityQueue:

    def __init__(self, queue=None):
        '''
        Queue should be an instance of class dict
        with keys as the city name and values as their cost.
        '''
        self.queue = {}
        if not isinstance(queue, dict):
            raise Exception("Queue should be an instance of class dict")
        if queue:
            self.queue.update(queue)

    def isEmpty(self):
        return len(self.queue)==0
    
    def push(self, element):
        '''
        Adds the element at the end of the queue if element is of the type dict.
        '''
        if not isinstance(element, dict):
            raise Exception("Element should be an instance of class dict")
        
        self.queue.update(element)
    
    def pop(self):
        '''
        Pop the element with highest priority from the queue if it is not empty. 
        '''
        if self.isEmpty():
            raise Exception('Priority queue is empty')
        max_p = list(self.queue.keys())[0]
        for key in (self.queue.keys()):
            if self.queue[max_p] > self.queue[key]:
                max_p = key
        max_p_dict = {max_p:self.queue[max_p]}
        del self.queue[max_p]
        return max_p_dict
    
    def get_cost(self, node):
        '''
        Return the cost of the node present in the frontier
        '''
        if node not in self.get_nodes():
            raise Exception('Invalid key {}'.format(node))
        
        return self.queue[self.get(node)]

    def get_nodes(self):
        '''
        Get the list of vertices of the nodes in frontier
        '''
        return [ver.vertex for ver in self.queue.keys()]

    def get(self, vertex):
        '''
        Return the node pertaining to the vertex
        '''
        for key in self.queue.keys():
            if key.vertex == vertex:
                return key

        raise Exception("Invalid Vertex") 
    
def goalTest(now, end):
    return now == end

def solution(start):
    '''
    Function to print the path of goal state.
    '''
    iter = start
    while(iter):
        print(iter.vertex)
        iter = iter.parent
    return True

def ucs(graph, start, end):
    '''
    Uniform cost search by using a priority queue as frontier and ordered by the
    path cost of the nodes in the graph.

    It is complete and optimal.
    '''    
    start_dict = {start:0}
    frontier = PriorityQueue(start_dict)
    explored = {}
    
    while not frontier.isEmpty():
        node = frontier.pop()
        city = list(node.items())[0][0]
        cost = list(node.items())[0][1]
        if goalTest(city.vertex, end):
            return solution(city)
        explored.update(node)
        explored_vertices = [ver.vertex for ver in explored.keys()]
        for child in graph[city.vertex].keys():
            if child not in frontier.get_nodes() and child not in explored_vertices:
                newNode = Node(child, city)
                frontier.push({newNode:cost+graph[city.vertex][child]})
            elif child in frontier.get_nodes() and (cost+graph[city.vertex][child]) < frontier.get_cost(child):
                newNode = frontier.get(child)
                newNode.parent = city
                frontier.push({newNode:cost+graph[city.vertex][child]})
    
    return False

def make_undirected_graph(graph):
    '''
    Computes a undirected graph using the given graph.
    The given should have edges along one direction only.
    '''
    import copy
    final_graph = copy.deepcopy(graph)

    for key in graph.keys():
        for inner_key in graph[key].keys():

            if inner_key in final_graph.keys():
                final_graph[inner_key].update({key:final_graph[key][inner_key]})
            else:
                final_graph[inner_key] = {}
                final_graph[inner_key].update({key:final_graph[key][inner_key]})
    return final_graph

def main():
    graph = dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142))

    graph = make_undirected_graph(graph)

    start = Node('Sibiu', None)

    end = 'Bucharest'

    print(ucs(graph, start, end))
    

if __name__ == '__main__':
    main()


    

