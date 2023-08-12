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
        for comb in list(combs):
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

    def query_cpt(self, query_var, sample, prob):
        current_val = 0
        for item in query_var.cpt[query_var.denotion].items():
            prob_dict = item[1]
            for p_item in query_var.parents or []:
                prob_dict = prob_dict[p_item.denotion][sample[p_item.topo_index-1]]
            if (current_val+prob_dict) > prob:
                sample.append(item[0])
                return
            current_val += prob_dict
        return 
    
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

    def normalize(self, distribution, query_combinations, query_vars):
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

    def generate_sample(self, required_values={}):
        samples = []
        top_order = {node.topo_index-1:node.denotion for node in self.random_vars}
        while len(samples)!=1000:
            sample = []
            flag = True
            for rv in self.random_vars:
                random_num = random.uniform(0,1)
                self.query_cpt(rv, sample, random_num)
            if required_values:
                for index in range(len(sample)):
                    if required_values[top_order[index]] and sample[index] not in required_values[top_order[index]]:
                        flag = False
                        break
            if flag:
                samples.append(sample)
        return samples
    
    def query_prior_sample(self, queries):
        samples = self.generate_sample()
        top_order = {node.denotion:node.topo_index-1 for node in self.random_vars}
        for query in queries:
            fav_indices = [_ for _ in range(len(samples))]
            for item in query['query'].items():
                fav_indices = [_ for _ in fav_indices if samples[_][top_order[item[0]]]==item[1]]
            evidence_fav_indices = [_ for _ in range(len(samples))]
            if query.get('evidence'):
                for item in query['evidence'].items():
                    fav_indices = [_ for _ in fav_indices if samples[_][top_order[item[0]]]==item[1]]
                    evidence_fav_indices = [_ for _ in evidence_fav_indices if samples[_][top_order[item[0]]]==item[1]]
            
            prob = (len(fav_indices)+1)/(len(evidence_fav_indices)+1)
            print(query, 'probability: ', prob)
    
    def rejection_sampling(self, queries):
        required_values = {rv.denotion:set() for rv in self.random_vars}
        for query in queries:
            if query.get('evidence'):
                for item in query.get('evidence').items():
                    required_values[item[0]].add(item[1])
        samples = self.generate_sample(required_values)
        top_order = {node.denotion:node.topo_index-1 for node in self.random_vars}
        for query in queries:
            fav_indices = [_ for _ in range(len(samples))]
            for item in query['query'].items():
                fav_indices = [_ for _ in fav_indices if samples[_][top_order[item[0]]]==item[1]]
            evidence_fav_indices = [_ for _ in range(len(samples))]
            if query.get('evidence'):
                for item in query['evidence'].items():
                    fav_indices = [_ for _ in fav_indices if samples[_][top_order[item[0]]]==item[1]]
                    evidence_fav_indices = [_ for _ in evidence_fav_indices if samples[_][top_order[item[0]]]==item[1]]
            prob = len(fav_indices)/len(evidence_fav_indices)
            print(query, 'probability: ', prob)
    
    def generate_likelihood_samples(self, query):
        samples = {}
        top_order = {node.denotion:node.topo_index-1 for node in self.random_vars}
        index = 0
        while index!=1000:
            sample = []
            weight = 1
            for rv in self.random_vars:
                if query.get('evidence').get(rv.denotion):
                    sample.append(query['evidence'][rv.denotion])
                    req_cpt_prob = self.random_vars[top_order[rv.denotion]].cpt[rv.denotion][query.get('evidence').get(rv.denotion)]
                    for parent in self.random_vars[top_order[rv.denotion]].parents or []:
                        req_cpt_prob = req_cpt_prob[parent.denotion][sample[top_order[parent.denotion]]]
                    weight = weight * req_cpt_prob
                else:
                    random_num = random.uniform(0,1)
                    self.query_cpt(rv, sample, random_num)
            sample = tuple(sample)
            if samples.get(sample):
                samples[sample]+=weight
            else:
                samples[sample] = weight
            index+=1
        return samples

    def likelihood_sampling(self, queries):
        top_order = {node.denotion:node.topo_index-1 for node in self.random_vars}
        for query in queries:
            samples = self.generate_likelihood_samples(query)
            total_weights = sum(samples.values())
            samples = list(samples.items())
            fav_indices = [_ for _ in range(len(samples))]
            for item in query['query'].items():
                fav_indices = [_ for _ in fav_indices if samples[_][0][top_order[item[0]]]==item[1]]
            fav_weights = 0
            for index in fav_indices:
                fav_weights += samples[index][1]
            prob = fav_weights/total_weights
            print(query, 'probability: ', prob)

    def query_gibbs_cpt(self, query_var, sample, prob, distribution, evidence):
        current_val = 0
        for item in distribution[query_var.denotion].items():
            prob_dict = item[1]
            for p_item in evidence or []:
                prob_dict = prob_dict[p_item.denotion][sample[p_item.topo_index-1]]
            if (current_val+prob_dict) > prob:
                sample[query_var.topo_index-1]=item[0]
                return
            current_val += prob_dict
        return 
            
    def generate_gibbs_samples(self, query):
        samples = {}
        sample = []
        for rv in self.random_vars:
            if rv.denotion in query.get('evidence'):
                sample.append(query['evidence'][rv.denotion])
            else:
                sample.append(rv.values[random.randint(0, len(rv.values)-1)])
        samples[tuple(sample)] = 1
        while sum(samples.values())!=10000:
            random_rv = self.random_vars[random.randint(0, len(self.random_vars)-1)]
            while random_rv.denotion in query.get('evidence').keys():
                random_rv = self.random_vars[random.randint(0, len(self.random_vars)-1)]
            evidence_vars = [_ for _ in random_rv.parents or []+random_rv.children or []]
            evidence_vars += [_ for child in random_rv.children or [] for _ in child.parents if _!=random_rv]
            evidence_vars = list(set(evidence_vars))
            prob_dist = self.enum_ask([random_rv], evidence_vars)
            self.query_gibbs_cpt(random_rv, sample, random.uniform(0,1), prob_dist, evidence_vars)
            if tuple(sample) in samples.keys():
                samples[tuple(sample)] += 1
            else:
                samples[tuple(sample)] = 1
        return samples

    def gibbs_sampling(self, queries):
        top_order = {node.denotion:node.topo_index-1 for node in self.random_vars}
        for query in queries:
            samples = self.generate_gibbs_samples(query)
            samples = list(samples.items())
            fav_indices = [_ for _ in range(len(samples))]
            for item in query['query'].items():
                fav_indices = [_ for _ in fav_indices if samples[_][0][top_order[item[0]]]==item[1]]
            evidence_fav_indices = [_ for _ in range(len(samples))]
            if query.get('evidence'):
                for item in query['evidence'].items():
                    fav_indices = [_ for _ in fav_indices if samples[_][0][top_order[item[0]]]==item[1]]
                    evidence_fav_indices = [_ for _ in evidence_fav_indices if samples[_][0][top_order[item[0]]]==item[1]]
            fav_events = 0
            for _ in fav_indices:
                fav_events += samples[_][1]
            evidence_events =0
            for _ in evidence_fav_indices:
                evidence_events += samples[_][1]
            prob = fav_events/evidence_events
            print(query, 'probability: ', prob)
            
def main():
    burglary = RandomVariable('Burglary', 'B', [True, False], None, None, None, 1)
    earthquake = RandomVariable('Earthquake', 'E', [True, False], None, None, None, 2)
    alarm = RandomVariable('Alarm', 'A', [True, False], None, None, None, 3)
    johncalls = RandomVariable('JohnCalls', 'J', [True, False], None, None, None, 4)
    marycalls = RandomVariable('MaryCalls', 'M', [True, False], None, None, None, 5)
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
    # queries = [{'query':{'B':True}, 'evidence':{'J':True, 'M':True}}]
    # queries = [{'query':{'J':True}, 'evidence':{'A':True}}]
    queries = [{'query':{'A':True}, 'evidence':{'B':True, 'E':True}}]
    bayes_network.query_prior_sample(queries)
    bayes_network.rejection_sampling(queries)
    bayes_network.likelihood_sampling(queries)
    bayes_network.gibbs_sampling(queries)


if __name__ == '__main__':
    main()