from flask import Flask, request, jsonify, send_from_directory
from summarizer import summarize
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
 
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")



@app.route('/api/summarize', methods=["POST"])
def api_summarize():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    n = int(data.get("n_senteces",3))

    try:
        result = summarize(text, n=n)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify(result)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)