# distance_matrix.py

import requests

# Dein Google Maps API-Key (für Testzwecke direkt hier)
GOOGLE_API_KEY = "AIzaSyANtlq-97oTsQsgFk9lO1i8yV8T5q5pR2I"

def get_distance_matrix(fahrten):
    addresses = [f["adresse"] for f in fahrten]
    ids = [f["id"] for f in fahrten]

    origins = "|".join(addresses)
    destinations = "|".join(addresses)

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": GOOGLE_API_KEY,
        "language": "de",
        "region": "de",
        "mode": "driving"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "OK":
        return {"status": "error", "details": data}

    result = []
    for i, row in enumerate(data["rows"]):
        for j, element in enumerate(row["elements"]):
            if element["status"] != "OK":
                continue
            distance_km = round(element["distance"]["value"] / 1000, 2)
            duration_min = round(element["duration"]["value"] / 60)
            result.append({
                "from": ids[i],
                "to": ids[j],
                "distance_km": distance_km,
                "duration_min": duration_min
            })

    return {
        "distances": result,
        "status": "ok"
    }
