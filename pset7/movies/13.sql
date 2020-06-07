SELECT people.name FROM people WHERE
	people.id IN (SELECT DISTINCT stars.person_id FROM stars WHERE
		stars.movie_id IN (SELECT DISTINCT stars.movie_id FROM stars WHERE
			EXISTS (SELECT people.id FROM people WHERE
				people.id = stars.person_id
				AND people.name = 'Kevin Bacon'
				AND people.birth = 1958))
		AND NOT EXISTS (SELECT people.id FROM people WHERE
			stars.person_id = people.id
			AND people.name = 'Kevin Bacon'
			AND people.birth = 1958));