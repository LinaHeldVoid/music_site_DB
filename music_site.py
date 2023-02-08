# создание таблиц
CREATE TABLE IF NOT EXISTS janre (
	id SERIAL PRIMARY KEY,
	janre_name VARCHAR(40) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS performer (
	id SERIAL PRIMARY KEY,
	performer_name VARCHAR(300) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS album (
	id SERIAL PRIMARY KEY,
	album_name VARCHAR(300) UNIQUE NOT NULL,
	release_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS track (
	id SERIAL PRIMARY KEY,
	track_name VARCHAR(200) UNIQUE NOT NULL,
	track_length INTEGER NOT NULL,
	album_id INTEGER NOT NULL REFERENCES album(id)
);

CREATE TABLE IF NOT EXISTS digest (
	id SERIAL PRIMARY KEY,
	digest_name VARCHAR(300) UNIQUE NOT NULL,
	release_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS performers_in_janres (
	janre_id INTEGER REFERENCES janre(id),
	performer_id INTEGER REFERENCES performer(id),
	CONSTRAINT pk PRIMARY KEY (janre_id, performer_id)
);

CREATE TABLE IF NOT EXISTS performers_albums (
	performer_id INTEGER REFERENCES performer(id),
	album_id INTEGER REFERENCES album(id),
	CONSTRAINT pk1 PRIMARY KEY (performer_id, album_id)
);

CREATE TABLE IF NOT EXISTS tracks_in_digests (
	track_id INTEGER REFERENCES track(id),
	digest_id INTEGER REFERENCES digest(id),
	CONSTRAINT pk2 PRIMARY KEY (track_id, digest_id)
);

# вставка данных в таблицы
INSERT INTO performer
VALUES (1, 'Powerwolf'),
       (2, 'Louis Armstrong'),
       (3, 'Elton John'),
       (4, 'Narsillion'),
       (5, 'Evanescence'),
       (6, 'Disturbed'),
       (7, 'Mono Inc.'),
       (8, 'Мельница'),
       (9, 'Аквариум')
       (10, 'Bear McCreary');

INSERT INTO janre
VALUES (1, 'Джаз'),
       (2, 'Пауэр-метал'),
       (3, 'Поп'),
       (4, 'Фолк'),
       (5, 'Русский рок'),
       (6, 'Неоклассика'),
       (7, 'Иностранный рок')
       (8, 'Саундтреки');

INSERT INTO album
VALUES (1, 'Fallen', 2003), (2, 'Welcome to Hell', 2018), (3, 'Too Low for Zero', 1983), (4, 'Kiss Of Fire', 1957),
       (5, 'Namárië', 2008), (6, 'Дорога сна', 2003), (7, 'Песни нелюбимых', 2016), (8, 'Call of the Wild', 2021),
       (9, 'Believe', 2003), (10, 'Best of the Blessed', 2020), (11, 'God of War IV', 2018);

INSERT INTO track
VALUES (1, 'My Immortal', 280, 1), (2, 'I"m still standing', 182, 3), (3, 'A Vagabond"s life', 266, 2), (4, 'Kiss of fire', 191, 4),
       (5, 'Who can dream forever', 466, 5), (6, 'Inside the fire', 231, 9), (7, 'Воин вереска', 351, 6), (8, 'Собачий вальс', 227, 7),
       (9, 'Alive or undead', 264, 8), (10, 'Funeral song', 230, 2), (11, 'Змей (на стихи Гумилёва)', 351, 6),
       (12, 'Dancing with the Dead', 245, 8), (13, 'Beast of Gévaudan', 211, 8), (14, 'El Retorn a la Infantesa', 405, 5),
       (15, 'Angmar', 453, 5), (16, 'Army of the Night', 201, 10), (17, 'Killers with the Cross', 249, 10), (18, 'God of War', 246, 11);

INSERT INTO digest
VALUES (1, 'Иностранный рок', 2001), (2, 'Русский рок', 1998), (3, 'Фолк-рок', 2019), (4, 'Погрустить', 2021), (5, 'Сатира', 2022),
       (6, 'Величайшие песни о любви', 2019), (7, 'Как звучит ностальгия', 2020), (8, 'Тёмные песни', 2022);

INSERT INTO tracks_in_digests
VALUES (1,1), (4,1), (6,1), (9,1), (10,1), (12,1), (13,1), (16,1), (17,1),
       (7,2), (8,2), (11,2),
       (7,3), (11,3),
       (1,4), (3,4), (5,4), (7,4), (9,4), (10,4), (11,4), (12, 4), (14,4), (15,4), (17,4),
       (7,5),
       (1,6), (2,6), (4,6), (7,6), (10,6), (11,6),
       (1,7), (3,7), (10,7), (14,7),
       (3,8), (6,8), (9,8), (10,8), (11,8), (12,8), (13,8), (15,8), (16,8), (17,8);

INSERT INTO performers_albums
VALUES (1,8), (2,4), (3,3), (4,5), (5,1), (6,9), (7,2), (8,6), (9,7), (1,10);

INSERT INTO performers_in_janres
VALUES (1,2), (2,1), (2,6), (3,3), (4,8), (5,8), (5,9), (6,4), (7,1), (7,5), (7,6), (7,7);


# SELECT-запросы
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