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

# Scrape CelesTrak for NORAD TLEs
norad_page_text = requests.get(
    "https://celestrak.com/pub/satcat.txt").text
with open(norad_page_text) as fp:  
   line = fp.readline()
   print(line)
   #while line:
    #   cnt = 1
     #  print("Line {}: {}".format(cnt, line.strip()))
      # line = fp.readline()
       #cnt += 1
       #print(cnt)

#dataDict = dict.fromkeys(['intDes','norad','D','name','source','launchDate','launchSite','decayDate','status','TLE1','TLE2','TLE3','TLE4','TLE5','TLE'])

#data = norad_page_text.split()
#for key in dataDict:
 #   while i<10:
  #      dataDict['key']=data[i]
   #     i+=1
#print(dataDict)
#print(dataDict['name'])
#for text in data:
    
 #      if text.isnumeric():
  #         if len(text) == 6:
           
   #         filename= text

            #print(filename)
    #        tle_file = requests.get(
     #   "https://celestrak.com/satcat/tle.php?CATNR=" + filename).text
      #      print(tle_file)
       #     parsed = json.loads(tle2czml.tles_to_czml(tle_file, silent=True))
            
#for entry in parsed:#
 #   czml_collection.replace_one(
  #  {'id': entry['id']}, entry, upsert=True)

#czml_collection.create_index([('id', TEXT)])