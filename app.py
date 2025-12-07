from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

api_key = os.getenv("SERPAPI_KEY")

app = Flask(__name__)
CORS(app) # povoli vsechny cross-origin requesty

def search_google_with_serpapi (query):
    api_key = os.getenv("SERPAPI_KEY")
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "engine": "google",
        "num": 10,  # 1. strana google vyhledávání prý zobrazí cca 10 výsledků +/-, omezuji tedy na 10
        "api_key": api_key } # my personal api key

    r = requests.get(url, params=params)
    r.raise_for_status()   # vyhodí výjimku pokud status != 200 (= kod, ktery nam rekne, ze request dostal opravdu nejaka data)
    return r.json() # nevraci JSON string ale python dictionary
    
def clean_serpapi_results(raw_json):
    organic = raw_json.get("organic_results", [])

    cleaned = []
    for item in organic:
        cleaned.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })
    return cleaned

@app.route("/api/search", methods=["POST"])
def api_search():
    # 1) přečtení JSON vstupu
    data = request.get_json()

    # 2) získání query ze vstupu
    query = data.get("query", "") if data else ""

    # 3) jednoduchá kontrola inputu
    if not query:
        return jsonify({"error": "Missing 'query' field"}), 400
    
    try:
        raw = search_google_with_serpapi(query)
        cleaned = clean_serpapi_results(raw)
        return jsonify(cleaned)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# return jsonify(results) # Flask musí převést Python objekt na:✔️ JSON string, ✔️ nastavit HTTP hlavičky (Content-Type: application/json), ✔️ serializovat vše, co jde do HTTP odpovědi

if __name__ == "__main__":
    app.run(debug=True)
