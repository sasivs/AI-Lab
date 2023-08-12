def independency_test(graph, v_set):
    '''
    Checks if the v_set is an independent set for the given graph.
    '''
    iter_v_set = []
    iter_v_set.extend(v_set)
    iter_v_set = set(iter_v_set)
    for ver in v_set:
        neighbours = set(graph[ver])
        iter_v_set.remove(ver)
        if len(neighbours&iter_v_set)!=0:
            return False
        iter_v_set.add(ver)
    return True

def isExplored(explored, v_set):
    '''
    Checks if the subset is already visited
    '''    
    return v_set in explored


def bfs(graph):
    import copy
    '''
    Visit all the subsets at the same level and check for independency.
    If independent, add them to solution set.
    '''
    frontier = [set([])]
    explored = []
    solution = []
    vertex_set = set(graph.keys())
    while(len(frontier)!=0):
        subset = frontier.pop(0)
        solution.append(copy.deepcopy(subset))
        explored.append(copy.deepcopy(subset))
        children = vertex_set-subset
        for ver in children:
            subset.add(ver)
            if independency_test(graph, subset):
                if subset not in frontier and not isExplored(explored, subset):
                    frontier.append(copy.deepcopy(subset))
            subset.remove(ver)
    
    return solution

def make_undirected_graph(graph):
    '''
    Computes a undirected graph using the given graph.
    The given graph should have edges along one direction only.
    '''
    import copy
    final_graph = copy.deepcopy(graph)
    for key in final_graph.keys():
        final_graph[key] = list(final_graph[key].keys())
    

    for key in graph.keys():
        for inner_key in graph[key].keys():

            if inner_key in final_graph.keys():
                final_graph[inner_key].append(key)
            else:
                final_graph[inner_key] = []
                final_graph[inner_key].append(key)
    return final_graph

def main():
    graph = dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    )

    # graph = dict(
    # Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    # Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    # Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    # Drobeta=dict(Mehadia=75),
    # Eforie=dict(Hirsova=86),
    # Fagaras=dict(Sibiu=99),
    # Hirsova=dict(Urziceni=98),
    # Iasi=dict(Vaslui=92, Neamt=87),
    # Lugoj=dict(Timisoara=111, Mehadia=70),
    # Oradea=dict(Zerind=71, Sibiu=151),
    # Pitesti=dict(Rimnicu=97),
    # Rimnicu=dict(Sibiu=80),
    # Urziceni=dict(Vaslui=142))

    graph = make_undirected_graph(graph)

    solution = bfs(graph)
    max_index = 0
    for i in range(len(solution)):
        if len(solution[i]) > len(solution[max_index]):
            max_index = i
    print(solution[max_index])

if __name__ == '__main__':
    main()
