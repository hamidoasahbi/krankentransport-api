from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/fahrten', methods=['POST'])
def fahrten():
    data = request.get_json()
    # Hier kannst du deine Logik reinpacken, z.B. Clustering etc.
    print("Empfangene Fahrten:", data)

    return jsonify({
        "status": "ok",
        "anzahl_fahrten": len(data.get("fahrten", [])),
        "cluster": [data.get("fahrten", [])]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
