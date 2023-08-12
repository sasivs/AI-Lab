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
                domain_points[sorted_domain[0][0]]+=1
        domains[vertex] = list(dict(sorted(domain_points.items(), key=lambda x:x[1], reverse=True)).keys())
        return domains

    def domain_changed(self, adj, ver, domains):
        '''
        Check if the domain is changed and if changed return the changed domain.
        '''
        i=0
        revised = False
        while(len(domains[adj])!=0) and i<len(domains[adj]):
            if not (set(domains[ver])-set([domains[adj][i]])):
                domains[adj].pop(i)
                revised = True
            else:
                i+=1
        return revised, domains

    def arc_consistency(self, vertex, assignment, domains):
        '''
        recursively check the consistency of the neighbouring vertices
        and return false if any of the domains of the adjacent vertices is empty.
        (Same as AC-3 arc consistency method in the textbook)
        '''
        neighbour_unassigned = [(ver, adj)for adj in self.graph[vertex] for ver in (set(self.graph[adj])-set(assignment.keys()))]
        while(len(neighbour_unassigned)!=0):
            ver, adj = neighbour_unassigned.pop(0)
            bool_, domains = self.domain_changed(ver, adj, domains)
            if bool_:
                if not domains[adj]:
                    return False
                neighbour_unassigned+=[(v, adj) for v in (set(self.graph[adj])-set(assignment.keys())-set([ver]))] 
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

    def reduce_domains(self, vertex, value, domains):
        '''
        Remove the value 'v' from the domains of vertices adjacent to vertex.
        '''
        for adj in self.graph[vertex]:
            if value in domains[adj]:
                domains[adj].remove(value)

    def extend_domains(self, vertex, value, domains):
        '''
        Add the value 'v' to the domains of vertices adjacent to vertex.
        '''
        for adj in self.graph[vertex]:
            if value not in domains[adj]:
                domains[adj].append(value)
    
    def backtracking_search(self, assignment, domains):
        '''
        Main algorithm to implement the above functions.
        1.) Select unassignedd variable/vertex from the avaiable variables.
        2.) order the domains based on least constraing value first
        3.) if the assignment is valid wrt to previous assignments, then move ahead.
        4.) reduce the domains of the adjacent vertices after the assigned value to 
        the current vertex is known to be valid.
        5.) Check arc-consistency and if it returns true recursively call the backtrack algorithm.
        6.) Further, if this assignment does not give a complete solution in the future, \
            repopulate the reduced domains of the adjacent vertices.
        7.) Intermedially, if a solution is found, return the solution.
        '''
        import copy
        if len(assignment.keys()) == len(self.graph.keys()):
            return assignment
        vertex = self.select_unassigned_variable(assignment, domains)
        domains = self.least_constraining_value(vertex, domains)
        for value in domains[vertex]:
            if self.is_valid(assignment, vertex, value):
                assignment[vertex] = value
                self.reduce_domains(vertex, value, domains)
                domains_copy = copy.deepcopy(domains)
                if self.arc_consistency(vertex, assignment, domains_copy):
                    result = self.backtracking_search(assignment, domains)
                    if result:
                        return result
                self.extend_domains(vertex, value, domains)
        return False


def make_graph(filename):
    '''
    Construct a graph from the file given as input.
    It constructs a bidirectional graph.
    '''
    filename = './instances/'+filename
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
        graph = {}
        for line in lines:
            line = line.split()
            if int(line[1]) in graph.keys():
                graph[int(line[1])].append(int(line[2]))
            else:
                graph[int(line[1])] = [int(line[2])]
            if int(line[2]) not in graph.keys():
                graph[int(line[2])] = []
        for key, value in graph.items():
            graph[key] = list(set(value))
    return graph

def check_graph_color(assignment, graph):
    for key, value in assignment.items():
        for adj in graph[key]:
            if value == assignment[adj]:
                print(adj, assignment[adj])
                print(key, value)
                return False
    return True

def main():
    '''
    Main function
    '''
    filenames = ['anna.col', 'school1.col']
    for filename in filenames:
        print('For file: ', filename)
        graph = make_graph(filename)
        if filename == 'anna.col':
            domains = {ver:[j for j in range(1,12)] for ver in graph.keys()}
        else:
            domains = {ver:[j for j in range(1,43)] for ver in graph.keys()}
        csp_problem = CSP(graph)
        result = csp_problem.backtracking_search(assignment={}, domains=domains)
        if result:
            print("Valid: ", check_graph_color(result, graph))
            print(dict(sorted(result.items(), key=lambda x:x[0])))
            print('No: of colors required = ',sorted(result.items(), key=lambda x:x[1])[-1][-1])
        else:
            print("No result")
        print()

if __name__ == '__main__':
    main()
