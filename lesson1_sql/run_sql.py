"""Runs the SQL in a file (or a single query) against scrabble_club.db.

Usage:
    python run_sql.py part_a.sql
    python run_sql.py "SELECT * FROM players;"
"""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "scrabble_club.db"


def print_table(cursor):
    headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    widths = [len(h) for h in headers]
    for row in rows:
        widths = [max(w, len(str(v))) for w, v in zip(widths, row)]
    line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-" * len(line))
    for row in rows:
        print("  ".join(str(v).ljust(w) for v, w in zip(row, widths)))
    print(f"({len(rows)} rows)")


def run(sql_text):
    con = sqlite3.connect(DB_PATH)
    label, buffer, ran = "", "", 0
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("-- Q"):
            label = stripped[3:]
        if stripped.startswith("--") or not stripped:
            continue
        buffer += line + "\n"
        if sqlite3.complete_statement(buffer):
            print(f"\n=== {label or 'Query'} ===")
            print(buffer.strip())
            print()
            try:
                cur = con.execute(buffer)
                if cur.description:
                    print_table(cur)
                else:
                    con.commit()
                    print(f"OK - {cur.rowcount} row(s) changed")
            except sqlite3.Error as err:
                print(f"SQL ERROR: {err}")
            buffer, label = "", ""
            ran += 1
    if buffer.strip():
        print(f"\nWARNING: unfinished statement (missing ;?)\n{buffer}")
    if ran == 0:
        print("No queries found yet - write one under a -- Q comment, ending with ;")
    con.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    arg = sys.argv[1]
    path = Path(arg)
    if not path.exists():
        path = Path(__file__).parent / arg
    run(path.read_text() if path.suffix == ".sql" and path.exists() else arg)
