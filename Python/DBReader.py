import sqlite3

def ReadField(table):

    connection = sqlite3.connect('Database/E-Commerce.db')
    cursor = connection.cursor()

    result = []
    for row in cursor.execute('SELECT * FROM ' + table):
        result.append(row)
    
    return result

def UserCheck(email, password):
    connection = sqlite3.connect('Database/E-Commerce.db')
    cursor = connection.cursor()

    for row in cursor.execute('SELECT * FROM User'):
        if row[3] == email and row[4] == password:
            return row[0]
    
    return -1

def ReadUser(code):
    connection = sqlite3.connect('Database/E-Commerce.db')
    cursor = connection.cursor()

    for name in cursor.execute('SELECT * FROM user WHERE code='+str(code)):
        return name
    return -1
