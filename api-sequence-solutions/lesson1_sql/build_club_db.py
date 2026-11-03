"""Builds scrabble_club.db for the SQL refresher lesson.

Run this any time to reset the database to its original state:
    python lesson1_sql/build_club_db.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "scrabble_club.db"

PLAYERS = [
    # (id, first_name, last_name, school, rating)
    (1, "Ava", "Thompson", "Dubbo", 1420),
    (2, "Sam", "Nguyen", "Broken Hill", 1385),
    (3, "Jack", "Wilson", "Moree", 1510),
    (4, "Mia", "Roberts", "Bourke", 1290),
    (5, "Liam", "Clarke", "Dubbo", 1605),
    (6, "Zoe", "Martin", "Cobar", 1350),
    (7, "Sam", "Nguyen", "Tamworth", 1475),
    (8, "Ella", "Walker", "Moree", 1550),
    (9, "Noah", "Kelly", "Bourke", 1220),
    (10, "Ruby", "Hughes", "Cobar", 1440),
]

GAMES = [
    # (player_id, score, best_word, played_on)
    (1, 342, "quixotic", "2026-07-21"), (1, 298, "zephyr", "2026-08-04"),
    (1, 365, "jukebox", "2026-08-18"), (2, 276, "fjord", "2026-07-21"),
    (2, 311, "oxygen", "2026-08-04"), (3, 402, "syzygy", "2026-07-21"),
    (3, 377, "quartz", "2026-08-04"), (3, 389, "waltz", "2026-08-18"),
    (4, 240, "zebra", "2026-07-21"), (4, 265, "quiz", "2026-08-18"),
    (5, 421, "buzzword", "2026-07-21"), (5, 398, "jazz", "2026-08-04"),
    (5, 433, "maximize", "2026-08-18"), (6, 288, "vex", "2026-08-04"),
    (6, 301, "glyph", "2026-08-18"), (7, 334, "quokka", "2026-07-21"),
    (7, 352, "jinx", "2026-08-04"), (8, 371, "zigzag", "2026-07-21"),
    (8, 385, "wombat", "2026-08-04"), (8, 360, "kayak", "2026-08-18"),
    (9, 231, "cat", "2026-07-21"), (9, 254, "fox", "2026-08-04"),
    (10, 329, "pizzazz", "2026-08-04"), (10, 318, "rhythm", "2026-08-18"),
]


def build():
    DB_PATH.unlink(missing_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript(
        """
        CREATE TABLE players (
            id          INTEGER PRIMARY KEY,
            first_name  TEXT NOT NULL,
            last_name   TEXT NOT NULL,
            school      TEXT NOT NULL,
            rating      INTEGER NOT NULL
        );
        CREATE TABLE games (
            id          INTEGER PRIMARY KEY,
            player_id   INTEGER NOT NULL REFERENCES players(id),
            score       INTEGER NOT NULL,
            best_word   TEXT NOT NULL,
            played_on   TEXT NOT NULL
        );
        """
    )
    con.executemany("INSERT INTO players VALUES (?, ?, ?, ?, ?)", PLAYERS)
    con.executemany(
        "INSERT INTO games (player_id, score, best_word, played_on) VALUES (?, ?, ?, ?)",
        GAMES,
    )
    con.commit()
    con.close()
    print(f"Built {DB_PATH.name}: {len(PLAYERS)} players, {len(GAMES)} games")


if __name__ == "__main__":
    build()
