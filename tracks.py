# INSTRUCTIONS
# 1. RUN THIS PYTHON
# 2. Enter file name: Library.xml
# 3. 

# import xml
import xml.etree.ElementTree as ET

# import sqlite3 because we are going to communicate with the database
import sqlite3

# we will connecto to trackdb.sqlite
# if theres no trackdb.sqlite it will create that file
conn = sqlite3.connect('trackdb.sqlite')

# file handler for database
cur = conn.cursor()

# Series of XML commands using semicolon
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
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
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# Python will ask a filename o xml
fname = input('Enter file name: ')

# If the input length is less than 1 then just equate fname = Library.xml
if ( len(fname) < 1 ) : fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False

    # This will going to loop the children inside the dictionary
    for child in d:

        # if found is true then return to the child.text
        if found : return child.text

        # if the child.tag has a particular "key" and text is key
        if child.tag == 'key' and child.text == key :

            # maniuplate the found variable into True
            found = True

    # return None
    return None

# python will going to parse the string from the varaiable fname
# xml et object
stuff = ET.parse(fname)

# inside stuff, find all dict inside a dict inside a dict
# then save ot all inside all
all = stuff.findall('dict/dict/dict')

# print the dictionary count with values of the length of all variable
print('Dict count:', len(all))

# for each entry in all variable, it will itterate all the values inside all
for entry in all:

    # if there is no track ID = is None, then skip/continue
    if ( lookup(entry, 'Track ID') is None ) : continue

    # look up for the values of Name then save it inside name
    name = lookup(entry, 'Name')

    # look up for the values of Arist and save it inside artist
    artist = lookup(entry, 'Artist')

    # look up for the value of Alum and save it inside artist
    album = lookup(entry, 'Album')

    # look up for the value of Play Count and then save it inside count 
    count = lookup(entry, 'Play Count')

    # look up for the value inside Rating and then save it inside rating
    rating = lookup(entry, 'Rating')

    # look up the value inside Total Time and save it inside length
    length = lookup(entry, 'Total Time')


    # SANITY CHECKING
    # if we didnt get name or artist or album, then continue
    if name is None or artist is None or album is None : 
        continue

    # Print all the values that we got
    print(name, artist, album, count, rating, length)

    # get primary key of the row
    # INSERT OR IGNORE = BECAUSE THE ARTIST NAME IS UNIQUE, IF THE NAME IS ALREADY THERE, DON'T INSERT IT AGAIN
    # ? = PLACEHOLDER
    # artist is a tuple , , is the second tuple
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )

    # I NEED THE ID OF THE ARTIST, IF ITS NOT THERE....
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))

    # WE WILL CREATE AN ID FROM THE RESULTING VALUE
    artist_id = cur.fetchone()[0]

    # INSERT OR IGNORE, IF TITLE AND ARTIST ID IS ALREADY THERE DON'T INSERT IT AGAIN,
    # title = album variable , artist_id = artist_id variable
    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )

    # SELECT THE ID FROM ALBUM WHERE TITLE = album variable
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))

    # get the first result which is the album id
    album_id = cur.fetchone()[0]

    # INSERT OR REPLACE = UPDATE, IF THERES NONE THEN INSERT, OTHERWISE OVERWRITE IT
    # title = name variable
    # album_id = album_id variable
    # len = length variable
    # rating = rating variable
    # count = count variable
    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ? )''', 
        ( name, album_id, length, rating, count ) )

    # commit the connection, results will be extracted to trackdb.sqlite
    conn.commit()

    # select track.title, Album.title, Artist.name From Track Join Album Join Artist ON Track.album_id = Album.id AND Album.artist_id = Artist.id