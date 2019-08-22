# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:57:31 2017

@author: user
"""

from tests.crossvalidation import cross_validation
import numpy as np
from cleaning import cleaning 

version=True
iterations=30
P=2
k_latent=10
seed=0
lambda_val=0.02
coeff=30
dict_user, dict_pro, data_f = cleaning.clean(False)
lambda_vect=np.array([0.01, 0.03, 0.1, 0.3, 1, 3])
coeff_vect=np.array([1,3,10,30,50])
seed_vect=np.array([1])#9,33,100])
k_vect=np.array([40,50,60,70,80])
score=np.zeros((len(seed_vect),len(k_vect)))
print('Starting iterations')
#==============================================================================
# for idx_lambda in range(len(lambda_vect)):
#     for idx_coeff in range(len(coeff_vect)):
#        print('start iteration')
#         #for seed in seed_vect:
#             #for k_latent in k_vect:
#        score[idx_lambda][idx_coeff] = cross_validation(dict_user, dict_pro, k_latent, P, version, lambda_vect[idx_lambda], coeff_vect[idx_coeff], iterations, seed)
# score=np.array(score)
# print(score)                
#==============================================================================

for idx_seed in range(len(seed_vect)):
    for idx_k in range(len(k_vect)):
        #for seed in seed_vect:
            #for k_latent in k_vect:
        score[idx_seed][idx_k] = cross_validation(dict_user, dict_pro, k_vect[idx_k], P, version, lambda_val, coeff, iterations, seed_vect[idx_seed])
                
score=np.array(score)
print(score)                