SELECT people.name FROM people WHERE
	people.id IN (SELECT DISTINCT directors.person_id FROM directors where
		directors.movie_id	IN (SELECT ratings.movie_id FROM ratings WHERE
			ratings.rating >= 9.0));
-- SELECT people.name FROM directors
-- INNER JOIN movies ON movies.id = directors.movie_id
-- INNER JOIN people ON people.id = directors.person_id
-- INNER JOIN ratings ON ratings.movie_id = directors.movie_id
-- WHERE ratings.rating >= 9.0  GROUP BY people.id;