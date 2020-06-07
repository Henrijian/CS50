SELECT movies.title FROM stars
INNER JOIN movies ON movies.id = stars.movie_id
INNER JOIN people ON people.id = stars.person_id
INNER JOIN ratings ON ratings.movie_id = stars.movie_id
WHERE people.name = 'Chadwick Boseman' ORDER BY ratings.rating DESC LIMIT 5;
