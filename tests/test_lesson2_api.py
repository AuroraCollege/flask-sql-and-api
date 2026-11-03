"""Tests for Lesson 2: Building APIs with Flask.

Checks YOUR code in lesson2_api/. You don't need to start Flask first:
the tests use Flask's built-in test client.

Run from the repo root:
    pytest tests/test_lesson2_api.py -v          # everything
    pytest tests/test_lesson2_api.py -k json     # Activity 1 only
    pytest tests/test_lesson2_api.py -k first    # Activity 2 only
    pytest tests/test_lesson2_api.py -k scrabble # Activity 3 only

PASSED  = it works
FAILED  = missing or wrong (read the message)
SKIPPED = stretch or extension task you haven't tried yet
"""
import importlib.util
import json
import re
import runpy
from pathlib import Path

import pytest

LESSON = Path(__file__).resolve().parent.parent / "lesson2_api"


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------
def load_app(folder, module_name):
    """Imports app.py from an activity folder and returns its Flask test client."""
    spec = importlib.util.spec_from_file_location(module_name, LESSON / folder / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.app.config["TESTING"] = True
    return module, module.app.test_client()


def has_route(client, rule, method="GET"):
    return any(r.rule == rule and method in r.methods for r in client.application.url_map.iter_rules())


def require_route(client, rule, method="GET", optional=False):
    if not has_route(client, rule, method):
        message = f"No {method} route for {rule} yet"
        if optional:
            pytest.skip(message)
        pytest.fail(message + " - add an @app.route for it")


def get_json(client, url, expected_status=200, method="GET", **kwargs):
    response = client.open(url, method=method, **kwargs)
    assert response.status_code == expected_status, \
        f"{method} {url}: expected status {expected_status}, got {response.status_code}"
    assert response.is_json, f"{method} {url}: response must be JSON - did you use jsonify()?"
    return response.get_json()


# ===============================================================
# Activity 1: JSON warm-up
# ===============================================================
@pytest.fixture(scope="module")
def json_tasks():
    """Runs json_practice.py and returns its variables."""
    return runpy.run_path(str(LESSON / "01_json_basics" / "json_practice.py"))


def test_json_task2_q_points(json_tasks):
    assert json_tasks["q_points"] == 10, "Task 2: Q should be worth 10. Look inside data['tiles']"


def test_json_task3_total_tiles(json_tasks):
    assert json_tasks["total"] == 100, f"Task 3: a full set has 100 tiles, you got {json_tasks['total']}"


def test_json_task4_dumps(json_tasks):
    text = json_tasks["player_json"]
    assert text, "Task 4: player_json is still empty - use json.dumps()"
    assert json.loads(text) == json_tasks["player"], "Task 4: player_json doesn't match the player dict"
    assert "true" in text and "null" in text, "Task 4: JSON should contain true and null"


@pytest.mark.parametrize("index, task", [(0, "5a"), (1, "5b"), (2, "5c")])
def test_json_task5_fixed(json_tasks, index, task):
    text = json_tasks["broken"][index]
    try:
        json.loads(text)
    except json.JSONDecodeError as err:
        pytest.fail(f"Task {task}: still invalid JSON -> {err}")


# ===============================================================
# Activity 2: First endpoints
# ===============================================================
@pytest.fixture(scope="module")
def first_api():
    return load_app("02_first_api", "first_api_app")[1]


def test_first_api_hello(first_api):
    assert get_json(first_api, "/api/hello") == {"message": "Hello, API!"}


def test_first_api_greet(first_api):
    require_route(first_api, "/api/greet/<name>")
    assert get_json(first_api, "/api/greet/Ava") == {"greeting": "G'day, Ava!"}
    assert get_json(first_api, "/api/greet/Sam") == {"greeting": "G'day, Sam!"}


@pytest.mark.parametrize("letter, expected", [("Q", 10), ("q", 10), ("a", 1), ("z", 10)])
def test_first_api_tile(first_api, letter, expected):
    require_route(first_api, "/api/tile/<letter>")
    data = get_json(first_api, f"/api/tile/{letter}")
    assert data == {"letter": letter.upper(), "points": expected}


@pytest.mark.parametrize("bad", ["7", "ab", "%21"])
def test_first_api_tile_not_a_letter(first_api, bad):
    require_route(first_api, "/api/tile/<letter>")
    data = get_json(first_api, f"/api/tile/{bad}", expected_status=404)
    assert "error" in data, "Return an {'error': ...} message with the 404"


def test_first_api_score_stretch(first_api):
    require_route(first_api, "/api/score", optional=True)
    assert get_json(first_api, "/api/score?word=quiz") == {"word": "quiz", "score": 22}
    data = get_json(first_api, "/api/score", expected_status=400)
    assert "error" in data, "Missing ?word= should return an error message with status 400"


# ===============================================================
# Activity 3: Scrabble Word Checker API
# ===============================================================
@pytest.fixture(scope="module")
def scrabble():
    folder = LESSON / "03_scrabble_api"
    if not (folder / "scrabble.db").exists():
        runpy.run_path(str(folder / "build_db.py"))  # builds scrabble.db
    return load_app("03_scrabble_api", "scrabble_app")


@pytest.fixture(scope="module")
def scrabble_client(scrabble):
    return scrabble[1]


@pytest.mark.parametrize("word, valid", [
    ("quiz", True), ("syzygy", True), ("cat", True),
    ("qwzx", False), ("catt", False),
])
def test_scrabble_task1_check(scrabble_client, word, valid):
    require_route(scrabble_client, "/api/check/<word>")
    data = get_json(scrabble_client, f"/api/check/{word}")
    assert data["word"] == word and data["valid"] is valid, \
        f"/api/check/{word} should say valid: {str(valid).lower()}"


def test_scrabble_task2_lowercase(scrabble_client):
    require_route(scrabble_client, "/api/check/<word>")
    data = get_json(scrabble_client, "/api/check/QuIz")
    assert data["word"] == "quiz" and data["valid"] is True, "Make the word lowercase before checking it"


@pytest.mark.parametrize("bad", ["abc123", "hello world", "don't"])
def test_scrabble_task2_rejects_non_letters(scrabble_client, bad):
    require_route(scrabble_client, "/api/check/<word>")
    data = get_json(scrabble_client, f"/api/check/{bad}", expected_status=400)
    assert "error" in data, "Return an {'error': ...} message with the 400"


@pytest.mark.parametrize("word, score", [("quiz", 22), ("cat", 5), ("syzygy", 25)])
def test_scrabble_task3_score(scrabble_client, word, score):
    require_route(scrabble_client, "/api/check/<word>")
    data = get_json(scrabble_client, f"/api/check/{word}")
    assert data.get("score") == score, f"{word} should score {score}, got {data.get('score')}"


def test_scrabble_sql_injection_fails(scrabble_client):
    """The classic attack must never make a fake word 'valid'."""
    require_route(scrabble_client, "/api/check/<word>")
    response = scrabble_client.get("/api/check/zzzz' OR '1'='1")
    data = response.get_json() or {}
    assert data.get("valid") is not True, "SQL injection worked! Use a ? placeholder, not an f-string"


def test_scrabble_no_fstring_sql(scrabble):
    """Checks your code never builds SQL with an f-string or + joins."""
    source = Path(scrabble[0].__file__).read_text()
    unsafe = re.findall(r"""f["'][^"']*\b(?:SELECT|INSERT|UPDATE|DELETE)\b""", source, re.IGNORECASE)
    unsafe += re.findall(r"""["'][^"']*\b(?:SELECT|WHERE)\b[^"']*["']\s*\+""", source, re.IGNORECASE)
    assert not unsafe, f"Unsafe SQL found: {unsafe}. Put ? in the SQL and pass values separately"


# ---------------------------------------------------------------
# Extensions (skipped until attempted)
# ---------------------------------------------------------------
def test_scrabble_ext1_starts(scrabble_client):
    require_route(scrabble_client, "/api/starts/<prefix>", optional=True)
    data = get_json(scrabble_client, "/api/starts/zy")
    assert data["prefix"] == "zy"
    assert len(data["words"]) == 10, "Default limit should be 10 words"
    assert all(w.startswith("zy") for w in data["words"])
    assert len(get_json(scrabble_client, "/api/starts/zy?limit=3")["words"]) == 3, "?limit=3 should give 3 words"


def test_scrabble_ext2_rack(scrabble_client):
    require_route(scrabble_client, "/api/rack/<letters>", optional=True)
    data = get_json(scrabble_client, "/api/rack/tac")
    assert sorted(data["words"]) == ["act", "at", "cat", "ta"]


def test_scrabble_ext3_post(scrabble_client):
    require_route(scrabble_client, "/api/check", method="POST", optional=True)
    data = get_json(scrabble_client, "/api/check", method="POST", json={"words": ["quiz", "qwzx"]})
    results = data.get("results", data)
    assert [r["valid"] for r in results] == [True, False], "quiz should be valid, qwzx should not"
