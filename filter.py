import json
import os

import requests
import tle2czml
from bs4 import BeautifulSoup
from pymongo import TEXT, MongoClient

mongo_uri = "mongodb://localhost:27017/orbits"
try:
    # This is what it's called by default on Heroku
    mongo_uri = os.environ["MONGODB_URI"]
except KeyError as e:
    pass
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()
czml_collection = db['czml']

found = 0
notFound = 0
with open('sats.json', encoding="utf8") as sats:    
    satellites = json.load(sats)
    lst = []
    for sat in satellites:
        
        id = "Satellite/" + sat
        if czml_collection.find_one({'id': id}):
            #the id of the spacecraft straight from the json key
            found += 1
            lst.append(id)
        elif czml_collection.find_one({'id': id.replace('-', ' ')}):
            #the id but with the dash replaced by a space (TDRS 11, not TDRS-11)
            found += 1
            lst.append(id.replace('-', ' '))
        elif czml_collection.find_one({'id': "Satellite/" + satellites[sat]['name'].upper()}):
            #The name of the spacecraft is different than the ID 
            #For some, the name is more desciptive and is used for the TLE data (THEMIS-A isntead of THA)
            found += 1
            lst.append("Satellite/" + satellites[sat]['name'].upper())
        elif czml_collection.find_one({'id': "Satellite/" + satellites[sat]['cid'].upper()}):
            found += 1
            lst.append("Satellite/" + satellites[sat]['cid'].upper())
        elif czml_collection.find_one({'id': "Satellite/" + satellites[sat]['name'].replace('-', ' ').upper()}):
            #Same as above but with spaces instead of dashes
            found += 1
            lst.append("Satellite/" + satellites[sat]['name'].replace('-', ' ').upper())
        else:
            print("*Not found: " + id)
            notFound += 1   

print("found: " + str(found))
print("not found: " + str(notFound))

print(lst)
