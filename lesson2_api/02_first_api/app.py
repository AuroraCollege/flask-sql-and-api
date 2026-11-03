"""Activity 2: Your first API endpoints

Run with:   python app.py
Then open the forwarded port 5000 (PORTS tab) and add a path, e.g. /api/hello
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

TILE_POINTS = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10,
}


# WORKED EXAMPLE - already done for you
# GET /api/hello  ->  {"message": "Hello, API!"}
@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello, API!"})


# TODO 1: GET /api/greet/<name>
# /api/greet/Ava  ->  {"greeting": "G'day, Ava!"}



# TODO 2: GET /api/tile/<letter>
# /api/tile/q  ->  {"letter": "Q", "points": 10}
# /api/tile/7  ->  {"error": "7 is not a letter"}  with status code 404
# Hints: letter.upper()   and   return jsonify({...}), 404



# STRETCH TODO 3: GET /api/score?word=quiz
# Read the word from the query string with request.args.get("word")
# /api/score?word=quiz  ->  {"word": "quiz", "score": 22}
# No word given?        ->  {"error": "Add ?word=... to the URL"}  with status 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
