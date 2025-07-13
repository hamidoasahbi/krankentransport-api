from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Neue Root-Route für Health-Check oder Doku
@app.route("/")
def index():
    return jsonify({
        "message": "Krankentransport API läuft 🚀",
        "endpoints": {
            "/distance-matrix": "POST - JSON: { 'adressen': ['Adresse1', 'Adresse2', ...] }"
        }
    })

@app.route("/distance-matrix", methods=["POST"])
def distance_matrix():
    data = request.get_json()

    # Safety-Check, falls kein JSON geschickt wird
    if not data:
        return jsonify({"error": "Kein JSON Body empfangen"}), 400

    addresses = data.get("adressen", [])
    if not addresses or len(addresses) < 2:
        return jsonify({"error": "Mindestens 2 Adressen benötigt"}), 400

    origins = "|".join(addresses)
    destinations = "|".join(addresses)

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": GOOGLE_API_KEY,
        "language": "de",
        "region": "de",
        "departure_time": "now"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        matrix = response.json()
    except Exception as e:
        return jsonify({"error": "Fehler beim Abruf der Google API", "details": str(e)}), 500

    if matrix.get("status") != "OK":
        return jsonify({"error": "Fehler bei Google API", "details": matrix}), 500

    result = {
        "matrix": [],
        "addresses": matrix.get("origin_addresses", [])
    }

    for row in matrix.get("rows", []):
        row_result = []
        for element in row.get("elements", []):
            row_result.append({
                "distance_meters": element.get("distance", {}).get("value"),
                "duration_seconds": element.get("duration", {}).get("value"),
                "status": element.get("status")
            })
        result["matrix"].append(row_result)

    return jsonify(result)

if __name__ == "__main__":
    # Lokales Testing
    app.run(debug=True, port=5000)
