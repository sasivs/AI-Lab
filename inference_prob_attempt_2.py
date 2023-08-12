import itertools, copy

class RandomVariable:
    '''
    Class to hold metadata about each random variable.
    '''

    def __init__(self, name, denotion, values, parents, children):
        self.name = name
        self.denotion = denotion
        self.values = values
        self.parents = parents
        self.children = children
        self.cpt = {}
        self.topo_index = None

    def __str__(self):
        return self.name


    def display_node(self):
        print('Name: ', self.name)
        print('Denoted by: ', self.denotion)
        print('Values: ', self.values)
        print('Parents: ', [parent.name for parent in self.parents or []])
        print('Children: ', [child.name for child in self.children or []])
        print("CPT: ")
        print(self.cpt)
        print(self.topo_index)


class BayesianNetwork():
    '''
    Bayesian network class to hold the network of nodes.
    It extends the itertools class to make use of combinations method by overriding it.
    '''

    def __init__(self, random_vars):
        self.random_vars = self.build_topological_order(random_vars)
        for index,rv in enumerate(self.random_vars):
            rv.topo_index = index
    
    def build_topological_order(self, random_vars):
        parents_list = [(node, [parent.denotion for parent in node.parents]) for node in random_vars]
        parents_list = sorted(parents_list, key = lambda c : len(c[1]))
        sorted_list = []
        while parents_list:
            iter_node = parents_list.pop(0)
            for _ in range(len(parents_list)):
                if iter_node[0].denotion in parents_list[_][1]:
                    parents_list[_][1].remove(iter_node[0].denotion)
            sorted_list.append(iter_node[0])
            parents_list = sorted(parents_list, key = lambda c : len(c[1]))
        return sorted_list
    
    def combinations(self, n, item_list):
        single_list = [__ for _ in item_list for __ in _]
        combs = itertools.combinations(single_list, n)
        valid_combs = []
        for comb in combs:
            flag = False
            for sub_list in item_list:
                for comb_2 in itertools.combinations(comb, 2):
                    if all(x in sub_list for x in comb_2):
                        flag = True
                        break
                if flag:
                    break
            if not flag:
                valid_combs.append(dict(comb))
        return valid_combs
    
    def enum_ask(self, query, evidence):
        query = sorted(query, key = lambda c:c.topo_index)
        evidence = sorted(evidence, key = lambda c:c.topo_index)
        query_list = [[(rv,value) for value in rv.values] for rv in query+evidence]
        query_combinations = self.combinations(len(query+evidence), query_list)
        distribution = {}
        for comb in query_combinations:
            key = [item[0].denotion+str(item[1]) for item in comb.items()]
            distribution[frozenset(key)] = self.enum_all(comb, 0)
        self.normalize(distribution, query[0])
        return distribution
    
    def normalize(self, distribution, rv):
        for value in rv.values:
            key = rv.denotion+str(value)
            for comb in [set(item[0]) for item in distribution.items() if key in item[0]]:
                norm_combs = [(frozenset(comb),distribution[frozenset(comb)])]
                comb_key = set(copy.deepcopy(comb))
                comb_key.remove(key)
                norm_combs += [item for item in distribution.items() if comb!=item[0] and comb_key.issubset(item[0])]
                prob_sum = sum(prob for _, prob in norm_combs)
                for item in norm_combs:
                    distribution[frozenset(item[0])] = distribution[frozenset(item[0])]/prob_sum

    def enum_all(self, query_comb, index):
        if index >= len(self.random_vars):
            return 1
        if self.random_vars[index] in query_comb.keys():
            parent_key = [parent.denotion+str(query_comb[parent]) for parent in self.random_vars[index].parents]
            if frozenset(parent_key+[self.random_vars[index].denotion+str(query_comb[self.random_vars[index]])]) not in self.random_vars[index].cpt.keys():
                return (1-sum([self.random_vars[index].cpt[_] for _ in self.random_vars[index].cpt.keys() if frozenset(parent_key).issubset(_)])) * self.enum_all(query_comb,index+1)
            else:
                return self.random_vars[index].cpt[frozenset(parent_key+[self.random_vars[index].denotion+str(query_comb[self.random_vars[index]])])] * self.enum_all(query_comb, index+1)
        else:
            prob = 0
            for value in self.random_vars[index].values:
                query_comb[self.random_vars[index]] = value
                parent_key = [parent.denotion+str(query_comb[parent]) for parent in self.random_vars[index].parents]
                if frozenset(parent_key+[self.random_vars[index].denotion+str(query_comb[self.random_vars[index]])]) not in self.random_vars[index].cpt.keys():
                    prob += ((1-sum([self.random_vars[index].cpt[_] for _ in self.random_vars[index].cpt.keys() if set(parent_key).issubset(_)])) * self.enum_all(query_comb,index+1))
                else:
                    prob += (self.random_vars[index].cpt[frozenset(parent_key+[self.random_vars[index].denotion+str(query_comb[self.random_vars[index]])])] * self.enum_all(query_comb, index+1))
            return prob

def main():
    burglary = RandomVariable('Burglary', 'B', [True, False], None, None)
    earthquake = RandomVariable('Earthquake', 'E', [True, False], None, None)
    alarm = RandomVariable('Alarm', 'A', [True, False], None, None)
    johncalls = RandomVariable('JohnCalls', 'J', [True, False],  None, None)
    marycalls = RandomVariable('MaryCalls', 'M', [True, False], None, None)
    burglary.parents = []
    burglary.children = [alarm]
    earthquake.parents = []
    earthquake.children = [alarm]
    alarm.children = [johncalls, marycalls]
    alarm.parents = [burglary, earthquake]
    johncalls.parents = [alarm]
    johncalls.children = []
    marycalls.parents = [alarm]
    marycalls.children = []
    burglary.cpt[frozenset(['BTrue'])] = 0.001
    earthquake.cpt[frozenset(['ETrue'])] = 0.002
    alarm.cpt[frozenset(['ATrue', 'BTrue', 'ETrue'])] = 0.95 
    alarm.cpt[frozenset(['ATrue', 'BTrue', 'EFalse'])] = 0.94 
    alarm.cpt[frozenset(['ATrue', 'BFalse', 'ETrue'])] = 0.29 
    alarm.cpt[frozenset(['ATrue', 'BFalse', 'EFalse'])] = 0.001
    johncalls.cpt[frozenset(['JTrue', 'ATrue'])] = 0.9
    johncalls.cpt[frozenset(['JTrue', 'AFalse'])] = 0.05
    marycalls.cpt[frozenset(['MTrue', 'ATrue'])] = 0.7
    marycalls.cpt[frozenset(['MTrue', 'AFalse'])] = 0.01
    nodes = [burglary, earthquake, alarm, johncalls, marycalls]
    bayes_network = BayesianNetwork(nodes)
    
    queries = [[[johncalls],[burglary, earthquake]],[[alarm],[burglary]],[[earthquake], [marycalls]], [[burglary], [alarm]], \
        [[johncalls, marycalls], [alarm]], [[johncalls], [alarm]], [[marycalls], [alarm]]]

    for query in queries:
        distribution = bayes_network.enum_ask(query[0], query[1])
        print('For the query: ', [[var.__str__() for var in q] for q in query])
        print(distribution)
        print()
    
if __name__ == '__main__':
    main()
