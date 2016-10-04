import classes.py
import cleaning.py
import numpy as np

DictUser,DictPro = cleaning.clean()

def RecommandActiveUser(ActiveUser,K,P):
    ListUser = []
    ListPro = []
    for user in DictUser.keys():
        ListUser.append(DictUser[user].id)
    for pro in ListPro.keys():
        ListPro.append(DictPro[pro].id)
    n = len(DictUser.keys())
    p = len(DictPro.keys())
    M = np.zeros((p, n))
    for k in range(n):
        idUser = ListUser[k]
        visits = DictUser[idUser].hist
        for visit in visits:
            j = ListPro.index(visit.pro_id)
            M[j][k] = 1

    i0 = ListUser.index(ActiveUser)
    weight = []
    for i in range(n):
        if i != i0:
            w = np.vdot(M[:,i],M[:,i0])
            weight.append((w,i))
        else :
            weight.append((-1,i0))
    weight.sort(key = lambda tup : tup[0])
    K = min(K,n-1)
    weight = weight[:K]

    pred = [0]*p
    compteur = 0
    for j in range(p):
        j_vues = [M[j][i] for (w,i) in weight]
        if M[j][i0] == 1:
            pred[j] = (-1,j)
            compteur += 1
        else:
            s = np.vdot(weight,np.ones(len(weight)))
            if s == 0:
                pred[j] = (0,j)
            elif s > 0:
                pred[j] = (np.vdot(weight,j_vues)/s,j)
    pred.sort(key = lambda tup : tup[0])
    compteur = max(p-compteur,0)
    P = min(P,p-compteur)
    pred = pred[:P]

    predF = [j for (w,j) in pred]
    return predF

def Recommand(K,P):
    RecommandDict = {}
    for user in DictUser.keys():
        l = RecommandActiveUser(DictUser[user].id,K,P)
        RecommandDict[DictUser[user].id] = l
    return RecommandDict