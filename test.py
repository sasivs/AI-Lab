def enum_all(self, query, index):
    if index == len(self.random_vars):
        return 1
    node = self.random_vars[index]
    if node.denotion in query.keys() and \
        all(parent.denotion in query.keys() for parent in node.parents):
        prob = node.cpt[query[node.denotion]]
        for parent in node.parents:
            prob = prob[query[parent.denotion]]
        return prob*self.enum_all(query, index+1)
    elif node.denotion in query.keys():
        prob = node.cpt[query[node.denotion]]
        for parent in node.parents:
            if parent.denotion not in query.keys():
                for value in parent.values:
                    query[parent.denotion] = value
                    # prob = 
 