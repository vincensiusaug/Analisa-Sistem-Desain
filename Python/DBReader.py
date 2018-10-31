import sqlite3

connection = sqlite3.connect('Database/E-Commerce.db')
cursor = connection.cursor()

pformat = "| {:^4} | {:^4} | {:^10} | {:^10} | {:^10} |"
pformat1 = "| {:-^4} | {:-^4} | {:-^10} | {:-^10} | {:-^10} |"

print(pformat1.format("-","-","-","-","-"))
print(pformat.format("ID", "Type", "Name", "Username", "Password"))
print(pformat1.format("-","-","-","-","-"))
for row in cursor.execute('SELECT * FROM User ORDER BY id'):
    print(pformat.format(row[0], row[1], row[2], row[3], row[4]))
print(pformat1.format("-","-","-","-","-"))