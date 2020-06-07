SELECT people.name FROM stars INNER JOIN movies ON movies.id = stars.movie_id INNER JOIN people ON people.id = stars.person_id
WHERE movies.year = 2004 GROUP BY people.id ORDER BY people.birth;