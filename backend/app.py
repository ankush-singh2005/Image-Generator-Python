from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

@app.route('/api/search')
def search_images():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query'}), 400

    url = "https://api.unsplash.com/search/photos"
    params = {
        "client_id": UNSPLASH_ACCESS_KEY,
        "query": query,
        "per_page": 10
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    images = [item["urls"]["regular"] for item in data.get("results", [])]
    return jsonify(images)

if __name__ == "__main__":
    app.run(debug=True)
