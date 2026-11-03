"""Tests for Lesson 1: SQL refresher.

Checks the queries YOU wrote in lesson1_sql/part_a.sql and part_b.sql.
Each question gets its own fresh copy of the database, so your files
never change the real scrabble_club.db.

Run from the repo root:
    pytest tests/test_lesson1_sql.py -v

PASSED  = query gives the right result
FAILED  = query is missing or gives the wrong result (read the message)
SKIPPED = extension question you haven't tried yet
"""
import importlib.util
import re
import sqlite3
from collections import Counter
from pathlib import Path

import pytest

LESSON = Path(__file__).resolve().parent.parent / "lesson1_sql"


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------
def load_answers(filename):
    """Reads a .sql file and returns {"Q1": ["SELECT ...;"], ...}."""
    answers, label, buffer = {}, None, ""
    for line in (LESSON / filename).read_text().splitlines():
        stripped = line.strip()
        match = re.match(r"--\s*(Q\d+)\b", stripped)
        if match:
            label = match.group(1)
            answers.setdefault(label, [])
        if stripped.startswith("--") or not stripped:
            continue
        buffer += line + "\n"
        if sqlite3.complete_statement(buffer):
            if label:
                answers[label].append(buffer.strip())
            buffer = ""
    return answers


ANSWERS = {**load_answers("part_a.sql"), **load_answers("part_b.sql")}


@pytest.fixture
def db(tmp_path):
    """A fresh copy of the Scrabble Club database for each test."""
    spec = importlib.util.spec_from_file_location("build_club_db", LESSON / "build_club_db.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.DB_PATH = tmp_path / "scrabble_club.db"
    builder.build()
    con = sqlite3.connect(builder.DB_PATH)
    yield con
    con.close()


def run_answer(con, q):
    """Runs every statement under question q and returns the last result's rows."""
    statements = ANSWERS.get(q, [])
    if not statements:
        return None
    rows = []
    for sql in statements:
        try:
            cur = con.execute(sql)
        except sqlite3.Error as err:
            pytest.fail(f"{q}: your SQL gave an error -> {err}\n    {sql}")
        rows = cur.fetchall() if cur.description else rows
    con.commit()
    return rows


def norm(row):
    """Puts a row in a standard form so column order and rounding don't matter."""
    values = [round(v, 1) if isinstance(v, float) else v for v in row]
    return tuple(sorted(map(str, values)))


def require(con, q, optional=False):
    rows = run_answer(con, q)
    if rows is None:
        if optional:
            pytest.skip(f"{q} is an extension - not attempted yet")
        pytest.fail(f"{q} has not been answered yet. Write a query under '-- {q}' ending with ;")
    return rows


# ---------------------------------------------------------------
# Reading data: compared against the teacher's query
#   ordered=True means ORDER BY matters
# ---------------------------------------------------------------
REFERENCE = {
    "Q1": ("SELECT * FROM players", False),
    "Q2": ("SELECT first_name, last_name, rating FROM players", False),
    "Q3": ("SELECT * FROM players WHERE school = 'Dubbo'", False),
    "Q4": ("SELECT * FROM players WHERE rating > 1450", False),
    "Q5": ("SELECT * FROM players ORDER BY rating DESC", True),
    "Q6": ("SELECT score, best_word FROM games ORDER BY score DESC LIMIT 3", True),
    "Q7": ("SELECT * FROM games WHERE played_on = '2026-08-04' AND score >= 300", False),
    "Q10": ("SELECT COUNT(*) FROM players", False),
    "Q11": ("SELECT MAX(score), AVG(score) FROM games", False),
    "Q12": ("SELECT school, COUNT(*) FROM players GROUP BY school", False),
}


@pytest.mark.parametrize("q", REFERENCE)
def test_select_queries(db, q):
    expected_sql, ordered = REFERENCE[q]
    got = [norm(r) for r in require(db, q)]
    expected = [norm(r) for r in db.execute(expected_sql).fetchall()]
    if ordered:
        assert got == expected, f"{q}: right rows? right ORDER BY? right LIMIT?"
    else:
        assert len(got) == len(expected), f"{q}: expected {len(expected)} rows, got {len(got)}"
        assert Counter(got) == Counter(expected), f"{q}: right number of rows, but the values are wrong"


# ---------------------------------------------------------------
# LIKE: any columns are fine, as long as the right games come back
# ---------------------------------------------------------------
@pytest.mark.parametrize("q, words", [
    ("Q8", {"quixotic", "quartz", "quiz", "quokka"}),
    ("Q9", {"buzzword", "jazz", "pizzazz"}),
])
def test_like_queries(db, q, words):
    rows = require(db, q)
    found = {v for row in rows for v in row if isinstance(v, str)} & words
    assert len(rows) == len(words), f"{q}: expected {len(words)} games, got {len(rows)}. Check your % wildcards"
    assert found == words, f"{q}: missing {words - found}. Did you include the best_word column?"


# ---------------------------------------------------------------
# Changing data
# ---------------------------------------------------------------
def test_q13_insert(db):
    require(db, "Q13")
    row = db.execute("SELECT * FROM players WHERE id = 11").fetchone()
    assert row == (11, "Isla", "Brown", "Moree", 1300), f"Q13: player 11 should be Isla Brown, Moree, 1300 - got {row}"
    assert db.execute("SELECT COUNT(*) FROM players").fetchone()[0] == 11, "Q13: should add exactly ONE player"


def test_q14_update(db):
    before = dict(db.execute("SELECT id, rating FROM players").fetchall())
    require(db, "Q13")
    require(db, "Q14")
    after = dict(db.execute("SELECT id, rating FROM players").fetchall())
    assert after.get(11) == 1360, f"Q14: Isla's rating should be 1360 - got {after.get(11)}"
    changed = [pid for pid, rating in before.items() if after[pid] != rating]
    assert not changed, f"Q14: you also changed players {changed}! Is your WHERE clause missing?"


# ---------------------------------------------------------------
# Extensions (skipped until attempted)
# ---------------------------------------------------------------
def test_q15_join(db):
    rows = require(db, "Q15", optional=True)
    expected = db.execute(
        "SELECT p.first_name, p.last_name, g.score FROM games g JOIN players p ON g.player_id = p.id"
    ).fetchall()
    assert Counter(map(norm, rows)) == Counter(map(norm, expected)), \
        "Q15: expected first_name, last_name and score for all 24 games"


def test_q16_average_by_player(db):
    rows = require(db, "Q16", optional=True)
    expected = db.execute(
        "SELECT player_id, AVG(score) AS a FROM games GROUP BY player_id ORDER BY a DESC"
    ).fetchall()
    assert [norm(r) for r in rows] == [norm(r) for r in expected], \
        "Q16: one row per player_id with their average score, best average first"
