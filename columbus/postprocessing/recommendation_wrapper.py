# -*- coding: utf-8 -*-

import numpy as np
from config import columbus
from cleaning import *
import time

def wrap_with_metadata(recommendation_output):
    """ Wraps recommendation to add metadata
    - Date of recommendation
    - Algorithm version
    - Algorithm type
    - etc.
    """
    wrapped = metadata()
    wrapped.update({
    	'recommendations': recommendation_output
    })
    return wrapped

def metadata():
    return {
    	'recommender_codename': 'Columbus',
    	'execution_date': time.time(),
    	'algorithm_version': columbus.version,
    }


def recommend_active_user(dict_user, dict_pro, list_user,
                          list_pro, active_user, K, P, flag_cross_validation, index_cross_validation = 0):
    """
    Returns a prediction list of P pros for a given active_user
    :param dict_user: dictionnary of users instances
    :param dict_pro: dictionnay of pros instances
    :param list_user: list of ids of users
    :param list_pro: list of ids of pros
    :param active_user: a string representing the id of the active user
    :param K: integer representing the number of the active user's nearest neighbors
    :param P: integer representing the number of pros' id recommanded
    :param flag_cross_validation : True if doing cross_validation : using two sublits of user history instead of one
    :param index_cross_validation : choose the sublist to use
    """
    n = len(dict_user.keys())
    p = len(dict_pro.keys())
    M = np.zeros((p, n))
    # m_i,j = 1 if the user j has visited the pro i and = 0 if not

    for k in range(n):
        idUser = list_user[k]
        if flag_cross_validation:
            visits = (dict_user[idUser].hist_cross_validation)[index_cross_validation]
        else:
            visits = dict_user[idUser].hist
        for visit in visits:
            j = list_pro.index(visit.pro_id)
            M[j][k] = 1

    i0 = list_user.index(active_user)
    # i0 is the index of the active_user in the list list_user

    weight = []
    # weight[i] is tuple (w,i)
    # where w is the weight of similarity between the active_user and the user i
    # and i is the id of the user
    for i in range(n):
        if i != i0:
            w = np.vdot(M[:, i], M[:, i0])
            # w is the number of pro visited in common between the active_user and the user i
            weight.append((w, i))
        else:
            weight.append((-1, i0))
            # we choose to set the similarity w between the active user and himself to w = -1
    weight.sort(key=lambda tup: tup[0], reverse=True)
    # Sort weight by decreasing similarity weights w

    K = min(K, n - 1)
    # In case we choose K >=  n

    weight = weight[:K]
    # Truncate weight list to keep only the K nearest neighbors

    prediction = []
    # List of tuples (r, j) where
    # r is the visit probability of the pro j by the active_user
    # j is the index of the pro in the list list_pro

    counter = 0
    # counter is the number of pro visited by the active_user

    for j in range(p):
        j_vues = [M[j][i] for (w, i) in weight]
        # j_vues[k] = 1 if the user i has visited the pro j

        if M[j][i0] == 1:
            # We do not want to recommend a pro already visited by the active_user
            prediction.append((-1, j))
            counter += 1
        else:
            weight_first_elt = [x for (x, i) in weight]
            s = np.vdot(weight_first_elt, np.ones(len(weight_first_elt)))
            if s == 0:
                # The similarity weight of the active_user compared to any other user
                # is null
                prediction.append((0, j))
            else:
                # Compute the visit probability
                prediction.append((np.vdot(weight_first_elt, j_vues) / s, j))

    prediction.sort(key=lambda tup: tup[0], reverse=True)
    # Sort the prediction list by decreasing probability
    counter = max(p - counter, 0)

    P = min(P, p - counter)
    # We do not want to recommend more pros than number of pros not visited yet
    prediction = prediction[:P]

    return prediction


def recommend(dict_user, dict_pro, K, P):
    """
       Returns a dictionnary {user_id : recommend_pro_list, ...}
       where recommend_pro_list is a list of P pros recommended to the user

       :param dict_user: dictionnary of users instances
       :param dict_pro: dictionnary of pros instances
       :param K: integer representing the number of the active user's nearest neighbors
       :param P: integer representing the number of pros' id recommanded
       """
    list_user, list_pro = transform_dict_to_list(dict_user, dict_pro)
    recommend_dict = {}
    blacklist_professional=cleaning.update_blacklist_pro(True)
    for user in dict_user.keys():
        l = recommend_active_user(dict_user, dict_pro, list_user, list_pro, dict_user[user].id, K, P, False)
        recommend_pro_list = [(list_pro[x], w) for (w, x) in l if list_pro[x] not in blacklist_professional]
        recommend_dict[dict_user[user].id] = recommend_pro_list
    return recommend_dict
