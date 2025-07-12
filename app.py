from flask import Flask, request, jsonify
from math import radians, cos, sin, asin, sqrt
import os

from distance_matrix import get_distance_matrix

app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    return R * 2 * asin(sqrt(a))

@app.route('/', methods=['GET'])
def home():
    return "API läuft!"

@app.route('/fahrten', methods=['POST'])
def fahrten():
    data = request.get_json()
    fahrten = data.get("fahrten", [])

    cluster = {
        "fahrer_1": [fahrten[0]] if len(fahrten) > 0 else [],
        "fahrer_2": [fahrten[1]] if len(fahrten) > 1 else []
    }

    return jsonify({
        "status": "ok",
        "anzahl_fahrten": len(fahrten),
        "cluster": cluster
    })

@app.route("/distance-matrix", methods=["POST"])
def distance_matrix():
    data = request.get_json()
    fahrten = data.get("fahrten", [])
    result = get_distance_matrix(fahrten)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
