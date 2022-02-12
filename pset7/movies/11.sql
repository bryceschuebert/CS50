SELECT title FROM movies, stars, people, ratings
WHERE movies.id = stars.movie_id
AND stars.person_id = people.id
AND ratings.movie_id = movies.id
AND people.name = "Chadwick Boseman"
ORDER BY ratings.rating DESC LIMIT 5;