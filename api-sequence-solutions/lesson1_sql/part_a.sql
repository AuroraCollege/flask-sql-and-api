-- PART A SOLUTIONS

-- Q1 Show every column for every player.
SELECT * FROM players;

-- Q2 Show only the first_name, last_name and rating of every player.
SELECT first_name, last_name, rating FROM players;

-- Q3 Show players from Dubbo.
SELECT * FROM players WHERE school = 'Dubbo';

-- Q4 Show players with a rating above 1450.
SELECT * FROM players WHERE rating > 1450;

-- Q5 Show all players, highest rating first.
SELECT * FROM players ORDER BY rating DESC;

-- Q6 Show the 3 highest game scores (score and best_word only).
SELECT score, best_word FROM games ORDER BY score DESC LIMIT 3;

-- Q7 Show games played on 2026-08-04 with a score of at least 300.
SELECT * FROM games WHERE played_on = '2026-08-04' AND score >= 300;
