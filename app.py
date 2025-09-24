
from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("❌ RAPIDAPI_KEY non trovata tra le variabili di ambiente")

BASE_URL = "https://free-api-live-football-data.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
}

def fetch_from_api(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

@app.route("/fixtures/today", methods=["GET"])
def get_today_fixtures():
    today = datetime.now().strftime("%Y-%m-%d")
    data = fetch_from_api("/fixtures", {"date": today})
    return jsonify(data)

@app.route("/fixtures/date/<date>", methods=["GET"])
def get_fixtures_by_date(date):
    data = fetch_from_api("/fixtures", {"date": date})
    return jsonify(data)

@app.route("/fixtures/team/<team_id>", methods=["GET"])
def get_team_fixtures(team_id):
    data = fetch_from_api("/fixtures", {"team": team_id})
    return jsonify(data)

@app.route("/standings/<league_id>", methods=["GET"])
def get_standings(league_id):
    data = fetch_from_api("/standings", {"league": league_id})
    return jsonify(data)

@app.route("/teams/<league_id>", methods=["GET"])
def get_teams_in_league(league_id):
    data = fetch_from_api("/teams", {"league": league_id})
    return jsonify(data)

@app.route("/last-matches/<team_id>", methods=["GET"])
def get_last_matches(team_id):
    data = fetch_from_api("/fixtures", {"team": team_id, "last": 5})
    return jsonify(data)

@app.route("/prediction/<match_id>", methods=["GET"])
def get_match_prediction(match_id):
    # Solo se supportato dalla nuova API, placeholder
    data = fetch_from_api("/predictions", {"fixture": match_id})
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)














