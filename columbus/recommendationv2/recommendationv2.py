# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from cleaning import cleaning
import copy 
COEFF_CONF_GRAD=20
COEFF_CONF_ALS=40
COEFF_CONF=COEFF_CONF_GRAD
LAMBDA_VAL=0.2
SEED=0
ITER_ALS=25
ITER_SGD=25

def transform_dict_to_list(dict_user, dict_pro):
    """ Transform a dictionnary dict_user to a list list_user
    in order to set a fixed order of users and pros to create our matrix

    cleaning returns dictonnaries : dict_user = {id_user_1 : user_instance_1, id_user_2 : user_instance_2 ...}
                                   pro_user = {id_pro_1 : pro_instance_1, id_pro_2 : pro_instance_2...}
    This function returns list : list_user = [id_user_1, id_user_2]
                                 list_pro = [id_pro_1, id_pro_2]
    """
    list_user = []
    list_pro = []
    for user in dict_user.keys():
        list_user.append(dict_user[user].id)
    for pro in dict_pro.keys():
        list_pro.append(dict_pro[pro].id)
    return list_user, list_pro


def sgd(training_set, k_latent, lambda_val=LAMBDA_VAL, coeff=COEFF_CONF_GRAD, seed=SEED, alpha=0.0002, steps=ITER_SGD):
    """ 
    returns:
    
    the matrix of estimated probabilities minimizing the regularized squared error on the set of the known visits with the gradient method.
    
    parameters:
    
    training_set - Our matrix of ratings with shape p x n, where n is the number of users and p is the number of pros.
    
    k_latent     - The number of latent features in the user/item feature vectors. The paper recommends varying this 
                   between 20-200. Increasing the number of features may overfit but could reduce bias. 
    
    lambda_val   - Used for regularization during gradient. Increasing this value may increase bias
                   but decrease variance. Default is 0.2. 
    
    coeff        - The parameter associated with the confidence matrix discussed in the paper, where Cui = 1 + coeff*Rui. 
                   The paper found a default of 40 most effective. Decreasing this will decrease the variability in confidence between
                   various ratings.
    
    seed         - Set the seed for reproducible results
    
    alpha        - Learning rate
    
    steps        - The number of times to alternate between both user feature vector and item feature vector in
                   alternating least squares. More iterations will allow better convergence at the cost of increased computation. 
    """
    
    print('Performing Gradient method')
    
    num_pro,num_user=np.shape(training_set)
    num_score=num_user*num_pro
    
    C=copy.deepcopy(training_set)
    C[C!=0]=1
    
    # initialize our U/P feature vectors randomly with a set seed
    rstate = np.random.RandomState(seed)
    U = rstate.uniform(size = (num_user, k_latent)) # Random numbers in a n x k_latent shape
    P = rstate.uniform(size = (num_pro, k_latent))  # Random numbers in a p x k_latent shape
    
    
    rmse_vect=[]
    U = U.T
    for step in range(steps):
#        print((step))
        for i in range(num_pro):
            stock_pi=copy.deepcopy(P[i,:])
            for j in range(num_user):
                #if training_set[i][j] > 0:
                    #learning rule: cost function decreases fastest in the direction of the negative gradient  
                    c=copy.deepcopy(1+coeff*training_set[i][j])
                    eij = copy.deepcopy(c*(C[i][j] - np.dot(stock_pi,U[:,j])))       #Calculate error for gradient
                    temp = copy.deepcopy(stock_pi + alpha * (2*eij * U[:,j] - lambda_val * stock_pi)) 
                    U[:,j] = copy.deepcopy(U[:,j] + alpha * (2*eij * stock_pi- lambda_val * U[:,j]))   #Update latent user feature matrix
                    P[i,:] = copy.deepcopy(temp)         #Update latent pro feature matrix
        rmse=np.sqrt(np.sum(np.square(C - np.dot(P,U)))/num_score)
        rmse_vect.append(rmse)   
        
    if rmse < 0.25:
        print('SGD converged')
        
    eR=np.dot(P,U)    
    eR=np.array(eR) 
    print(eR[np.nonzero(training_set)])
    plt.plot(range(steps), rmse_vect, marker='o', label='Costfunction');
    plt.show()
    return eR     
    
    
def implicit_weighted_ALS(training_set, k_latent, lambda_val = LAMBDA_VAL, coeff = COEFF_CONF_ALS,  seed = SEED, steps = ITER_ALS):
    '''
    Implicit weighted ALS taken from Hu, Koren, and Volinsky 2008. Designed for alternating least squares and implicit
    feedback based collaborative filtering. 
    returns:
    
    The feature vectors for users and items. The dot product of these feature vectors should give you the expected 
    "rating" at each point in your original matrix. 
    
    parameters:
    
    training_set - Our matrix of ratings with shape p x n, where n is the number of users and p is the number of pros.
    
    k_latent     - The number of latent features in the user/item feature vectors. The paper recommends varying this 
                   between 20-200. Increasing the number of features may overfit but could reduce bias. 
    
    lambda_val   - Used for regularization during alternating least squares. Increasing this value may increase bias
                   but decrease variance. Default is 0.2. 
    
    coeff        - The parameter associated with the confidence matrix discussed in the paper, where Cui = 1 + coeff*Rui. 
                   The paper found a default of 40 most effective. Decreasing this will decrease the variability in confidence between
                   various ratings.
    
    seed         - Set the seed for reproducible results
    
    steps        - The number of times to alternate between both user feature vector and item feature vector in
                   alternating least squares. More iterations will allow better convergence at the cost of increased computation. 
    '''
    
    print('Performing Implicit weighted ALS')
    
    # Get the size of our original ratings matrix, p x n  
    num_pro, num_user = np.shape(training_set)  
    num_score=num_user*num_pro  
    
    C=copy.deepcopy(training_set)
    C[C!=0]=1
    
    training_set=training_set.T
    
    # first set up our confidence matrix
    conf = coeff*training_set 
    
    # initialize our U/P feature vectors randomly with a set seed
    rstate = np.random.RandomState(seed)
    U = rstate.uniform(size = (num_user, k_latent)) # Random numbers in a n x k_latent shape
    P = rstate.uniform(size = (num_pro, k_latent))  # Random numbers in a p x k_latent shape 
    U_eye = np.eye(num_user)
    P_eye = np.eye(num_pro)
    lambda_eye = lambda_val * np.eye(k_latent) # Our regularization term lambda*I. 
    
   
    rmse_vect=[]
    # Begin iterations
   
    for iter_step in range(steps): # Iterate back and forth between solving U given fixed P and vice versa
        # Compute pTp and uTu at beginning of each iteration to save computing time
        pTp = P.T.dot(P)
        uTu = U.T.dot(U)
        # Being iteration to solve for U based on fixed P
        for u in range(num_user):
            conf_samp = copy.deepcopy(conf[u,:])   
            pref = conf_samp        
            pref[pref != 0] = 1     # Create binarized preference vector 
            conf_samp = conf_samp + 1 # Add one to each user index so that every user-item is given minimal confidence
            CuI = np.diag(conf_samp, 0) # Get Cu - P term
            pTCuIP = P.T.dot(CuI).dot(P) # This is the pT(Cu-I)P term 
            pTCuqu = P.T.dot(CuI+P_eye).dot(pref.T) # This is the pTCuqu term, where we add the eye back in Cu - I + I = Cu
            U[u,:] = np.linalg.solve(pTp + pTCuIP + lambda_eye, pTCuqu)# Solve for Uu = ((pTp + pT(Cu-I)P + lambda*I)^-1)pTCuqu  
            
        # Begin iteration to solve for P based on fixed U 
        for i in range(num_pro):
            conf_samp = copy.deepcopy(conf[:,i].T)     
            pref = conf_samp
            pref[pref != 0] = 1         # Create binarized preference vector
            conf_samp = conf_samp + 1 # Add one to each item index so that every user-item is given minimal confidence
            CiI = np.diag(conf_samp, 0) # Get Ci - I term
            uTCiIU = U.T.dot(CiI).dot(U) # This is the uT(Cu-I)U term
            uTCiqi = U.T.dot(CiI+ U_eye).dot(pref.T) # This is the uTCiqi term
            P[i,:] = np.linalg.solve(uTu + uTCiIU + lambda_eye, uTCiqi)# Solve for Pi = ((uTu + uT(Cu-I)U) + lambda*I)^-1)uTCiqi
            
        rmse=np.sqrt(np.sum(np.square(C -np.dot(P,U.T)))/num_score)
        rmse_vect.append(rmse)     
    U=np.array(U)
    P=np.array(P)
    eR=np.dot(P,U.T) 
    eR=np.array(eR)
    print(eR[np.nonzero(training_set.T)])
    plt.plot(range(steps), rmse_vect, marker='o', label='Costfunction');
    plt.show()
    # End iterations
    return eR      
    

def matrix_factorization(dict_user, dict_pro, list_user, list_pro, k_latent, lambda_val = LAMBDA_VAL, coeff = COEFF_CONF, seed = SEED):
    """
    Returns a prediction list of P pros for a given active_user
    :param dict_user: dictionnary of users instances
    :param dict_pro: dictionnay of pros instances
    :param list_user: list of ids of users
    :param list_pro: list of ids of pros
    :param active_user: a string representing the id of the active user
    :param K: integer representing the number of the active user's nearest neighbors
    :param P: integer representing the number of pros' id recommanded
    
    """
    
    n = len(dict_user.keys())
#    print('%d users on MJG platform' %n)
    p = len(dict_pro.keys())
#    print('%d Professionnels on MJG platform' %p)
    
    # m_i,j =  visit number by user j to pro i 
    M = np.zeros((p, n))
    for k in range(n):
        idUser = list_user[k]
        visits = dict_user[idUser].hist
        for visit in visits:
            j = list_pro.index(visit.pro_id)
            M[j][k]=+1
            
    M=np.array(M)  
    #eR=sgd(M, k_latent, lambda_val, coeff, seed)
    eR=implicit_weighted_ALS(M, k_latent, lambda_val, coeff, seed)
    return eR,M
     
def recommend_active_user(M, eR, list_user, active_user, P):   
    # i0 is the index of the active_user in the list list_user
    i0 = list_user.index(active_user)
    p,n=np.shape(M)
    prediction=[]
    # List of tuples (r, j) where
    # r is the visit probability of the pro j by the active_user
    # j is the index of the pro in the list list_pro
    counter = 0
    # counter is the number of pro visited by the active_user
    for j in range(p):
        if M[j][i0] !=0:
            # We do not want to recommend a pro already visited by the active_user
            prediction.append((-1, j))
            counter += 1
        else:
            prediction.append((eR[j,i0], j))
    prediction.sort(key=lambda tup: tup[0], reverse=True)
    # Sort the prediction list by decreasing probability
    counter = max(p - counter, 0)
    P = min(P, p - counter)
    # We do not want to recommend more pros than number of pros not visited yet
    prediction = prediction[:P]

    return prediction


def recommend(dict_user, dict_pro, k_latent, P, lambda_val = LAMBDA_VAL, coeff = COEFF_CONF, seed = SEED):
    """
       Returns a dictionnary {user_id : recommend_pro_list, ...}
       where recommend_pro_list is a list of P pros recommended to the user

       :param dict_user: dictionnary of users instances
       :param dict_pro: dictionnary of pros instances
       :param P: integer representing the number of pros'id recommanded
       """
    list_user, list_pro = transform_dict_to_list(dict_user, dict_pro)
    recommend_dict = {}
    blacklist_professional = cleaning.update_blacklist_pro(False)
    eR, M=matrix_factorization(dict_user, dict_pro, list_user, list_pro, k_latent, lambda_val, coeff, seed)
    
    for user in dict_user.keys():
        l = recommend_active_user(M, eR, list_user, dict_user[user].id, P)
        recommend_pro_list = [
            {
                'pro_id': list_pro[x],
                'score': w
            } for (w, x) in l if list_pro[x] not in blacklist_professional
            ]
        recommend_dict[dict_user[user].id] = recommend_pro_list
       
    #checking the results    
    for l in range(200):
         for k in range(200):
             if M[k][l]>1:
                 #if eR[k][l] >0.15:
                     print((k,l, M[k][l], eR[k][l]))
        
    return recommend_dict
    
