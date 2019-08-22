# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from config import columbus
from models.professional import *
from models.user import *
from models.visit import *
from aws.aws import *

import json as js
import os

def read_or_pull_file(file_type, file_name, reimport_file, environment='development'):
    """TODO : should not be here ! refactor inside aws.py
    Loading a file
    If import event_file = True, then downloading a new version from AWS
    Else, trying to import events file
        If, events file not found, downloading the file nonetheless"""
    if reimport_file:
        path = pull_file(file_name)
        file = open(path)
        return file
    else:
        try:
            file = open(os.path.join(columbus.data, file_name))
            print(file_type + ' file already downloaded')
            return file
        except:
            path = pull_file(file_name)
            file = open(path)
            return file

def events_file(reimport_file):
    return read_or_pull_file('Events', 'events.json', reimport_file)

def blacklist_user_file(reimport_file):
    return read_or_pull_file('User Blacklist', 'blacklist_user.json', reimport_file)

# Expects a dict pro_id: user_id
# TODO get rid of this, we have pro <-> user ID with the professionals.json file
def blacklist_pro_user_file(reimport_file):
    return read_or_pull_file('Pro -> User blacklist', 'blacklist_pro_user.json', reimport_file)

def blacklist_pro_file(reimport_file):
    return read_or_pull_file('Pro Blacklist', 'blacklist_professional.json', reimport_file)

def update_blacklist(reimport_file):
    file_black_user=blacklist_user_file(reimport_file)
    file_black_pro_user=blacklist_pro_user_file(reimport_file)
    # list containing id to not take into account
    blacklist = []

    data_black_user = js.load(file_black_user)
    for k in data_black_user:
        blacklist.append(k["id"])

    data_black_pro_user = js.load(file_black_pro_user)
    for key in data_black_pro_user:
        blacklist.append(data_black_pro_user[key])

    return blacklist

def update_blacklist_pro(reimport_file):
    file_blacklist_professional=blacklist_pro_file(reimport_file)
    n=3
    blacklist_professional=[]
    for line in file_blacklist_professional:
        if n%2==1:
            s01=line.find('"')
            s02=line.find('"', s01+1)
            s11=line.find('"', s02+1)
            s12=line.find('"', s11+1)
            id=line[s11+1:s12]
            blacklist_professional.append(id)
        n=n+1
    blacklist_professional=blacklist_professional[2:len(blacklist_professional)-1]
    return blacklist_professional

def clean(reimport_file):
    """Selecting relevant data in events.json.
       defining and keeping up-to-date appropriate dictionaries to implement recommendation algorithm"""
    file = events_file(reimport_file)

    # defining user dictionary
    listuser = {}

    # defining professional dictionary
    listpros = {}
    cwd = os.path.dirname(__file__)

    # auxiliary list of dictionaries to read the JSON file
    data = []
    # auxiliary list of dictionaries to export cleaned data
    data_f = []

    # Defining the user blacklist to not take into account in computing prediction
    blacklist = update_blacklist(reimport_file)

    for line in file:
        data.append(js.loads(line))

    for line in data:
        if line.get("name") == "Viewed professional" and line.get("user_id") != None and (line.get("user_id").get('$oid') not in blacklist):
            # Selecting relevant data
            del line['_id']

            line["professional"] = line["properties"]["id"]
            pro=line["professional"]
            if pro not in listpros:
                # keeping up-to-date professional dictionary
                pro_add=Professional(pro)
                listpros[pro]=pro_add
            del line["properties"]["id"]
            del line["properties"]

            temps = line["time"]["$date"]
            del line["time"]["$date"]
            line["time"] = temps

            visit = line['visit_id']['$binary']
            del line['visit_id']['$binary']
            line['visit_id'] = visit

            user = line["user_id"]["$oid"]
            del line["user_id"]["$oid"]
            line["user_id"] = user
            if user not in listuser:
                # keeping up-to-date user dictionary
                us_add=User(user)
                listuser[user]=us_add

            data_f.append(line)
            newvisit = Visit(pro,temps)
            # keeping up-to-date navigation history of the current user
            listuser[user].hist.append(newvisit)

    return listuser, listpros, data_f

def export_history_file(listuser):
    """ Export of cleaned data in data/output_history.json"""

    data_h = []

    for user in listuser.keys():
        listvisit = []
        for i in range(len(listuser[user].hist)):  # re-creating navigation history of the current user in an easier to handle format! the better solution i found to print a list of instances of Visit class.
            visit = (listuser[user].hist[i].pro_id, listuser[user].hist[i].time)
            listvisit.append(visit)
        data_h.append({"user_id": listuser[user].id, "navigation history": listvisit})

    """ Export of navigation history in data/output_history.json"""
    patht = os.path.join(columbus.data, 'output_history.json')
    with open(patht, 'w') as f:
        js.dump(data_h, f, indent=4, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
