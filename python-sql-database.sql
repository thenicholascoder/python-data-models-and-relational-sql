CREATE TABLE Genre (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT
)

CREATE TABLE Artist (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT
)

CREATE TABLE Album (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	artist_id INTEGER, 
	title TEXT
)

CREATE TABLE Track (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title TEXT,
	album_id INTEGER,
	genre_id INTEGER,	
	len INTEGER, rating INTEGER, count INTEGER
)

-- ------------------------------------------------------------
-- INSERTING RELATIONAL DATA
INSERT INTO Artist (name) VALUES ('Led Zeppelin')

INSERT INTO Artist (name) VALUES ('AC/DC')

-- YOU CAN STACK ALL THE CODES AND SEPARATE EVERY LINE WITH SEMI COLON ;
INSERT INTO Genre (name) VALUES ('Rock');
INSERT INTO Genre (name) VALUES ('Metal')

-- FOR FOREIGN KEYS
INSERT INTO Album (title,artist_id) VALUES ('Who Made Who',2);
INSERT INTO Album (title,artist_id) VALUES ('IV',1)

INSERT INTO Track (title,rating,len, count, album_id, genre_id) VALUES ('Black Dog', 5, 297, 0, 2, 1);
INSERT INTO Track (title,rating,len, count, album_id, genre_id) VALUES ('Stairway', 5, 482, 0, 2, 1);
INSERT INTO Track (title,rating,len, count, album_id, genre_id) VALUES ('About to Rock', 5, 313, 0, 1, 2);
INSERT INTO Track (title,rating,len, count, album_id, genre_id) VALUES ('Who Made Who', 5, 207, 0, 1, 2)

-- -----------------------------------------------------------
-- RECONSTRUCTING DATA WITH JOIN
-- BUILDING RELATIONSHIPS

--     	what we want to see           from with join                 where
SELECT Album.title, Artist.name FROM Album JOIN ARTIST ON Album.artist_id = Artist.id
--  STARTING POINT   END POINT     STARTING TABLE  ENDING TABLE  STARTING POINT = ENDING POINT


-- CHILD FIRST THEN PARENT                                                       on is like where
SELECT Album.title, Album.artist_id, Artist.id, Artist.name FROM Album JOIN Artist ON Album.artist_id = Artist.id

SELECT Track.title, Genre.name from Track join Genre on Track.genre_id = Genre.id

-- SHOW ALL POSSIBLE COMBINATION BY NOT PUTTING ON
SELECT Track.title, Track.genre_id, Genre.id, Genre.name from Track join Genre

-- 
SELECT Track.title, Artist.name, Album.title, Genre.name 
from Track join Genre join Album join Artist
on Track.genre_id = Genre.id and Track.album_id = Album.id and Album.artist_id = Artist.id 


-- STEPS FOR START UP BUILDING A DATABASE
-- 1. UI we designed that had replication
-- 2. logical data model
-- 3. physical data model
-- 4. connect data using numbers instead of strings
-- 5. susing join to reconstruct it 