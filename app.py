from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

# Prende la chiave RapidAPI dalle variabili di ambiente
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("❌ RAPIDAPI_KEY non trovata tra le variabili di ambiente")

# Host richiesto da RapidAPI
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
}

BASE_URL = "https://free-api-live-football-data.p.rapidapi.com"

@app.route('/players/search', methods=['GET'])
def search_players():
    query = request.args.get("q", default="", type=str)
    url = f"{BASE_URL}/football-players-search"
    params = {"search": query}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)













