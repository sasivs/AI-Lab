class Node:
    '''
    Node to hold the metadata about the vertex in the graph.
    '''

    def __init__(self, vertex, parent):
        self.vertex = vertex
        self.parent = parent

def goal_test(node, end):
    '''
    Check if the goal state is arrived.
    '''
    return node == end

def solution(start):
    '''
    Function to print the path of goal state.
    '''
    iter = start
    while(iter):
        print(iter.vertex)
        iter = iter.parent
    return True

def isExplored(explored, vertex):
    '''
    Checks if a given vertex is already explored or not.
    '''
    vertices = [ver.vertex for ver in explored]
    return vertex in vertices

import operator as op
def bfs(graph, start, end):
    '''
    Visit all the nodes at the same level first.

    It is complete and not optimal as the edge costs are not same.
    '''
    if goal_test(start.vertex, end):
        return solution(start)
    frontier = [start]
    explored = []
    while len(frontier)!=0:
        node = frontier.pop(0)
        explored.append(node)
        for child in graph[node.vertex].keys():
            if not isExplored(explored, child):
                newNode = Node(child, node)
                if goal_test(child, end):
                    return solution(newNode)
                frontier.append(newNode)
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
    print(bfs(graph, start, end))

if __name__ == '__main__':
    main()