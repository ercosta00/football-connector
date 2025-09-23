from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime


API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

app = Flask(__name__)

def get_matches_by_date(date, league_id=None):
    url = f"{BASE_URL}/fixtures"
    params = {
        "season": 2025,
        "date": date
    }

    if league_id is not None:
        params["league"] = league_id

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

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
    return jsonify(matches)

@app.route('/matches/date/<date>', methods=['GET'])
def matches_by_date(date):
    league_id = request.args.get("league", default=None, type=int)
    matches = get_matches_by_date(date, league_id=league_id)
    return jsonify(matches)

if __name__ == '__main__':
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)



