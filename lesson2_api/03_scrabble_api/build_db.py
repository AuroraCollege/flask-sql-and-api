"""Builds scrabble.db from words.txt (the public-domain ENABLE word list).

Already run for you when the Codespace starts. To rebuild:
    python lesson2_api/03_scrabble_api/build_db.py
"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB_PATH = HERE / "scrabble.db"

DB_PATH.unlink(missing_ok=True)
con = sqlite3.connect(DB_PATH)
con.execute("CREATE TABLE words (word TEXT PRIMARY KEY)")
with open(HERE / "words.txt") as f:
    words = [(line.strip().lower(),) for line in f if line.strip()]
con.executemany("INSERT OR IGNORE INTO words VALUES (?)", words)
con.commit()
count = con.execute("SELECT COUNT(*) FROM words").fetchone()[0]
con.close()
print(f"Built {DB_PATH.name}: {count:,} words")
