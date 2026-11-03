"""Activity 1: JSON warm-up

For each task: PREDICT the output first, then RUN the file to check.
Run with:  python json_practice.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent

# ---------------------------------------------------------------
# TASK 1: Load the JSON file into Python
# Predict: what Python type is `data`?   My prediction: ________
# ---------------------------------------------------------------
with open(HERE / "tiles.json") as f:
    data = json.load(f)

print("Task 1:", type(data))
print("Task 1:", data["game"], "| blank tiles?", data["has_blank_tiles"])
# Predict: JSON has `true`. What does Python print?   ________


# ---------------------------------------------------------------
# TASK 2: How many points is the letter Q worth?
# TODO: replace None with an expression that reads it from `data`.
# ---------------------------------------------------------------
q_points = data["tiles"]["Q"]["points"]
print("Task 2: Q is worth", q_points)


# ---------------------------------------------------------------
# TASK 3: How many tiles are in a full Scrabble set?
# TODO: loop through data["tiles"] and add up every "count".
# (Answer should be 100.)
# ---------------------------------------------------------------
total = 0
for letter, info in data["tiles"].items():
    total += info["count"]
print("Task 3: total tiles =", total)


# ---------------------------------------------------------------
# TASK 4: Python dict -> JSON string
# TODO: use json.dumps() with indent=2 to turn `player` into JSON.
# Predict: what happens to True and None?   ________
# ---------------------------------------------------------------
player = {"name": "Ava", "rating": 1420, "active": True, "coach": None, "best_words": ["quixotic", "zephyr"]}
player_json = json.dumps(player, indent=2)
print("Task 4:\n" + player_json)


# ---------------------------------------------------------------
# TASK 5: Fix the broken JSON
# Each string below is INVALID JSON. Run the file to see the error,
# then edit the string so it becomes valid.
# ---------------------------------------------------------------
broken = [
    '{"word": "quiz", "valid": true}',           # 5a: double quotes only
    '{"word": "jazz", "score": 29}',             # 5b: no trailing comma
    '{"word": "fox", "valid": true}',            # 5c: lowercase true
]
for i, text in enumerate(broken):
    try:
        json.loads(text)
        print(f"Task 5{'abc'[i]}: valid!")
    except json.JSONDecodeError as err:
        print(f"Task 5{'abc'[i]}: INVALID - {err}")
