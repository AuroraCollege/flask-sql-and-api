# SQL and APIs

Two lessons:

| Folder | Lesson |
|---|---|
| `lesson1_sql/` | SQL refresher (50 min) |
| `lesson2_api/` | Building APIs with Flask and SQL (100 min) |

The databases and Flask are set up automatically when the Codespace starts.
If a database is missing, run its build script (see below).

---

## Lesson 1: SQL refresher

```bash
cd lesson1_sql
python run_sql.py part_a.sql          # runs every query in the file
python run_sql.py "SELECT * FROM players;"   # runs one query
python build_club_db.py               # resets the database
```

Write your queries under each `-- Q` comment in `part_a.sql` and `part_b.sql`.
End every query with `;`.

**Tip:** click `scrabble_club.db` in the Explorer to view the tables.

---

## Lesson 2: APIs

### Activity 1: JSON warm-up
```bash
cd lesson2_api/01_json_basics
python json_practice.py
```

### Activity 2 and 3: Running a Flask API
```bash
cd lesson2_api/02_first_api      # or 03_scrabble_api
python app.py
```
1. Open the **PORTS** tab and click the globe icon next to port **5000**.
2. Add the endpoint to the end of the URL, e.g. `/api/hello`.
3. Flask reloads automatically when you save. Refresh the browser to see changes.
4. Stop the server with **Ctrl + C**.

Or test from a second terminal:
```bash
curl localhost:5000/api/hello
```

### Missing `scrabble.db`?
```bash
python lesson2_api/03_scrabble_api/build_db.py
```

---

`words.txt` is the ENABLE word list (public domain).
