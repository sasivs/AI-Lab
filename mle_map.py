import itertools, copy, random

class RandomVariable:
    '''
    Class to hold metadata about each random variable.
    '''

    def __init__(self, name, denotion, values, parents, children, cpt, topo_index):
        self.name = name
        self.denotion = denotion
        self.values = values
        self.parents = parents
        self.children = children
        self.cpt = cpt
        self.topo_index = topo_index

    def __str__(self):
        return self.name
    
    def call_build_distribution(self):
        if self.parents:
            dis = self.build_distribution(self.parents, 0)
            cpt = {self.denotion:{value:copy.deepcopy(dis) for value in self.values}}
        else:
            cpt = {self.denotion:{value:0 for value in self.values}}
        self.cpt = cpt
        return 
    
    def build_distribution(self, rvars, index):
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
        if (index+1) == len(rvars):
            iter_dis = {rvars[index].denotion:{value:0 for value in rvars[index].values}}
            return iter_dis
        else:
            next_iter_dict = self.build_distribution(rvars, index+1)
            iter_dis = {rvars[index].denotion:{value:copy.deepcopy(next_iter_dict) for value in rvars[index].values}}
            return iter_dis


    def enum_ask(self, query, evidence):
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

    def normalize(self, distribution, query_combinations, query_vars, flag=True):
        query_vars = [var.denotion for var in query_vars]
        normalize_dict = {}
        for comb in query_combinations:
            key = ''
            value = distribution
            for item in comb.items():
                if not flag:
                    value = value[item[0].denotion][item[1]]
                else:
                    value = value[item[0]][item[1]]
                # if not item[0] in query_vars:
                if not flag:
                    if not item[0].denotion in query_vars:
                        key += item[0].denotion+str(item[1])
                else: 
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
                if not flag:
                    value = value[items[i][0].denotion][items[i][1]]
                else:
                    value = value[items[i][0]][items[i][1]]
                if not flag:
                    if not items[i][0].denotion in query_vars:
                        key += items[i][0].denotion+str(items[i][1])
                else: 
                    if not items[i][0] in query_vars:
                        key += str(items[i][0])+str(items[i][1])
            i+=1
            key += str(items[i][0])+str(items[i][1])
            if not flag:
                value[items[i][0].denotion][items[i][1]] = (value[items[i][0].denotion][items[i][1]]/normalize_dict[key])
            else:
                value[items[i][0]][items[i][1]] = (value[items[i][0]][items[i][1]]/normalize_dict[key])

    def ml_query(self, queries, samples):
        samples = list(samples.items())
        for query in queries:
            distribution = self.build_distribution(query[0]+query[1], 0)
            query_list = [[(rv,value) for value in rv.values] for rv in query[0]+query[1]]
            combinations = self.combinations(len(query[0]+query[1]), query_list)
            for comb in combinations:
                prob_dict = distribution
                fav_indices = [_ for _ in range(len(samples))]
                evidence_indices = [_ for _ in range(len(samples))]
                comb = list(comb.items())
                for index in range(len(comb)):
                    if index != (len(comb)-1):
                        prob_dict = prob_dict[comb[index][0].denotion][comb[index][1]]
                    fav_indices = [_ for _ in fav_indices if samples[_][0][comb[index][0].topo_index-1] == comb[index][1]]
                    if comb[index][0] in query[1]:
                        evidence_indices = [_ for _ in evidence_indices if samples[_][0][comb[index][0].topo_index-1] == comb[index][1]]
                fav_choices = 0
                for ind in fav_indices:
                    fav_choices += samples[ind][1]
                evidence_choices = 0
                for ind in evidence_indices:
                    evidence_choices += samples[ind][1]
                prob = fav_choices/evidence_choices
                prob_dict[comb[index][0].denotion][comb[index][1]] = prob
            print('probability: ', distribution)
            print()

    def map_query(self, queries, samples):
        samples = list(samples.items())
        for query in queries:
            distribution = self.build_distribution(query[0]+query[1], 0)
            query_list = [[(rv,value) for value in rv.values] for rv in query[0]+query[1]]
            combinations = self.combinations(len(query[0]+query[1]), query_list)
            for comb in combinations:
                prob_dict = distribution
                fav_indices = [_ for _ in range(len(samples))]
                comb = list(comb.items())
                for index in range(len(comb)):
                    if index != (len(comb)-1):
                        prob_dict = prob_dict[comb[index][0].denotion][comb[index][1]]
                    fav_indices = [_ for _ in fav_indices if samples[_][0][comb[index][0].topo_index-1] == comb[index][1]]
                fav_choices = 1
                for ind in fav_indices:
                    fav_choices += samples[ind][1]
                total_choices = 1
                for ind in range(len(samples)):
                    total_choices += samples[ind][1]
                prob = fav_choices/total_choices
                prob_dict[comb[index][0].denotion][comb[index][1]] = prob
            self.normalize(distribution, combinations, query[0], False)
            print('probability: ', distribution)
            print()

                    
def main():
    a = RandomVariable('A', 'A', [True, False], None, None, None, 1)
    b = RandomVariable('B', 'B', [True, False], None, None, None, 2)
    c = RandomVariable('C', 'C', [True, False], None, None, None, 3)
    d = RandomVariable('D', 'D', [True, False], None, None, None, 4)
    e = RandomVariable('E', 'E', [True, False], None, None, None, 5)
    a.children = [c]
    b.children = [c]
    c.parents = [a, b]
    c.children = [d,e]
    d.parents = [c]
    e.parents = [e]
    bayes_net = BayesianNetwork([a,b,c,d,e])

    samples = {
        (0,0,0,1,0):5, (0,0,0,0,1):1, (0,0,0,1,1):1, 
        (0,0,0,0,0):50, (0,0,1,1,0):1, (0,0,1,0,1):1,
        (0,0,1,1,1):1, (0,0,1,0,0):0, (1,0,0,1,0):1,
        (1,0,0,0,1):1, (1,0,0,1,1):0, (1,0,0,0,0):10, 
        (1,0,1,1,0):6, (1,0,1,0,1):8, (1,0,1,1,1):15,
        (1,0,1,0,0):1, (1,1,0,1,0):1, (1,1,0,0,1):1,
        (1,1,0,1,1):0, (1,1,0,0,0):2, (1,1,1,1,0):12,
        (1,1,1,0,1):15, (1,1,1,1,1):29, (1,1,1,0,0):0
    }
    queries = [[[a], [c,d]], [[a,b], [c]], [[c], [d,e]], [[b,c], [d,e]], [[d,e], [c]]]
    bayes_net.ml_query(queries, samples)
    bayes_net.map_query(queries, samples)

if __name__ == '__main__':
    main()