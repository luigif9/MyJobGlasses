""" First step
Goal : clean the data file events.json to remove useless information
Intput : Data/events.json
Output : JSON file named output.json
"""

import json as js
import os

cwd = os.path.dirname(__file__)
path = os.path.join(cwd,"Data/events.json")
file = open(path)

data = [] #Read the JSON file
dataF = [] #Output

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
        del line["user_id"]["$oid"]
        line["user_id"] = user
        visit = line['visit_id']['$binary']
        del line['visit_id']['$binary']
        line['visit_id'] = visit
        dataF.append(line)

path = os.path.join(cwd,'Data/output.json')
with open(path,'w') as f:
    js.dump(dataF,f, indent = 4,sort_keys=True, separators=(',', ':'),ensure_ascii=False)

#----! Test !-----

# for line in data:
#     if line.get("name") == "Viewed professional" and line.get("user_id") != None and (line.get("user_id").get('$oid') not in user_admin):
#         dataF.append(line)
#
# for line in data:
#     if line.get("name") == 'Viewed professional':
#         dataF2.append(line)

# for line in file:
#     line = js.loads(line)
#     if line.get("name") == "Viewed professional":
#         dataF2.append(js.loads(line))
