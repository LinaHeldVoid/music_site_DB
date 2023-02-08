SELECT janre_name FROM janre j;

SELECT j.janre_name, COUNT(performer_id) FROM performers_in_janres pij
JOIN janre j ON pij.janre_id = j.id
GROUP BY janre_name;

SELECT COUNT(*) FROM track t
JOIN album a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

SELECT AVG(track_length), album_name FROM album a
JOIN track t ON t.album_id = a.id
GROUP BY a.album_name;

SELECT performer_name FROM performer p
WHERE p.performer_name NOT IN (
      SELECT performer_name FROM performer p
      JOIN performers_albums pa ON p.id = pa.performer_id
      JOIN album a ON pa.album_id = a.id
      WHERE a.release_year = 2020
);

SELECT DISTINCT digest_name FROM digest d
JOIN tracks_in_digests tid ON d.id = tid.digest_id
JOIN track t ON tid.track_id = t.id
JOIN album a ON t.album_id = a.id
JOIN performers_albums pa ON a.id = pa.album_id
JOIN performer p ON pa.performer_id = p.id
WHERE p.performer_name LIKE 'Powerwolf';

SELECT album_name FROM album a
JOIN performers_albums pa ON a.id = pa.album_id
JOIN performer p ON pa.performer_id = p.id
JOIN performers_in_janres pij ON p.id = pij.performer_id
GROUP BY a.album_name
HAVING COUNT(pij.janre_id) > 1;

SELECT track_name FROM track t
LEFT JOIN tracks_in_digests tid ON t.id = tid.track_id
LEFT JOIN digest d ON tid.digest_id = d.id
WHERE digest_name IS NULL;

SELECT performer_name FROM performer p
JOIN performers_albums pa ON pa.performer_id = p.id
JOIN album a ON pa.album_id = a.id
JOIN track t ON t.album_id = a.id
WHERE track_length = (
	SELECT MIN(track_length) FROM track
);

SELECT album_name FROM album a
JOIN track t ON t.album_id = a.id
GROUP BY a.album_name
HAVING COUNT(t.track_name) = (
	SELECT COUNT(track_name) FROM track t
	JOIN album a ON t.album_id = a.id
	GROUP BY a.album_name
	ORDER BY COUNT(t.track_name)
	LIMIT 1
);