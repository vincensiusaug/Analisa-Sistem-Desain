import sqlite3

conn = sqlite3.connect('E-Commerce.db')
c = conn.cursor()

print("%3s | %10s | %10s | %10s"%("ID", "Name", "Username", "Password"))
for row in c.execute('SELECT * FROM User ORDER BY userId'):
    print("%3s | %10s | %10s | %10s"%(row[0], row[1], row[2], row[3]))