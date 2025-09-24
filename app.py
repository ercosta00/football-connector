from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# ⚠️ Sostituisci con la tua chiave reale
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    raise ValueError("❌ RAPIDAPI_KEY non trovata tra le variabili di ambiente")

BASE_URL = "https://free-api-live-football-data.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

@app.route('/players/search', methods=['GET'])
def search_players():
    search_term = request.args.get('search', default='m', type=str)

    url = f"{BASE_URL}/football-players-search"
    params = { "search": search_term }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Errore durante la richiesta", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)












