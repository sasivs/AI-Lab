# -*- coding: utf-8 -*-
"""
Perform clustering of data uisng Expectation Maximization (emObj)
Created on Sun Nov 27 18:01:32 2022
"""
import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal

class EM:
    def __init__(self, k, max_iter=5):
        self.k = k
        self.max_iter = int(max_iter)

    def initialize(self, X):
        self.shape = X.shape
        self.n, self.m = self.shape
        print(self.n, self.m)
        #ProbCluster_i is prob of each class, 1/k
        self.ProbCluster_i = np.full(shape=self.k, fill_value=1/self.k)
        #weight = 1/k
        self.weights = np.full( shape=self.shape, fill_value=1/self.k)
        
        random_rows = np.random.randint(low=0, high=self.n, size=self.k) #get k values
        #take a random sample as the mean vector
        self.mu = [X[row_index,:] for row_index in random_rows ]
        print(self.mu)
        print(X.T)
        #consider the covariance of the entire data
        self.sigma = [np.cov(X.T) for _ in range(self.k) ]  #np.cov():each row represents a variable
        print(self.sigma)

    def e_step(self, X):
        # E-Step: update weights and ProbCluster_i holding mu and sigma constant
        # calculating the probability that Xi came from each class and normalizing
        self.weights = self.predict_prob(X) #array of size(n,k), pij
        print(self.weights)
        #ProbCluster_i is estimated by averaging over all examples
        self.ProbCluster_i = self.weights.mean(axis=0) #for k clusters
        print(self.ProbCluster_i)
    
    def m_step(self, X):
        # M-Step: update mu and sigma holding ProbCluster_i and weights constant
        for i in range(self.k):
            weight = self.weights[:, [i]] #ith cluster weight, pij
            print(weight)
            total_weight = weight.sum() #ni = sum(pij)
            self.mu[i] = (X * weight).sum(axis=0) / total_weight
            self.sigma[i] = np.cov(X.T, 
                aweights=(weight/total_weight).flatten(), 
                bias=True) #
        print(self.mu)
        print(self.sigma)

    def fit(self, X):
        self.initialize(X)
        
        for iteration in range(self.max_iter):
            self.e_step(X)
            self.m_step(X)
            break
            
    # use multivariate normal distribution to compute Prob
    # calculating the probability that Xi came from each class and normalizing
    def predict_prob(self, X):
        likelihood = np.zeros( (self.n, self.k) )
        for i in range(self.k):
            distribution = multivariate_normal(
                mean=self.mu[i], 
                cov=self.sigma[i])
            likelihood[:,i] = distribution.pdf(X)    #P(Xj|Ci)
        # print(likelihood, self.ProbCluster_i)
        print(np.shape(likelihood))
        numerator = likelihood * self.ProbCluster_i #pdf of each cluster
        denominator = numerator.sum(axis=1)[:, np.newaxis] #sum over all clusters
        weights = numerator / denominator #pij
        return weights
    
    def predict(self, X):
        weights = self.predict_prob(X)
        #hard assignment of cluster label
        return np.argmax(weights, axis=1) #the cluster with highest weight
    

X = pd.read_csv('dataset.csv', header=0).values
print(X)

np.random.seed(1)
emObj = EM(k=3, max_iter=100)
emObj.fit(X)
predictions = emObj.predict(X)
print("Predictions:", predictions)