"""Teacher live demo: why we never build SQL with f-strings.

Run from the 03_scrabble_api folder (needs scrabble.db):
    python ../../teacher_demos/injection_demo.py
"""
import sqlite3

con = sqlite3.connect("scrabble.db")

attack = "zzzz' OR '1'='1"

# UNSAFE: the input becomes part of the SQL code
unsafe_sql = f"SELECT word FROM words WHERE word = '{attack}'"
print("UNSAFE SQL :", unsafe_sql)
print("Rows found :", len(con.execute(unsafe_sql).fetchall()))  # every word -> "valid"!

# SAFE: the input is sent separately as data
safe_sql = "SELECT word FROM words WHERE word = ?"
print("\nSAFE SQL   :", safe_sql, " params:", (attack,))
print("Rows found :", len(con.execute(safe_sql, (attack,)).fetchall()))  # 0
