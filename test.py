import sqlite3
conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('SELECT * FROM users')
print(c.fetchone()["id"])