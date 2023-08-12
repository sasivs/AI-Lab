import itertools, copy

class RandomVariable:
    '''
    Class to hold metadata about each random variable.
    '''

    def __init__(self, name, denotion, values, parents, children, cpt):
        self.name = name
        self.denotion = denotion
        self.values = values
        self.parents = parents
        self.children = children
        self.cpt = cpt

    def __str__(self):
        return self.name
    
    def call_build_distribution(self):
        '''
        Helper to call build distributions
        '''
        if self.parents:
            dis = self.build_distribution(self.parents, 0)
            cpt = {self.denotion:{value:copy.deepcopy(dis) for value in self.values}}
        else:
            cpt = {self.denotion:{value:0 for value in self.values}}
        self.cpt = cpt
        return 
    
    def build_distribution(self, rvars, index):
        '''
        Builds an empty cpt table for entering values
        '''
        if (index+1) == len(rvars):
            iter_dis = {rvars[index].denotion:{value:0 for value in rvars[index].values}}
            return iter_dis
        else:
            next_iter_dict = self.build_distribution(rvars, index+1)
            iter_dis = {rvars[index].denotion:{value:copy.deepcopy(next_iter_dict) for value in rvars[index].values}}
            return iter_dis

    def display_node(self):
        print('Name: ', self.name)
        print('Denoted by: ', self.denotion)
        print('Values: ', self.values)
        print('Parents: ', [parent.name for parent in self.parents or []])
        print('Children: ', [child.name for child in self.children or []])
        print("CPT: ")
        print(self.cpt)


class BayesianNetwork():
    '''
    Bayesian network class to hold the network of nodes.
    It extends the itertools class to make use of combinations method by overriding it.
    '''

    def __init__(self, random_vars):
        self.random_vars = random_vars

    
    def combinations(self, n, item_list):
        '''
        Returns all the possible combinations of n items of item_list
        Used for framing the queries containing n random variables
        '''
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
    
    def build_distribution(self, rvars, index):
        '''
        Builds empty distribution to enter probability values
        '''
        if (index+1) == len(rvars):
            iter_dis = {rvars[index].denotion:{value:0 for value in rvars[index].values}}
            return iter_dis
        else:
            next_iter_dict = self.build_distribution(rvars, index+1)
            iter_dis = {rvars[index].denotion:{value:copy.deepcopy(next_iter_dict) for value in rvars[index].values}}
            return iter_dis


    def enum_ask(self, query, evidence):
        '''
        Method for querying, calls enum_all method to find the probability distribution for the given random variables.
        '''
        query_list = [[(rv.denotion,value) for value in rv.values] for rv in query+evidence]
        query_combinations = self.combinations(len(query+evidence), query_list)
        distribution = self.build_distribution(query+evidence, 0)
        self.call_enum_all(query_combinations, distribution)
        self.normalize(distribution, query_combinations, query)
        return distribution
    
    def call_enum_all(self, query_combinations, distribution):
        for query in query_combinations:
            prob_dis = distribution 
            query_items = list(query.items())
            for i in range(len(query)-1):
                prob_dis = prob_dis[query_items[i][0]][query_items[i][1]]
            i+=1
            prob_dis[query_items[i][0]][query_items[i][1]] = self.enum_all(query)
        return 
    
    def enum_all(self, query):
        marginilaise_vars = [rv for rv in self.random_vars if rv.denotion not in query.keys()]
        marginalize_query_list = [[(rv.denotion,value) for value in rv.values] for rv in marginilaise_vars]
        marg_query_comb = self.combinations(len(marginilaise_vars), marginalize_query_list)
        new_queries = [copy.deepcopy(query|marg_query) for marg_query in marg_query_comb]
        total_prob = 0
        for que in new_queries:
            marg_prob = 1
            for rv in self.random_vars:
                prob = rv.cpt[rv.denotion][que[rv.denotion]]
                for parent in rv.parents or []:
                    prob = prob[parent.denotion][que[parent.denotion]]
                marg_prob = marg_prob*prob
            total_prob += marg_prob
        return total_prob

    def normalize(self, distribution, query_combinations, query_vars):
        '''
        Method for normalizing the probabilites
        '''
        query_vars = [var.denotion for var in query_vars]
        normalize_dict = {}
        for comb in query_combinations:
            key = ''
            value = distribution
            for item in comb.items():
                value = value[item[0]][item[1]]
                if not item[0] in query_vars:
                    key += str(item[0])+str(item[1])
            if key not in normalize_dict.keys():
                normalize_dict[key] = value
            else:
                normalize_dict[key] += value
        for comb in query_combinations:
            key = ''
            value = distribution
            items = list(comb.items())
            for i in range(len(items)-1):
                value = value[items[i][0]][items[i][1]]
                if not items[i][0] in query_vars:
                    key += str(items[i][0])+str(items[i][1])
            i+=1
            key += str(items[i][0])+str(items[i][1])
            value[items[i][0]][items[i][1]] = (value[items[i][0]][items[i][1]]/normalize_dict[key])

def main():
    burglary = RandomVariable('Burglary', 'B', [True, False], None, None, None)
    earthquake = RandomVariable('Earthquake', 'E', [True, False], None, None, None)
    alarm = RandomVariable('Alarm', 'A', [True, False], None, None, None)
    johncalls = RandomVariable('JohnCalls', 'J', [True, False], None, None, None)
    marycalls = RandomVariable('MaryCalls', 'M', [True, False], None, None, None)
    burglary.children = [alarm]
    earthquake.children = [alarm]
    alarm.children = [johncalls, marycalls]
    alarm.parents = [burglary, earthquake]
    johncalls.parents = [alarm]
    marycalls.parents = [alarm]
    nodes = [burglary, earthquake, alarm, johncalls, marycalls]
    for node in nodes: node.call_build_distribution()
    burglary.cpt['B'][True] = 0.001; burglary.cpt['B'][False] = 0.999
    earthquake.cpt['E'][True] = 0.002; earthquake.cpt['E'][False] = 0.998 
    alarm.cpt['A'][True]['B'][True]['E'][True] = 0.95 
    alarm.cpt['A'][True]['B'][True]['E'][False] = 0.94 
    alarm.cpt['A'][True]['B'][False]['E'][True] = 0.29 
    alarm.cpt['A'][True]['B'][False]['E'][False] = 0.001
    alarm.cpt['A'][False]['B'][True]['E'][True] = 0.05 
    alarm.cpt['A'][False]['B'][True]['E'][False] = 0.06 
    alarm.cpt['A'][False]['B'][False]['E'][True] = 0.71 
    alarm.cpt['A'][False]['B'][False]['E'][False] = 0.999
    johncalls.cpt['J'][True]['A'][True] = 0.9
    johncalls.cpt['J'][True]['A'][False] = 0.05
    johncalls.cpt['J'][False]['A'][True] = 0.1
    johncalls.cpt['J'][False]['A'][False] = 0.95
    marycalls.cpt['M'][True]['A'][True] = 0.7
    marycalls.cpt['M'][True]['A'][False] = 0.01
    marycalls.cpt['M'][False]['A'][True] = 0.3
    marycalls.cpt['M'][False]['A'][False] = 0.99

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
