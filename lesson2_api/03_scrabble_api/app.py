"""Activity 3: Scrabble Word Checker API

The database scrabble.db has ONE table:
    words(word TEXT PRIMARY KEY)   - about 172,000 lowercase words

Run with:   python app.py
Test in the browser:   /api/check/quiz   /api/check/qwzx   /api/check/abc123
"""
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = Path(__file__).parent / "scrabble.db"

TILE_POINTS = {
    "a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1,
    "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1,
    "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10,
}


def query_db(sql, params=()):
    """Runs a SELECT and returns a list of rows. Always pass values in params!"""
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(sql, params).fetchall()
    con.close()
    return rows


@app.route("/")
def index():
    return jsonify({"message": "Scrabble API running. Try /api/check/quiz"})


# ---------------------------------------------------------------
# CORE TASK 1: GET /api/check/<word>
#   /api/check/quiz  ->  {"word": "quiz", "valid": true}
#   /api/check/qwzx  ->  {"word": "qwzx", "valid": false}
#   Use query_db() with a ? placeholder. NEVER build SQL with an f-string.
#
# CORE TASK 2: Clean and check the input
#   - make the word lowercase (QUIZ should work)
#   - if it contains anything other than letters, return
#     {"error": "Words can only contain letters"} with status 400
#     Hint: word.isalpha()
#
# CORE TASK 3: Add a "score" to valid words
#   /api/check/quiz  ->  {"word": "quiz", "valid": true, "score": 22}
# ---------------------------------------------------------------




# ---------------------------------------------------------------
# EXTENSION 1: GET /api/starts/<prefix>?limit=10
#   Returns up to `limit` words starting with prefix (default 10).
#   ->  {"prefix": "zy", "words": ["zydeco", "zygoid", ...]}
#   Hints: LIKE ?   with the parameter prefix + "%"
#          request.args.get("limit", 10, type=int)
#
# EXTENSION 2: GET /api/rack/<letters>
#   Returns all valid words that can be made from a rack of up to 7 tiles.
#   /api/rack/tac  ->  {"rack": "tac", "words": ["act", "at", "cat", "ta"]}
#
# EXTENSION 3: POST /api/check
#   Accepts a JSON body: {"words": ["quiz", "qwzx"]}
#   Returns a result for each word.   Hint: request.get_json()
#   Test it from the terminal:
#   curl -X POST localhost:5000/api/check -H "Content-Type: application/json" -d '{"words": ["quiz", "qwzx"]}'
# ---------------------------------------------------------------




if __name__ == "__main__":
    if not DB_PATH.exists():
        raise SystemExit("scrabble.db not found - run: python build_db.py")
    app.run(host="0.0.0.0", port=5000, debug=True)
