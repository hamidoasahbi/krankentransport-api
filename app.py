from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("AIzaSyANtlq-97oTsQsgFk9lO1i8yV8T5q5pR2I")

@app.route("/distance-matrix", methods=["POST"])
def distance_matrix():
    data = request.get_json()

    addresses = data.get("adressen", [])
    if not addresses or len(addresses) < 2:
        return jsonify({"error": "Mindestens 2 Adressen benötigt"}), 400

    origins = "|".join(addresses)
    destinations = "|".join(addresses)

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": AIzaSyANtlq-97oTsQsgFk9lO1i8yV8T5q5pR2I,
        "language": "de",
        "region": "de",
        "departure_time": "now"
    }

    response = requests.get(url, params=params)
    matrix = response.json()

    if matrix.get("status") != "OK":
        return jsonify({"error": "Fehler bei Google API", "details": matrix}), 500

    result = {
        "matrix": [],
        "addresses": matrix.get("origin_addresses", [])
    }

    for i, row in enumerate(matrix["rows"]):
        result["matrix"].append([])
        for j, element in enumerate(row["elements"]):
            result["matrix"][i].append({
                "distance_meters": element.get("distance", {}).get("value"),
                "duration_seconds": element.get("duration", {}).get("value"),
                "status": element.get("status")
            })

    return jsonify(result)
