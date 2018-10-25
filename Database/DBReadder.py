import sqlite3

connection = sqlite3.connect('E-Commerce.db')
cursor = connection.cursor()

pformat = "| {:^4} | {:^4} | {:^10} | {:^10} | {:^10} |"

print(pformat.format("ID", "Type", "Name", "Username", "Password"))
for row in cursor.execute('SELECT * FROM User ORDER BY userId'):
    print(pformat.format(row[0], row[1], row[2], row[3], row[4]))