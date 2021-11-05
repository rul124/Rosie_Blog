import sqlite3

# create data base
connection = sqlite3.connect('database.db')

# run sql command in db.sql
with open('db.sql') as f:
    connection.executescript(f.read())

# create a cursor
cur = connection.cursor()

# insert two blogs
cur.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    (
        'Test1', 'Test_01'
    )
)
cur.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    (
        'Test2', 'Test_02'
    )
)

# commit the commands
connection.commit()

# close link
connection.close()
