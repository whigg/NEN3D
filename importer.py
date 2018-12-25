import json
import os

import requests
import tle2czml
import sats.json
from bs4 import BeautifulSoup
from pymongo import TEXT, MongoClient
from file_read_backwards import FileReadBackwards

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
entries ={}
norad_page_text = requests.get(
    "https://celestrak.com/pub/satcat.txt").text
f = open("files.txt", "r+")
f.write(norad_page_text)
i = 0
#with open("files.txt") as fa:
with FileReadBackwards("files.txt", encoding="utf-8") as fa:
    for line in fa:
        data = line.split()
        key, values = i, data[0:15]
        
        entries[key] = values
        #if entries[i][3] == sats in satellites || sats.cid in satellites:
        tle_file = requests.get("https://celestrak.com/satcat/tle.php?CATNR=" + entries[i][1]).text
        soup = BeautifulSoup(tle_file, features="html.parser")
        tle_txt = soup.select("pre")
        i +=1
        for line in tle_txt:
            filename = soup.pre.text
    #print(filename.startswith( '1'))
    #print(filename)
            parsed = json.loads(tle2czml.tles_to_czml(filename, silent=True))
        for entry in parsed:
            czml_collection.replace_one(
                {'id': entry['id']}, entry, upsert=True)
    

czml_collection.create_index([('id', TEXT)])
f.close()