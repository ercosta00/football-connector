from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Recupera la chiave API da variabili d'ambiente
API_KEY = os.getenv("API_FOOTBALL_KEY")
if not API_KEY:
    raise ValueError("⚠️ La chiave API_FOOTBALL_KEY non è stata trovata nelle variabili d'ambiente.")

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": API_KEY
}

# Funzione per recuperare le partite da API-Football
def get_matches(date=None, league_id=None, season=None):
    url = f"{BASE_URL}/fixtures"
    params = {}

    if date:
        params["date"] = date
    if league_id:
        params["league"] = league_id
    if season:
        params["season"] = season

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        print("✅ URL:", response.url)
        print("📦 JSON:", data)

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

    except Exception as e:
        print("❌ Errore:", str(e))
        return {"error": "Errore durante la richiesta all’API Football", "details": str(e)}

# Endpoint: partite di oggi
@app.route('/matches/today', methods=['GET'])
def today_matches():
    today = datetime.now().strftime("%Y-%m-%d")
    matches = get_matches(date=today)
    return jsonify(matches), 200

# Endpoint: partite per data (con opzioni query)
@app.route('/matches/date/<date>', methods=['GET'])
def matches_by_date(date):
    league_id = request.args.get("league", default=None, type=int)
    season = request.args.get("season", default=None, type=int)
    matches = get_matches(date=date, league_id=league_id, season=season)
    return jsonify(matches), 200

# Server Flask
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)











