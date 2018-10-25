import sqlite3
conn = sqlite3.connect('E-Commerce.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM User'):
    print(row)