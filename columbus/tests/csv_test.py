# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:42:41 2016

@author: Saad
"""

from models.user import *
from models.visit import *
from models.professional import *
from cleaning.cleaning import *
from recommendationv1.recommendationv1 import *
import numpy as np
import os
import json as js
import csv
import numpy as np

K = 2
P = 2


def str2array(s):
    res = np.array([])
    if len(s) >= 2:
        s = s[s.find('[')+1:s.find(']')]
        s = s.split(',')
        for e in s:
            res = np.append(res, float(e))
    return res


def rmSpaces(src):
    src = src.lstrip()
    return src.rstrip()


def read_pro_databse(filename):
    pro_database={}
    file=open(filename,'r')
    for line in file:
        separed_line=line.split('|')
        pro_database[rmSpaces((separed_line[0]))]=[separed_line[4]+' '+'chez'+' '+separed_line[2],separed_line[1],separed_line[5]]
    return pro_database


def process_overview(filename, rec_dict, dict_user):
    pro_database=read_pro_databse(filename)
    col1=['Utilisateur','id']
    col2=['Profils visités','id']
    col3=['','poste']
    col4=['','secteur']
    col5=['','vues']
    col6=['Profils recommandés','id']
    col7=['','poste']
    col8=['','secteur']
    col9=['','vues']
    for user in dict_user.keys():
        visits = dict_user[user].hist
        unique_visits=[]
        for visit in visits:
            pro=visit.pro_id
            if pro not in unique_visits:
                unique_visits.append(pro)
        n=len((unique_visits))
        col1.append(user)
        if n>1:
            for i in range(n-1):
                col1.append('-')
        for pro in unique_visits:
            col2.append(pro)
            if pro in pro_database :
                col3.append((pro_database[pro])[0])
                col4.append((pro_database[pro])[1])
                col5.append((pro_database[pro])[2])
            else:
                col3.append('deleted profile')
                col4.append('deleted profile')
                col5.append('deleted profile')
        recommendations=rec_dict[user]
        m=len(recommendations)
        if m>n:
            for i in range(m-n):
                col1.append('-')
                col2.append('')
                col3.append('')
                col4.append('')
                col5.append('')
        for pro_rec in recommendations:
            col6.append(pro_rec)
            if pro_rec in pro_database :
                col7.append((pro_database[pro_rec])[0])
                col8.append((pro_database[pro_rec])[1])
                col9.append((pro_database[pro_rec])[2])
            else:
                col7.append('deleted profile')
                col8.append('deleted profile')
                col9.append('deleted profile')
        if m<n:
            for i in range(n-m):
                col6.append('')
                col7.append('')
                col8.append('')
                col9.append('')
    return [col1, col2, col3, col4, col5, col6, col7, col8, col9]


def render(filename, rec_dict, dict_user):
    A = [process_overview(filename, rec_dict, dict_user)[i] for i in range(8)]
#    out = open('out.csv', 'w')
#    for row in A:
#        for column in row:
#            out.write('%d;' % column)
#            out.write('\n')
#    out.close()
    with open('temp/out.csv','w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(zip(*A))