'''
Time complexity of MST: v^2logv
Time complexity of goal_test: v
Time complexity of solution: v
Time complexity of RBFS: 
    Best Case:
    T(v) = v + v^3logv + v + vlogv + T(v-1)
           (goal_test, adjacent_computing_loop, updating f_costs, sorting vertices while True, RBFS call)
        <= v^3logv + T(v-1)
    Worst Case:
    T(v) = v + v^3logv + v + vlogv + 47T(v-1)
         <= v^3logv + 47T(v-1)
When a graph of function is plotted for both the cases, both of them come out to be exponential.
So, it takes a long time to compute the tsp of a complete graph involving 48 vertices.
With this thought we move to the local search techniques.
'''

class Node:
    '''
    Node to hold the metadata about the vertex in the graph
    '''

    def __init__(self, vertex, parent, path_cost):
        self.vertex = vertex
        self.parent = parent
        self.gen_cost = path_cost
        self.heu_cost = 0
        self.f_cost = path_cost

class TSP:
    '''
    Using rbfs search technique to find the tsp in a given graph.
    '''
    def __init__(self, graph, initial_node):
        self.graph = graph
        self.initial_vertex = initial_node
        self.MAX_LIMIT = self.calculate_maximum_cost(graph)

    def calculate_maximum_cost(self, graph):
        '''
        Calculates a f_limit value for rbfs.
        '''
        import operator as op
        cost = 0
        for ver in graph.keys():
            adjacent_vertices = sorted(graph[ver].items(), key=op.itemgetter(1), reverse=True)
            cost += adjacent_vertices[0][1]
        return cost

    def mst_heuristic(self, node):
        '''
        calculates the heuristic value based on the mst from the unvisited vertices. 
        '''
        import operator as op
        visited = []
        iter = node
        while(iter.parent != node and iter.parent != None):
            visited.append(iter.vertex)
            iter = iter.parent
        if iter.parent != None:
            visited.append(iter.vertex)
        vertices = set(self.graph.keys())-set(visited)
        vertices.add(self.initial_vertex); vertices.add(node.vertex)
        vertices = {ver:self.MAX_LIMIT for ver in vertices}
        vertices[self.initial_vertex] = 0
        cost = 0
        while(len(vertices)!=0):
            vertices = sorted(vertices.items(), key=op.itemgetter(1))
            p_vertex = vertices.pop(0); cost+=p_vertex[1]; p_vertex = p_vertex[0]
            vertices = dict(vertices)
            for key,value in self.graph[p_vertex].items():
                if key in vertices.keys() and vertices[key]>value:
                    vertices[key] = value
        return cost


    def mst_based_heuristic(self, node):
        '''
        calculates the heuristic value based on the st from the unvisited vertices. 
        '''
        visited = []
        iter = node
        while(iter.parent != node and iter.parent != None):
            visited.append(iter.vertex)
            iter = iter.parent
        if iter.parent != None:
            visited.append(iter.vertex)
        import operator as op
        cost = 0
        vertices = set(self.graph.keys())-set(visited)
        vertices.add(self.initial_vertex)
        for ver in vertices:
            adjacent_vertices = sorted(self.graph[ver].items(), key=op.itemgetter(1))
            cost += adjacent_vertices[0][1]
        return cost

    def goal_test(self, node):
        '''
        Checks if all the nodes are visited and also if the start and last vertex is same.
        '''
        if node.vertex != self.initial_vertex: return False
        visited = []
        iter = node
        while(iter != None):
            visited.append(iter.vertex)
            iter = iter.parent
        if visited[-1] != self.initial_vertex: return False
        diff = set(self.graph.keys())-set(visited)
        if diff:
            return False
        return True
    
    def emit_shallow_node(self, adjacent):
        '''
        Returns the best node popped along with updated adjacent.
        '''
        if not adjacent: return None, adjacent
        # print(adjacent)
        new_adjacent = sorted(adjacent, key=lambda x: x.f_cost)
        first = new_adjacent[0]
        new_adjacent.pop(0)
        return first, new_adjacent

    def isVisited(self, node, vertex):
        '''
        To Check if the given vertex is already included in the tour.
        '''
        if vertex == self.initial_vertex: return False
        visited = []
        iter = node
        while(iter != None):
            visited.append(iter.vertex)
            iter = iter.parent
        return vertex in visited


    def solution(self, node):
        '''
        Function to print the path of TSP
        '''
        iter = node
        while(iter != None):
            print(iter.vertex)
            iter = iter.parent
        print("Cost: ", node.gen_cost)
        return True
        

    def call_rbfs(self):
        '''
        Helper function to call rbfs.
        '''
        node = Node(self.initial_vertex, None, 0)
        node.heu_cost = self.mst_heuristic(node)
        node.f_cost = node.heu_cost+node.gen_cost
        self.init_node = node
        return self.rbfs(node, self.MAX_LIMIT)
    
    def rbfs(self, node, f_limit):
        '''
        Recursive best first search by exploring and updating the f value in caase of failure.
        '''
        if self.goal_test(node):
            return self.solution(node), node.f_cost
        
        adjacent = []
        for key in self.graph[node.vertex].keys():
            if not self.isVisited(node, key):
                newNode = Node(key, node, node.gen_cost+self.graph[node.vertex][key])
                newNode.heu_cost = self.mst_heuristic(newNode)
                newNode.f_cost = newNode.gen_cost+newNode.heu_cost
                adjacent.append(newNode)
        
        if not len(adjacent):
            return False, self.MAX_LIMIT
        
        for adj in adjacent:
            adj.f_cost = max(adj.f_cost, node.f_cost)
        
        while True:
            best_node, adjacent = self.emit_shallow_node(adjacent)
            if best_node.f_cost > f_limit:
                return False, best_node.f_cost
            alt_node, adjacent = self.emit_shallow_node(adjacent)
            if alt_node:
                result, best_node.f_cost = self.rbfs(best_node, min(f_limit, alt_node.f_cost))
            else:
                result, best_node.f_cost = self.rbfs(best_node, min(f_limit, self.MAX_LIMIT))
            if result:
                return result, best_node.f_cost
            if best_node:
                adjacent.append(best_node)
            if alt_node:
                adjacent.append(alt_node)

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
            if vertex>10:
                break
            line = f.readline()
    graph = make_undirected_graph(vertices)

    tsp = TSP(graph ,2)
    tsp.call_rbfs()

if __name__ == '__main__':
    main()
