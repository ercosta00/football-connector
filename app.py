from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

def get_matches_by_date(date, league_id=None):
    url = f"{BASE_URL}/fixtures"
    params = {
        "season": 2025,
        "date": date
    }

    if league_id is not None:
        params["league"] = league_id

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return {"error": "Errore nella richiesta esterna", "details": str(e)}

    matches = []
    for match in data.get('response', []):
        matches.append({
            "league": match["league"]["name"],
            "country": match["league"]["country"],
            "home_team": match["teams"]["home"]["name"],
            "away_team": match["teams"]["away"]["name"],
            "date": match["fixture"]["date"],
            "venue": match["fixture"]["venue"]["name"],
            "status": match["fixture"]["status"]["long"]
        })

    return matches

@app.route('/matches/today', methods=['GET'])
def today_matches():
    today = datetime.now().strftime("%Y-%m-%d")
    matches = get_matches_by_date(today)
    return jsonify(matches), 200

@app.route('/matches/date/<date>', methods=['GET'])
def matches_by_date(date):
    league_id = request.args.get("league", default=None, type=int)
    matches = get_matches_by_date(date, league_id=league_id)
    return jsonify(matches), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)







