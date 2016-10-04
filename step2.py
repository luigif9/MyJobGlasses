# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
class User:
        def __init__(self, user_id):
            self.id=user_id
            self.hist=[]
        
        def appendU(self, pro_id, time):
           if visit not in self.hist:
                self.hist.append(pro_id)
                self.hist.append(time)
        
        def showhist(self):
            for i in range(self.hist):
                print(self.hist(i))
            
            
class Pro:
        def __init__(self, pro_id):    
            self.id=pro_id       
'''
class Relation:
        def __init__(self,user_id, pro_id, time):
            self.user_id=user_id
            self.pro_id=pro_id
            self.time=[time]
            self.number=1
'''

listuser={}

import json as js 
import os 
 
#cwd = os.path.dirname(__file__)
cwd = os.path.dirname("/Users/adrien/PycharmProjects/MyJobGlasses/")
path = os.path.join(cwd,"Data/events.json") 
file = open(path) 

 
data = [] #Read the JSON file 
dataF = [] #Output 
dataH =[]
 
user_admin = ['575722626ba9ba0b9d4e98db','575722626ba9ba0b9d4e98d8','575d93286ba9ba634b63c0f6','575d8d8b6ba9ba5ea08968b5','577e245066703f78c1487259'] 

 
for line in file: 
    data.append(js.loads(line)) 
#data is a list of dictionnaries 

 
for line in data: 
    if line.get("name") == "Viewed professional" and line.get("user_id") != None and (line.get("user_id").get('$oid') not in user_admin): 
        del line['_id'] 
        del line['visit_id']['$type'] 
        line["professional"] = line["properties"]["id"] 
        del line["properties"]["id"] 
        temps = line["time"]["$date"] 
        del line["time"]["$date"] 
        line["time"] = temps 
        del line["properties"] 
        user = line["user_id"]["$oid"]
        if user not in listuser:  
            Us=User(user)
            listuser[user]=Us
        del line["user_id"]["$oid"] 
        line["user_id"] = user 
        visit = line['visit_id']['$binary'] 
        del line['visit_id']['$binary'] 
        line['visit_id'] = visit 
        dataF.append(line) 
        listuser[user].appendU(line["professional"],temps)

for user in listuser.keys():
    dataH.append({"user_id":listuser[user].id, "navigation history":listuser[user].hist})

path = os.path.join(cwd,'Data/output.json') 
with open(path,'w') as f: 
    js.dump(dataF,f, indent = 4,sort_keys=True, separators=(',', ':'),ensure_ascii=False) 
    

pathH = os.path.join(cwd,'Data/outputH.json') 
with open(pathH,'w') as f: 
    js.dump(dataH,f, indent = 4,sort_keys=True, separators=(',', ':'),ensure_ascii=False) 
    

