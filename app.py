from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = "123"  # chiave pubblica
BASE_URL = "https://www.thesportsdb.com/api/v1/json"

def get_matches_by_date(date):
    # TheSportsDB non supporta direttamente "per data", quindi si simula via eventi prossimi
    url = f"{BASE_URL}/{API_KEY}/eventsday.php"
    params = {
        "d": date,
        "s": "Soccer"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"error": "Errore durante la richiesta", "details": str(e)}

    matches = []
    for match in data.get('events', []):
        matches.append({
            "league": match.get("strLeague"),
            "home_team": match.get("strHomeTeam"),
            "away_team": match.get("strAwayTeam"),
            "date": match.get("dateEvent"),
            "time": match.get("strTime"),
            "venue": match.get("strVenue")
        })

    return matches

@app.route('/matches/date/<date>', methods=['GET'])
def matches_by_date(date):
    matches = get_matches_by_date(date)
    return jsonify(matches), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)













