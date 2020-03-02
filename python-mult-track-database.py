"""Musical Track Database
This application will read an iTunes export file in XML and produce a properly 
normalized database with this structure:
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT
);
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
If you run the program multiple times in testing or with different files, make
sure to empty out the data before each run.
You can use this code as a starting point for your application: 
http://www.pythonlearn.com/code/tracks.zip. The ZIP file contains the Library.xml
file to be used for this assignment. You can export your own tracks from iTunes
and create a database, but for the database that you turn in for this assignment,
only use the Library.xml data that is provided.
To grade this assignment, the program will run a query like this on your uploaded
database and look for the data it expects to see:
SELECT Track.title, Artist.name, Album.title, Genre.name 
    FROM Track JOIN Genre JOIN Album JOIN Artist 
    ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
        AND Album.artist_id = Artist.id
    ORDER BY Artist.name LIMIT 3
The expected result of this query on your database is:
Track   Artist  Album   Genre
Chase the Ace   AC/DC   Who Made Who    Rock
D.T.    AC/DC   Who Made Who    Rock
For Those About To Rock (We Salute You) AC/DC   Who Made Who    Rock
"""

import sqlite3
import xml.etree.ElementTree as ET

# PART 1: PREPARING THE DATABASE
# Connecting to the file in which we want to store our db
print("Connecting to database..")
conn = sqlite3.connect('tracks.sqlite')
print("conn class type is " + str(type(conn)))

cur = conn.cursor()
print("cur class type is " + str(type(cur)))

# Getting sure it is empty
# We can use "executescript" to execute several statements at the same time
print("Executing the script")
cur.executescript("""
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Album; 
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Track
    """)
print(type(cur.executescript("""
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Album; 
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Track
    """)))

# Creating it
cur.executescript(''' CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# PART 2: INSERTING THE DATA
# Getting the data and parsing it
filehandler = input("What XML Document to open: ")
print("Running the filehandler")
print("filehandler class type is " + str(type(filehandler)))
print("Opening the filehandler")
data_source = open(filehandler)
print("opening the data_source, the class type is " + str(type(data_source)))

data = data_source.read()
print("opening the data, the class type is " + str(type(data)))
xml_data = ET.fromstring(data)
print("opening the xml_data, the class type is " + str(type(xml_data)))
# Obtaining every tag with track data
tracks_data = xml_data.findall("dict/dict/dict")
print("opening the tracks_data, the class type is " + str(type(tracks_data)))

# tracks_data is a list, getting each of track inside a list will result to a <Element .. 'dict'> = find all <dict> tags as proposed in line 145
for track in tracks_data:

    # defined function find_field, it will take all each track from the list
    # the list from tracks_data has 34-ish trees dict[34], of key and value text
    # the wanted_field is like the key field , example <key>wanted_field</key><integer>34</integer>
    def find_field(track, wanted_field):

        # default sense of this function, the tag is not yet found which is found = false
        found = False

        # for each tree, in track, 1 tree is like <tag.tag>tag.text</tag.tag>
        for tag in track:

            # if found is not true === if found is false
            if not found:
                # if tag.tag == "key" means <key></key>
                # if tag.text means <key>tag.text</key>
                if (tag.tag == "key" and tag.text == wanted_field):

                    # found = true means we have found the <key>Title..</key>
                    found = True

            # else means if found is true === if found is not false
            else:
                # After founding it, we return the content of the following
                # tag (the one with its value)
                # <tag.tag>tag.text</tag.tag> <tag.tag>tag.text</tag.tag> <--- the tag.text of the second one will be returned since we have done already the first on if not
                return tag.text

        # reset the found value to false
        return False

    # find_field will return the tag.text (string or integer) value of the field
    title = find_field(track, "Name")
    artist = find_field(track, "Artist")
    genre = find_field(track, "Genre")
    album = find_field(track, "Album")
    length = find_field(track, "Total Time")
    count = find_field(track, "Play Count")
    rating = find_field(track, "Rating")

    # Artist
    if (artist):  # If artist is true = artist has a value

        # If the value hasn't been introduced yet and exists, we'll insert it
        # SQL STATEMENT = it has 2 "?" meaning 2 placeholders
        artist_statement = """INSERT INTO Artist(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Artist WHERE name = ?)"""

        # 2 parameters inside the variable that is needed to insert to the SQL
        SQLparams = (artist, artist)

        # execute variable, variable parameters
        cur.execute(artist_statement, SQLparams)

    # Genre
    if (genre):  # If it's a filled string, != False
        # If the value hasn't been introduced yet and exists, we'll insert it
        genre_statement = """INSERT INTO Genre(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Genre WHERE name = ?)"""
        SQLparams = (genre, genre)
        cur.execute(genre_statement, SQLparams)

    # Album
    if (album):  # If it's a filled string, != False
        # First of all, we'll get the artist id
        artistID_statement = "SELECT id from Artist WHERE name = ?"
        cur.execute(artistID_statement, (artist,))
        # .fetchone() returns a one-element tuple, and we want its content
        artist_id = cur.fetchone()[0]

        # Now we're going to insert the data
        album_statement = """INSERT INTO Album(title, artist_id) 
            SELECT ?, ? WHERE NOT EXISTS (SELECT * FROM Album WHERE title = ?)"""
        SQLparams = (album, artist_id, album)
        cur.execute(album_statement, SQLparams)

    # Track
    if (title):  # if title is present

        # Objective, we need to get Genre id

        # Select genre using query, then put it inside variable
        genreID_statement = "SELECT id from Genre WHERE name = ?"

        # Execute var script , parameter = (genre,) no value for the other tuple
        cur.execute(genreID_statement, (genre,))
        try:
            # when the query is run, it will fetch the first value and save it inside genre_id
            genre_id = cur.fetchone()[0]

        # exception typeerror
        except TypeError:
            # set genre id to 0
            genre_id = 0

        # Objective = obrain album id

        # get id using query statement SELECT id from Album Where title = ?
        albumID_statement = "SELECT id from Album WHERE title = ?"

        # run execute query with (query statement, album title string)
        cur.execute(albumID_statement, (album,))

        # if it runs
        try:

            # get the first resulting value
            album_id = cur.fetchone()[0]

        # if it blows up
        except TypeError:

            # set album id to 0
            album_id = 0

        # Inserting data
        # SUMMARIZING ALL THE DATA
        # title = title , album_id = album_id , genre_id = genre_id , len = length , rating = rating, count = count
        # MULTIPLE INSERT
        track_statement = """
        INSERT INTO Track(title, album_id, genre_id, len, rating, count) 
        SELECT ?, ?, ?, ?, ?, ? 
        WHERE NOT EXISTS 
        (SELECT * FROM Track WHERE title = ?)
        """
        SQLparams = (title, album_id, genre_id, length, rating, count, title)

        # track_statement should have 6 placeholders , SQLparams should have 6 variables with values in it
        cur.execute(track_statement, SQLparams)

print("Committing..")
conn.commit()
print("Commit done successfully!")
cur.close()