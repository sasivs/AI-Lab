class CSP:
    '''
    Class to solve a problem using CSP approach.
    Contains all the functions relevant to the CSP.
    '''

    def __init__(self, graph):
        self.graph = graph

    def degree_heuristic(self, vertices):
        '''
        orders the vertices of the graph based on the degree 
        and returns the vertex with max degree.
        '''
        return sorted(vertices.items(), key=lambda x: len(x[1]), reverse=True)[0][0]
    
    def minimum_remaining_values_heuristic(self, domains):
        '''
        Orders the vertices for which assignment have to be done
        based on the number of valid values available for them in their domain. 
        '''
        ordering = sorted(domains.items(), key=lambda x: len(x[1]))
        ties = {}
        for index in range(1,len(ordering)):
            if len(ordering[index][1]) == len(ordering[index-1][1]):
                ties[ordering[index][0]] = self.graph[ordering[index][0]]
                ties[ordering[index-1][0]] = self.graph[ordering[index-1][0]]
            else:
                break
        if ties:
            return self.degree_heuristic(ties)
        return ordering[0][0]

    def select_unassigned_variable(self, assignment, domains):
        '''
        Selects the next vertex for assignment from the set of unassigned
        vertices based on mrv heuristic and uses degree heuristic for tie-breaks.
        '''
        unassigned = set(self.graph.keys())-set(assignment.keys())
        unassigned_domains = {ver:domains[ver] for ver in unassigned}
        return self.minimum_remaining_values_heuristic(unassigned_domains)
    
    def least_constraining_value(self, vertex, domains):
        '''
        Orders the domain vlaues of the vertex in a way that it maximizes the
        available domain values for its neighbouring vertices.
        '''
        domain_points = {d_val:0 for d_val in domains[vertex]}
        value_domains = {}
        for adj in self.graph[vertex]:
            value_domains[adj] = {}
            for value in domains[vertex]:
                value_domains[adj][value] = list(set(domains[adj])-set([value]))
            sorted_domain = sorted(value_domains[adj].items(), key=lambda x:len(x[1]), reverse=True)
            if sorted_domain:
                domain_points[sorted(value_domains[adj].items(), key=lambda x:len(x[1]), reverse=True)[0][0]]+=1
        domains[vertex] = list(dict(sorted(domain_points.items(), key=lambda x:x[1], reverse=True)).keys())
        return domains

    def domain_changed(self, adj, values, domains):
        '''
        Check if the domain is changed and if changed return the changed domain.
        '''
        for value in values:
            if value in domains[adj]:
                domains[adj].remove(value)
                return True, domains
        return False, domains

    def arc_consistency(self, vertex, value, assignment, domains):
        '''
        Check the consistency of values for its neighbouring vertices
        if the current vertex is assigned this value.
        '''
        unassigned_adj = set(self.graph[vertex])-set(assignment.keys())
        for adj in unassigned_adj:
            bool_, domains = self.domain_changed(adj, [value], domains)
            if bool_:
                if not domains[adj]:
                    return False
                neighbour_unassigned = set(self.graph[adj])-set(assignment.keys())
                for nei_adj in neighbour_unassigned:
                    bool_, domains = self.domain_changed(nei_adj, domains[adj], domains)
                    if bool_:
                        if not domains[adj]:
                            return False
        return True

    def is_valid(self, assignment, vertex, value):
        '''
        Check if this assignment is valid.
        '''
        for adj in self.graph[vertex]:
            if adj in assignment.keys():
                if value == assignment[adj]:
                    return False
        return True
    
    def backtracking_search(self, assignment, domains):
        '''
        Main algorithm to implement the above functions.
        '''
        import copy
        if len(assignment.keys()) == len(self.graph.keys()):
            return assignment
        vertex = self.select_unassigned_variable(assignment, domains)
        domains = self.least_constraining_value(vertex, domains)
        for value in domains[vertex]:
            if self.is_valid(assignment, vertex, value):
                assignment[vertex] = value
            if self.arc_consistency(vertex, value, assignment, domains):
                result = self.backtracking_search(assignment, domains)
                if result:
                    return result
        return False

def make_graph(filename):
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
        graph = {}
        for line in lines:
            line = line.split()
            if int(line[1]) in graph.keys():
                graph[int(line[1])].append(int(line[2]))
            else:
                graph[int(line[1])] = [int(line[2])]
            if int(line[2]) in graph.keys():
                graph[int(line[2])].append(int(line[1]))
            else:
                graph[int(line[2])] = [int(line[1])]
        for key, value in graph.items():
            graph[key] = list(set(value))
    return graph

def main():
    # graph = {1:[2,3,5], 2:[1,5,6], 3:[1,5,6], 4:[6], 5:[1,2,3,6], 6:[2,3,4,5]}
    # domains = {ver:[1,2,3] for ver in graph.keys()}
    # filenames = ['anna.col', 'school1.col']
    filenames = ['anna.col']
    for filename in filenames:
        print('For file: ', filename)
        graph = make_graph(filename)
        for i in range(1,len(graph.keys())+1):
            domains = {ver:[j for j in range(1,i+1)] for ver in graph.keys()}
            csp_problem = CSP(graph)
            result = csp_problem.backtracking_search(assignment={}, domains=domains)
            if result:
                print('No: of colors: ', i)
                break
        print(dict(sorted(result.items(), key=lambda x:x[0])))
        print()

if __name__ == '__main__':
    main()

# not(studie(john)).
# lucky(john).
# lottery(X):- lucky(X).
# pass(X,Y):- studies(X,Y).
# pass(X,Y):- lucky(X).
# happys(X):- pass(X,history), lottery(X).