from flask import Flask, request, jsonify
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    # Entfernung in Kilometern berechnen
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    return R * 2 * asin(sqrt(a))

@app.route('/fahrten', methods=['POST'])
def fahrten():
    data = request.get_json()
    fahrten = data.get("fahrten", [])

    # Dummy-Logik: Erste Fahrt = Fahrer A, zweite = Fahrer B (kannst du ausbauen)
    cluster = {
        "fahrer_1": [fahrten[0]] if len(fahrten) > 0 else [],
        "fahrer_2": [fahrten[1]] if len(fahrten) > 1 else []
    }

    return jsonify({
        "status": "ok",
        "anzahl_fahrten": len(fahrten),
        "cluster": cluster
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
