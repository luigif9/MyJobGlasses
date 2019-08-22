# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:42:41 2016

@author: Saad
"""
#Script for e-mail recommendation analysis
import numpy as np
import os
import json as js
import csv
import numpy as np
import copy
import scipy.stats

keys_list_pro=["photopro","entreprisepro","secteurpro","positionpro","proschool","experiencepro"]
keys_list_mail=["userid","score","datemail","clicked","clickdate","conversation","appointment"]        
keys_list=["proid","score","datemail","clicked","clickdate","conversation","appointment","photopro","entreprisepro","secteurpro","positionpro","proschool","experiencepro"]

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



def read_user_school_database(filename1,filename2):
    user_database={}
    school_database={}
    file1=open(filename1,'r')
    file2=open(filename2,'r')
    for line in file2:
        separed_line0=line.split(',')
        separed_line1=separed_line0[0].split('{')
        school_id=rmSpaces((separed_line1[2].split('"'))[3])
        separed_line2=separed_line0[1].split('"')
        school_name=rmSpaces(separed_line2[2])
        school_database[school_id]=[school_name]        
    for line in file1:
        separed_line0=line.split(',')
        separed_line1=separed_line0[8].split('{')
        current_id=rmSpaces((separed_line1[1].split('"'))[3])
        separed_line2=separed_line0[10].split('{')
        current_school=rmSpaces((separed_line2[1].split('"'))[3])                
        user_database[current_id]=[school_database[current_school]]
    return user_database,school_database

def user_overview(filename):
    mail_database={}
    null_element={"proid":"","score":"","datemail":"","clicked":"","clickdate":"","conversation":"","appointment":"","photopro":"","entreprisepro":"","secteurpro":"","positionpro":"","proschool":"","experiencepro":""}
    file=open(filename,'r')
    for line in file :
        separed_line=line.split(',')
        if rmSpaces(separed_line[0])!='StudentUserID':
            userid=rmSpaces(separed_line[0])
            if userid not in mail_database.keys():
                mail_database[userid]={"qt_mails":float(0)}
    for line in file:
        separed_line=line.split(',')
        if rmSpaces(separed_line[0])!='StudentUserID':
            userid=rmSpaces(separed_line[0]) 
            mail_database[userid]["qt_mails"]+=1
            mail_number='mail'+str(mail_database[userid]["qt_mails"])
            mail_database[userid][mail_number]=copy.deepcopy(null_element)
            for i in range(1,14):
                mail_database[userid][mail_number][keys_list[i]]=separed_line[i]
    return mail_database
def pro_overview(mail_database):
    pro_database={}
    for userid in mail_database.keys():
        for i in range(1,mail_database[userid]["qt_mails"]):
            mail_number='mail'+str(i)
            proid=mail_database[userid][mail_number]["proid"]
            if proid not in pro_database.keys():
                pro_database[proid]={"qt_mails":float(1),"photopro":"","entreprisepro":"","secteurpro":"","positionpro":"","proschool":"","experiencepro":""}
                for j in range(len(keys_list_pro)):
                    pro_database[proid][keys_list_pro[j]]=mail_database[userid][mail_number][keys_list_pro[j]]
                pro_database[proid]["mail1"]={"userid":userid,"score":"","datemail":"","clicked":"","clickdate":"","conversation":"","appointment":""}
                for k in range(len(keys_list_mail)):
                    pro_database[proid]["mail1"][keys_list_mail[k]]=mail_database[userid][mail_number][keys_list_mail[k]]
            else :
                pro_database[proid]["qt_mails"]+=1
                mail_number='mail'+str(pro_database[proid]["qt_mails"])
                for j in range(len(keys_list_pro)):
                    pro_database[proid][keys_list_pro[j]]=mail_database[userid][mail_number][keys_list_pro[j]]
                pro_database[proid]["mail_number"]={"userid":userid,"score":"","datemail":"","clicked":"","clickdate":"","conversation":"","appointment":""}
                for k in range(len(keys_list_mail)):
                    pro_database[proid]["mail_number"][keys_list_mail[k]]=mail_database[userid][mail_number][keys_list_mail[k]]
    return pro_database

def pro_stats(pro_database,mail_database,user_database,school_database):
    L=[]
    reco_list=[proid for proid in pro_database.keys()]
    reco_qt=[pro_database[proid]["qt_mails"] for proid in reco_list]
    different_pros_reco=len(pro_database.keys())
    L.append(["Nombre de professionnels différents recommandés",different_pros_reco])
    total_recos=len(mail_database.keys())
    L.append(["Nombre d'utilisateurs ciblés",total_recos])
    reco_qt=[pro_database[proid]["qt_mails"] for proid in reco_list]
    reco_mean=np.mean(reco_qt)
    L.append(["Nombre moyen de recommandations par professionnel",reco_mean])
    reco_std=np.std(reco_qt)
    L.append(["Ecart type des recommandations par professionnel",reco_std])
    clicked_pros=[]
    not_clicked_pros=[]
    for proid in reco_list:
        click_check=0
        mails_quantity=pro_database[proid]["qt_mails"]
        for j in range(1,mails_quantity+1):
            mail_number='mail'+str(j)
            if pro_database[proid][mail_number]["clicked"]=="true":
                click_check+=1
        if click_check==0:
            not_clicked_pros.append(proid)
        else :
            clicked_pros.append(proid)
    def check_pro_clicked(proid):
        h=0
        if proid in clicked_pros:
            h=1
        return(h)
    click_bool=[check_pro_clicked(proid) for proid in reco_list]
    photo_bool=[float(pro_database[proid]["photopro"]=="true") for proid in reco_list]
    photo_correlation=(scipy.stats.pearsonr(click_bool,photo_bool))[0]
    L.append(["Corrélation entre clique et photo",photo_correlation])
    experience_bool=[float(pro_database[proid]["experiencepro"]>=10) for proid in reco_list]
    experience_correlation=(scipy.stats.pearsonr(click_bool,experience_bool))[0]
    L.append(["Corrélation entre clique et expériece",experience_correlation])
    school_cor_counter=0
    for proid in reco_list:
        mail_quant=pro_database[proid]["qt_mails"]
        for i in range(1,mail_quant):
            mail_number='mail'+str(i)
            userid=pro_database[proid]["mail_number"]["userid"]
            proschoolid=pro_database[proid]["proschool"]
            proschool=school_database[proschoolid]
            userschool=user_database[userid]
            school_cor_counter+=float(proschool==userschool)
    L.append(["cliques sur des professionnels venant de la même école",school_cor_counter])
    return L
def process_render(filename1,filename2):
    user_database=read_user_school_database(filename1,filename2)[0]
    school_database=read_user_school_database(filename1,filename2)[1]
    mail_database=user_overview(filename1)
    pro_database=pro_overview(mail_database)
    L=pro_stats(pro_database,mail_database,user_database,school_database)
    return L
def render(filename1,filename2):
    A=process_render(filename1,filename2)
    with open('temp/result_analysis.csv','w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(A)

render("columbus_clicks.csv","seekers.json")