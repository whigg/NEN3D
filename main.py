import os

import requests
import tle2czml
from bson import json_util
from flask import (Flask, Response, json, jsonify, render_template,
                   send_from_directory)
from pymongo import MongoClient

mongo_uri = "mongodb://localhost:27017/orbits"
try:
    # This is what it's called by default on Heroku
    mongo_uri = os.environ["MONGODB_URI"]
except KeyError as e:
    pass
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()
czml_collection = db['czml']

app = Flask("tleapp")

sats = ['document' ,'Satellite/AIM', 'Satellite/TERRA', 'Satellite/AQUA', 'Satellite/AURA', 'Satellite/GOES 14', 'Satellite/GOES 15', 'Satellite/GOES 16', 'Satellite/GOES 17', 'Satellite/HST', 'Satellite/ICESAT-2', 'Satellite/IMAGE', 'Satellite/IRIS', 'Satellite/LANDSAT 7', 'Satellite/LANDSAT 8', 'Satellite/METOP-A', 'Satellite/METOP-B', 'Satellite/METOP-C', 'Satellite/NUSTAR', 'Satellite/OCO 2', 'Satellite/SMAP', 'Satellite/SORCE', 'Satellite/SWAS', 'Satellite/SWIFT', 'Satellite/TDRS 10', 'Satellite/TDRS 11', 'Satellite/TDRS 12', 'Satellite/TDRS 13', 'Satellite/TDRS 3', 'Satellite/TDRS 5', 'Satellite/TDRS 6', 'Satellite/TDRS 7', 'Satellite/TDRS 8', 'Satellite/TDRS 9', 'Satellite/THEMIS A', 'Satellite/THEMIS D', 'Satellite/THEMIS E', 'Satellite/HINODE (SOLAR-B)', 'Satellite/ISS (ZARYA)']

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cesium/<path:path>")
def send_cesium_files(path):
    return send_from_directory("node_modules/cesium/Build/Cesium", path)


@app.route("/orbit/<id>")
def get_orbit(id):
    return Response(json_util.dumps([
        czml_collection.find_one({'id': 'document'}),
        czml_collection.find_one({'$text': {'$search': id}})
    ]), status=200, content_type="application/json")


@app.route("/orbits")
def get_orbits():
    return Response(json_util.dumps(czml_collection.aggregate([
        {'$match': {
            'id': {'$in': sats}}},
        {'$limit': 100}
    ])), status=200, content_type="application/json")

if __name__ == "__main__":
    app.run()
