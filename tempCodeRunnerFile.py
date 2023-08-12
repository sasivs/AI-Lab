def normalize(self, distribution):
    #     for rv in distribution.keys():
    #         total_prob = 0
    #         for value in distribution[rv].keys():
    #             iter_dict = distribution[rv][value]
    #             while True:
    #                 if isinstance(iter_dict, float):
    #                     total_prob += iter_dict
    #                     break
    #                 iter_dict = iter_dict[list(iter_dict.keys())[0]]
    #         print(total_prob)