SELECT movies.title FROM movies WHERE movies.id
IN
(SELECT stars.movie_id FROM stars WHERE EXISTS
    (SELECT people.id FROM people WHERE (people.id = stars.person_id) AND
    (people.name = 'Johnny Depp' OR people.name = 'Helena Bonham Carter'))
    GROUP BY stars.movie_id
    HAVING COUNT(stars.person_id) = 2
);