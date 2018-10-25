import sqlite3

conn = sqlite3.connect('E-Commerce.db')
c = conn.cursor()

pformat = "| {:^4} | {:^10} | {:^10} | {:^10} |"

print(pformat.format("ID", "Name", "Username", "Password"))
for row in c.execute('SELECT * FROM User ORDER BY userId'):
    print(pformat.format(row[0], row[1], row[2], row[3]))