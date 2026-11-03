-- PART B SOLUTIONS

-- Q8 Show games whose best_word starts with 'q'.
SELECT * FROM games WHERE best_word LIKE 'q%';

-- Q9 Show games whose best_word contains 'zz'.
SELECT * FROM games WHERE best_word LIKE '%zz%';

-- Q10 How many players are in the club?
SELECT COUNT(*) AS num_players FROM players;

-- Q11 Show the highest score and the average score across all games.
SELECT MAX(score) AS highest, ROUND(AVG(score), 1) AS average FROM games;

-- Q12 Show each school and how many players it has.
SELECT school, COUNT(*) AS num_players FROM players GROUP BY school;

-- Q13 Add a new player: id 11, Isla Brown, from Moree, rating 1300.
INSERT INTO players (id, first_name, last_name, school, rating)
VALUES (11, 'Isla', 'Brown', 'Moree', 1300);

-- Q14 Change Isla's rating to 1360. (Without WHERE, EVERY player becomes 1360.)
UPDATE players SET rating = 1360 WHERE id = 11;

-- Q15 Show each game's score next to the player's first and last name.
SELECT players.first_name, players.last_name, games.score
FROM games
JOIN players ON games.player_id = players.id;

-- Q16 Each player's id and average score, best average first.
SELECT player_id, ROUND(AVG(score), 1) AS avg_score
FROM games
GROUP BY player_id
ORDER BY avg_score DESC;
