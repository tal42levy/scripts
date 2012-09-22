import sqlite3

dbUrl = "example.db"

conn = sqlite3.connect(dbUrl)
c = conn.cursor()
c.execute('select id from departments where code = ?', ["ARCH"])
print c.fetchone()[0]
c.execute('drop table departments')