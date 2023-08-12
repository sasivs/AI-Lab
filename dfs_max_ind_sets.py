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

def dfs(graph, subset=set([]), solution=[], explored=[]):
    '''
    Start with an empty set and add each vertex one by one to it to form
    subsets of the vertices set.
    Check if the subset is an independent set and add it to the solution list.
    '''
    import copy
    if independency_test(graph, subset):
        solution.append(copy.deepcopy(subset))
    
    explored.append(copy.deepcopy(subset))
    children = set(graph.keys())-subset
    
    for ver in children:
        subset.add(ver)
        if independency_test(graph, subset):
            if not isExplored(explored, subset):
                solution = dfs(graph, subset, solution, explored)
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
    # graph = dict(
    # Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    # Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    # Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    # )

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

    solution = dfs(graph)
    max_index = 0
    for i in range(len(solution)):
        if len(solution[i]) > len(solution[max_index]):
            max_index = i
    print(solution[max_index])

if __name__ == '__main__':
    main()

